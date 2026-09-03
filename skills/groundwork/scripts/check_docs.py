#!/usr/bin/env python3
"""Structural checker for a groundwork docs/ tree.

It reads identifiers and file names, the two things groundwork never
translates, so it behaves the same in every working language. It answers
whether the documents point at things that exist. Whether what they say is any
good is the half that is still read by hand.

    python check_docs.py docs/
    python check_docs.py --selftest
"""

import re
import sys
from pathlib import Path

ID = re.compile(r"\b(?:RF|RNF|HU|CA|AD)-\d+(?:\.\d+)?\b")
HEADING = re.compile(r"^#{1,6}\s+((?:RF|RNF|HU|AD)-\d+(?:\.\d+)?)\b", re.M)
PATHISH = re.compile(r"`([^`\s]+(?:\.md|/))`")


def check(docs):
    root = docs.parent
    md = sorted(docs.rglob("*.md"))
    if not md:
        return ["%s holds no Markdown files" % docs]
    entry = [p for p in (root / "AGENTS.md", root / "CLAUDE.md") if p.is_file()]
    text = {p: p.read_text(encoding="utf-8") for p in md + entry}

    defined = set()
    for p in md:
        defined |= {m.group(1) for m in HEADING.finditer(text[p])}
        if p.name == "historias.md":
            defined |= {i for i in ID.findall(text[p]) if i.startswith("CA-")}

    out = []
    for p in md + entry:
        rel = p.relative_to(root).as_posix()
        for missing in sorted(set(ID.findall(text[p])) - defined):
            out.append("%s: %s is referenced and defined nowhere" % (rel, missing))
        for ref in sorted(set(PATHISH.findall(text[p]))):
            if "<" in ref or "*" in ref:  # a template placeholder, not a pointer
                continue
            if not any((base / ref).exists() for base in (root, docs, p.parent)):
                out.append("%s: points at %s, which does not exist" % (rel, ref))
        if p in md and not text[p].lstrip().startswith(">"):
            out.append("%s: no header block (status, last updated, mode)" % rel)

    features = docs / "features"
    for d in sorted(x for x in features.iterdir() if x.is_dir()) if features.is_dir() else []:
        reqs, hist = d / "requisitos.md", d / "historias.md"
        stories = text.get(hist, "")
        for rid in sorted({m.group(1) for m in HEADING.finditer(text.get(reqs, ""))}):
            if rid not in ID.findall(stories):
                out.append("%s: %s is covered by no story" % (d.name, rid))
        for hu in sorted({m.group(1) for m in HEADING.finditer(stories)
                          if m.group(1).startswith("HU-")}):
            if not re.search(r"\bCA-%s\.\d+\b" % hu.split("-")[1], stories):
                out.append("%s: %s has no acceptance criterion" % (d.name, hu))

    # Decisions are matched by identifier alone, so two features numbering their
    # own AD-01 share one index entry. Prefix the slug if that ever bites.
    index = ID.findall(text.get(docs / "03-arquitectura.md", ""))
    for p in md:
        if p.name != "decisiones.md":
            continue
        for ad in sorted({m.group(1) for m in HEADING.finditer(text[p])
                          if m.group(1).startswith("AD-")}):
            if ad not in index:
                out.append("%s: %s is missing from the index in 03-arquitectura.md"
                           % (p.relative_to(root).as_posix(), ad))
    return out


def selftest():
    import tempfile

    def tree(base, files):
        for name, body in files.items():
            f = base / name
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(body, encoding="utf-8")

    clean = {
        "docs/00-contexto.md": "> Estado: aprobado\n\n# Contexto\n",
        "docs/03-arquitectura.md": "> Estado: aprobado\n\nAD-01, ver `00-contexto.md`\n",
        "docs/features/reserva/requisitos.md": "> Estado: aprobado\n\n### RF-01: pedir\n",
        "docs/features/reserva/historias.md":
            "> Estado: aprobado\n\n## HU-01: pedir\n\nCubre: RF-01\n\n1. CA-01.1 se ve\n",
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
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        tree(base, broken)
        found = check(base / "docs")
        for expected in ("RF-02 is covered by no story",
                         "HU-02 has no acceptance criterion",
                         "CA-09.9 is referenced and defined nowhere",
                         "HU-09 is referenced and defined nowhere",
                         "AD-02 is missing from the index",
                         "points at 05-nada.md",
                         "04-calidad.md: no header block"):
            assert any(expected in line for line in found), (expected, found)
        assert len(found) == 7, found


def main(argv):
    if "--selftest" in argv:
        selftest()
        print("selftest ok")
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
