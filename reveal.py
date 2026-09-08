#!/usr/bin/env python3
"""
Reveals one stage of a reference solution at a time, so you can check
your work (or get unstuck) without spoiling every other stage.

Usage:
    python reveal.py backend 3
    python reveal.py frontend 2
    python reveal.py backend all       # prints the whole solution file
"""

import re
import sys

SOLUTIONS = {
    "backend": "backend/solutions/main_solution.py",
    "frontend": "frontend/solutions/App_solution.jsx",
}


def extract_stage(text, stage):
    # Marker lines can be #, //, or {/* */} comments — match any of them
    # so both Python and JSX solution files work with the same script.
    # A stage can appear in more than one marker pair (e.g. a React
    # state/effect block plus a separate JSX snippet using it) — collect
    # every pair, not just the first.
    pattern = re.compile(
        rf"^.*STAGE {stage} SOLUTION START.*$\n"
        rf"([\s\S]*?)"
        rf"^.*STAGE {stage} SOLUTION END.*$",
        re.MULTILINE,
    )
    matches = pattern.findall(text)
    if not matches:
        return None
    separator = "\n\n    ⋮ (continues elsewhere in the file)\n\n"
    return separator.join(m.rstrip("\n") for m in matches)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in SOLUTIONS:
        print(__doc__)
        sys.exit(1)

    component, stage = sys.argv[1], sys.argv[2]
    path = SOLUTIONS[component]

    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Couldn't find {path} — run this from the project root.")
        sys.exit(1)

    if stage == "all":
        print(text)
        return

    snippet = extract_stage(text, stage)
    if snippet is None:
        print(f"No stage {stage} found in {path}.")
        sys.exit(1)

    print(f"\n--- {component} / stage {stage} solution " + "-" * 20)
    print(snippet)
    print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
