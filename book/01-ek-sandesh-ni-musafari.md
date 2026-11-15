# પ્રકરણ 1 — એક સંદેશાની આખી મુસાફરી

> **Level 1 · વાર્તાનો દિવસ 3–4.**
> આખા પ્રકરણમાં એક જ સંદેશો: **"પટેલ પરિવારના લગ્ન માટે હોલ, કેટરર અને ભાવ નક્કી કરો."**
> ઑફિસમાં જે ઘટના બને છે તે જ Hermes નો નિયમ છે; દરેક ઘટના પછી ઈશા એ નિયમ pinned source માં ખોલે છે.
> પહેલાં: [પ્રકરણ 0](00-paayo-ane-pratham-run.md). આખો નકશો: [સમગ્ર નકશો](overview-samagra-naksho.md).

## 🎯 આ પ્રકરણ પછી તમે શું કરી શકશો

- **Turn** અને **iteration** નો તફાવત સમજાવી, કોઈ પણ કામમાં કેટલા model calls થયા તે ગણી શકશો.
- `agent/conversation_loop.py` ના `while` ને line-by-line વાંચી, દરેક તબક્કાનું કામ કહી શકશો.
- **Iteration budget**, **interrupt**, અને **role alternation** — loop ની ત્રણ વાડ — કેમ છે તે કહી શકશો.
- `labs/01-loop/mini_loop.py` ચલાવી, પાંચેય પરિણામ પહેલેથી ધારી શકશો.

## 🗺️ નકશો: એક સંદેશાના આઠ સ્ટેશન

| # | ઑફિસમાં | Hermes માં | દૃશ્ય |
|---|---|---|---|
| 1 | સંદેશો આવ્યો | Entry point → `AIAgent.run_conversation()` | 1 |
| 2 | ફાઈલમાં ઉમેરાયો | User message `messages` માં append | 1 |
| 3 | પાટી તૈયાર | System prompt બને કે cache માંથી આવે | (પ્રકરણ 2) |
| 4 | શાસ્ત્રીજીને ફોન | Model API call (interruptible) | 2, 5 |
| 5 | ચિઠ્ઠી કે જવાબ? | `tool_calls` છે કે નહીં | 2 |
| 6 | ઓજાર ચાલ્યું | Tool round; પરિણામ `messages` માં | 3 |
| 7 | રોજમેળમાં નોંધ | Session DB માં persist | (પ્રકરણ 4) |
| 8 | જવાબ પહોંચ્યો | `final_response` | 1 |

**યાદ-ચાવી "1-3-3":** આ સંદેશામાં **1** turn, **3** model calls, **3** tool calls.

---

## દૃશ્ય 1 — એક કામ, ત્રણ ફોન: turn અને iteration

🎬 સવારે સ્મિતાબેન હર્ષને કહે છે: "પટેલના લગ્ન માટે હોલ, કેટરર અને ભાવ નક્કી કર." ઈશા હર્ષની પાછળ ફરે છે અને ગણે છે.

- **ફોન 1.** શાસ્ત્રીજી: "હોલની ઉપલબ્ધતા તપાસ, અને કેટરરને ફોન કર." (બે ચિઠ્ઠી એકસાથે.)
- હર્ષ બંને કામ કરે છે.
- **ફોન 2.** શાસ્ત્રીજી: "હવે ભાવ નોંધી લે." (એક ચિઠ્ઠી.)
- હર્ષ ભાવ નોંધે છે.
- **ફોન 3.** શાસ્ત્રીજી: "ત્રણેય કામ થઈ ગયાં." કોઈ ચિઠ્ઠી નથી.

સ્મિતાબેને **એક** કામ આપ્યું હતું. હર્ષે **ત્રણ** ફોન કર્યા.

❓ "બિલ કામ પ્રમાણે આવે કે ફોન પ્રમાણે?"

"ફોન પ્રમાણે. એટલે બે જુદાં નામ જોઈએ."

💻 Hermes માં:

