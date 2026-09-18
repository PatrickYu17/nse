#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import shutil
import sys


NAME = "no-slop-engineering"
SOURCE = Path(__file__).resolve().parents[1]
LOCATIONS = {
    "shared": (".agents/skills", ".agents/skills"),
    "codex": (".agents/skills", ".agents/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "pi": (".pi/agent/skills", ".pi/skills"),
    "opencode": (".config/opencode/skills", ".opencode/skills"),
    "kilo": (".kilo/skills", ".kilo/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "gemini": (".gemini/skills", ".gemini/skills"),
    "copilot": (".copilot/skills", ".github/skills"),
}


def destination_for(harness, project=None):
    user_parent, project_parent = LOCATIONS[harness]
    if project is not None:
        root = Path(project).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"project directory does not exist: {root}")
        return root / project_parent / NAME
    home = Path.home()
    parent = home / user_parent
    if harness == "opencode" and os.environ.get("XDG_CONFIG_HOME"):
        parent = Path(os.environ["XDG_CONFIG_HOME"]).expanduser() / "opencode/skills"
    if harness == "pi" and os.environ.get("PI_CODING_AGENT_DIR"):
        parent = Path(os.environ["PI_CODING_AGENT_DIR"]).expanduser() / "skills"
    if not parent.is_absolute():
        raise ValueError("configured user directory must be absolute; use --destination instead")
    return parent / NAME


def install(destination, dry_run=False):
    destination = Path(destination).expanduser().absolute()
    if destination.name != NAME:
        raise ValueError(f"destination must end in /{NAME}")
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"destination already exists; preserve/move it before installing: {destination}")
    resolved = destination.resolve()
    if resolved == SOURCE or SOURCE in resolved.parents:
        raise ValueError("destination cannot be inside the source package")
    if not (SOURCE / "SKILL.md").is_file():
        raise ValueError("source package is incomplete: SKILL.md missing")
    if dry_run:
        print(f"Would copy {SOURCE} -> {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        SOURCE, destination, symlinks=True,
        ignore=shutil.ignore_patterns(".git", ".lake", "__pycache__", ".DS_Store"),
    )
    print(f"Package copied to {destination}")
    print(f"Entry: {destination / 'SKILL.md'}")
    print("Activation pending: complete always-on setup by merging adapters/activation.md into your host's automatically loaded instructions.")
    print("Reload or start a new session, then run the documented installation smoke check.")


def main():
    parser = argparse.ArgumentParser(description="Install the portable NSE package without overwriting files.")
    parser.add_argument("--harness", choices=sorted(LOCATIONS))
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--global", dest="global_scope", action="store_true", help="install for this user")
    scope.add_argument("--project", metavar="PATH", help="install in an existing project")
    scope.add_argument("--destination", metavar="PATH", help="explicit no-slop-engineering directory")
    parser.add_argument("--dry-run", action="store_true", help="show destination without copying files")
    args = parser.parse_args()
    if args.destination and args.harness:
        parser.error("--destination does not take --harness")
    if not args.destination and not args.harness:
        parser.error("--harness is required with --global or --project")
    try:
        destination = args.destination or destination_for(args.harness, args.project)
        install(destination, args.dry_run)
    except (ValueError, OSError, shutil.Error) as error:
        print(f"install: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
