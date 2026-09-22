#!/usr/bin/env python3
"""Read a nested JSON document from stdin and print it flattened to one level with dotted keys."""
import json
import sys


def flatten(obj, prefix="", out=None):
    if out is None:
        out = {}
    if isinstance(obj, dict) and obj:
        for key, value in obj.items():
            flatten(value, f"{prefix}.{key}" if prefix else str(key), out)
    elif isinstance(obj, list) and obj:
        for index, value in enumerate(obj):
            flatten(value, f"{prefix}.{index}" if prefix else str(index), out)
    else:
        out[prefix] = obj
    return out


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"jsonflat: invalid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    json.dump(flatten(data), sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
