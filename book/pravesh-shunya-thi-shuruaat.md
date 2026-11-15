# પ્રવેશ — શૂન્યથી શરૂઆત

> **Level −1 · વાર્તાનો દિવસ 1.**
> આ પ્રકરણ એવા વાચક માટે છે જેણે કદી programming કર્યું નથી. અંતે તમે 45 line નો એક **રમકડા-agent** ચલાવશો અને સમજશો કે Hermes જેવું મોટું agent અંદરથી આ જ વસ્તુ છે.
> આખો નકશો: [સમગ્ર નકશો](overview-samagra-naksho.md).

## 🎯 આ પ્રકરણ પછી તમે શું કરી શકશો

- Terminal ખોલીને file જોઈ, program ચલાવી શકશો.
- JSON અને YAML વાંચી શકશો; Hermes ની settings આ બે ભાષામાં છે.
- "Model", "API", "token", "tool call" અને "agent" નો તફાવત એક-એક વાક્યમાં કહી શકશો.
- `labs/pravesh/toy_agent.py` ચલાવી, તેનું output પહેલેથી ધારી શકશો.

## 🗺️ નકશો

| # | દૃશ્ય | નવો વિચાર |
|---|---|---|
| 1 | ઑફિસનું કબાટ | File, folder, path |
| 2 | બોલીને કામ | Terminal અને command |
| 3 | ફોર્મ ભરવાની બે રીત | JSON અને YAML |
| 4 | કાશીનો ફોન | Model, API, token |
| 5 | ચિઠ્ઠી | Tool call |
| 6 | હર્ષનો દિવસ | Agent loop — 45 line માં |

---

## દૃશ્ય 1 — ઑફિસનું કબાટ: file, folder, path

🎬 પહેલા દિવસે નિખિલમામા ઈશાને ઑફિસનું લોખંડનું કબાટ બતાવે છે. ઉપરના ખાનામાં "2026", તેમાં "પટેલ-લગ્ન" નામનું ફોલ્ડર, તેમાં "મહેમાન-યાદી" નામનો કાગળ.

❓ "મામા, computer માં પણ આવું જ હોય?"

💻 બરાબર આવું જ.

- **File** = એક કાગળ. ઉદાહરણ: `rsvp.csv`.
- **Folder** (directory) = ફોલ્ડર, જેમાં files અને બીજાં folders હોય.
- **Path** = કાગળ સુધી પહોંચવાનો રસ્તો. ઉદાહરણ: `labs/07-plugin/fixtures/rsvp.csv` એટલે "`labs` માં, `07-plugin` માં, `fixtures` માં, `rsvp.csv`".
- **Home directory** = તમારું પોતાનું ખાનું; ટૂંકમાં `~` લખાય. Hermes પોતાનો બધો સામાન `~/.hermes` માં રાખે છે (પ્રકરણ 0).

નામની શરૂઆતમાં ટપકું (`.hermes`) હોય તે folder સામાન્ય રીતે છુપાયેલું રહે છે: settings માટેનો રિવાજ.

🔬 **Expert નજર.** Software ની અડધી ભૂલો "ખોટો કાગળ વાંચ્યો" પ્રકારની હોય છે. Expert કોઈ પણ વર્તન જોઈને પહેલાં પૂછે છે: **"આ કઈ file માંથી આવ્યું?"** Hermes ના developers આ પ્રશ્નને એટલો ગંભીર ગણે છે કે code માં `~/.hermes` સીધું લખવાની મનાઈ છે; દરેક જગ્યાએ એક જ function પૂછવું પડે છે (પ્રકરણ 0, દૃશ્ય 3).

## દૃશ્ય 2 — બોલીને કામ: terminal

🎬 સ્મિતાબેન હર્ષને કામ આંગળી ચીંધીને નથી બતાવતાં; **બોલીને** કહે છે: "પટેલની ફાઈલ લાવ." ટૂંકું, ચોક્કસ.

💻 **Terminal** એ computer સાથે બોલીને કામ કરવાની બારી છે. તમે એક line લખો (**command**), Enter દબાવો, computer જવાબ લખે.

```bash
pwd
```

```bash
ls
```

```bash
python3 --version
```

- `pwd` = "હું અત્યારે કયા folder માં છું?"
- `ls` = "અહીં શું શું છે?"
- `python3 --version` = "Python નો કયો version છે?" આ પુસ્તકની labs Python 3.11 કે નવા પર ચાલે છે. 🧪 (લખતી વખતે: `Python 3.13.18`)

