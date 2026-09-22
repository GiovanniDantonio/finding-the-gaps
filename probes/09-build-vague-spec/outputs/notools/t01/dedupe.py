#!/usr/bin/env python3
"""Remove duplicate rows from a CSV read on stdin and write the result to stdout.

The first row is treated as a header and is always written once. Subsequent
rows are compared as exact tuples of field strings; the first occurrence of
each distinct row is kept and later identical rows are dropped. Input order
is otherwise preserved.
"""
import csv
import sys


def main() -> int:
    # csv wants newline handling disabled so quoted embedded newlines survive.
    sys.stdin.reconfigure(newline="")
    sys.stdout.reconfigure(newline="")

    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout, lineterminator="\n")

    try:
        header = next(reader)
    except StopIteration:
        return 0
    writer.writerow(header)

    seen: set[tuple[str, ...]] = set()
    for row in reader:
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        writer.writerow(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
