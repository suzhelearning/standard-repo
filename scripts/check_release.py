"""Check the published documentation and skill contract using only Python's standard library."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/standardize-repo/SKILL.md")


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


def check(tag):
    errors = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    spec = (ROOT / "docs/repository-types.md").read_text(encoding="utf-8")
    skill = (ROOT / SKILL).read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    type_row = r"^\| ([A-G]) [^|]*?`([a-z]+)` \|"
    types = re.findall(type_row, spec, re.MULTILINE)
    names = [name for _, name in types]
    if [key for key, _ in types] != list("ABCDEFG") or len(set(names)) != 7:
        errors.append("docs/repository-types.md: give each v1 type A–G a unique name")
    if re.findall(r"--type (auto(?:\|[a-z]+)+)", skill) != ["|".join(["auto"] + names)]:
        errors.append(f"{SKILL}: align --type options with docs/repository-types.md")
    if "--plan" not in skill:
        errors.append(f"{SKILL}: document the read-only --plan option")
    workflow = (ROOT / "docs/migration.md").read_text(encoding="utf-8")
    for name, body, targets in (
        ("README.md", readme, ("docs/migration.md", "docs/repository-types.md")),
        ("docs/migration.md", workflow, ("../README.md", "repository-types.md", "verification.md")),
        (str(SKILL), skill, ("../../docs/migration.md", "../../docs/repository-types.md")),
    ):
        for target in targets:
            if f"]({target})" not in body:
                errors.append(f"{name}: link to {target}")

    latest = re.search(r"^## (v\d+\.\d+\.\d+)\b", changelog, re.MULTILINE)
    if not latest:
        errors.append("CHANGELOG.md: add a version heading for the release")
    else:
        version = latest.group(1)
        if tag and tag != version:
            errors.append(f"CHANGELOG.md: newest release is {version}, requested {tag}")
        for name, body, snippet in [
            ("README.md", readme, f"**{version}**"),
            ("docs/repository-types.md", spec, f"规范版本 {version}。"),
            ("docs/verification.md", (ROOT / "docs/verification.md").read_text(encoding="utf-8"),
             f"python3 scripts/check_release.py --tag {version}\n"),
        ]:
            if snippet not in body:
                errors.append(f"{name}: update release reference to {version}")

    for path in [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / SKILL, *sorted((ROOT / "docs").rglob("*.md"))]:
        check_links(path, errors)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="expected Git release tag (for example, v1.0.0)")
    args = parser.parse_args()
    try:
        problems = check(args.tag)
    except OSError as error:
        sys.exit(str(error))
    if problems:
        sys.exit("\n".join(problems))
    print("OK: release version, seven repository types, skill options and local file links")
