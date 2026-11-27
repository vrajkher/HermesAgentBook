"""બધી book labs ચલાવો — Windows, macOS અને Linux પર એક જ રીતે. Book lab code.

    Windows (PowerShell):  py labs\\run_all.py
    macOS / Linux:         python3 labs/run_all.py

Labs ગુજરાતી છાપે છે. Windows નું console ઘણી વાર જૂનું code page (cp1252) વાપરે છે, અને ત્યાં
ગુજરાતી છાપતાં Python `UnicodeEncodeError` આપે. એટલે આ runner દરેક lab ને UTF-8 mode માં ચલાવે છે
(`PYTHONUTF8=1`) અને outputs `evidence/` માં UTF-8 તરીકે લખે છે. Hermes પોતે પણ Windows પર આ જ કરે છે
(`hermes_cli/stdio.py::configure_windows_stdio`).
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS = [
    ("pravesh-toy-agent.out", "પ્રવેશ", ["labs/pravesh/toy_agent.py"]),
    ("01-mini-loop.out", "પ્રકરણ 1", ["labs/01-loop/mini_loop.py"]),
    ("02-cache-sim.out", "પ્રકરણ 2", ["labs/02-prompt/cache_sim.py"]),
    ("03-mini-registry.out", "પ્રકરણ 3", ["labs/03-tools/mini_registry.py"]),
    ("03-mini-exec.out", "પ્રકરણ 3b", ["labs/03-tools/mini_exec.py"]),
    ("04-mini-memory.out", "પ્રકરણ 4", ["labs/04-memory/mini_memory.py"]),
    ("05-check-skill.out", "પ્રકરણ 5", ["labs/05-skills/check_skill.py", "labs/05-skills/lagna-mehmaan-yadi/SKILL.md"]),
    ("06-mini-gateway.out", "પ્રકરણ 6", ["labs/06-gateway/mini_gateway.py"]),
    ("07-test-plugin.out", "પ્રકરણ 7", ["labs/07-plugin/test_plugin.py"]),
]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    (ROOT / "evidence").mkdir(exist_ok=True)
    for out_name, label, args in LABS:
        print(f"== {label}")
        result = subprocess.run([sys.executable, *args], cwd=ROOT, env=env, capture_output=True)
        text = result.stdout.decode("utf-8")
        print(text, end="")
        if result.returncode != 0:
            print(result.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
            print(f"નિષ્ફળ: {label} (exit {result.returncode})")
            return 1
        (ROOT / "evidence" / out_name).write_text(text, encoding="utf-8", newline="\n")
    print("બધી labs પાસ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