- **Turn** = વપરાશકર્તાના એક સંદેશાથી અંતિમ જવાબ સુધીનું આખું કામ. Code માં: `run_conversation()` નો એક call ([conversation_loop.py][loop-runconv]) ✅. તેનો docstring: "Run one turn".
- **Iteration** = turn ની અંદર loop નું એક ચક્કર: એક model call, અને તેણે માગેલાં tools.

`AIAgent` ના બે દરવાજા છે ([agent/AGENTS.md][agent-shape]) ✅:

```python
# Repository code — agent/turn_facade.py
def chat(self, message: str, stream_callback: Optional[callable] = None) -> str:
    """Final response string of one turn; ``stream_callback`` receives each text delta."""
    return self.run_conversation(message, stream_callback=stream_callback)["final_response"]
```

([turn_facade.py][facade-chat]) ✅. `chat()` સાદો દરવાજો છે: ફક્ત જવાબ. `run_conversation()` પૂરો દરવાજો: `final_response` સાથે આખા `messages`.

🔬 **Expert નજર.** "આ agent કેટલું મોંઘું પડશે?" નો જવાબ turn માં નથી, **iteration** માં છે. અને દરેક iteration માં **આખી ફાઈલ** ફરી જાય છે, એટલે ત્રીજો ફોન પહેલા કરતાં મોંઘો છે: તેમાં પહેલા બે ફોનનાં પરિણામ પણ છે. કોઈ પણ agent નું વર્તન જોતાં expert નો પહેલો પ્રશ્ન: **"કેટલા iterations, અને દરેક કેમ જરૂરી હતો?"**

## દૃશ્ય 2 — હર્ષનો દિવસ, ખરા code માં: `while`

🎬 નિખિલમામા પ્રવેશ પ્રકરણનો ત્રણ-લીટીનો કાગળ કાઢે છે. "આ રમકડું હતું. હવે ખરો જુઓ."

💻 **Repository code** — આખા Hermes નું હૃદય ([conversation_loop.py][loop-while]) ✅:

```python
while _prelude_action != "break" and (
    (s.api_call_count < agent.max_iterations and agent.iteration_budget.remaining > 0) or agent._budget_grace_call
):
```

ત્રણ શરતો વાંચો:

1. `s.api_call_count < agent.max_iterations` — આ turn માં ફોનની સંખ્યા મર્યાદાની અંદર છે.
2. `agent.iteration_budget.remaining > 0` — ચક્કર-મર્યાદામાં હજી ચક્કર બાકી છે.
3. `or agent._budget_grace_call` — મર્યાદા પૂરી થઈ હોય તો પણ **એક છેલ્લો ફોન** ("grace call"), જેથી હર્ષ અધૂરું કામ સમેટીને અહેવાલ આપી શકે.

Loop ની અંદર દરેક તબક્કો અલગ function છે. નામ પોતે વાર્તા કહે છે:

| તબક્કો | કામ | વાર્તામાં |
|---|---|---|
| `begin_iteration` | Interrupt અને budget તપાસો; `api_call_count` વધારો | "કોઈએ રોક્યો તો નથી ને? ચક્કર બાકી છે?" |
| `prepare_iteration` | `messages` તૈયાર કરો (steer, repair) — દરેક ફેરફાર cache-safe | ફાઈલ સરખી કરો, પણ જૂનાં પાનાં અડ્યા વગર |
| `assemble_api_request` | Request બનાવો | ફાઈલ ક્રમમાં ગોઠવો |
| `run_preflight_gate` | મોકલતાં પહેલાં છેલ્લી તપાસ | ફોન લગાડતાં પહેલાં |
| `_run_api_retry_loop` | Model call, retries સાથે | ફોન; ન લાગે તો ફરી |
| `normalize_model_response` | જવાબ એક રૂપમાં લાવો | શાસ્ત્રીજીના શબ્દો નોંધો |
| `run_tool_round` **કે** `finish_text_response` | ચિઠ્ઠી → ઓજાર; જવાબ → પૂરું | છેલ્લો નિર્ણય |

