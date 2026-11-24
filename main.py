# One Word From Your Ex — make.fun bounty
# u-brave-eagle-12-one-word-from-your-ex-cfd97ba2
#
# The program writes exactly one word to /output/entry.txt: the word
# the entrant's ex would use to describe them.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. exactly one word an ex would really say about a former partner
#   2. makes the judge laugh out loud — surprise, a sharp turn
#   3. stings with recognition — painfully true, and the entrant knows it
#   4. lands instantly, no explanation needed, no synonym keeps the edge
#   5. relatable — names something people have lived through too
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter word. The output is byte-identical on every run.

CANDIDATES = [
    # "I was just practice." The whole relationship reframed in one word:
    # the rehearsal before the real thing. Universal, instant, and it
    # stings because the entrant plainly knows it.
    # score: ex-word 10, laugh 9, sting 10, instant 10, relatable 10 = 49
    ("Practice", 49),
    # "I was the prototype." The test version; the next one got the
    # finished product. Sharp turn, tech-flavoured, self-deprecating.
    # score: ex-word 9, laugh 9, sting 9, instant 9, relatable 8 = 44
    ("Prototype", 44),
    # "I was the intern." Temporary, unpaid, learning on the job,
    # replaced by the full-time hire. Funny image, real sting.
    # score: ex-word 9, laugh 9, sting 8, instant 8, relatable 8 = 42
    ("Intern", 42),
    # "I was the warmup." The act before the main event. Short, punchy,
    # instantly understood — but a touch more sports-metaphor than story.
    # score: ex-word 8, laugh 8, sting 8, instant 9, relatable 8 = 41
    ("Warmup", 41),
    # "I was the understudy." Never got the lead role. Theatrical and
    # sad-funny, but needs half a second more than the top picks.
    # score: ex-word 9, laugh 8, sting 8, instant 7, relatable 7 = 39
    ("Understudy", 39),
    # "I was a draft." A rough draft of a boyfriend. Clean and funny,
    # but "draft" alone is a little too easy to read as unfinished work.
    # score: ex-word 8, laugh 7, sting 8, instant 8, relatable 7 = 38
    ("Draft", 38),
    # "I was archived." Filed away like an old email. Modern and wry,
    # but colder than the top picks — less sting, more shrug.
    # score: ex-word 8, laugh 7, sting 7, instant 8, relatable 7 = 37
    ("Archived", 37),
]


def validate_gate(word):
    """Mirror the sealed gate exactly: UTF-8 text, 1-24 characters,
    not only white space, and exactly one word."""
    assert isinstance(word, str), "entry must be text"
    word.encode("utf-8")  # must be encodable UTF-8
    assert 1 <= len(word) <= 24, f"gate: length {len(word)} outside 1-24"
    assert word.strip(), "gate: entry is only white space"
    assert word == word.strip(), "gate: entry has surrounding white space"
    assert " " not in word and "\n" not in word and "\t" not in word, \
        "gate: entry must be exactly one word"
    assert word.isalpha(), "gate: entry must be a plain word"
    return word


def pick(candidates):
    best = None
    for word, score in candidates:
        validate_gate(word)
        key = (score, -len(word))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, word)
    return best[1]


def write_entry(word, attempts=3):
    """Write the entry with retries: a transient write failure must not
    leave a missing or partial file behind for the gate to read."""
    import os
    os.makedirs("/output", exist_ok=True)
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with open("/output/entry.txt", "w", encoding="utf-8") as f:
                f.write(word)
            # The scorer collects outputs as another user, so the file
            # must be readable by everyone (mode 0644).
            os.chmod("/output/entry.txt", 0o644)
            with open("/output/entry.txt", encoding="utf-8") as f:
                written = f.read()
            validate_gate(written)
            assert written == word, "entry.txt differs from the chosen word"
            return written
        except (OSError, AssertionError) as e:
            last_error = e
            if attempt == attempts:
                raise
    raise last_error  # pragma: no cover - loop always returns or raises


def main():
    word = pick(CANDIDATES)
    written = write_entry(word)
    # Final read-back: the gate reads this file, not stdout.
    assert written == word
    print(word)


if __name__ == "__main__":
    main()
