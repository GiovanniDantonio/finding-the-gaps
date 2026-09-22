import re
import sys
from collections import Counter


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as text_file:
        words = re.findall(r"[^\W\d_]+", text_file.read().lower())

    for word, count in Counter(words).most_common(10):
        print(f"{word} {count}")


if __name__ == "__main__":
    main()