અને છેલ્લો નિર્ણય એક જ line માં ([conversation_loop.py][loop-branch]) ✅:

```python
_v = _run_phase(
    run_tool_round if s.assistant_message.tool_calls else finish_text_response, agent, s
)
```

**ચિઠ્ઠી છે? → ઓજારનું ચક્કર. નથી? → જવાબ સમેટો.** પ્રવેશ પ્રકરણના રમકડાની `if not reply.get("tool_calls")` બરાબર આ line છે.

⚠️ **વાર્તા અને ખરું વર્તન.** વાર્તામાં હર્ષ એક માણસ છે. Code માં `AIAgent` અનેક mixins થી જોડાયેલો class છે, અને turn શરૂ થતાં પહેલાં session નું **turn lease** લેવાય છે, જેથી એક જ વાતચીત પર બે turns એકસાથે ન ચાલે ([agent/AGENTS.md][agent-shape]) ✅.

🔬 **Expert નજર.** દરેક તબક્કો અલગ file (`agent/turn_*.py`) માં કેમ? Guide કારણ આપે છે: overflow handling બદલવું હોય તો એક ~600-line file અડવી પડે, આખો loop નહીં. પહેલાં આ બધું એક "god file" માં હતું. **જે code એક સ્ક્રીન પર ન સમાય, તેનો review પણ ન થાય** — અને જેનો review ન થાય, તેમાં bugs રહે.

## દૃશ્ય 3 — બે ચિઠ્ઠી એકસાથે: parallel tools અને ક્રમ

🎬 ફોન 1 માં બે ચિઠ્ઠી હતી: "હોલ તપાસ" અને "કેટરરને ફોન". હર્ષ બંને **એકસાથે** શરૂ કરે છે — હોલવાળાને સંદેશો મૂકીને તરત કેટરરને ફોન. કેટરરનો જવાબ પહેલો આવે છે, હોલનો પછી.

પણ ફાઈલમાં હર્ષ **પહેલાં હોલનું**, પછી કેટરરનું પરિણામ લખે છે.

❓ "જે પહેલું આવ્યું તે પહેલું કેમ નહીં?"

"શાસ્ત્રીજીએ **જે ક્રમમાં માગ્યું**, તે ક્રમમાં જવાબ જોઈએ. નહીં તો તે ગૂંચવાય કે કયો જવાબ કઈ ચિઠ્ઠીનો."

💻 Agent loop doc ([Sequential vs Concurrent][doc-loop-concurrent]) ✅:

- **એક** tool call → સીધું main thread માં.
- **અનેક** tool calls → thread pool માં એકસાથે.
- અપવાદ: interactive tools (જેમ કે `clarify`) હોય તો ક્રમસર.
- **"Results are reinserted in the original tool call order regardless of completion order."**

કેટલાંક tools કબાટ સુધી જતાં જ નથી; હર્ષ તે **પોતે** કરે છે, કારણ કે તે તેની પોતાની સ્થિતિ બદલે છે. Code માં આ `INLINE_TOOL_EXECUTORS` table છે: `todo_list`, `session_search`, `memory` ([inline_tool_executors.py][inline-exec]) ✅. બાકીનાં `handle_function_call()` મારફતે registry માં જાય છે ([model_tools.py][handle-fc]) ✅ — તે પ્રકરણ 3 નો વિષય.

🔬 **Expert નજર.** Guide નવા agent-level tool માટે કહે છે: table માં નોંધણી કરો, "no `if name == ...` chain". નામની સીડી (`if … elif … elif …`) દરેક નવા tool સાથે લાંબી થાય અને દરેક ફેરફારમાં merge conflict આપે; table માં નવી line ઉમેરાય, જૂની અડાય નહીં.

## દૃશ્ય 4 — "લસણ વગર" નહીં, "ક્રમ વગર" નો ઝઘડો: role alternation

