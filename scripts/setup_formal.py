#!/usr/bin/env python3
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys


SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG = '''name = "nse_formal"
defaultTargets = ["Formal"]
moreLeanArgs = ["-DwarningAsError=true"]

[[require]]
name = "leanfmt"
path = "../vendor/leanfmt"

[[lean_lib]]
name = "Formal"
'''


def require_plain_path(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"symlinked managed path: {part}")


def snapshot(root):
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".lake" in relative.parts:
            continue
        if path.is_symlink():
            raise ValueError(f"symlink in vendor tree: {path}")
        if path.is_file():
            result[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            result[str(relative)] = "directory"
        else:
            raise ValueError(f"unsupported vendor entry: {path}")
    return result


def scaffold(project, scaffold_only):
    require_plain_path(project)
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")
    formal = project / "formal"
    vendor = project / "vendor" / "leanfmt"
    source = SKILL_DIR / "vendor" / "leanfmt"
    toolchain = (source / "lean-toolchain").read_bytes()
    files = {
        "lakefile.toml": CONFIG.encode(),
        "lean-toolchain": toolchain,
        "Formal.lean": b"import Formal.Spec\nimport Formal.Impl\nimport Formal.Proofs\n",
        "Formal/Spec.lean": b"namespace Formal\nend Formal\n",
        "Formal/Impl.lean": b"import Formal.Spec\n\nnamespace Formal\nend Formal\n",
        "Formal/Proofs.lean": b"import Formal.Impl\n\nnamespace Formal\nend Formal\n",
        "theorems.txt": b"# Register fully qualified guarantee theorems, one per line.\n",
        "check-proofs.py": (SKILL_DIR / "scripts" / "check-proofs.py").read_bytes(),
        ".gitignore": b".lake/\n__pycache__/\n",
    }
    for path in (formal, vendor, *(formal / name for name in files)):
        require_plain_path(path)
    if formal.exists() and not formal.is_dir():
        raise ValueError(f"not a directory: {formal}")
    if (formal / "lakefile.lean").exists() or (formal / "lakefile.lean").is_symlink():
        raise ValueError("existing lakefile.lean requires manual integration; no files changed")
    existing = (formal / "lakefile.toml").exists()
    if existing:
        for name in files:
            if not (formal / name).is_file():
                raise ValueError(f"incomplete or incompatible package: missing {name}")
        for name in ("lakefile.toml", "lean-toolchain", "check-proofs.py"):
            if (formal / name).read_bytes() != files[name]:
                raise ValueError(f"existing {name} differs; integrate manually, no files changed")
    elif formal.exists() and any(formal.iterdir()):
        raise ValueError("nonempty formal/ without managed configuration; no files changed")
    source_snapshot = snapshot(source)
    if vendor.exists():
        if not vendor.is_dir() or snapshot(vendor) != source_snapshot:
            raise ValueError("existing vendor/leanfmt differs; no files changed")
    elif vendor.parent.exists() and not vendor.parent.is_dir():
        raise ValueError("vendor is not a directory; no files changed")
    if not scaffold_only:
        for command in ("elan", "lake"):
            if shutil.which(command) is None:
                raise ValueError(f"{command} unavailable; provision Lean or use --scaffold-only")

    if not vendor.exists():
        vendor.parent.mkdir(exist_ok=True)
        shutil.copytree(source, vendor, ignore=shutil.ignore_patterns(".lake"))
    if not existing:
        formal.mkdir(exist_ok=True)
        (formal / "Formal").mkdir()
        for name, content in files.items():
            with (formal / name).open("xb") as target:
                target.write(content)
    if scaffold_only:
        print(f"Scaffold ready: {formal}. Lean was NOT run; no proof is verified.")
    else:
        subprocess.run(["lake", "update", "--keep-toolchain"], cwd=formal, check=True)
        subprocess.run(["lake", "build", "Formal"], cwd=formal, check=True)
        print(f"Scaffold build passed: {formal}. Implement and register guarantee theorems next.")
    print("Delivery checks: python3 check-proofs.py; lake exe fmt --check -r Formal.lean Formal")


def main():
    parser = argparse.ArgumentParser(description="Create a non-overwriting NSE formal package.")
    parser.add_argument("--scaffold-only", action="store_true", help="do not invoke Lean or Lake")
    parser.add_argument("project", nargs="?", default=".")
    args = parser.parse_args()
    try:
        scaffold(Path(os.path.abspath(args.project)), args.scaffold_only)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"setup-formal: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
