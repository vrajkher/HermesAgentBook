"""પ્રકરણ 2 lab: સૂચના-પાટી ના ત્રણ થર અને prefix cache. Book lab code.

નકલ કરેલો નિયમ: agent/system_prompt.py — stable → context → volatile, અને
"system prompt વાતચીત દરમિયાન byte-stable". Cache અહીં સરળ model છે: બે સળંગ request નો
જેટલો શરૂઆતી ભાગ અક્ષરશઃ સરખો, તેટલો "સસ્તો" (ભાવનો દસમો ભાગ).
ચલાવો:  python3 labs/02-prompt/cache_sim.py
"""

def build_system_prompt(memory, memory_first=False):
    stable = "તું હર્ષ છે, શુભમંગલનો સહાયક. " + "ઓજાર વાપરવાના નિયમ… " * 40
    context = "PROJECT (AGENTS.md): પટેલ પરિવારનાં લગ્ન, 12 ડિસેમ્બર, વડોદરા. " * 6
    volatile = f"રીત-પોથી સૂચિ: mehmaan-yadi, mandap-checklist\nMEMORY: {memory}\nસમય: સવારે 9:00"
    if memory_first:                                     # ખોટો ક્રમ: બદલાતી વસ્તુ સૌથી ઉપર
        return "\n\n".join([volatile, stable, context])
    return "\n\n".join([stable, context, volatile])      # Hermes નો ક્રમ: stable → context → volatile


def common_prefix(a, b):
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n


def cost(request, previous):
    """આગલા request સાથે સરખો શરૂઆતી ભાગ 0.1 ભાવે, બાકીનો 1.0 ભાવે."""
    cached = common_prefix(request, previous) if previous else 0
    return cached, len(request) - cached, round(cached * 0.1 + (len(request) - cached) * 1.0)


def conversation(turns, freeze_system_prompt, memory_first=False):
    memory = "સ્મિતાબેનને ટૂંકા જવાબ ગમે"
    system = build_system_prompt(memory, memory_first)
    history, previous, total = "", None, 0
    for i, user_text in enumerate(turns, 1):
        if i == 3:                                   # ત્રીજા turn માં agent memory માં નવી નોંધ ઉમેરે
            memory += "; કેટરર: જલારામ"
            if not freeze_system_prompt:             # ખોટી રીત: પાટી તરત ફરી લખવી
                system = build_system_prompt(memory, memory_first)
        history += f"\nUSER: {user_text}\nASSISTANT: " + "જવાબ… " * 30
        request = system + history
        cached, fresh, price = cost(request, previous)
        total += price
        print(f"   turn {i}: કુલ {len(request):5d} અક્ષર | cache {cached:5d} | નવા {fresh:5d} | ભાવ {price:5d}")
        previous = request
    return total


if __name__ == "__main__":
    turns = ["હોલ કયો?", "મેનુ?", "કેટરર યાદ રાખ.", "મહેમાન કેટલા?", "બજેટ?"]
    print("A) Hermes ની રીત — પાટી આખી વાતચીત સ્થિર (frozen snapshot):")
    a = conversation(turns, freeze_system_prompt=True)
    print("B) ખોટી રીત — memory બદલાય કે તરત પાટી ફરી લખવી:")
    b = conversation(turns, freeze_system_prompt=False)
    print("C) બમણી ભૂલ — પાટી ફરી લખવી, અને બદલાતો ભાગ (memory) સૌથી ઉપર:")
    c = conversation(turns, freeze_system_prompt=False, memory_first=True)
    print(f"કુલ ભાવ: A = {a}, B = {b}, C = {c}")