🎬 ઈશા મદદ કરવા ફાઈલમાં ગ્રાહકના બે સંદેશા **સળંગ** ચોંટાડી દે છે, વચ્ચે શાસ્ત્રીજીનો જવાબ લખ્યા વગર. ફોન પર શાસ્ત્રીજી અટકી જાય છે: "આ ફાઈલ ગરબડ છે. પ્રશ્ન પછી જવાબ હોય; બે પ્રશ્ન સળંગ કેમ?" અને ફોન કાપી નાખે છે.

💻 Hermes આ ક્રમ **કડક** રીતે પાળે છે ([agent loop doc][doc-loop-alternation]) ✅:

- System message પછી: `user → assistant → user → assistant → …`
- Tool calling દરમિયાન: `assistant (tool_calls) → tool → tool → … → assistant`
- **કદી** બે assistant સળંગ નહીં; **કદી** બે user સળંગ નહીં.
- ફક્ત `tool` role સળંગ આવી શકે (parallel પરિણામ).

કેમ? Doc: "Providers validate these sequences and will reject malformed histories." — model કંપનીનું server ખોટા ક્રમની ફાઈલ **reject** કરે છે.

Guide એક ઝીણો અપવાદ નોંધે છે: `/steer` (કામ ચાલુ હોય ત્યારે દિશા બદલવી) tool result **પછી** અલગ user row તરીકે જાય છે; `assistant(tool_calls) → tool → user` દરેક provider પર માન્ય છે ([agent/AGENTS.md][agent-flow-invariants]) ✅.

🔬 **Expert નજર.** Guide કહે છે કે cron ના deliveries **પોતાના અલગ session** માં રહે છે, આ જ કારણે: ચાલુ વાતચીતની વચ્ચે એલાર્મનો સંદેશો ઘુસાડો તો alternation તૂટે. એક નાનો નિયમ (ક્રમ) એક મોટો design નિર્ણય (cron અલગ session) નક્કી કરે છે. Architecture આમ જ બને છે: **નિયમો ઉપરથી નથી આવતા; એક invariant ના પરિણામ તરીકે નીચેથી ઊગે છે.**

## દૃશ્ય 5 — હોલવાળા પાસે 40 ચક્કર: iteration budget

🎬 એક દિવસ હર્ષ હોલવાળાને ફોન કરે છે; લાઈન વ્યસ્ત. શાસ્ત્રીજી કહે: "ફરી કર." વ્યસ્ત. "ફરી કર." બપોર સુધીમાં 40 ફોન, અને શાસ્ત્રીજીનું બિલ ચડતું જાય છે.

સ્મિતાબેન: "એક કામ પાછળ વધુમાં વધુ આટલા ફોન. પછી **જે થયું હોય તે સમેટીને** મને કહે."

💻 આ `IterationBudget` છે — ફક્ત 34 lines ([iteration_budget.py][budget-class]) ✅:

```python
# Repository code — agent/iteration_budget.py
def consume(self) -> bool:
    """Try to consume one iteration.  Returns True if allowed."""
    with self._lock:
        if self._used >= self.max_total:
            return False
        self._used += 1
        return True

def refund(self) -> None:
    """Give back one iteration (e.g. for execute_code turns)."""
    with self._lock:
        if self._used > 0:
            self._used -= 1
```

- `consume()` = એક ચક્કર વાપરો; મર્યાદા પૂરી હોય તો `False`.
- `refund()` = ચક્કર પાછું આપો. `execute_code` (એક script જે અંદરથી અનેક tools બોલાવે) ના iterations પાછા અપાય છે, જેથી તે budget ન ખાય.
- `_lock` = thread-safe; parallel tools એકસાથે ગણતરી બગાડે નહીં.

**દરેક agent નું પોતાનું budget** છે: parent નું અલગ, દરેક subagent નું અલગ (પ્રકરણ 6).

### ⚠️ Docs અને code જુદું કહે છે: expert શું કરે?

અહીં એક સાચો, pinned commit માંનો વિરોધાભાસ છે:

