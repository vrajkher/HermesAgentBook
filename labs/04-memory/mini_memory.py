"""પ્રકરણ 4 lab: ખિસ્સા-ડાયરી, રોજમેળ અને સાર-નોંધ. Book lab code.

નકલ કરેલા નિયમ (pinned source): tools/memory_tool_store.py — "§" delimiter, અક્ષર-મર્યાદા,
frozen snapshot; persistence/sqlite/_schema_ddl.py — SQLite FTS5; context-compression doc — જૂનાં tool
પરિણામ સાફ, માથું અને પૂંછડી સચવાય.
ચલાવો:  python3 labs/04-memory/mini_memory.py
"""
import sqlite3

DELIM = "\n§\n"
PLACEHOLDER = "[Old tool output cleared to save context space]"


class MemoryStore:
    def __init__(self, limit=2200):
        self.limit, self.entries, self.snapshot = limit, [], ""

    def load(self):                       # session શરૂ: snapshot થીજી જાય
        self.snapshot = DELIM.join(self.entries)

    def add(self, content):
        if len(DELIM.join(self.entries + [content])) > self.limit:
            used = len(DELIM.join(self.entries))
            return {"success": False, "error": f"would exceed the limit ({used}/{self.limit} chars)"}
        self.entries.append(content)      # disk પર તરત; snapshot માં નહીં
        return {"success": True, "usage": f"{len(DELIM.join(self.entries))}/{self.limit}"}


def session_search_demo():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, session_id TEXT, role TEXT, content TEXT)")
    db.execute("CREATE VIRTUAL TABLE messages_fts USING fts5(content, content=messages, content_rowid=id)")
    rows = [("s1", "user", "Patel wedding caterer is Jalaram, 450 plates"),
            ("s1", "assistant", "Noted: Jalaram caterer, 450 plates for 12 December"),
            ("s2", "user", "Shah engagement needs a florist near Alkapuri"),
            ("s3", "user", "Change Patel wedding plates to 480")]
    for r in rows:
        cur = db.execute("INSERT INTO messages (session_id, role, content) VALUES (?,?,?)", r)
        db.execute("INSERT INTO messages_fts (rowid, content) VALUES (?,?)", (cur.lastrowid, r[2]))
    q = "SELECT m.session_id, m.content FROM messages_fts f JOIN messages m ON m.id = f.rowid WHERE messages_fts MATCH ?"
    return db.execute(q, ("plates",)).fetchall()


def compress(messages, protect_first=3, protect_last=4):
    """Phase 1 (સસ્તો): વચ્ચેનાં લાંબાં tool પરિણામ સાફ. Phase 2-4: વચ્ચેનો ભાગ એક સાર-નોંધ."""
    head, middle, tail = messages[:protect_first], messages[protect_first:-protect_last], messages[-protect_last:]
    pruned = [{**m, "content": PLACEHOLDER} if m["role"] == "tool" and len(m["content"]) > 200 else m for m in middle]
    summary = {"role": "user", "content": f"[સાર-નોંધ: વચ્ચેના {len(middle)} સંદેશા — હોલ નક્કી, કેટરર જલારામ, 450 થાળી]"}
    return head + [summary] + tail, sum(m["content"] == PLACEHOLDER for m in pruned)


if __name__ == "__main__":
    mem = MemoryStore(limit=120)
    mem.entries = ["સ્મિતાબેનને ટૂંકા જવાબ ગમે"]
    mem.load()
    print("1) add            :", mem.add("પટેલ લગ્ન: કેટરર જલારામ, 450 થાળી"))
    print("   પાટી પરનો snapshot:", repr(mem.snapshot), "← નવી નોંધ આ session માં નથી દેખાતી")
    print("2) મર્યાદા ઉપર     :", mem.add("મંડપવાળાનો નંબર, ફૂલવાળાનો નંબર, બેન્ડવાળાનો નંબર, ઘોડીવાળાનો નંબર"))
    mem.load()
    print("3) નવું session    :", repr(mem.snapshot))
    print("4) session_search 'plates':")
    for sid, content in session_search_demo():
        print("     ", sid, "|", content)
    msgs = [{"role": "system", "content": "પાટી"}, {"role": "user", "content": "શરૂ"}, {"role": "assistant", "content": "હા"}]
    for i in range(6):
        msgs += [{"role": "assistant", "content": f"tool call {i}"}, {"role": "tool", "content": "હોલની વિગત… " * 40}]
    msgs += [{"role": "user", "content": "છેલ્લો પ્રશ્ન"}, {"role": "assistant", "content": "છેલ્લો જવાબ"}]
    out, cleared = compress(msgs)
    print(f"5) compression    : {len(msgs)} સંદેશા → {len(out)} | સાફ થયેલાં tool પરિણામ: {cleared}")
    print("   roles          :", " ".join(m["role"][0] for m in out), "(s=system u=user a=assistant t=tool)")