Command પૂરો થાય ત્યારે એક **exit code** આપે: `0` એટલે "બરાબર", બીજું કંઈ પણ એટલે "ગરબડ".

🔬 **Expert નજર.** Agent માટે terminal સૌથી શક્તિશાળી ઓજાર છે: જે તમે terminal માં કરી શકો, તે agent પણ કરી શકે. એટલે જ સૌથી જોખમી પણ. Hermes ના `terminal` tool ની આગળ એક આખી સુરક્ષા-ચોકી છે (પ્રકરણ 3).

## દૃશ્ય 3 — ફોર્મ ભરવાની બે રીત: JSON અને YAML

🎬 ઑફિસમાં બુકિંગ-ફોર્મ બે જાતનાં છે. એક છાપેલું, ખાનાંવાળું, કડક — મશીન માટે. બીજું હાથે લખેલી નોંધ જેવું — માણસ માટે.

💻 **JSON** કડક ફોર્મ છે. Programs એકબીજા સાથે આ ભાષામાં વાત કરે છે:

```json
{"event": "lagna", "plates": 450, "confirmed": true, "dishes": ["દાળ", "ભાત"]}
```

- `{ }` = એક વસ્તુ (object), `"નામ": કિંમત` ની જોડીઓ સાથે.
- `[ ]` = યાદી (list).
- લખાણ હંમેશા `"…"` માં; આંકડા અને `true`/`false` અવતરણ વગર.

**YAML** એ જ માહિતી, માણસને વાંચવી સહેલી પડે તે રીતે. Hermes ની settings (`config.yaml`) YAML માં છે:

```yaml
compression:
  enabled: true
  threshold: 0.50
```

YAML માં **ખાલી જગ્યા (indentation) જ બંધારણ છે**. `threshold` બે જગ્યા અંદર છે, એટલે તે `compression` ની અંદર છે.

🔬 **Expert નજર.** Model અને agent વચ્ચેની દરેક વાત JSON છે: model "આ tool ચલાવો" કહે તે JSON, tool નું પરિણામ JSON. Hermes ના દરેક tool handler નો પહેલો નિયમ: **"હંમેશા JSON string પાછી આપો, ભૂલ હોય તો પણ"** ([plugin guide][doc-plugin-handlers]) ✅. કેમ? કારણ કે બીજી બાજુ વાંચનાર માણસ નથી, program છે; તે અધૂરું ફોર્મ વાંચી શકતો નથી.

## દૃશ્ય 4 — કાશીનો ફોન: model, API, token

🎬 બપોરે હર્ષ શાસ્ત્રીજીને ફોન કરે છે. ઈશા સાંભળે છે: હર્ષ **આખી ફાઈલ** શરૂઆતથી વાંચે છે, પછી પ્રશ્ન પૂછે છે. શાસ્ત્રીજી જવાબ આપે છે. ફોન મુકાય છે.

દસ મિનિટ પછી બીજો ફોન. હર્ષ **ફરી આખી ફાઈલ** વાંચે છે.

❓ "હમણાં તો વાંચી હતી! ફરી કેમ?"

નિખિલમામા: "કારણ કે શાસ્ત્રીજી ફોન મૂકતાં જ બધું ભૂલી જાય છે. તેમની પાસે કોઈ ચોપડો નથી. જે યાદ છે તે હર્ષની ફાઈલમાં છે."

💻 આ AI model નું સાચું વર્ણન છે.

- **Model (LLM)** = એક program જે text વાંચીને આગળનું text લખે. તે **stateless** છે: બે calls વચ્ચે કંઈ યાદ રાખતું નથી.
- **API** = model સાથે વાત કરવાનો "ફોન નંબર". તમારો program internet પર એક request મોકલે; model કંપનીનું server જવાબ મોકલે.
- **API key** = તમારી ઓળખ અને બિલનું ખાતું. ગુપ્ત રાખવાની; Hermes માં તે `.env` file માં રહે છે, settings માં કદી નહીં.
- **Token** = model માટે text નો નાનો ટુકડો (લગભગ અડધો-પોણો શબ્દ). **બિલ token પ્રમાણે આવે**: જેટલું મોકલો (input) અને જેટલું મળે (output).
- **Context window** = એક ફોનમાં વધુમાં વધુ કેટલા tokens સમાય. ફાઈલ આનાથી જાડી થાય તો ફોન થાય જ નહીં.