| સ્રોત | Parent ની default મર્યાદા | Subagent ની default |
|---|---|---|
| `iteration_budget.py` નો docstring ([link][budget-doc]) | 500 | 50 |
| Agent loop doc ([link][doc-loop-budget]) | 500 | 50 |
| `AIAgent.__init__` signature ([link][aiagent-maxiter]) | `sys.maxsize` — "unlimited … by default" | — |
| `config_defaults.py` ([link][config-max-turns]) | `"max_turns": None` | — |
| `delegate_tool.py` ([link][delegate-maxiter]) | — | `DEFAULT_MAX_ITERATIONS = 250` |

✅ પાંચેય links ખોલીને ચકાસેલી છે. `hermes_cli/config.py` માં `TURN_LIMIT_UNLIMITED = sys.maxsize` છે ([link][turn-unlimited]), અને તેની ઉપરની comment સમજાવે છે કે આ મોટો આંકડો દરેક `<` / `>=` સરખામણીમાં "unlimited" ના ખાસ case વગર કામ કરે છે.

**નિષ્કર્ષ:** આ commit પર code માં parent ની default મર્યાદા **અમર્યાદ** છે (`agent.max_turns` સેટ કરો તો જ મર્યાદા), અને subagent ની **250**. Docstring અને doc જૂનાં રહી ગયાં છે.

🔬 **Expert નજર.** આ પુસ્તકનો સૌથી કામનો પાઠ કદાચ આ છે: **doc કહે તે દાવો છે; code કરે તે હકીકત છે.** બંને જુદાં પડે ત્યારે expert (1) code ને સાચો માને, (2) ચલાવીને ખાતરી કરે, (3) doc સુધારવાની PR મોકલે. Hermes માં નવા config key કે slash command સાથે docs ફરજિયાત કરતો test (`tests/ci/test_docs_drift.py`) છે — છતાં એક docstring નો આંકડો તેની પહોંચની બહાર રહી ગયો. કોઈ તપાસ સંપૂર્ણ નથી; એટલે વાંચનારની આંખ જોઈએ.

## દૃશ્ય 6 — "રોકાઈ જા!": interrupt

🎬 હર્ષ શાસ્ત્રીજી સાથે ફોન પર છે; જવાબ લાંબો ચાલે છે. સ્મિતાબેન બૂમ પાડે છે: "રોકાઈ જા! પટેલ પરિવારે તારીખ બદલી!" હર્ષ ફોન **કાપી નાખે છે**. શાસ્ત્રીજીનો અડધો જવાબ ફાઈલમાં લખતો નથી.

❓ "અડધો જવાબ પણ કામનો નહોતો?"

"અડધું વાક્ય ફાઈલમાં જાય, તો આગલા ફોનમાં શાસ્ત્રીજી તેને પૂરું સત્ય માની લે."

💻 Agent loop doc ([Interruptible API Calls][doc-loop-lifecycle]) ✅ અને code ([`interruptible_api_call`][interruptible-call]) ✅: HTTP call **background thread** માં ચાલે છે; main thread ત્રણ વસ્તુની રાહ જુએ છે — જવાબ, interrupt, timeout. Interrupt આવે ત્યારે:

- API thread છોડી દેવાય છે; response discard.
- **"No partial response is injected into conversation history."**

Loop ની શરૂઆતમાં `begin_iteration` પણ interrupt તપાસે છે, એટલે બે tools ની વચ્ચે પણ હર્ષ રોકાઈ શકે.

🔬 **Expert નજર.** "Interruptible" Hermes ના છ design principles માંનો એક છે ([architecture][doc-arch-principles]) ✅. જે agent રોકી ન શકાય, તે **વાપરી ન શકાય**: તમે ભૂલ જુઓ અને લાચાર બેસી રહો. અને અડધો જવાબ ન લખવાનો નિયમ પ્રકરણ 4 ના મોટા સિદ્ધાંતનું પહેલું ઉદાહરણ છે: **ફાઈલમાં જે છે, તે જ model માટે સત્ય છે** — એટલે ફાઈલમાં જૂઠું કે અધૂરું કદી ન જવું જોઈએ.

## Source map: આ ક્રમમાં ખોલો

