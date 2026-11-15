"""પ્રકરણ 3 lab (ભાગ 2): એક-એક ઓજાર vs એક script — `execute_code` નો વિચાર. Book lab code.

નકલ કરેલો નિયમ (pinned docs): user-guide/features/code-execution.md — "Only the script's print()
output is returned to the LLM; intermediate tool results never enter the context window."
ચલાવો:  python3 labs/03-tools/mini_exec.py
"""
import json
import random

random.seed(12)
# 30 કેટરરનાં ભાવપત્રક: દરેક file લાંબી છે (મેનુ, શરતો, ફોન નંબર…), પણ કામની વાત ફક્ત ભાવ.
CATERERS = {f"caterer_{i:02d}.txt": {"name": f"કેટરર {i:02d}", "per_plate": random.randint(380, 720),
                                     "jain": random.random() < 0.4, "filler": "મેનુ અને શરતો… " * 60}
            for i in range(1, 31)}


def read_file(path):
    return json.dumps(CATERERS[path], ensure_ascii=False)


def one_tool_at_a_time():
    """દરેક read_file એક અલગ model call; દરેક પરિણામ આખું ફાઈલમાં (context માં) જાય."""
    context, model_calls = ["system + user: 'સૌથી સસ્તો જૈન કેટરર કયો?'"], 0
    for path in CATERERS:
        model_calls += 1                     # model: "read_file(path)" માગે
        context.append(read_file(path))      # આખું પરિણામ ફાઈલમાં
    model_calls += 1                         # છેલ્લો call: જવાબ
    return model_calls, sum(len(c) for c in context)


def one_script():
    """Model એક script લખે; script અંદરથી 30 વાર read_file બોલાવે; ફક્ત print() પાછું જાય."""
    context, model_calls = ["system + user: 'સૌથી સસ્તો જૈન કેટરર કયો?'"], 1   # call 1: script લખે
    script_tool_calls = 0
    best = None
    for path in CATERERS:                    # આ loop script ની અંદર ચાલે છે, model ની નહીં
        script_tool_calls += 1
        c = json.loads(read_file(path))
        if c["jain"] and (best is None or c["per_plate"] < best["per_plate"]):
            best = c
    printed = f"{best['name']}: ₹{best['per_plate']} / થાળી (જૈન)"
    context.append(printed)                  # ફક્ત આ એક લીટી context માં
    model_calls += 1                         # call 2: જવાબ
    return model_calls, sum(len(c) for c in context), script_tool_calls, printed


if __name__ == "__main__":
    a_calls, a_chars = one_tool_at_a_time()
    b_calls, b_chars, inner, printed = one_script()
    print(f"A) એક-એક ઓજાર : model calls {a_calls:2d} | context {a_chars:6d} અક્ષર")
    print(f"B) એક script   : model calls {b_calls:2d} | context {b_chars:6d} અક્ષર | script ની અંદર tool calls {inner}")
    print(f"   script નું print(): {printed}")
    print(f"   context {round(a_chars / b_chars)} ગણો નાનો, model calls {a_calls - b_calls} ઓછા")
