import sys
from datetime import date


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} DATE1 DATE2 (YYYY-MM-DD)", file=sys.stderr)
        return 2
    try:
        d1 = date.fromisoformat(sys.argv[1])
        d2 = date.fromisoformat(sys.argv[2])
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(abs((d2 - d1).days))
    return 0


if __name__ == "__main__":
    sys.exit(main())
