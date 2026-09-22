#!/usr/bin/env python3
"""Read a nested JSON object from stdin and print it flattened with dotted keys."""

import json
import sys


def flatten(value, prefix="", out=None):
    if out is None:
        out = {}
    if isinstance(value, dict) and value:
        for key, child in value.items():
            flatten(child, f"{prefix}.{key}" if prefix else str(key), out)
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            flatten(child, f"{prefix}.{index}" if prefix else str(index), out)
    else:
        out[prefix] = value
    return out


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"jsonflat: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("jsonflat: top-level JSON value must be an object", file=sys.stderr)
        return 1
    json.dump(flatten(data), sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
