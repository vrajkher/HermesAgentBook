"""પ્રકરણ 7 lab: plugin ને Hermes વગર ચકાસો — નકલી ctx સાથે. Book lab code.

Hermes માં સાચી ચકાસણી `hermes plugins doctor <path>` કરે છે; આ test ફક્ત એટલું સાબિત કરે છે કે
register(ctx) સાચા નામે tool અને hook નોંધે છે અને handler ના નિયમ પાળે છે.
ચલાવો:  python3 labs/07-plugin/test_plugin.py
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


class FakeCtx:
    def __init__(self):
        self.tools, self.hooks = {}, {}

    def register_tool(self, name, toolset, schema, handler, **kw):
        assert isinstance(schema, dict) and isinstance(schema.get("parameters"), dict), "schema must be a dict"
        assert schema["name"] == name
        self.tools[name] = (toolset, handler)

    def register_hook(self, hook_name, callback, **kw):
        self.hooks[hook_name] = callback


def load_plugin():
    spec = importlib.util.spec_from_file_location(
        "mehmaan_tally", HERE / "mehmaan-tally" / "__init__.py",
        submodule_search_locations=[str(HERE / "mehmaan-tally")])
    module = importlib.util.module_from_spec(spec)
    sys.modules["mehmaan_tally"] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    ctx = FakeCtx()
    load_plugin().register(ctx)
    declared = [ln.strip("- \n") for ln in (HERE / "mehmaan-tally" / "plugin.yaml").read_text().split("provides_tools:")[1].split("provides_hooks:")[0].splitlines() if ln.strip()]
    print("1) નોંધાયેલાં tools:", sorted(ctx.tools), "| plugin.yaml માં જાહેર:", declared, "| hooks:", sorted(ctx.hooks))
    assert sorted(ctx.tools) == sorted(declared)

    handler = ctx.tools["mehmaan_tally"][1]
    out = json.loads(handler({"rsvp_path": str(HERE / "fixtures/rsvp.csv"), "caterer_path": str(HERE / "fixtures/caterer.csv")},
                             task_id="t1", session_id="s1"))
    print("2) પરિણામ:")
    for e in out["events"]:
        print(f"     {e['event']:<10} મહેમાન={e['guests']!s:<5} થાળી={e['plates']!s:<5} ફરક={e['difference']!s:<5} {e['status']}")
    print("   maybe (ગણ્યા નથી):", out["unconfirmed_maybe"], "| all_ok:", out["all_ok"])
    assert [e["status"] for e in out["events"]] == ["shortage", "missing_in_rsvp", "ok", "missing_in_caterer"]

    for label, args in (("ખૂટતો arg", {}), ("ખૂટતી file", {"rsvp_path": "/no/file.csv", "caterer_path": "/no/file.csv"})):
        raw = handler(args)                      # raise ન થવું જોઈએ; JSON string જ આવે
        print(f"3) {label}:", json.loads(raw)["error"][:60])
    ctx.hooks["post_tool_call"]("mehmaan_tally", {}, "{}", "t1", duration_ms=3)
    ctx.hooks["post_tool_call"]("terminal", {}, "{}", "t1", duration_ms=3)
    print("4) hook બે વાર ચાલ્યો, crash નથી. બધી ચકાસણી પાસ ✅")