1. [agent/AGENTS.md — Shape][agent-shape] (નકશો)
2. [turn_facade.py — `chat()`][facade-chat] (દરવાજો)
3. [conversation_loop.py — `run_conversation()`][loop-runconv] (turn)
4. [conversation_loop.py — `while`][loop-while] (loop)
5. [conversation_loop.py — tool round કે text][loop-branch] (નિર્ણય)
6. [iteration_budget.py — `IterationBudget`][budget-class] (વાડ)
7. [agent/AGENTS.md — Message-flow invariants][agent-flow-invariants] (નિયમો)

## 🧪 Lab 1 — loop ના ચાર નિયમ, નાના રૂપમાં

[`labs/01-loop/mini_loop.py`](../labs/01-loop/mini_loop.py) આ પ્રકરણનો સંદેશો scripted model સાથે ચલાવે છે: `IterationBudget` ની નકલ, parallel tools, alternation checker.

**પહેલાં ધારો:**

1. `હોલ_તપાસ` 0.3 સેકન્ડ લે છે, `કેટરર_ફોન` 0.1. ફાઈલમાં કયું પરિણામ પહેલું હશે?
2. Budget 2 હોય અને script માં 3 model calls જોઈએ, તો status શું?
3. `consume, consume, refund` પછી budget 3 માંથી કેટલું બાકી?

```bash
python3 labs/01-loop/mini_loop.py
```

અપેક્ષિત output 🧪 ([evidence](../evidence/01-mini-loop.out)):

```text
1) સામાન્ય turn  : completed | model calls: 3
   roles         : system → user → assistant → tool → tool → assistant → tool → assistant
   tool પરિણામ ક્રમ: ['હોલ_તપાસ પૂરું (0.3s)', 'કેટરર_ફોન પૂરું (0.1s)']
   alternation   : બરાબર
2) budget = 2    : budget_exhausted | model calls: 2
3) interrupt     : interrupted | model calls: 1
4) refund        : વપરાયા 2, પાછો 1 → બાકી 2
5) ખોટી ફાઈલ      : ભંગ: સળંગ બે 'user'
```

**વાંચો:** line 1 માં ધીમું tool (0.3s) પહેલું છે, ઝડપી (0.1s) પછી — **મૂળ ક્રમ, પૂરા થવાનો ક્રમ નહીં**. `roles` line માં `tool → tool` સળંગ છે, અને તે એકમાત્ર માન્ય પુનરાવર્તન છે.

**પ્રયોગ.** `run_turn` માં `for f in futures:` ને બદલે `concurrent.futures.as_completed(futures)` વાપરો. Line 1 નો ક્રમ ઊંધો થઈ જશે: આ એ bug છે જેનાથી Hermes નો નિયમ બચાવે છે.

⚠️ આ lab નિયમોની **નકલ** છે, Hermes નો code નથી. ખરા loop માં retries, fallback, streaming અને compression પણ છે.

## 🔮 આગાહી કસોટી

Model એક જ જવાબમાં **ચાર** tool calls આપે છે, અને તેમાંનો એક `clarify` (વપરાશકર્તાને પ્રશ્ન) છે. ચારેય એકસાથે ચાલશે? દૃશ્ય 3 પરથી જવાબ આપો. ([પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch1))

## 🩺 નિષ્ફળતા: "Agent અટક્યા વગર ચાલ્યા જ કરે છે"

**લક્ષણ.** એક સાદા પ્રશ્ન પર agent 60 tool calls કરે છે; બિલ ચડે છે.

**નિદાન.**

1. દૃશ્ય 5: આ commit પર parent ની default મર્યાદા **અમર્યાદ** છે. `config.yaml` માં `agent.max_turns` સેટ કરો.
2. Tool દર વખતે error આપે છે અને model ફરી ફરી એ જ પ્રયત્ન કરે છે? Session માં tool results વાંચો (પ્રકરણ 4).
3. તરત રોકવા: CLI માં `Ctrl+C`, messaging માં `/stop` ([README](https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/README.md)) ⚠️.