Model "યાદ રાખતું" લાગે છે તેનું કારણ: **દરેક call માં આખો history ફરી મોકલાય છે.**

🔬 **Expert નજર.** આ એક હકીકતમાંથી ત્રણ મોટી વાતો નીકળે છે, અને તે આખા પુસ્તકના ત્રણ ભાગ છે:

1. History દર વખતે જાય → લાંબી વાતચીત **મોંઘી** → cache જોઈએ (પ્રકરણ 2).
2. History context window માં સમાવો જોઈએ → **compression** જોઈએ (પ્રકરણ 4).
3. Model પોતે કંઈ યાદ ન રાખે → **memory** agent એ બહાર રાખવી પડે (પ્રકરણ 4, 5).

## દૃશ્ય 5 — ચિઠ્ઠી: tool call

🎬 હર્ષ પૂછે છે: "પટેલ પરિવારના લગ્નમાં કેટલા પ્રસંગ છે?" શાસ્ત્રીજી જવાબ નથી આપતા. કહે છે: **"પહેલાં પ્રસંગ-યાદી લાવ."** હર્ષ ફોન મૂકે, કબાટમાંથી યાદી લાવે, ફરી ફોન કરે, યાદી વાંચે. હવે શાસ્ત્રીજી કહે: "પાંચ પ્રસંગ છે."

❓ "શાસ્ત્રીજી પોતે કેમ જોઈ નથી લેતા?"

"તે કાશીમાં છે. આપણા કબાટને અડી શકતા નથી. તે ફક્ત બે કામ કરી શકે: **જવાબ આપવો**, અથવા **'આ લાવ' કહેવું**."

💻 Model file વાંચી શકતું નથી, command ચલાવી શકતું નથી, internet ખોલી શકતું નથી. તે ફક્ત text આપે છે. પણ એ text ક્યારેક એક ખાસ JSON હોય છે: **"આ નામનું tool, આ arguments સાથે ચલાવો."** આને **tool call** કહેવાય. Tool ખરેખર ચલાવે છે **agent**.

Agent model ને દરેક call સાથે **tools ની યાદી** પણ મોકલે છે: દરેકનું નામ, વર્ણન અને કયા arguments લે છે (**schema**). Model એ વર્ણન વાંચીને નક્કી કરે છે કે કયું tool માગવું.

🔬 **Expert નજર.** યાદી **દરેક call માં** જાય છે. 70 tools હોય તો 70 વર્ણનના tokens દરેક ફોનમાં. Hermes ની બીજી invariant — "core is a narrow waist" — આ એક વાક્યમાંથી જન્મે છે ([AGENTS.md][agents-invariants]) ✅.

## દૃશ્ય 6 — હર્ષનો દિવસ: agent loop, 45 line માં

🎬 સાંજે નિખિલમામા કાગળ પર હર્ષના આખા દિવસનું કામ ત્રણ લીટીમાં લખે છે:

1. આખી ફાઈલ લઈને શાસ્ત્રીજીને ફોન કર.
2. જવાબ મળ્યો? → ગ્રાહકને આપ. પૂરું.
3. ચિઠ્ઠી મળી? → ઓજાર ચલાવ, પરિણામ ફાઈલમાં લખ, **પાછો 1 પર જા**.

"બસ. આને **agent loop** કહેવાય. Hermes માં હજારો lines છે, પણ હૃદય આ ત્રણ લીટી છે."

💻 **Book lab code** — [`labs/pravesh/toy_agent.py`](../labs/pravesh/toy_agent.py) નો મુખ્ય ભાગ:

```python
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
```

ચાર **roles** યાદ રાખો; Hermes પણ આ જ ચાર વાપરે છે ([agent loop doc][doc-loop-lifecycle]) ✅:

| Role | વાર્તામાં | કોણ લખે |
|---|---|---|
| `system` | સૂચના-પાટી | Agent, શરૂઆતમાં એક વાર |
| `user` | ગ્રાહકનો સંદેશો | વપરાશકર્તા |
| `assistant` | શાસ્ત્રીજીનો જવાબ કે ચિઠ્ઠી | Model |
| `tool` | ઓજારનું પરિણામ | Agent, tool ચલાવ્યા પછી |

