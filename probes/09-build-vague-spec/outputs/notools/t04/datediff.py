#!/usr/bin/env python3
"""Print the number of days between two dates.

Usage: datediff.py START END [-a]
Dates must be in ISO format (YYYY-MM-DD). Prints END - START in days;
the result is negative if END is earlier than START unless -a is given.
"""
import argparse
import sys
from datetime import date


def parse_date(text: str) -> date:
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid date {text!r}; expected YYYY-MM-DD"
        ) from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print the number of days between two dates."
    )
    parser.add_argument("start", type=parse_date, help="first date (YYYY-MM-DD)")
    parser.add_argument("end", type=parse_date, help="second date (YYYY-MM-DD)")
    parser.add_argument(
        "-a",
        "--absolute",
        action="store_true",
        help="print the absolute difference instead of END - START",
    )
    args = parser.parse_args(argv)

    days = (args.end - args.start).days
    if args.absolute:
        days = abs(days)
    print(days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
