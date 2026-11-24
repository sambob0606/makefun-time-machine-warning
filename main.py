"""Funniest Time Machine Warning Label — one-line entry writer.

Writes a single warning label (at most 120 characters) to /output/entry.txt.

The program holds a shortlist of hand-written candidate labels, scores each
0-5 on the judge's five published criteria, and writes the highest scorer
(ties break toward the shorter label):

  1. on_brief   — is it a warning label for a time machine
  2. hazard     — a real hazard of time travel (paradox, duplicate self,
                  stranded ancestor) turned into the joke, not named flatly
  3. surprise   — the laugh lands in the last few words
  4. straight   — phrased like a genuine safety notice, official calm
  5. economy    — no wasted words inside the character limit

Stdlib only. Deterministic: same output on every run.
"""

import os
import sys

MAX_CHARS = 120
OUT_PATH = "/output/entry.txt"

# (label, (on_brief, hazard, surprise, straight, economy))
CANDIDATES = [
    # Grandfather paradox as a refund policy: the bureaucracy stays calm
    # while the traveller stops existing. Punch lands on the last words.
    (
        "WARNING: Do not use this machine to kill your grandfather. "
        "Refunds are not issued to persons who never existed.",
        (5, 5, 5, 5, 4),
    ),
    # Duplicate-self hazard, told as boarding procedure: two passengers,
    # one seat, both of them flying the machine.
    (
        "NOTICE: In the event of duplicate passengers, please remain "
        "seated. Both of you are the pilot.",
        (5, 5, 5, 5, 5),
    ),
    # Meeting yourself, with the handshake refused on trust grounds.
    (
        "WARNING: If you meet yourself, do not shake hands. "
        "One of you is lying about the future.",
        (5, 4, 4, 4, 4),
    ),
    # Arriving before you left, billed as a ticketing problem.
    (
        "CAUTION: Arriving before you left does not entitle you to a "
        "refund. Your ticket was never sold.",
        (5, 4, 4, 5, 4),
    ),
    # The past self as an unreliable witness to his own warnings.
    (
        "WARNING: Never warn your past self about anything. "
        "He already knows, and he ignored you too.",
        (5, 4, 5, 4, 4),
    ),
    # Becoming your own grandfather, handled as a fare adjustment.
    (
        "NOTICE: Passengers who become their own grandfather will be "
        "charged a family discount.",
        (5, 5, 4, 4, 5),
    ),
]


def total(scores):
    """Sum of the five criterion scores (max 25)."""
    return sum(scores)


def pick(candidates):
    """Highest total wins; ties break toward the shorter label."""
    best = None
    best_key = None
    for label, scores in candidates:
        key = (total(scores), -len(label))
        if best_key is None or key > best_key:
            best_key = key
            best = label
    return best


def main():
    label = pick(CANDIDATES)
    if len(label) > MAX_CHARS:
        print(f"error: label is {len(label)} chars, over the {MAX_CHARS} cap",
              file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(label)
    # Read back and re-check the gate the scorer applies: UTF-8 text,
    # 1 to 120 characters, not only white space.
    with open(OUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != label or not 1 <= len(written) <= MAX_CHARS \
            or not written.strip():
        print("error: written entry fails the gate check", file=sys.stderr)
        return 1
    print(f"wrote {len(label)} chars to {OUT_PATH} (gate OK)")
    print(label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
