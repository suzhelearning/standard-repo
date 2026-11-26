"""Check the published v2 documentation, type contracts, and skill alignment using only Python's standard library."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/standardize-repo/SKILL.md")
CORE_ARCHETYPES = ("lib", "app", "assets", "dataset", "content", "research")
ALL_TARGETS = (*CORE_ARCHETYPES, "workspace")
REQUIRED_CARD_FIELDS = (
    "交付物与入口",
    "布局与生态优先",
    "禁止越界",
    "最小可执行不变量",
)


def check_links(path, errors):
    fenced = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in re.findall(r"\]\(([^()\s]+)\)", line):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            if not (path.parent / unquote(url.path)).is_file():
                errors.append(f"{path.relative_to(ROOT)}:{number}: fix missing link {target}")


def extract_sections(markdown_text):
    headings = list(re.finditer(r"^### `([a-z]+)`：", markdown_text, re.MULTILINE))
    sections = {}
    for idx, match in enumerate(headings):
        name = match.group(1)
        start = match.end()
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(markdown_text)
        sections[name] = markdown_text[start:end]
    return sections


def check(tag):
    errors = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    spec = (ROOT / "docs/repository-types.md").read_text(encoding="utf-8")
    verification = (ROOT / "docs/verification.md").read_text(encoding="utf-8")
    workflow = (ROOT / "docs/migration.md").read_text(encoding="utf-8")
    skill = (ROOT / SKILL).read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    # 1. Verify the 6 core archetypes table in docs/repository-types.md
    table_types = re.findall(r"^\| `([a-z]+)` \|", spec, re.MULTILINE)
    if tuple(table_types) != CORE_ARCHETYPES:
        errors.append(
            "docs/repository-types.md: align the archetype selection table with "
            + ", ".join(CORE_ARCHETYPES)
        )

    # 2. Verify every archetype + workspace card has the 4-part anti-slop contract
    sections = extract_sections(spec)
    for target in ALL_TARGETS:
        if target not in sections:
            errors.append(f"docs/repository-types.md: add '### `{target}`：' contract section")
            continue
        body = sections[target]
        for field in REQUIRED_CARD_FIELDS:
            if f"- **{field}**" not in body:
                errors.append(
                    f"docs/repository-types.md: add '- **{field}**' bullet under '### `{target}`：'"
                )

    # 3. Verify verification.md covers all 6 archetypes + workspace
    verified_targets = set(re.findall(r"^\| `([a-z]+)` \|", verification, re.MULTILINE))
    missing_verified = [t for t in ALL_TARGETS if t not in verified_targets]
    if missing_verified:
        errors.append(
            "docs/verification.md: add Feature Map & L3 guardrail rows for "
            + ", ".join(missing_verified)
        )

    # 4. Verify SKILL.md options and v1 alias compatibility
    expected_cli = "|".join(["auto", *ALL_TARGETS])
    if re.findall(r"--type (auto(?:\|[a-z]+)+)", skill) != [expected_cli]:
        errors.append(f"{SKILL}: align --type options with {expected_cli}")
    if "--plan" not in skill:
        errors.append(f"{SKILL}: document the read-only --plan option")
    for alias in ("`software`", "`ros`"):
        if alias not in skill:
            errors.append(f"{SKILL}: document v1 alias compatibility for {alias}")

    # 5. Verify core entry cross-links
    for name, body, targets in (
        ("README.md", readme, ("docs/migration.md", "docs/repository-types.md", "docs/verification.md")),
        ("docs/migration.md", workflow, ("../README.md", "repository-types.md", "verification.md")),
        ("docs/repository-types.md", spec, ("verification.md",)),
        ("docs/verification.md", verification, ("repository-types.md", "migration.md")),
        (str(SKILL), skill, ("../../docs/migration.md", "../../docs/repository-types.md", "../../docs/verification.md")),
    ):
        for target in targets:
            if f"]({target})" not in body:
                errors.append(f"{name}: add markdown link to {target}")

    # 6. Verify release version consistency across entry docs
    latest = re.search(r"^## (v\d+\.\d+\.\d+)\b", changelog, re.MULTILINE)
    if not latest:
        errors.append("CHANGELOG.md: add a version heading (e.g. '## v2.0.0')")
    else:
        version = latest.group(1)
        if tag and tag != version:
            errors.append(f"CHANGELOG.md: newest release is {version}, requested {tag}")
        for name, body, snippet in [
            ("README.md", readme, f"**{version}**"),
            ("docs/repository-types.md", spec, f"规范版本 {version}。"),
            (
                "docs/verification.md",
                verification,
                f"python3 scripts/check_release.py --tag {version}\n",
            ),
        ]:
            if snippet not in body:
                errors.append(f"{name}: update release reference to {version}")

    # 7. Verify all local relative links across every Markdown document
    for path in [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / SKILL, *sorted((ROOT / "docs").rglob("*.md"))]:
        check_links(path, errors)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="expected Git release tag (for example, v2.0.0)")
    args = parser.parse_args()
    try:
        problems = check(args.tag)
    except OSError as error:
        sys.exit(str(error))
    if problems:
        sys.exit("\n".join(problems))
    print("OK: v2 release version, 6+1 orthogonal type contracts, L3 guardrail coverage, skill options and local links")
