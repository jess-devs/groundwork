#!/usr/bin/env python3
"""Structural checker for a groundwork docs/ tree.

It reads identifiers and file names, the two things groundwork never
translates, so it behaves the same in every working language. It answers
whether the documents point at things that exist. Whether what they say is any
good is the half that is still read by hand.

    python check_docs.py docs/
    python check_docs.py --count docs/features/<slug>/historias.md
    python check_docs.py --status docs/
    python check_docs.py --selftest
"""

import re
import sys
from pathlib import Path

ID = re.compile(r"\b(?:RF|RNF|HU|CA|AD)-\d+(?:\.\d+)?\b")
HEADING = re.compile(r"^#{1,6}\s+((?:RF|RNF|HU|AD)-\d+(?:\.\d+)?)\b", re.M)
PATHISH = re.compile(r"`([^`\s]+(?:\.md|/))`")


def check(docs):
    docs = docs.resolve()
    root = docs.parent
    md = sorted(
        p
        for p in docs.rglob("*.md")
        if "referencias" not in p.relative_to(docs).parts[:1]
    )
    if not md:
        return ["%s holds no Markdown files" % docs]
    entry = [p for p in (root / "AGENTS.md", root / "CLAUDE.md") if p.is_file()]
    text = {p: p.read_text(encoding="utf-8") for p in md + entry}

    defined, where = set(), {}
    for p in md:
        parts = p.relative_to(docs).parts
        scope = parts[1] if parts[0] == "features" and len(parts) > 2 else ""
        for m in HEADING.finditer(text[p]):
            where.setdefault(m.group(1), []).append(
                (p.relative_to(root).as_posix(), scope)
            )
        if p.name == "historias.md":
            defined |= {i for i in ID.findall(text[p]) if i.startswith("CA-")}
    defined |= set(where)

    numbered_globally = len({s for _, s in where.get("HU-01", [])}) <= 1
    out = []
    for ident, locs in sorted(where.items()):
        scopes = [s for _, s in locs]
        clash = len(scopes) > len(set(scopes)) or "" in scopes or numbered_globally
        if len(locs) > 1 and clash:
            out.append(
                "%s is defined in more than one place: %s"
                % (ident, ", ".join(f for f, _ in locs))
            )
    for p in md + entry:
        rel = p.relative_to(root).as_posix()
        for missing in sorted(set(ID.findall(text[p])) - defined):
            out.append("%s: %s is referenced and defined nowhere" % (rel, missing))
        for ref in sorted(set(PATHISH.findall(text[p]))):
            if "<" in ref or "*" in ref:  # a template placeholder, not a pointer
                continue
            if "://" in ref or not re.search(r"\w", ref):
                continue
            if not any((base / ref).exists() for base in (root, docs, p.parent)):
                out.append("%s: points at %s, which does not exist" % (rel, ref))
        if p in md and not text[p].lstrip().startswith(">"):
            out.append("%s: no header block (status, last updated, mode)" % rel)

    features = docs / "features"
    for d in (
        sorted(x for x in features.iterdir() if x.is_dir()) if features.is_dir() else []
    ):
        reqs, hist = d / "requisitos.md", d / "historias.md"
        stories = text.get(hist, "")
        for rid in sorted({m.group(1) for m in HEADING.finditer(text.get(reqs, ""))}):
            if rid not in ID.findall(stories):
                out.append("%s: %s is covered by no story" % (d.name, rid))
        for hu in sorted(
            {
                m.group(1)
                for m in HEADING.finditer(stories)
                if m.group(1).startswith("HU-")
            }
        ):
            if not re.search(r"\bCA-%s\.\d+\b" % hu.split("-")[1], stories):
                out.append("%s: %s has no acceptance criterion" % (d.name, hu))

    # Decisions are matched by identifier alone, so two features numbering their
    # own AD-01 share one index entry. Prefix the slug if that ever bites.
    index = ID.findall(text.get(docs / "03-arquitectura.md", ""))
    for p in md:
        if p.name != "decisiones.md":
            continue
        for ad in sorted(
            {
                m.group(1)
                for m in HEADING.finditer(text[p])
                if m.group(1).startswith("AD-")
            }
        ):
            if ad not in index:
                out.append(
                    "%s: %s is missing from the index in 03-arquitectura.md"
                    % (p.relative_to(root).as_posix(), ad)
                )
    return out


