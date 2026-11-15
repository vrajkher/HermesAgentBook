#!/usr/bin/env python3
"""Build the single-page web edition of the book from the repository files.

    python3 tools/build-artifact.py book.html

The page embeds every chapter, appendix, lab source and evidence file as JSON and renders
Markdown in the browser with marked (loaded from cdnjs). No other network access is needed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (id, repo path, short label, group)
DOCS = [
    ("home", "README.md", "મુખપૃષ્ઠ", "પુસ્તક"),
    ("naksho", "book/overview-samagra-naksho.md", "સમગ્ર નકશો", "પુસ્તક"),
    ("pravesh", "book/pravesh-shunya-thi-shuruaat.md", "પ્રવેશ — શૂન્યથી શરૂઆત", "પુસ્તક"),
    ("ch0", "book/00-paayo-ane-pratham-run.md", "0 · પાયો અને પ્રથમ run", "પુસ્તક"),
    ("ch1", "book/01-ek-sandesh-ni-musafari.md", "1 · એક સંદેશાની મુસાફરી", "પુસ્તક"),
    ("ch2", "book/02-suchna-pati-prompt-ane-cache.md", "2 · સૂચના-પાટી", "પુસ્તક"),
    ("ch3", "book/03-ojar-kabat-tools.md", "3 · ઓજાર-કબાટ", "પુસ્તક"),
    ("ch4", "book/04-yaad-memory-sessions.md", "4 · યાદ", "પુસ્તક"),
    ("ch5", "book/05-reet-pothi-skills.md", "5 · રીત-પોથી", "પુસ્તક"),
    ("ch6", "book/06-bario-ghadiyal-shikhau.md", "6 · બારીઓ, ઘડિયાળ, શિખાઉ", "પુસ્તક"),
    ("ch7", "book/07-potanu-ojar-ane-mastery.md", "7 · પોતાનું ઓજાર અને mastery", "પુસ્તક"),
    ("app-a", "appendix/A-source-index.md", "A · Source index", "પરિશિષ્ટ"),
    ("app-b", "appendix/B-command-reference.md", "B · Commands", "પરિશિષ્ટ"),
    ("app-c", "appendix/C-glossary.md", "C · Glossary", "પરિશિષ્ટ"),
    ("app-d", "appendix/D-lab-solutions.md", "D · જવાબો", "પરિશિષ્ટ"),
    ("app-e", "appendix/E-mastery-rubric.md", "E · Mastery rubric", "પરિશિષ્ટ"),
    ("app-f", "appendix/F-verification-log.md", "F · Verification log", "પરિશિષ્ટ"),
    ("app-cites", "appendix/citations.generated.md", "Citations table", "પરિશિષ્ટ"),
    ("labs", "labs/README.md", "Labs — શરૂઆત", "Labs"),
]

TEMPLATE = (ROOT / "tools" / "artifact-template.html").read_text(encoding="utf-8")


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "book.html")
    docs = [{"id": i, "path": p, "label": label, "group": g, "md": (ROOT / p).read_text(encoding="utf-8")}
            for i, p, label, g in DOCS]
    files = {}
    for folder in ("labs", "evidence"):
        for f in sorted((ROOT / folder).rglob("*")):
            if f.is_file() and f.name != "README.md" and "__pycache__" not in f.parts:
                files[str(f.relative_to(ROOT))] = f.read_text(encoding="utf-8")
    images = {str(f.relative_to(ROOT)): f.read_text(encoding="utf-8")
              for f in sorted((ROOT / "book" / "images").rglob("*.svg"))}
    data = json.dumps({"docs": docs, "files": files, "images": images}, ensure_ascii=False).replace("</", "<\\/")
    out.write_text(TEMPLATE.replace("/*__BOOK_DATA__*/null", data), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(docs)} docs, {len(files)} files)")


if __name__ == "__main__":
    main()
