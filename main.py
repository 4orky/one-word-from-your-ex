"""One word from your ex.

The brief asks for exactly one word: the word your ex would use to
describe you. A judge reads entries two at a time and keeps the
funniest, most painfully honest word, weighing these in order:

    1. it is really a word an ex would say about a former partner
    2. it makes the judge laugh out loud, through surprise or a turn
    3. it stings with recognition, because it is plainly true
    4. it lands instantly, needing no explanation at all
    5. it is relatable, naming something people have lived through

Twelve words were drafted by hand and marked 0-10 on each point above.
The winner is the highest total, with a tie going to the shorter word.
This program writes the winner, and nothing else, to /output/entry.txt.
"""

import os
import re

OUTPUT_DIR = "/output"
ENTRY_PATH = os.path.join(OUTPUT_DIR, "entry.txt")
STAGING_PATH = os.path.join(OUTPUT_DIR, ".entry.tmp")

WORD_PATTERN = re.compile(r"[A-Za-z]+")

# Marks are (believable, funny, sting, instant, relatable), each out of 10.
# Listed weakest first, so the winner closes the list.
ENTRIES = (
    {
        "word": "Detour",
        "why": "A scenic route that went nowhere. Cute image, but it reads "
               "more like a travel complaint than a verdict on a person.",
        "marks": (7, 8, 7, 7, 7),
    },
    {
        "word": "Archived",
        "why": "Filed away like an old email thread. Modern and wry, yet "
               "cooler than the best picks: more shrug than sting.",
        "marks": (8, 7, 7, 8, 7),
    },
    {
        "word": "Draft",
        "why": "A rough draft of a boyfriend. Clean and funny, but on its "
               "own it leans too hard on unfinished work to carry the joke.",
        "marks": (8, 7, 8, 8, 7),
    },
    {
        "word": "Backup",
        "why": "Kept around in case the first choice fell through. Honest "
               "and relatable, though it sounds more practical than funny.",
        "marks": (8, 7, 7, 8, 8),
    },
    {
        "word": "Trial",
        "why": "A trial run, thirty days and then the subscription lapsed. "
               "Short and clear, but it loses the human sting of the top pick.",
        "marks": (7, 7, 8, 9, 8),
    },
    {
        "word": "Understudy",
        "why": "Never got the lead role. Theatrical and sad-funny, but it "
               "asks for half a second more thought than the winner does.",
        "marks": (9, 8, 8, 7, 7),
    },
    {
        "word": "Rehearsal",
        "why": "The run-through before opening night. Close cousin of the "
               "winner, yet it belongs to the stage, not the relationship.",
        "marks": (8, 8, 8, 8, 8),
    },
    {
        "word": "Warmup",
        "why": "The act before the main event. Punchy and instantly "
               "understood, but it leans on a sports metaphor, not a story.",
        "marks": (8, 8, 8, 9, 8),
    },
    {
        "word": "Intern",
        "why": "Temporary, unpaid, learning on the job, replaced by the "
               "full-time hire. A funny image with a real sting in it.",
        "marks": (9, 9, 8, 8, 8),
    },
    {
        "word": "Placeholder",
        "why": "Holding the seat until the real thing arrived. Painfully "
               "accurate, though a touch clinical for a laugh-out-loud word.",
        "marks": (9, 8, 9, 8, 8),
    },
    {
        "word": "Prototype",
        "why": "The test version; the next one got the finished product. "
               "Sharp, tech-flavoured and self-deprecating, a close second.",
        "marks": (9, 9, 9, 9, 8),
    },
    {
        "word": "Practice",
        "why": "I was just practice. The whole relationship reframed in a "
               "single word: the rehearsal before the real thing. Universal, "
               "instant, and it stings because the entrant plainly knows it.",
        "marks": (10, 9, 10, 10, 10),
    },
)


def check_marks(entry):
    """Check one candidate's marks: exactly five whole numbers, each 0-10.
    A typo in a score tuple must fail loudly instead of skewing the pick."""
    marks = entry["marks"]
    if len(marks) != 5:
        raise ValueError("%s must carry five marks, got %d"
                         % (entry["word"], len(marks)))
    for mark in marks:
        if not isinstance(mark, int) or isinstance(mark, bool):
            raise TypeError("%s has a non-integer mark: %r"
                            % (entry["word"], mark))
        if not 0 <= mark <= 10:
            raise ValueError("%s has a mark outside 0-10: %d"
                             % (entry["word"], mark))
    return entry


def total_marks(entry):
    """Add up one candidate's five marks."""
    return sum(check_marks(entry)["marks"])


def check_entry(text):
    """Check one word against the sealed gate: UTF-8 text, 1-24
    characters, not only whitespace, and exactly one plain word."""
    if not isinstance(text, str):
        raise TypeError("entry must be text, got %s" % type(text).__name__)
    text.encode("utf-8")
    if not 1 <= len(text) <= 24:
        raise ValueError("entry length %d is outside 1-24" % len(text))
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has surrounding whitespace")
    if WORD_PATTERN.fullmatch(text) is None:
        raise ValueError("entry must be a single plain word")
    return text


def choose(entries):
    """Return the winning word: highest total marks, ties to the shorter."""
    for entry in entries:
        check_entry(entry["word"])
    winner = max(entries, key=lambda e: (total_marks(e), -len(e["word"])))
    return winner["word"]


def publish(word):
    """Write the word to the entry file via a staging file, so a failure
    mid-write can never leave a partial entry behind for the gate."""
    check_entry(word)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(STAGING_PATH, "w", encoding="utf-8") as handle:
        handle.write(word)
    os.chmod(STAGING_PATH, 0o644)
    os.replace(STAGING_PATH, ENTRY_PATH)
    with open(ENTRY_PATH, encoding="utf-8") as handle:
        stored = handle.read()
    check_entry(stored)
    if stored != word:
        raise ValueError("entry file does not match the chosen word")
    return stored


def run():
    chosen = choose(ENTRIES)
    stored = publish(chosen)
    if stored != chosen:
        raise ValueError("stored entry differs from the chosen word")
    print(chosen)
    return 0


_RUN_AS_SCRIPT = __name__ == "__main__"
if _RUN_AS_SCRIPT:
    raise SystemExit(run())
