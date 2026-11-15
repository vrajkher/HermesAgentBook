"""પ્રકરણ 1 lab: Hermes ના loop ના ચાર નિયમ નાના રૂપમાં. Book lab code.

નકલ કરેલા નિયમ (pinned source): agent/conversation_loop.py નો while, agent/iteration_budget.py,
અને docs/developer-guide/agent-loop.md ના alternation + parallel-order નિયમ.
ચલાવો:  python3 labs/01-loop/mini_loop.py
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class IterationBudget:
    """agent/iteration_budget.py જેવું જ: consume / refund / remaining."""

    def __init__(self, max_total):
        self.max_total, self._used, self._lock = max_total, 0, threading.Lock()

    def consume(self):
        with self._lock:
            if self._used >= self.max_total:
                return False
            self._used += 1
            return True

    def refund(self):
        with self._lock:
            self._used = max(0, self._used - 1)

    @property
    def remaining(self):
        return max(0, self.max_total - self._used)


def check_alternation(messages):
    """બે user કે બે assistant સળંગ ન આવે; ફક્ત tool સળંગ આવી શકે."""
    for prev, cur in zip(messages, messages[1:]):
        if prev["role"] == cur["role"] and cur["role"] != "tool":
            return f"ભંગ: સળંગ બે '{cur['role']}'"
    return "બરાબર"


def slow_tool(name, seconds):
    time.sleep(seconds)
    return f"{name} પૂરું ({seconds}s)"


def run_turn(script, budget, interrupt_after=None):
    """script = model ના scripted જવાબોની યાદી. દરેક જવાબ: list of tool calls, અથવા text."""
    messages = [{"role": "system", "content": "…"}, {"role": "user", "content": "કામ"}]
    api_calls = 0
    while api_calls < 10 and budget.remaining > 0:
        if interrupt_after is not None and api_calls >= interrupt_after:
            return "interrupted", api_calls, messages
        budget.consume()
        reply = script[api_calls]
        api_calls += 1
        if isinstance(reply, str):                       # text → turn પૂરો
            messages.append({"role": "assistant", "content": reply})
            return "completed", api_calls, messages
        messages.append({"role": "assistant", "tool_calls": [c[0] for c in reply]})
        with ThreadPoolExecutor() as pool:               # એકથી વધુ tool call → સાથે ચાલે
            futures = [pool.submit(slow_tool, name, secs) for name, secs in reply]
            for f in futures:                            # પણ પરિણામ મૂળ ક્રમમાં જ ઉમેરાય
                messages.append({"role": "tool", "content": f.result()})
    return "budget_exhausted", api_calls, messages


if __name__ == "__main__":
    script = [[("હોલ_તપાસ", 0.3), ("કેટરર_ફોન", 0.1)], [("ભાવ_નોંધ", 0.0)], "ત્રણેય કામ થઈ ગયાં."]

    status, calls, msgs = run_turn(script, IterationBudget(50))
    print("1) સામાન્ય turn  :", status, "| model calls:", calls)
    print("   roles         :", " → ".join(m["role"] for m in msgs))
    print("   tool પરિણામ ક્રમ:", [m["content"] for m in msgs if m["role"] == "tool"][:2])
    print("   alternation   :", check_alternation(msgs))

    status, calls, _ = run_turn(script, IterationBudget(2))
    print("2) budget = 2    :", status, "| model calls:", calls)

    status, calls, _ = run_turn(script, IterationBudget(50), interrupt_after=1)
    print("3) interrupt     :", status, "| model calls:", calls)

    b = IterationBudget(3)
    b.consume(); b.consume(); b.refund()
    print("4) refund        : વપરાયા 2, પાછો 1 → બાકી", b.remaining)

    bad = [{"role": "user"}, {"role": "assistant"}, {"role": "tool"}, {"role": "user"}, {"role": "user"}]
    print("5) ખોટી ફાઈલ      :", check_alternation(bad))
