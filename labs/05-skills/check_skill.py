"""પ્રકરણ 5 lab: SKILL.md ને Hermes ના authoring standards સામે તપાસો. Book lab code.

નકલ કરેલા નિયમ (pinned source): skills/AGENTS.md "Authoring standards" — description ≤ 60 અક્ષર,
એક વાક્ય, પૂર્ણવિરામથી અંત; marketing શબ્દો નહીં; વિભાગોનો નિશ્ચિત ક્રમ.
ચલાવો:  python3 labs/05-skills/check_skill.py labs/05-skills/lagna-mehmaan-yadi/SKILL.md
"""
import re
import sys

SECTIONS = ["## When to Use", "## Prerequisites", "## How to Run", "## Quick Reference",
            "## Procedure", "## Pitfalls", "## Verification"]
MARKETING = ("powerful", "comprehensive", "seamless", "advanced")
WRAPPED = {"grep": "search_files", "cat": "read_file", "sed": "patch", "awk": "patch"}


def check(text):
    problems = []
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        return ["frontmatter (--- … ---) નથી"]
    front, body = m.group(1), m.group(2)
    fields = dict(re.findall(r"^(\w+):\s*(.+)$", front, re.M))
    for key in ("name", "description", "version", "author", "license"):
        if key not in fields:
            problems.append(f"frontmatter માં '{key}' નથી")
    desc = fields.get("description", "")
    if len(desc) > 60:
        problems.append(f"description {len(desc)} અક્ષર છે (મર્યાદા 60)")
    if desc and not desc.endswith("."):
        problems.append("description પૂર્ણવિરામથી પૂરું નથી થતું")
    problems += [f"marketing શબ્દ: '{w}'" for w in MARKETING if w in desc.lower()]
    positions = [body.find(s) for s in SECTIONS]
    problems += [f"વિભાગ નથી: {s}" for s, p in zip(SECTIONS, positions) if p < 0]
    found = [p for p in positions if p >= 0]
    if found != sorted(found):
        problems.append("વિભાગોનો ક્રમ ખોટો છે")
    for util, tool in WRAPPED.items():
        if re.search(rf"`{util}\b", body):
            problems.append(f"shell utility `{util}` નહીં, Hermes tool `{tool}` લખો")
    return problems


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read()
    problems = check(text)
    desc = re.search(r"^description:\s*(.+)$", text, re.M).group(1)
    print(f"description ({len(desc)} અક્ષર): {desc}")
    print("પરિણામ:", "બધું બરાબર ✅" if not problems else "")
    for p in problems:
        print("  ✗", p)
    bad = text.replace("Reconcile a wedding guest list with caterer counts.",
                       "A powerful and comprehensive skill that reconciles wedding guest lists with caterers")
    print("બગાડેલી નકલ:")
    for p in check(bad.replace("`read_file`", "`cat`")):
        print("  ✗", p)
    sys.exit(1 if problems else 0)
