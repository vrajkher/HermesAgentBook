"""પ્રવેશ lab: 45 line નો રમકડા-agent. Book lab code (Hermes નો code નથી).

શાસ્ત્રીજી (model) અહીં scripted છે: API key કે internet જોઈતું નથી.
ચલાવો:  python3 labs/pravesh/toy_agent.py
"""
import json

MENU = ["મહેંદી", "સંગીત", "હલ્દી", "લગ્ન", "રિસેપ્શન"]


def shastriji(messages):
    """Scripted model: ફાઈલમાં tool નું પરિણામ ન હોય તો tool માગે, હોય તો જવાબ આપે."""
    if messages[-1]["role"] == "tool":
        count = json.loads(messages[-1]["content"])["count"]
        return {"role": "assistant", "content": f"પટેલ પરિવારના લગ્નમાં {count} પ્રસંગ છે."}
    return {"role": "assistant", "content": None,
            "tool_calls": [{"id": "call_1", "name": "prasang_list", "args": {}}]}


TOOLS = {"prasang_list": lambda args: json.dumps({"items": MENU, "count": len(MENU)}, ensure_ascii=False)}


def run(user_message):
    messages = [{"role": "system", "content": "તું શુભમંગલ વેડિંગ પ્લાનર્સનો સહાયક છે."},
                {"role": "user", "content": user_message}]
    model_calls = 0
    while True:
        reply = shastriji(messages)          # 1. આખી ફાઈલ model ને મોકલો
        model_calls += 1
        messages.append(reply)
        if not reply.get("tool_calls"):      # 2. tool call નથી → જવાબ તૈયાર
            return reply["content"], model_calls, messages
        for call in reply["tool_calls"]:     # 3. tool ચલાવો, પરિણામ ફાઈલમાં ઉમેરો
            result = TOOLS[call["name"]](call["args"])
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})


if __name__ == "__main__":
    answer, calls, messages = run("પટેલ પરિવારના લગ્નમાં કેટલા પ્રસંગ છે?")
    print("roles:", " → ".join(m["role"] for m in messages))
    print("modelCalls:", calls)
    print("જવાબ:", answer)
