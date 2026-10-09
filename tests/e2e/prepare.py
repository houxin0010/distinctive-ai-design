"""Create a fresh repo-scoped skill fixture; never overwrite an existing directory."""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FILES = ("SKILL.md", "agents/openai.yaml", "references/review-and-media.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    subprocess.run(["git", "init", "-q", str(destination)], check=True)
    skill = destination / ".agents/skills/distinctive-ai-design"
    for relative in FILES:
        target = skill / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    for filename in ("index.html", "design-prompt.txt"):
        shutil.copyfile(Path(__file__).parent / filename, destination / filename)
    (destination / "evidence").mkdir()
    (destination / "evidence/source-revision.txt").write_text(
        subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True)
        + subprocess.check_output(["git", "-C", str(ROOT), "status", "--short"], text=True))
    print(f"Prepared {destination}; Codex discovery and design are NOT VERIFIED.")


if __name__ == "__main__":
    main()
