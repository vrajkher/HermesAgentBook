"""પ્રકરણ 6 lab: બારીઓ (gateway), એલાર્મ-ચોપડી (cron) અને શિખાઉ (subagent). Book lab code.

નકલ કરેલા નિયમ (pinned source): security doc "Authorization Check Order"; gateway-internals નું
session key રૂપ; cron/AGENTS.md "next_run_at BEFORE dispatch"; tools/delegate_tool_toolsets.py.
ચલાવો:  python3 labs/06-gateway/mini_gateway.py
"""

def is_authorized(platform, user_id, cfg):
    """ક્રમ મહત્ત્વનો છે; છેલ્લે default: deny."""
    if cfg.get(f"{platform}_allow_all"):
        return True, "platform allow-all"
    if user_id in cfg.get("paired", ()):
        return True, "DM pairing"
    if user_id in cfg.get(f"{platform}_allowed", ()):
        return True, "platform allowlist"
    if user_id in cfg.get("gateway_allowed", ()):
        return True, "global allowlist"
    if cfg.get("gateway_allow_all"):
        return True, "global allow-all"
    return False, "default: deny"


def session_key(platform, chat_type, chat_id, namespace="main"):
    return f"agent:{namespace}:{platform}:{chat_type}:{chat_id}"


class Gateway:
    def __init__(self):
        self.active, self.pending, self.log = set(), {}, []

    def on_message(self, key, text):
        if text == "/stop":                          # control command: કતારમાં નહીં, તરત
            self.log.append(f"{key} ← /stop (તરત પહોંચ્યો)")
        elif key in self.active:                     # હર્ષ વ્યસ્ત: સંદેશો કતારમાં
            self.pending.setdefault(key, []).append(text)
            self.log.append(f"{key} ← '{text}' કતારમાં")
        else:
            self.active.add(key)
            self.log.append(f"{key} ← '{text}' turn શરૂ")


def cron_tick(job, now, crash_during_run=False):
    """due હોય તો: પહેલાં next_run આગળ ખસેડો, પછી ચલાવો (at-most-once)."""
    if now < job["next_run"]:
        return "due નથી"
    job["next_run"] += job["every"]                  # ← dispatch પહેલાં
    if crash_during_run:
        return "ચાલતાં crash"
    job["runs"] += 1
    return "ચાલ્યું"


BLOCKED = {"delegate_task", "clarify", "memory", "send_message", "cronjob_manage"}


def delegate(parent_tools, parent_history, goal):
    child_tools = sorted(set(parent_tools) - BLOCKED)
    child_history = [{"role": "user", "content": goal}]      # કોરી ફાઈલ: parent નો ઇતિહાસ નહીં
    child_history += [{"role": "assistant", "content": "…"}] * 40   # બાળક 40 સંદેશાનું કામ કરે
    summary = f"સાર: '{goal}' પૂરું; 3 હોલ મળ્યા."
    parent_history.append({"role": "tool", "content": summary})   # parent ને ફક્ત સાર
    return child_tools, len(child_history)


if __name__ == "__main__":
    cfg = {"telegram_allowed": {"111"}, "paired": {"222"}}
    for uid in ("111", "222", "999"):
        print(f"1) telegram user {uid}:", is_authorized("telegram", uid, cfg))
    print("2) keys:", session_key("telegram", "private", "111"), "|", session_key("whatsapp", "private", "111"))
    gw, key = Gateway(), session_key("telegram", "private", "111")
    for text in ("હોલ શોધ", "અને કેટરર પણ", "/stop"):
        gw.on_message(key, text)
    print("3)", *gw.log, sep="\n   ")
    job = {"next_run": 100, "every": 60, "runs": 0}
    print("4) t=90 :", cron_tick(job, 90), "| t=100:", cron_tick(job, 100, crash_during_run=True),
          "| restart t=101:", cron_tick(job, 101), "| t=160:", cron_tick(job, 160), "| કુલ runs:", job["runs"])
    parent_history = [{"role": "user", "content": "…"}] * 6
    tools, child_len = delegate(["terminal", "read_file", "web_search", "memory", "delegate_task", "clarify"],
                                parent_history, "વડોદરામાં 500 મહેમાનના હોલ શોધ")
    print("5) બાળકનાં tools:", tools)
    print(f"   બાળકની ફાઈલ: {child_len} સંદેશા | parent ની ફાઈલ: 6 → {len(parent_history)} (ફક્ત સાર ઉમેરાયો)")
