#!/usr/bin/env python3

import re
import sys
from collections import Counter


WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*", re.UNICODE)


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as file:
        text = file.read().lower()

    words = WORD_RE.findall(text)
    for word, count in Counter(words).most_common(10):
        print(f"{word} {count}")


if __name__ == "__main__":
    main()