⚠️ **વાર્તા અને ખરું વર્તન.** આ lab માં `shastriji()` ખરું model નથી; scripted function છે, જેથી API key વગર ચાલે. ખરા agent માં આ જગ્યાએ internet પર API call હોય.

### 🧪 Lab −1: રમકડા-agent ચલાવો

**પહેલાં ધારો** (કાગળ પર લખો): model કેટલી વાર બોલાવાશે? `messages` માં roles કયા ક્રમમાં હશે?

```bash
python3 labs/pravesh/toy_agent.py
```

અપેક્ષિત output 🧪 ([evidence](../evidence/pravesh-toy-agent.out)):

```text
roles: system → user → assistant → tool → assistant
modelCalls: 2
જવાબ: પટેલ પરિવારના લગ્નમાં 5 પ્રસંગ છે.
```

**એક પ્રશ્ન, બે model calls.** પહેલા call માં model એ tool માગ્યું; બીજામાં, પરિણામ હાથમાં આવ્યા પછી, જવાબ આપ્યો.

**પ્રયોગ.** `MENU` માં `"ગરબા"` ઉમેરો અને ફરી ચલાવો. જવાબ બદલાયો, પણ `modelCalls` નહીં. કેમ? કારણ કે model ને ડેટા **tool મારફતે** મળે છે; model ની અંદર કંઈ બદલાયું નથી.

## ✅ સાર — ઈશાની નોટબુકનું પહેલું પાનું

### છ ઘટના, છ વિચાર

| 🎬 ઘટના | 💻 વિચાર |
|---|---|
| કબાટ → ફોલ્ડર → કાગળ | Path કહે છે કે માહિતી ક્યાંથી આવી |
| બોલીને કામ | Terminal: command, output, exit code |
| બે જાતનાં ફોર્મ | JSON મશીન માટે, YAML settings માટે |
| દરેક ફોનમાં આખી ફાઈલ | Model stateless; history દર વખતે જાય |
| "પહેલાં યાદી લાવ" | Tool call: model માગે, agent ચલાવે |
| ત્રણ લીટીનો દિવસ | Agent loop |

### યાદ-ચાવી

**"ફોન – ચિઠ્ઠી – ઓજાર – ફરી ફોન."** Agent આટલું જ છે. બાકીનું બધું — cache, memory, skills, gateway — આ ચાર શબ્દોને **સસ્તા, સલામત અને યાદશક્તિવાળા** બનાવવાની કળા છે.

### સામાન્ય ગેરસમજો

| ગેરસમજ | હકીકત |
|---|---|
| "Model ને ગઈ વાતચીત યાદ છે." | ના. Agent દર વખતે આખો history મોકલે છે. |
| "Model file વાંચે છે." | ના. Model tool માગે છે; agent વાંચીને પરિણામ મોકલે છે. |
| "Agent એટલે બુદ્ધિશાળી model." | Agent = model + loop + tools + memory. Model એ ફક્ત એક ભાગ. |

### મિત્રને સમજાવો (2 મિનિટ)

પહેલાં વાર્તાથી: "કાશીમાં એક પંડિત છે જે ફોન મૂકતાં જ ભૂલી જાય…" પછી વાર્તા વગર: "LLM stateless છે; agent loop history અને tools સંભાળે છે."

## 🧠 Mastery check

1. `toy_agent.py` માં `messages` ની છેલ્લી entry નો role `tool` હોય ત્યારે `shastriji()` શું કરે છે, અને કેમ?
2. એક વાતચીતમાં 10 turns થયા. દસમા turn ના પહેલા model call માં કેટલા turns નો history જાય છે?
3. Tool handler exception ફેંકે અને agent તેને પકડે નહીં, તો loop નું શું થાય? (જવાબ પ્રકરણ 3 માં ચકાસશો.)

જવાબો: [પરિશિષ્ટ D](../appendix/D-lab-solutions.md#pravesh).

## 🎬 આગળ શું

રાત્રે ઈશા પૂછે છે: "મામા, આ રમકડું તો સમજાયું. પણ ખરો હર્ષ — Hermes — ક્યાં રહે છે? તેનો સામાન ક્યાં છે?"

"કાલે તેનું ઘર જોઈશું." → [પ્રકરણ 0 — પાયો અને પ્રથમ run](00-paayo-ane-pratham-run.md)
