"""Run every problem in a probe against a list of models and save raw outputs.

Usage: python harness/run.py probes/<slug> --models gpt,claude,gemini --samples 5
Writes probes/<slug>/outputs/<model>/<problem>/sample_<n>.json
"""
import argparse, json, pathlib, datetime

def call_model(model: str, prompt: str) -> dict:
    raise NotImplementedError("wire up the API clients here; return {'text': ..., 'version': ..., 'usage': ...}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("probe"); ap.add_argument("--models", required=True); ap.add_argument("--samples", type=int, default=3)
    a = ap.parse_args()
    probe = pathlib.Path(a.probe)
    for prob in sorted((probe / "problems").glob("p*.md")):
        prompt = prob.read_text()
        for model in a.models.split(","):
            out = probe / "outputs" / model / prob.stem
            out.mkdir(parents=True, exist_ok=True)
            for i in range(a.samples):
                r = call_model(model, prompt)
                r.update(problem=prob.stem, model=model, sample=i, prompt=prompt, ts=datetime.datetime.utcnow().isoformat())
                (out / f"sample_{i}.json").write_text(json.dumps(r, indent=2))

if __name__ == "__main__":
    main()