**પાઠ.** Budget **સલામતી-જાળ** છે, ઉપાય નથી. ઉપાય એ સમજવું છે કે model દરેક iteration માં **શું જોઈને** આગળ વધ્યો.

## ✅ સાર — ઈશાની નોટબુક

### છ ઘટના, છ નિયમ

| 🎬 ઘટના | 💻 નિયમ | તૂટે તો |
|---|---|---|
| એક કામ, ત્રણ ફોન | Turn ≠ iteration | ખર્ચ ખોટો ગણાય |
| ચિઠ્ઠી કે જવાબ | `tool_calls` → `run_tool_round`, નહીં તો `finish_text_response` | — |
| બે ચિઠ્ઠી એકસાથે | Parallel ચાલે, મૂળ ક્રમમાં નોંધાય | Model પરિણામ ભેળવે |
| બે પ્રશ્ન સળંગ | Strict role alternation | Provider request reject કરે |
| 40 ચક્કર | `IterationBudget`; grace call | અનંત loop |
| "રોકાઈ જા!" | Interrupt; અડધો જવાબ ફાઈલમાં નહીં | Agent બેકાબૂ; history માં જૂઠ |

### નવા શબ્દો

Turn · iteration · `run_conversation` · tool round · inline tool · alternation · iteration budget · grace call · interrupt · docs drift.

### યાદ-ચાવીઓ

- **"1-3-3"**: 1 turn, 3 model calls, 3 tool calls.
- **"ક્રમ માગ્યાનો, પૂરા થયાનો નહીં."**
- **"Doc દાવો, code હકીકત."**

### સામાન્ય ગેરસમજો

| ગેરસમજ | હકીકત |
|---|---|
| "એક પ્રશ્ન = એક model call." | એક turn માં અનેક iterations હોય. |
| "Parallel tools નાં પરિણામ જેમ આવે તેમ લખાય." | મૂળ tool call ક્રમમાં. |
| "Default મર્યાદા 500 છે." | આ commit પર code માં અમર્યાદ; doc જૂનું. |

### પુનરાવર્તન કાર્ડ

| પ્રશ્ન | જવાબ |
|---|---|
| Loop કઈ file માં? | `agent/conversation_loop.py` |
| `chat()` શું પાછું આપે? | `run_conversation(...)["final_response"]` |
| કયો role સળંગ આવી શકે? | ફક્ત `tool` |
| `refund()` કોના માટે? | `execute_code` iterations |
| Interrupt વખતે અડધા જવાબનું શું? | Discard; history માં નહીં |

### મિત્રને સમજાવો (3 મિનિટ)

પહેલાં વાર્તાથી (એક કામ, ત્રણ ફોન, 40 ચક્કર), પછી વાર્તા વગર: turn, iteration, budget, alternation, interrupt.

## 🧠 Mastery check

1. `while` ની ત્રણેય શરતો તમારા શબ્દોમાં લખો. Grace call ન હોત તો વપરાશકર્તાને શું નુકસાન થાત?
2. Cron delivery અલગ session માં કેમ જાય છે? કયો invariant તેને ફરજ પાડે છે?
3. દૃશ્ય 5 ના table પરથી: subagent ની default મર્યાદા કેટલી? તમે **કયા સ્રોત** પર ભરોસો કર્યો, અને કેમ?
4. `mini_loop.py` માં `as_completed` વાપરવાથી કયો નિયમ તૂટે છે?

જવાબો: [પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch1).

## 🎬 આગળ શું

મહિનાના અંતે શાસ્ત્રીજીનું ફોન-બિલ આવે છે: ગયા મહિના કરતાં **બમણું**. કામ તો એટલું જ હતું. સ્મિતાબેન ઈશા સામે જુએ છે. ઈશાને યાદ આવે છે: ગયા અઠવાડિયે તેણે બપોરે સૂચના-પાટી પર "એક નાની લીટી" ઉમેરી હતી…

→ [પ્રકરણ 2 — સૂચના-પાટી: prompt અને cache](02-suchna-pati-prompt-ane-cache.md)
