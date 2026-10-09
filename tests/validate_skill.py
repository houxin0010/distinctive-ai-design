"""Repository contract checks, not a Codex runtime or visual-quality test."""
import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from markdown_it import MarkdownIt
except ImportError:
    sys.exit("Missing test dependency: python3 -m pip install -r tests/requirements.txt")

REQUIRED = ("SKILL.md", "agents/openai.yaml", "README.md", "README.en.md",
            "references/review-and-media.md")
EXPECTED_NAME = "distinctive-ai-design"


class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML parsing that refuses ambiguous duplicate keys."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_mapping(text):
    value = yaml.load(text, Loader=UniqueSafeLoader)
    if not isinstance(value, dict):
        raise ValueError("YAML root must be a mapping")
    return value


def require_text(mapping, key, max_length=None):
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    if max_length and len(value) > max_length:
        raise ValueError(f"{key} exceeds {max_length} characters")
    return value


def markdown_targets(text):
    # CommonMark parser handles inline/reference links and images, ignores code.
    def walk(tokens):
        for token in tokens:
            if token.type in ("link_open", "image"):
                yield token.attrGet("href" if token.type == "link_open" else "src")
            if token.children:
                yield from walk(token.children)
    yield from walk(MarkdownIt("commonmark").parse(text))


def validate(root):
    root = Path(root).resolve()
    errors = []
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
        else:
            try:
                if not path.read_text(encoding="utf-8").strip():
                    errors.append(f"empty required file: {relative}")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{relative}: {exc}")

    name = None
    try:
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z", skill, re.S)
        if not match:
            raise ValueError("SKILL.md must start with --- delimited YAML front matter")
        metadata = load_mapping(match[1])
        name = require_text(metadata, "name", 64)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("name must be lowercase letters/digits with single hyphens")
        if name != EXPECTED_NAME:
            raise ValueError(f"name must match repository contract: {EXPECTED_NAME}")
        require_text(metadata, "description", 1024)
        if not match[2].strip():
            raise ValueError("SKILL.md instruction body is empty")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"SKILL.md: {exc}")

    try:
        config = load_mapping((root / "agents/openai.yaml").read_text(encoding="utf-8"))
        interface = config.get("interface")
        if not isinstance(interface, dict):
            raise ValueError("interface must be a mapping")
        require_text(interface, "display_name")
        require_text(interface, "short_description")
        prompt = require_text(interface, "default_prompt")
        calls = re.findall(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)", prompt)
        if calls != [name]:
            raise ValueError("default_prompt must invoke exactly $<SKILL.md name>")
        if "policy" in config:
            policy = config["policy"]
            if not isinstance(policy, dict):
                raise ValueError("policy must be a mapping")
            if "allow_implicit_invocation" in policy and not isinstance(
                    policy["allow_implicit_invocation"], bool):
                raise ValueError("allow_implicit_invocation must be a boolean")
        for key in ("icon_small", "icon_large", "brand_color"):
            if key in interface:
                value = require_text(interface, key)
                if key == "brand_color":
                    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
                        raise ValueError("brand_color must be #RRGGBB")
                else:
                    target = (root / value).resolve()
                    if not target.is_relative_to(root) or not target.is_file():
                        raise ValueError(f"{key} must reference a file inside the skill")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"agents/openai.yaml: {exc}")

    for relative in ("README.md", "README.en.md"):
        try:
            text = (root / relative).read_text(encoding="utf-8")
            calls = re.findall(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)", text)
            if name not in calls or any(call != name for call in calls):
                errors.append(f"{relative}: documented $skill calls must match SKILL.md name")
        except (OSError, UnicodeError):
            pass  # Already reported by required-file check.

    # Check repository Markdown, not generated outputs, dependencies or Git internals.
    excluded = {".git", ".venv", "venv", "node_modules", "artifacts", "__pycache__"}
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in excluded for part in relative.parts):
            continue
        try:
            for target in markdown_targets(path.read_text(encoding="utf-8")):
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                destination = (path.parent / unquote(url.path)).resolve()
                if not destination.is_relative_to(root) or not destination.exists():
                    errors.append(f"{relative}: broken/escaping relative link: {target}")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print("PASS required files, strict YAML, metadata, interface, skill names, Markdown file links")
    print("NOT VERIFIED Codex discovery/invocation, generated design, screenshots, visual review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
