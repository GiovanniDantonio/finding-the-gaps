"""Run every problem in a probe as a Devin session and save raw outputs.

Usage: python harness/run.py probes/<slug> --modes tools,notools --samples 3
Writes probes/<slug>/outputs/<mode>/<problem>/sample_<n>.json

Needs DEVIN_API_KEY in the environment (or in .env). Each (problem, mode, sample)
is one fresh session with structured output {answer, reasoning}.
"""
import argparse, json, os, pathlib, datetime, time, urllib.request

API = "https://api.devin.ai/v1"

MODES = {
    "tools": "",
    "notools": (
        "Answer from reasoning alone. Do not run code, open a browser, search the web, "
        "or use any tool. Put the final answer in the structured output.\n\n"
    ),
}

SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}, "reasoning": {"type": "string"}},
    "required": ["answer", "reasoning"],
}


def api(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {os.environ['DEVIN_API_KEY']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def run_session(mode: str, prompt: str, tag: str, timeout_s: int = 1800) -> dict:
    s = api("POST", "/sessions", {
        "prompt": MODES[mode] + prompt,
        "structured_output_schema": SCHEMA,
        "tags": ["finding-the-gaps", tag, mode],
        "unlisted": True,
        "max_acu_limit": 5,
    })
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api("GET", f"/sessions/{s['session_id']}")
        if d.get("status_enum") in ("finished", "blocked", "expired"):
            out = d.get("structured_output") or {}
            return {"text": out.get("answer", ""), "reasoning": out.get("reasoning", ""),
                    "status": d.get("status_enum"), "session_url": s["url"], "session_id": s["session_id"]}
        time.sleep(20)
    return {"text": "", "reasoning": "", "status": "timeout", "session_url": s["url"], "session_id": s["session_id"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("probe"); ap.add_argument("--modes", default="tools"); ap.add_argument("--samples", type=int, default=3)
    a = ap.parse_args()
    probe = pathlib.Path(a.probe)
    for prob in sorted((probe / "problems").glob("p*.md")):
        prompt = prob.read_text()
        for mode in a.modes.split(","):
            out = probe / "outputs" / mode / prob.stem
            out.mkdir(parents=True, exist_ok=True)
            for i in range(a.samples):
                f = out / f"sample_{i}.json"
                if f.exists():
                    continue
                r = run_session(mode, prompt, f"{probe.name}/{prob.stem}")
                r.update(problem=prob.stem, model=mode, sample=i, prompt=prompt,
                         ts=datetime.datetime.now(datetime.timezone.utc).isoformat())
                f.write_text(json.dumps(r, indent=2))
                print(f"{prob.stem} {mode} #{i}: {r['status']} -> {r['text'][:60]!r}")


if __name__ == "__main__":
    main()
