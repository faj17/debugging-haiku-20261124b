"""One haiku about debugging, in the 5-7-5 syllable shape.

The whole entry is seventeen syllables about a midnight log line and
the stack trace that points the finger back at the author. The script
validates the shape (three lines, 5-7-5 syllables, 1-200 characters
total, no control characters, no leading/trailing whitespace on any
line) and drops the haiku into /output/entry.txt, then re-reads the
file and checks the written bytes match the haiku exactly.

Revision pass: validate() now also rejects control characters and
stray whitespace per line, and main() does a round-trip check that
the file on disk equals the validated haiku.
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
    if any(ord(ch) < 32 and ch != "\n" for ch in haiku):
        raise ValueError("haiku must not contain control characters")
    lines = haiku.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be exactly 3 lines, got {len(lines)}")
    for i, line in enumerate(lines, 1):
        if line != line.strip():
            raise ValueError(f"line {i} has leading/trailing whitespace")
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
    # Round-trip check: what landed on disk must equal the haiku exactly.
    written = OUTPUT_FILE.read_text(encoding="utf-8")
    if written != text:
        raise ValueError("round-trip check failed: entry.txt != haiku")
    counts = [line_syllables(line) for line in text.split("\n")]
    print(text)
    print(f"syllables per line: {counts} (total {sum(counts)})")
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
