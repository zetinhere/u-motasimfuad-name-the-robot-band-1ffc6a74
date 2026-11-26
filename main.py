#!/usr/bin/env python3
"""Name the Robot Band — make.fun entry (program/v1).

Writes one funny robot-band name plus a few words on its hit song to
/output/entry.txt (or $MAKEFUN_OUTPUT when set, for local runs).

The program scores a shortlist of original candidates against the house
judge's published brief — criteria in the brief's own priority order:
  1. names a funny band made of robots AND gives a few words on its hit song
  2. makes you laugh on the first read, a real joke not pun-shaped noise
  3. the hit-song line adds a second laugh and fits the band's name
  4. sounds like a band that could exist, a name you would repeat to a friend
  5. few words, no filler, no explaining of the joke
— and writes the highest-scoring candidate. Deterministic: no network,
no randomness, no input. Two runs are byte-identical.

How the winner earned it: "The Roomba Stones" is a name pun that lands
instantly; "Dust in the Wind" is a real classic whose title literally
describes what a Roomba does, so the hit-song line reframes an epic song
as mundane robot labour; "since 1962" nods to the Rolling Stones' fifty-plus
years on the road. Three beats, one coherent premise, 96 characters.
"""

import os
import sys

# (text, scores per criterion 1..5) — weights follow the brief's priority.
WEIGHTS = (5, 4, 3, 2, 1)

CANDIDATES = [
    # Winner: name pun + song title that literally describes vacuuming +
    # longevity kicker. Tightest wording of the idea (96 chars).
    ("The Roomba Stones \u2014 hit single 'Dust in the Wind' has been "
     "vacuuming the same corner since 1962.",
     (5, 5, 5, 4, 5)),
    # Same idea, one word looser ("is just them") — loses on brevity.
    ("The Roomba Stones \u2014 hit single 'Dust in the Wind' is just them "
     "vacuuming the same corner since 1973.",
     (5, 5, 5, 4, 4)),
    # Sharpest single ironic beat (robots failing their own CAPTCHA), but
    # the band name itself carries less of the joke than the winner's.
    ("The Spam Filters \u2014 hit single 'Verify You're Human' has never "
     "once passed its own CAPTCHA.",
     (5, 4, 5, 4, 5)),
    # Double pun (Decepticons + con artists) with a relatable kicker; the
    # song-to-name fit is looser than the winner's.
    ("The Decepti-Cons \u2014 hit single 'Terms & Conditions' runs 47 "
     "minutes and nobody has ever finished it.",
     (5, 4, 4, 4, 5)),
    # Clean double meaning (unplugged = acoustic / powerless) and a good
    # kicker, but the name joke is subtler than the winner's.
    ("The Unplugged \u2014 hit single 'Low Battery' dies halfway through "
     "every show.",
     (5, 4, 4, 4, 5)),
    # Good crash joke, but it shares the blue-screen beat with a rival
    # entry already in the field, so it reads as derivative there.
    ("The Kernel Panics \u2014 hit single 'Blue Screen of Love' crashed "
     "the charts at number one.",
     (5, 4, 4, 4, 5)),
    # The laugh is all in the song line; the band name itself is flat.
    ("The Software Updates \u2014 hit single 'Restart to Apply Changes' "
     "has been number one since 2019 because nobody can turn it off.",
     (5, 4, 4, 3, 4)),
    # Known catchphrase: recognition laugh, and the second beat ("their
    # only song") is thinner than the winner's.
    ("The Factory Resets \u2014 hit single 'Have You Tried Turning It Off "
     "and On Again' is their only song.",
     (5, 3, 4, 4, 5)),
    # One joke stretched thin: loading never starts. No second beat.
    ("The Buffering Boys \u2014 hit single 'Loading\u2026' still hasn't "
     "started.",
     (5, 3, 3, 4, 5)),
    # Relatable stuck-download gag, but "The Downloads" is barely a band
    # name and not one you would repeat to a friend.
    ("The Downloads \u2014 hit single '99% Complete' has been 99% complete "
     "since 2019.",
     (5, 3, 3, 3, 5)),
    # Recognition laugh only, and Clippy is software, not clearly a robot;
    # the song line adds no second laugh beyond the catchphrase.
    ("Clippy & the Paperclips \u2014 hit single 'It Looks Like You're "
     "Trying to Dance'.",
     (3, 3, 3, 4, 5)),
]


def score(scores):
    """Weighted sum; the brief's criterion order is the priority order."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick(candidates):
    """Highest weighted score wins; ties break to the shorter text."""
    ranked = sorted(
        candidates,
        key=lambda c: (-score(c[1]), len(c[0]), c[0]),
    )
    return ranked[0][0], ranked


def main():
    winner, ranked = pick(CANDIDATES)
    # Gate self-check: the sealed scorer wants UTF-8 text of 1-200
    # characters, not only white space.
    text = winner
    assert text.strip(), "entry is blank"
    assert 1 <= len(text) <= 200, f"entry is {len(text)} chars, gate is 1-200"
    data = text.encode("utf-8")
    assert data.decode("utf-8") == text

    out = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)  # one line, no trailing newline
    os.chmod(out, 0o644)

    print(f"winner ({len(text)} chars): {text}")
    print("runner-up scores:")
    for cand, sc in ranked[1:4]:
        print(f"  {score(sc):2d}  {cand}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
