"""પ્રકરણ 3 lab: ઓજાર-કબાટ (tool registry) નાના રૂપમાં. Book lab code.

નકલ કરેલા નિયમ (pinned source): tools/registry.py — register() schema તપાસે, get_definitions()
check_fn પાસ થાય તે જ tools આપે, dispatch() દરેક exception ને {"error": …} માં ફેરવે;
tools/approval_detection.py — જોખમી command ની પેટર્ન.
ચલાવો:  python3 labs/03-tools/mini_registry.py
"""
import json
import os
import re


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, toolset, schema, handler, check_fn=None):
        if not isinstance(schema, dict):             # ખરાબ schema નોંધણી વખતે જ પકડાય
            raise ValueError(f"Tool {name!r}: schema must be a dict, got {type(schema).__name__}")
        self._tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "check_fn": check_fn}

    def get_definitions(self, tool_names):
        """Model ને દેખાતી યાદી: માગેલાં નામ, સૉર્ટ કરેલાં, અને check_fn પાસ થાય તે જ."""
        out = []
        for name in sorted(tool_names):
            entry = self._tools.get(name)
            if entry and (entry["check_fn"] is None or entry["check_fn"]()):
                out.append({**entry["schema"], "name": name})
        return out

    def dispatch(self, name, args):
        entry = self._tools.get(name)
        if not entry:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            return entry["handler"](args)
        except Exception as e:                       # handler ફાટે તો પણ loop ન તૂટે
            return json.dumps({"error": f"Tool execution failed: {type(e).__name__}: {e}"})


registry = ToolRegistry()

# દરેક tool પોતાની નોંધણી પોતે કરે (Hermes માં: tools/*.py import થતાં જ).
registry.register("read_file", "file", {"description": "file વાંચો", "parameters": {"type": "object"}},
                  lambda a: json.dumps({"content": open(a["path"], encoding="utf-8").read()[:60]}))
registry.register("terminal", "terminal", {"description": "command ચલાવો", "parameters": {"type": "object"}},
                  lambda a: json.dumps({"would_run": a["command"]}))
registry.register("web_search", "web", {"description": "web શોધ", "parameters": {"type": "object"}},
                  lambda a: json.dumps({"results": []}),
                  check_fn=lambda: bool(os.getenv("DEMO_SEARCH_KEY")))   # key ન હોય તો model ને દેખાય જ નહીં

TOOLSETS = {"file": ["read_file"], "terminal": ["terminal"], "web": ["web_search"]}

# જોખમી command: Hermes ની ખરી યાદી ઘણી લાંબી છે; આ ત્રણ ફક્ત વિચાર બતાવે છે.
HARDLINE = [(r"\brm\s+-[a-z]*r[a-z]*\s+/(\s|$)", "recursive delete of root filesystem")]
DANGEROUS = [(r"\brm\s+-[^\s]*r", "recursive delete"), (r"\bgit\s+push\s+.*--force", "force push")]


def approval(command, owner_says):
    for pattern, why in HARDLINE:
        if re.search(pattern, command):
            return f"BLOCKED ({why}) — સહી કે YOLO પણ નહીં ચાલે"
    for pattern, why in DANGEROUS:
        if re.search(pattern, command):
            return f"{'approved' if owner_says else 'denied'} ({why}) — સ્મિતાબેનને પૂછ્યું"
    return "safe — પૂછવાની જરૂર નથી"


if __name__ == "__main__":
    wanted = {n for ts in ("file", "terminal", "web") for n in TOOLSETS[ts]}
    print("1) model ને દેખાતાં tools (key વગર):", [d["name"] for d in registry.get_definitions(wanted)])
    os.environ["DEMO_SEARCH_KEY"] = "x"
    print("   key મૂક્યા પછી               :", [d["name"] for d in registry.get_definitions(wanted)])
    print("2) અજાણ્યું tool   :", registry.dispatch("fly_drone", {}))
    print("3) handler ફાટ્યો  :", registry.dispatch("read_file", {"path": "/no/such/file"}))
    try:
        registry.register("bad", "x", ["not", "a", "dict"], lambda a: "")
    except ValueError as e:
        print("4) ખરાબ schema    :", e)
    for cmd in ("ls -la", "rm -rf build/", "rm -rf /"):
        print(f"5) {cmd:<14}:", approval(cmd, owner_says=False))