def count(artifact, checklist=None):
    checklist = (
        checklist
        or Path(__file__).resolve().parent.parent / "references" / "validation.md"
    )
    name = Path(artifact).name
    total, used = 0, []
    for block in re.split(r"^## ", checklist.read_text(encoding="utf-8"), flags=re.M)[
        1:
    ]:
        title = block.splitlines()[0]
        words = title.split()
        if title == "Every artifact" or any(
            w == name or w.endswith("/" + name) for w in words
        ):
            n = len(re.findall(r"^- \[ \]", block, re.M))
            total += n
            used.append("%s (%d)" % (title, n))
    return total, used


def criteria(cell):
    found = []
    for m in re.finditer(r"\bCA-(\d+)\.(\d+)(?:\s*(?:a|to|-|–)\s*CA-\1\.(\d+))?", cell):
        story, first, last = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        found += ["CA-%s.%d" % (story, n) for n in range(first, last + 1)]
    return found


def status(docs):
    docs = docs.resolve()
    out = []
    for hist in sorted(docs.glob("features/*/historias.md")):
        text = hist.read_text(encoding="utf-8")
        parts = re.split(r"^#{1,6}\s+(HU-\d+)\b.*$", text, flags=re.M)
        stories = []
        for hu, body in zip(parts[1::2], parts[2::2]):
            labels = re.findall(r"^\*\*[^*]+\.\*\*[ \t]*(\S.*)$", body, re.M)
            stories.append("%s %s" % (hu, labels[-1].strip() if labels else "?"))
        out.append("%s: %s" % (hist.parent.name, ", ".join(stories) or "no stories"))

    latest = {}
    quality = docs / "04-calidad.md"
    for line in (
        quality.read_text(encoding="utf-8").splitlines() if quality.is_file() else []
    ):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for ca in criteria(cells[1].split(":")[0]) if len(cells) >= 5 else []:
            latest[(cells[0], ca)] = cells[2:5]
    if latest:
        tally = {}
        for result, _, _ in latest.values():
            tally[result] = tally.get(result, 0) + 1
        common = max(tally, key=tally.get)
        out.append(
            "criteria by current result: "
            + ", ".join(
                "%s %d" % kv for kv in sorted(tally.items(), key=lambda kv: -kv[1])
            )
        )
        for (story, ca), (result, date, evidence) in sorted(latest.items()):
            if result != common:
                out.append(
                    "  %s %s: %s (%s) %s" % (story, ca, result, date, evidence[:120])
                )
    return out


