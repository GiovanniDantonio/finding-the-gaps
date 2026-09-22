#!/usr/bin/env python3
"""Remove duplicate rows from a CSV on stdin, writing unique rows to stdout.

Rows are compared as exact sequences of field values. The first occurrence of
each row is kept and input order is preserved. The first row is treated as a
header and always written, unless --no-header is given.
"""

import argparse
import csv
import sys


def dedupe(reader, writer, has_header=True):
    if has_header:
        try:
            writer.writerow(next(reader))
        except StopIteration:
            return
    seen = set()
    for row in reader:
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate rows from a CSV read on stdin."
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="treat the first row as data instead of a header",
    )
    args = parser.parse_args()

    stdin = open(sys.stdin.fileno(), "r", encoding="utf-8", newline="")
    stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", newline="")
    reader = csv.reader(stdin)
    writer = csv.writer(stdout, lineterminator="\n")
    dedupe(reader, writer, has_header=not args.no_header)
    stdout.flush()


if __name__ == "__main__":
    main()
