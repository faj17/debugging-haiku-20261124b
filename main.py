"""One haiku about debugging, in the 5-7-5 syllable shape.

The whole entry is seventeen syllables about a midnight log line and
the stack trace that points the finger back at the author. The script
validates the shape (three lines, 5-7-5 syllables, 1-200 characters
total) and drops the haiku into /output/entry.txt.
"""

from pathlib import Path

# The haiku itself: 5-7-5 syllables, 73 characters including newlines.
HAIKU = (
    "Log line at midnight\n"
    "the stack trace points at my code\n"
    "my fault all along"
)

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200
EXPECTED_SYLLABLES = (5, 7, 5)

VOWELS = "aeiouy"


def count_syllables(word: str) -> int:
    """Count syllables in one word by vowel groups.

    A syllable is roughly one run of vowels; a silent trailing 'e'
    (as in 'line', 'trace', 'code') does not add one, and every word
    has at least one. Verified by hand against every word of the
    haiku in BUILD_LOG.md.
    """
    w = word.strip(".,;:!?\"'").lower()
    if not w:
        return 0
    groups = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            groups += 1
        prev_vowel = is_vowel
    if w.endswith("e") and groups > 1:
        groups -= 1
    return max(groups, 1)


def line_syllables(line: str) -> int:
    return sum(count_syllables(w) for w in line.split())


def validate(text: str) -> str:
    """Strip and sanity-check the haiku; raise ValueError on bad input."""
    haiku = text.strip()
    if not MIN_CHARS <= len(haiku) <= MAX_CHARS:
        raise ValueError(
            f"haiku must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(haiku)}"
        )
    lines = haiku.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be exactly 3 lines, got {len(lines)}")
    counts = tuple(line_syllables(line) for line in lines)
    if counts != EXPECTED_SYLLABLES:
        raise ValueError(
            f"haiku must be 5-7-5 syllables, got {counts}"
        )
    return haiku


def main() -> None:
    text = validate(HAIKU)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    counts = [line_syllables(line) for line in text.split("\n")]
    print(text)
    print(f"syllables per line: {counts} (total {sum(counts)})")
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