def selftest():
    import tempfile

    def tree(base, files):
        for name, body in files.items():
            f = base / name
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(body, encoding="utf-8")

    clean = {
        "docs/00-contexto.md": "> Estado: aprobado\n\n# Contexto\n\nDatos en `s3://bucket/`, `//`\n",
        "docs/features/pago/historias.md": "> Estado: aprobado\n\n## HU-01: pagar\n\n1. CA-01.1 se ve\n",
        "docs/referencias/reto.md": "# Reto\n\nVer `anexo.md`, RF-77\n",
        "docs/03-arquitectura.md": "> Estado: aprobado\n\nAD-01, ver `00-contexto.md`\n",
        "docs/features/reserva/requisitos.md": "> Estado: aprobado\n\n### RF-01: pedir\n",
        "docs/features/reserva/historias.md": "> Estado: aprobado\n\n## HU-01: pedir\n\nCubre: RF-01\n\n1. CA-01.1 se ve\n",
        "docs/features/reserva/decisiones.md": "> Estado: aprobado\n\n## AD-01: sqlite\n",
    }
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        tree(base, clean)
        assert check(base / "docs") == [], check(base / "docs")

    broken = dict(clean)
    broken["docs/features/reserva/requisitos.md"] += "\n### RF-02: cancelar\n"
    broken["docs/features/reserva/historias.md"] += "\n## HU-02: cancelar\n"
    broken["docs/features/reserva/decisiones.md"] += "\n## AD-02: cola\n"
    broken["docs/04-calidad.md"] = "# Calidad\n\n| HU-09 | CA-09.9 | pasa |\n"
    broken["docs/00-contexto.md"] += "\nVer `05-nada.md`\n"
    broken["docs/features/pago/historias.md"] = (
        "> Estado: borrador\n\n## HU-02: pagar\n\n1. CA-02.1 se ve\n"
    )
    broken["AGENTS.md"] = "Docs in `docs/no-existe.md`\n"
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        tree(base, broken)
        found = check(base / "docs")
        for expected in (
            "RF-02 is covered by no story",
            "HU-02 has no acceptance criterion",
            "CA-09.9 is referenced and defined nowhere",
            "HU-09 is referenced and defined nowhere",
            "AD-02 is missing from the index",
            "points at 05-nada.md",
            "04-calidad.md: no header block",
            "HU-02 is defined in more than one place",
            "AGENTS.md: points at docs/no-existe.md",
        ):
            assert any(expected in line for line in found), (expected, found)
        assert len(found) == 9, found
        import os

        cwd = os.getcwd()
        os.chdir(base / "docs")
        try:
            assert check(Path(".")) == found, check(Path("."))
        finally:
            os.chdir(cwd)

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        tree(
            base,
            {
                "validation.md": "## Every artifact\n\n- [ ] a\n- [ ] b\n\n"
                "## 02-requisitos.md and features/*/requisitos.md\n\n- [ ] c\n\n"
                "## features/*/historias.md\n\n- [ ] d\n- [ ] e\n- [ ] f\n",
                "docs/features/reserva/historias.md": "## HU-01: pedir\n\n**Story.** As a user\n\n**Status.** verified\n\n"
                "## HU-02: cancelar\n\n**Estado.** en progreso\n",
                "docs/04-calidad.md": "| Story | Criterion | Result | Date | Evidence |\n| --- | --- | --- | --- | --- |\n"
                "| HU-01 | CA-01.1: x | pass | 2026-01-01 | seen |\n"
                "| HU-02 | CA-02.1: y | pass | 2026-01-01 | seen |\n"
                "| HU-01 | CA-01.2: z | pass | 2026-01-01 | seen |\n"
                "| HU-02 | CA-02.1: y | blocked | 2026-01-02 | code changed |\n",
            },
        )
        assert count("features/reserva/historias.md", base / "validation.md")[0] == 5
        assert count("docs/02-requisitos.md", base / "validation.md")[0] == 3
        lines = status(base / "docs")
        assert lines[0] == "reserva: HU-01 verified, HU-02 en progreso", lines
        assert lines[1] == "criteria by current result: pass 2, blocked 1", lines
        assert lines[2].startswith("  HU-02 CA-02.1: blocked (2026-01-02)"), lines
        assert len(lines) == 3, lines
        assert criteria("CA-02.1 a CA-02.3") == ["CA-02.1", "CA-02.2", "CA-02.3"]
        assert criteria("CA-01.6 y CA-01.8") == ["CA-01.6", "CA-01.8"]

    skill = (Path(__file__).resolve().parent.parent / "SKILL.md").read_bytes()
    body = skill.decode("utf-8").split("---", 2)[2]
    assert len(body) <= 19000, (
        "SKILL.md body is %d chars; compaction cuts at 20000" % len(body)
    )


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in argv:
        selftest()
        print("selftest ok")
        return 0
    if "--count" in argv:
        n, used = count(argv[argv.index("--count") + 1])
        print("N = %d: %s" % (n, " + ".join(used)))
        return 0
    if "--status" in argv:
        rest = [a for a in argv[1:] if a != "--status"]
        for line in status(Path(rest[0] if rest else "docs")):
            print(line)
        return 0
    docs = Path(argv[1] if len(argv) > 1 else "docs")
    if not docs.is_dir():
        print("not a directory: %s" % docs)
        return 2
    problems = check(docs)
    for line in problems:
        print(line)
    print("%d structural problem(s) in %s" % (len(problems), docs))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
