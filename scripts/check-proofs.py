#!/usr/bin/env python3
import re
from pathlib import Path
import subprocess
import sys


ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9']*(?:\.[A-Za-z_][A-Za-z_0-9']*)+")


def read_theorems(path):
    names = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        name = line.split("#", 1)[0].strip()
        if not name:
            continue
        if not NAME.fullmatch(name):
            raise ValueError(f"{path.name}:{number}: expected a fully qualified Lean declaration")
        if name in names:
            raise ValueError(f"{path.name}:{number}: duplicate theorem {name}")
        names.append(name)
    if not names:
        raise ValueError("no guarantee theorems registered in theorems.txt; scaffold is not a proof")
    return names


def check_axioms(name, output):
    prefix = re.escape(f"'{name}'")
    empty = re.findall(prefix + r" does not depend on any axioms", output)
    lists = re.findall(prefix + r" depends on axioms:\s*\[([^\]]*)\]", output)
    if len(empty) + len(lists) != 1:
        raise ValueError(f"{name}: missing or ambiguous Lean axiom report:\n{output}")
    axioms = {item.strip() for item in lists[0].split(",") if item.strip()} if lists else set()
    forbidden = axioms - ALLOWED_AXIOMS
    if forbidden:
        raise ValueError(f"{name}: unapproved axioms: {', '.join(sorted(forbidden))}")
    return axioms


def main():
    root = Path(__file__).resolve().parent
    try:
        names = read_theorems(root / "theorems.txt")
        subprocess.run(["lake", "build", "Formal"], cwd=root, check=True)
        for name in names:
            result = subprocess.run(
                ["lake", "env", "lean", "-DwarningAsError=true", "--stdin"],
                input=f"import Formal\n#print axioms {name}\n",
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=root,
            )
            if result.returncode:
                raise ValueError(f"{name}: Lean audit failed:\n{result.stdout}")
            axioms = check_axioms(name, result.stdout)
            print(f"PASS {name}: axioms = {', '.join(sorted(axioms)) or '(none)'}")
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"check-proofs: {error}", file=sys.stderr)
        return 1
    print("Axiom policy passed. Theorem relevance and model/port fidelity require separate review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
