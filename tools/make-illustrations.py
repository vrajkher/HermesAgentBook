#!/usr/bin/env python3
"""Draw one illustration per chapter as SVG: book/images/chapters/<chapter>.svg

    python3 tools/make-illustrations.py

Each picture is a scene from the story drawn as stations (an icon, a Gujarati label and the
Hermes name under it) joined by arrows. The drawings use their own paper background, so they
read the same on light and dark pages.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "book" / "images" / "chapters"
W, H = 960, 440
PAPER, INK, MUTED = "#fbf4e4", "#2a2420", "#6b5f55"
MARIGOLD, BANDHANI, MEHNDI, INDIGO, CLAY = "#d98a00", "#a3195b", "#2f6b3a", "#2c4a8a", "#b4532a"
FONT = "'Noto Sans Gujarati','Shruti','Lohit Gujarati',sans-serif"
MONO = "'JetBrains Mono','DejaVu Sans Mono',monospace"


# ---- icons: each draws inside a 64x64 box with its top-left at (x, y) ------------------------
def person(x, y, c):
    return (f'<circle cx="{x+32}" cy="{y+16}" r="12" fill="{c}"/>'
            f'<path d="M{x+10} {y+62} q0 -30 22 -30 q22 0 22 30 z" fill="{c}"/>')


def phone(x, y, c):
    return (f'<rect x="{x+18}" y="{y+4}" width="28" height="56" rx="6" fill="{c}"/>'
            f'<rect x="{x+22}" y="{y+12}" width="20" height="34" rx="2" fill="{PAPER}"/>'
            f'<circle cx="{x+32}" cy="{y+53}" r="3" fill="{PAPER}"/>')


def slate(x, y, c):
    return (f'<rect x="{x+4}" y="{y+8}" width="56" height="44" rx="4" fill="{c}"/>'
            + "".join(f'<rect x="{x+11}" y="{y+16+i*10}" width="{40-i*8}" height="4" rx="2" fill="{PAPER}"/>' for i in range(3))
            + f'<rect x="{x+28}" y="{y+52}" width="8" height="10" fill="{c}"/>')


def cupboard(x, y, c):
    return (f'<rect x="{x+8}" y="{y+2}" width="48" height="60" rx="3" fill="{c}"/>'
            f'<line x1="{x+32}" y1="{y+6}" x2="{x+32}" y2="{y+58}" stroke="{PAPER}" stroke-width="2"/>'
            f'<circle cx="{x+28}" cy="{y+32}" r="2.5" fill="{PAPER}"/><circle cx="{x+36}" cy="{y+32}" r="2.5" fill="{PAPER}"/>')


def diary(x, y, c):
    return (f'<rect x="{x+12}" y="{y+4}" width="40" height="56" rx="4" fill="{c}"/>'
            f'<rect x="{x+16}" y="{y+4}" width="4" height="56" fill="{PAPER}" opacity=".5"/>'
            f'<rect x="{x+26}" y="{y+16}" width="20" height="4" rx="2" fill="{PAPER}"/>'
            f'<rect x="{x+26}" y="{y+26}" width="14" height="4" rx="2" fill="{PAPER}"/>')


def ledger(x, y, c):
    return (f'<path d="M{x+4} {y+12} q14 -8 28 0 v46 q-14 -8 -28 0 z" fill="{c}"/>'
            f'<path d="M{x+60} {y+12} q-14 -8 -28 0 v46 q14 -8 28 0 z" fill="{c}" opacity=".8"/>'
            + "".join(f'<rect x="{x+10}" y="{y+20+i*9}" width="16" height="3" fill="{PAPER}"/>' for i in range(4)))


def book(x, y, c):
    return (f'<rect x="{x+10}" y="{y+6}" width="44" height="54" rx="3" fill="{c}"/>'
            f'<rect x="{x+14}" y="{y+10}" width="36" height="46" rx="2" fill="{PAPER}"/>'
            + "".join(f'<rect x="{x+19}" y="{y+16+i*9}" width="{26-(i%2)*8}" height="3" fill="{c}"/>' for i in range(4)))


def window(x, y, c):
    return (f'<rect x="{x+6}" y="{y+6}" width="52" height="52" rx="4" fill="{c}"/>'
            f'<rect x="{x+12}" y="{y+12}" width="18" height="18" fill="{PAPER}"/><rect x="{x+34}" y="{y+12}" width="18" height="18" fill="{PAPER}"/>'
            f'<rect x="{x+12}" y="{y+34}" width="18" height="18" fill="{PAPER}"/><rect x="{x+34}" y="{y+34}" width="18" height="18" fill="{PAPER}"/>')


def clock(x, y, c):
    return (f'<circle cx="{x+32}" cy="{y+34}" r="26" fill="{c}"/><circle cx="{x+32}" cy="{y+34}" r="20" fill="{PAPER}"/>'
            f'<line x1="{x+32}" y1="{y+34}" x2="{x+32}" y2="{y+20}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
            f'<line x1="{x+32}" y1="{y+34}" x2="{x+42}" y2="{y+38}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
            f'<rect x="{x+26}" y="{y+2}" width="12" height="6" rx="2" fill="{c}"/>')


def safe(x, y, c):
    return (f'<rect x="{x+6}" y="{y+8}" width="52" height="50" rx="5" fill="{c}"/>'
            f'<circle cx="{x+32}" cy="{y+33}" r="11" fill="none" stroke="{PAPER}" stroke-width="3"/>'
            f'<line x1="{x+32}" y1="{y+33}" x2="{x+39}" y2="{y+28}" stroke="{PAPER}" stroke-width="3"/>')


def plug(x, y, c):
    return (f'<rect x="{x+14}" y="{y+20}" width="36" height="26" rx="5" fill="{c}"/>'
            f'<rect x="{x+22}" y="{y+6}" width="5" height="16" fill="{c}"/><rect x="{x+37}" y="{y+6}" width="5" height="16" fill="{c}"/>'
            f'<path d="M{x+32} {y+46} v14" stroke="{c}" stroke-width="5"/>')


def bell(x, y, c):
    return (f'<path d="M{x+14} {y+46} q0 -34 18 -34 q18 0 18 34 z" fill="{c}"/>'
            f'<rect x="{x+10}" y="{y+44}" width="44" height="6" rx="3" fill="{c}"/><circle cx="{x+32}" cy="{y+56}" r="5" fill="{c}"/>')


def gate(x, y, c):
    return (f'<rect x="{x+6}" y="{y+6}" width="8" height="54" fill="{c}"/><rect x="{x+50}" y="{y+6}" width="8" height="54" fill="{c}"/>'
            + "".join(f'<rect x="{x+14}" y="{y+14+i*14}" width="36" height="5" fill="{c}" opacity=".7"/>' for i in range(3)))


def note(x, y, c):
    return (f'<path d="M{x+10} {y+4} h34 l12 12 v44 h-46 z" fill="{c}"/><path d="M{x+44} {y+4} v12 h12" fill="{PAPER}" opacity=".6"/>'
            + "".join(f'<rect x="{x+16}" y="{y+24+i*9}" width="28" height="3" fill="{PAPER}"/>' for i in range(3)))


def camera(x, y, c):
    return (f'<rect x="{x+6}" y="{y+16}" width="52" height="38" rx="6" fill="{c}"/><rect x="{x+22}" y="{y+8}" width="20" height="10" rx="2" fill="{c}"/>'
            f'<circle cx="{x+32}" cy="{y+35}" r="11" fill="{PAPER}"/><circle cx="{x+32}" cy="{y+35}" r="6" fill="{c}"/>')


ICONS = dict(person=person, phone=phone, slate=slate, cupboard=cupboard, diary=diary, ledger=ledger, book=book,
             window=window, clock=clock, safe=safe, plug=plug, bell=bell, gate=gate, note=note, camera=camera)


# ---- drawing -----------------------------------------------------------------------------------
def station(cx, cy, icon, color, label, code):
    x, y = cx - 32, cy - 44
    return (f'<g>{ICONS[icon](x, y, color)}'
            f'<text x="{cx}" y="{cy+42}" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="600" fill="{INK}">{escape(label)}</text>'
            + (f'<text x="{cx}" y="{cy+62}" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{escape(code)}</text>' if code else "")
            + "</g>")


def arrow(x1, y1, x2, y2, label="", curve=0, color=INK, dashed=False):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    out = (f'<path d="M{x1} {y1} Q{mx} {my} {x2} {y2}" fill="none" stroke="{color}" stroke-width="2.2"{dash} marker-end="url(#ah)"/>')
    if label:
        ly = (y1 + y2) / 2 - curve / 2 - 8
        out += f'<text x="{mx}" y="{ly}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{color}">{escape(label)}</text>'
    return out


def frame(name, title, subtitle, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">'
           f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>'
           f'<rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/>'
           f'<rect x="0" y="0" width="{W}" height="8" fill="{MARIGOLD}"/>'
           + "".join(f'<circle cx="{40+i*40}" cy="8" r="6" fill="{[MARIGOLD, BANDHANI, MEHNDI][i % 3]}"/>' for i in range(23))
           + f'<text x="40" y="56" font-family="{FONT}" font-size="25" font-weight="700" fill="{BANDHANI}">{escape(title)}</text>'
           f'<text x="40" y="84" font-family="{FONT}" font-size="15.5" fill="{MUTED}">{escape(subtitle)}</text>'
           f'{body}</svg>')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def tiers():
    """Chapter 2: the slate as three tiers, and the cached prefix under it."""
    rows = [("stable — ઓળખ, ઓજારના નિયમ", MEHNDI, 540), ("context — પ્રોજેક્ટ (AGENTS.md)", INDIGO, 440),
            ("volatile — ડાયરી, રીત-સૂચિ, સમય", MARIGOLD, 350)]
    out, y = "", 120
    for text, color, w in rows:
        out += (f'<rect x="60" y="{y}" width="{w}" height="46" rx="8" fill="{color}"/>'
                f'<text x="76" y="{y+30}" font-family="{FONT}" font-size="16.5" font-weight="600" fill="{PAPER}">{escape(text)}</text>')
        y += 58
    out += (f'<text x="60" y="{y+26}" font-family="{FONT}" font-size="15" fill="{MUTED}">ઉપર: લગભગ કદી ન બદલાય · નીચે: સૌથી વધુ બદલાય</text>'
            f'<rect x="640" y="120" width="270" height="162" rx="10" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>'
            f'<text x="775" y="160" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="600" fill="{INK}">ફોન 2: શરૂઆત એ જ?</text>'
            f'<rect x="660" y="178" width="160" height="20" rx="4" fill="{MEHNDI}"/><rect x="820" y="178" width="70" height="20" rx="4" fill="{CLAY}"/>'
            f'<text x="740" y="220" text-anchor="middle" font-family="{FONT}" font-size="14.5" fill="{MEHNDI}">સરખો prefix: સસ્તો</text>'
            f'<text x="855" y="220" text-anchor="middle" font-family="{FONT}" font-size="14.5" fill="{CLAY}">નવો: પૂરો</text>'
            f'<text x="775" y="256" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">byte-stable system prompt</text>')
    out += station(775, 352, "slate", BANDHANI, "પાટી દિવસભર અડશો નહીં", "rebuild: ફક્ત compression પછી")
    return out


def main():
    frame("pravesh-shunya-thi-shuruaat", "પ્રવેશ — ફોન, ચિઠ્ઠી, ઓજાર, ફરી ફોન",
          "શાસ્ત્રીજી કાશીમાં: વિચારે, પણ હાથ-પગ નથી. હર્ષ દરેક ફોનમાં આખી ફાઈલ વાંચે છે.",
          station(120, 200, "person", INDIGO, "ગ્રાહક", "user") + arrow(170, 190, 360, 190, "સંદેશો")
          + station(420, 200, "person", MARIGOLD, "હર્ષ", "agent loop") + arrow(470, 178, 690, 178, "આખી ફાઈલ", 30)
          + arrow(690, 212, 470, 212, "ચિઠ્ઠી: tool call", -30, BANDHANI)
          + station(750, 200, "phone", BANDHANI, "શાસ્ત્રીજી", "model (stateless)")
          + arrow(420, 276, 420, 316, "", 0, MEHNDI) + station(420, 368, "cupboard", MEHNDI, "", "")
          + f'<text x="470" y="360" font-family="{FONT}" font-size="15" fill="{MEHNDI}">ઓજાર ચલાવે, પરિણામ ફાઈલમાં</text>')

    tiles = [("safe", CLAY, "તિજોરી", ".env"), ("slate", MARIGOLD, "નોટિસ-બોર્ડ", "config.yaml"),
             ("person", BANDHANI, "ઓળખ-કાર્ડ", "SOUL.md"), ("diary", MEHNDI, "ડાયરી", "memories/"),
             ("ledger", INDIGO, "રોજમેળ", "state.db"), ("book", MEHNDI, "રીત-પોથી", "skills/"),
             ("clock", MARIGOLD, "એલાર્મ", "cron/"), ("plug", CLAY, "કારીગર", "plugins/")]
    body = (f'<rect x="40" y="108" width="880" height="300" rx="14" fill="none" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="60" y="96" width="250" height="26" rx="6" fill="{PAPER}"/>'
            f'<text x="72" y="116" font-family="{MONO}" font-size="16" font-weight="600" fill="{INK}">get_hermes_home()</text>')
    for i, (icon, color, label, code) in enumerate(tiles):
        body += station(130 + (i % 4) * 230, 190 + (i // 4) * 140, icon, color, label, code)
    frame("00-paayo-ane-pratham-run", "પ્રકરણ 0 — હર્ષનું ઘર: ~/.hermes",
          "દરેક શાખા (profile) નું પોતાનું ઘર. સરનામું મોઢે નહીં: દર વખતે રજિસ્ટરમાં જુઓ.", body)

    frame("01-ek-sandesh-ni-musafari", "પ્રકરણ 1 — એક કામ, ત્રણ ફોન",
          "Turn = એક કામ. Iteration = એક ફોન. ચિઠ્ઠી આવે તો ઓજાર, પછી ફરી ફોન.",
          station(90, 180, "person", INDIGO, "સંદેશો", "run_conversation()") + arrow(140, 170, 230, 170)
          + station(285, 180, "slate", MARIGOLD, "પાટી", "system prompt") + arrow(335, 170, 425, 170)
          + station(480, 180, "phone", BANDHANI, "ફોન", "model call") + arrow(530, 170, 620, 170)
          + station(680, 180, "note", CLAY, "ચિઠ્ઠી?", "tool_calls") + arrow(730, 170, 820, 170, "ના")
          + station(870, 180, "person", MEHNDI, "જવાબ", "final_response")
          + arrow(680, 258, 640, 330, "હા", 0, MEHNDI) + station(590, 370, "cupboard", MEHNDI, "", "")
          + arrow(545, 345, 480, 258, "ફરી ફોન", 0, MEHNDI, True)
          + f'<text x="645" y="392" font-family="{FONT}" font-size="15" fill="{MEHNDI}">run_tool_round (ચક્કર-મર્યાદા સુધી)</text>')

    frame("02-suchna-pati-prompt-ane-cache", "પ્રકરણ 2 — સૂચના-પાટી અને ફી-માફી",
          "જે ઓછું બદલાય તે ઉપર. શરૂઆત અક્ષરશઃ એ જ હોય, તેટલો ભાગ સસ્તો.", tiers())

    frame("03-ojar-kabat-tools", "પ્રકરણ 3 — નાનો કબાટ, મોટા કિનારા",
          "દરેક ઓજાર પોતાની ચિઠ્ઠી સાથે જાતે ગોઠવાય. જોખમી કામ પહેલાં સહી; તિજોરી સહીથી પણ નહીં.",
          station(140, 190, "cupboard", MEHNDI, "core ઓજાર", "_HERMES_CORE_TOOLS")
          + station(360, 190, "plug", CLAY, "કિનારે", "skill · plugin · MCP")
          + arrow(190, 165, 300, 165, "નવું ઓજાર?", 24, CLAY, True)
          + station(580, 190, "gate", MARIGOLD, "સહી", "approval: smart")
          + arrow(150, 270, 570, 270, "", -70)
          + f'<text x="360" y="330" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{INK}">terminal: rm -rf …</text>'
          + station(800, 190, "safe", BANDHANI, "તિજોરી", "hardline")
          + arrow(630, 180, 740, 180, "તોય નહીં", 0, BANDHANI)
          + f'<text x="80" y="395" font-family="{FONT}" font-size="15.5" fill="{MUTED}">ભૂલ પણ જવાબ છે: handler ફાટે તો {{"error": …}} model પાસે પાછો જાય</text>')

    frame("04-yaad-memory-sessions", "પ્રકરણ 4 — ભૂલકણા પંડિત સાથે યાદ રાખવું",
          "ડાયરી હંમેશા, રોજમેળ માગો ત્યારે, સાર-નોંધ ફાઈલ જાડી થાય ત્યારે, ફોટો ફેરફાર પહેલાં.",
          station(130, 200, "diary", MEHNDI, "ખિસ્સા-ડાયરી", "MEMORY.md 2,200")
          + station(350, 200, "ledger", INDIGO, "રોજમેળ", "state.db + FTS5")
          + station(570, 200, "note", MARIGOLD, "સાર-નોંધ", "compression 50%")
          + station(790, 200, "camera", CLAY, "ફોટો", "checkpoints")
          + f'<text x="80" y="340" font-family="{FONT}" font-size="15.5" fill="{MUTED}">ડાયરીની નકલ સવારે પાટી પર: નવી નોંધ આવતા session માં દેખાય (frozen snapshot)</text>')

    frame("05-reet-pothi-skills", "પ્રકરણ 5 — રીત-પોથી",
          "હકીકત ડાયરીમાં, રીત પોથીમાં. સૂચિ હંમેશા, પાનું માગો ત્યારે, પરિશિષ્ટ વધુ ઊંડે.",
          station(130, 210, "slate", MARIGOLD, "સૂચિ", "skills_list") + arrow(180, 200, 300, 200)
          + station(360, 210, "book", MEHNDI, "પાનું", "skill_view(name)") + arrow(410, 200, 530, 200)
          + station(590, 210, "note", INDIGO, "પરિશિષ્ટ", "references/")
          + station(820, 210, "person", BANDHANI, "હર્ષ લખે", "skill_manage")
          + arrow(820, 290, 380, 290, "", -60, BANDHANI, True)
          + f'<text x="600" y="345" text-anchor="middle" font-family="{FONT}" font-size="15" fill="{BANDHANI}">નવું પાનું: નિયમ + કારણ</text>'
          + f'<text x="80" y="395" font-family="{FONT}" font-size="15.5" fill="{MUTED}">Curator: ફક્ત હર્ષે લખેલાં પાનાં; પેટીમાં, ભઠ્ઠીમાં નહીં; પિન કરેલું અડાય નહીં</text>')

    frame("06-bario-ghadiyal-shikhau", "પ્રકરણ 6 — બારીઓ, ઘડિયાળ અને શિખાઉ",
          "બારી અનેક, હર્ષ એક. યાદીમાં નથી → ના. પહેલાં ચોપડી, પછી કામ. કોરી ફાઈલ લઈ જા, સાર લઈ આવ.",
          station(100, 170, "window", INDIGO, "Telegram", "") + station(100, 310, "window", MEHNDI, "WhatsApp", "")
          + arrow(150, 170, 270, 225) + arrow(150, 310, 270, 255)
          + station(330, 240, "gate", CLAY, "રઘુકાકા", "default deny") + arrow(380, 240, 500, 240, "session key")
          + station(560, 240, "person", MARIGOLD, "હર્ષ", "AIAgent")
          + station(560, 380, "clock", BANDHANI, "", "") + f'<text x="610" y="390" font-family="{FONT}" font-size="15" fill="{BANDHANI}">cron: next_run પહેલાં, પછી કામ</text>'
          + arrow(612, 214, 765, 160, "", 0) + station(820, 170, "person", MEHNDI, "જય", "subagent")
          + arrow(770, 196, 615, 250, "", 0, MEHNDI, True)
          + f'<text x="660" y="168" font-family="{FONT}" font-size="14" fill="{INK}">કોરી ફાઈલ</text>'
          + f'<text x="700" y="250" font-family="{FONT}" font-size="14" fill="{MEHNDI}">ફક્ત સાર</text>')

    frame("07-potanu-ojar-ane-mastery", "પ્રકરણ 7 — દીવાલ નહીં, plug point",
          "Plugin core ને અડતો નથી: ctx થી ઓજાર અને ઘંટડી નોંધે. અંતિમ પ્રોજેક્ટ: 18 મહેમાન, 16 થાળી.",
          f'<rect x="60" y="130" width="16" height="230" fill="{INK}" opacity=".85"/>'
          + f'<text x="68" y="385" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{MUTED}">core</text>'
          + station(190, 240, "plug", CLAY, "plug point", "register(ctx)") + arrow(240, 240, 340, 240)
          + station(400, 240, "cupboard", MEHNDI, "mehmaan_tally", "read-only tool")
          + station(610, 240, "bell", MARIGOLD, "ઘંટડી", "post_tool_call")
          + station(820, 240, "window", INDIGO, "બહારની દુકાન", "mcp__server__tool")
          + f'<text x="130" y="390" font-family="{FONT}" font-size="15.5" fill="{BANDHANI}">lagna: મહેમાન 18 · થાળી 16 · shortage</text>')
    print("wrote", len(list(OUT.glob("*.svg"))), "illustrations to", OUT)


if __name__ == "__main__":
    main()
