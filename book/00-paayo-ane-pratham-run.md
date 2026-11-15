# પ્રકરણ 0 — પાયો અને પ્રથમ run

> **Level 0 · વાર્તાનો દિવસ 2.**
> આજે ઈશા Hermes નું **ઘર** જુએ છે: તે ક્યાં install થાય, પોતાનો સામાન ક્યાં રાખે, અને source code માં કયો ઓરડો કોનો છે.
> પહેલાં: [પ્રવેશ](pravesh-shunya-thi-shuruaat.md). આખો નકશો: [સમગ્ર નકશો](overview-samagra-naksho.md).

![~/.hermes નું ઘર: તિજોરી (.env), નોટિસ-બોર્ડ (config.yaml), ઓળખ-કાર્ડ (SOUL.md), ડાયરી, રોજમેળ, રીત-પોથી, એલાર્મ અને કારીગર.](images/chapters/00-paayo-ane-pratham-run.svg)

## 🎯 આ પ્રકરણ પછી તમે શું કરી શકશો

- Hermes install કરી, પહેલી વાતચીત શરૂ કરવાના commands કહી શકશો.
- `~/.hermes` ની દરેક મુખ્ય file નું કામ કહી શકશો, અને "settings ક્યાં, secrets ક્યાં" નો નિયમ સમજાવી શકશો.
- Source ને ચોક્કસ commit પર **pin** કરી શકશો, જેથી આ પુસ્તકની દરેક link તમારા computer પર એ જ line બતાવે.
- "Facade + siblings" ગોઠવણ સમજી, કોઈ પણ function ને `grep` થી શોધી શકશો.

## 🗺️ નકશો

| # | દૃશ્ય | Hermes માં |
|---|---|---|
| 1 | નવો માણસ ઑફિસમાં | Install, `hermes setup`, `hermes doctor` |
| 2 | તિજોરી અને નોટિસ-બોર્ડ | `.env` (secrets) vs `config.yaml` (વર્તન) |
| 3 | "ઑફિસ ક્યાં છે?" | `get_hermes_home()` અને profiles |
| 4 | એ જ દિવસનો ફોટો | Commit pinning |
| 5 | રિસેપ્શન અને અંદરના ઓરડા | Facade + siblings |

---

## દૃશ્ય 1 — નવો માણસ ઑફિસમાં: install અને પહેલી વાત

🎬 હર્ષ જે દિવસે નોકરીએ આવ્યો, સ્મિતાબેને ત્રણ કામ કર્યાં: ટેબલ આપ્યું, શાસ્ત્રીજીનો ફોન નંબર આપ્યો, અને પૂછ્યું "બધું બરાબર ચાલે છે?"

💻 Hermes માં આ ત્રણ commands છે ([README][readme-getting-started]) ✅ ⚠️ (ચલાવ્યા નથી):

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

```bash
hermes setup
```

```bash
hermes doctor
```

- પહેલો command installer ચલાવે છે (Linux, macOS, WSL2). Windows માટે PowerShell નો અલગ one-liner README માં છે.
- `hermes setup` wizard છે: કયો model provider, કઈ API key, કયાં tools.
- `hermes doctor` તપાસે છે કે બધું જોડાયેલું છે.

પછી રોજના commands:

| Command | કામ |
|---|---|
| `hermes` | વાતચીત શરૂ |
| `hermes chat -q "…"` | એક પ્રશ્ન, એક જવાબ, બહાર |
| `hermes model` | Model અને provider પસંદ કરો |
| `hermes tools` | કયાં tools ચાલુ |
| `hermes config set …` | એક setting બદલો |
| `hermes gateway` | Telegram, WhatsApp વગેરેની બારીઓ (પ્રકરણ 6) |

⚠️ **Installer વિશે.** `curl … | bash` internet પરથી script લાવીને ચલાવે છે. Expert તેને પહેલાં **વાંચે** છે. અને Hermes model એ બનાવેલા commands ચલાવી શકે છે; [SECURITY.md](https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/SECURITY.md) પહેલાં વાંચો.

🔬 **Expert નજર.** `hermes chat` terminal ની અંદર agent ચલાવતું **નથી**. Docs કહે છે: classic CLI એક **gateway client** છે; તે profile નો gateway શોધે કે શરૂ કરે, session ત્યાં બનાવે, અને local WebSocket પર જોડાય ([CLI doc][doc-cli-gateway-client]) ✅. Terminal બંધ કરો તો કામ અટકતું નથી. વાર્તામાં: ગ્રાહક ફોન મૂકી દે, તો પણ હર્ષ કામ પૂરું કરે છે. આ વાત પ્રકરણ 6 માં ફરી આવશે.

## દૃશ્ય 2 — તિજોરી અને નોટિસ-બોર્ડ: secrets ક્યાં, settings ક્યાં

🎬 ઈશા નોટિસ-બોર્ડ પર એક ચિઠ્ઠી જુએ છે: "બેંક PIN: 4471". સ્મિતાબેન તરત ફાડી નાખે છે. "PIN **તિજોરીમાં** રહે. બોર્ડ પર ફક્ત કામના નિયમ."

❓ "ફરક શું? બંને ઑફિસની અંદર જ છે."

"બોર્ડનો ફોટો હું કારીગરોને મોકલું છું. તિજોરીનો કદી નહીં."

💻 Hermes માં બરાબર આ બે જગ્યા છે:

| File | શું રહે | વાર્તામાં |
|---|---|---|
| `~/.hermes/.env` | **ફક્ત secrets**: API keys, tokens | તિજોરી |
| `~/.hermes/config.yaml` | **વર્તન**: model, compression, approvals, memory limits… | નોટિસ-બોર્ડ |

Development guide આને કડક નિયમ તરીકે લખે છે: non-secret config માટે નવું `HERMES_*` environment variable ઉમેરવાની PR **reject** થાય છે — "`.env` is secrets only, behaviour goes in `config.yaml`" ([AGENTS.md][agents-rejected]) ✅.

`~/.hermes` ની અંદર બીજું શું છે ([which-file doc][doc-which-file], [memory doc][doc-memory]) ✅:

| Path | કામ | પ્રકરણ |
|---|---|---|
| `SOUL.md` | Agent ની ઓળખ અને બોલવાની રીત; system prompt નો પહેલો ભાગ | 2 |
| `memories/MEMORY.md`, `memories/USER.md` | ખિસ્સા-ડાયરી અને ગ્રાહક-કાર્ડ | 4 |
| `state.db` | દરેક વાતચીત (SQLite) | 4 |
| `skills/` | રીત-પોથી | 5 |
| `cron/jobs.json` | એલાર્મ-ચોપડી | 6 |
| `plugins/` | બહારના કારીગર | 7 |
| `logs/` | Logs (`hermes logs`) | — |

🔬 **Expert નજર.** આ વિભાજન સગવડ નથી, **સુરક્ષા** છે. `config.yaml` તમે મિત્રને મોકલી શકો, bug report માં ચોંટાડી શકો, backup માં મૂકી શકો. `.env` કદી નહીં. જો બંને એક file માં હોત, તો દરેક "મારું config જુઓ" એક key-ચોરીનું જોખમ બનત.

## દૃશ્ય 3 — "ઑફિસ ક્યાં છે?": એક જ જગ્યાએ પૂછો

🎬 શુભમંગલની સુરતમાં નવી શાખા ખૂલી. પહેલા જ અઠવાડિયે ગરબડ: સુરતના કુરિયરવાળાએ વડોદરાના સરનામે કાર્ડ મોકલ્યાં, કારણ કે તેના **મોઢે** વડોદરાનું સરનામું હતું.

સ્મિતાબેનનો નવો નિયમ: "સરનામું કોઈએ મોઢે ન રાખવું. દર વખતે **રજિસ્ટરમાં જુઓ** કે આ કામ કઈ શાખાનું છે."

💻 Hermes માં શાખા = **profile**. દરેક profile નું પોતાનું ઘર છે: પોતાનું config, પોતાની memory, પોતાનો `state.db`. નવી profile ([profiles doc][doc-profiles]) ✅ ⚠️:

```bash
hermes profile create coder
```

અને "રજિસ્ટરમાં જુઓ" નો નિયમ એક function છે — `get_hermes_home()` ([hermes_constants.py][hermes-home]) ✅. Session storage doc તેનો ક્રમ લખે છે ([doc][doc-session-home]) ✅:

1. Context-local override (ચાલુ કામ કઈ profile નું છે),
2. પછી `HERMES_HOME` environment variable,
3. છેલ્લે platform default: `~/.hermes` (Windows પર `%LOCALAPPDATA%/hermes`).

Code માં `~/.hermes` સીધું લખવું lint rule **HX001** થી પકડાય છે: "Never hardcode `~/.hermes`".

🔬 **Expert નજર.** આ નિયમ કેમ આટલો કડક? કારણ કે **એક process અનેક profiles ની સેવા કરી શકે છે** (gateway). Guide કહે છે કે turn ની બહાર ચાલતો code — timers, callbacks, નવા threads — જો profile scope **બાંધે નહીં**, તો તે "silent default-profile leak" છે: સુરતનું કામ ચૂપચાપ વડોદરાના ચોપડામાં લખાઈ જાય. Error નહીં, crash નહીં; ફક્ત **ખોટી જગ્યાએ ડેટા**. સૌથી ખરાબ પ્રકારની bug એ છે જે અવાજ નથી કરતી.

## દૃશ્ય 4 — એ જ દિવસનો ફોટો: commit pinning

🎬 ઈશા મંડપવાળાને ફોન પર કહે છે: "ગયા અઠવાડિયે જોયો તેવો જ મંડપ." મંડપવાળો બીજો જ મંડપ બાંધે છે; ગયા અઠવાડિયા પછી તેણે design બદલી નાખી હતી.

નિખિલમામા: "'ગયા અઠવાડિયા જેવો' ન કહેવાય. **એ દિવસનો ફોટો** મોકલવો પડે."

💻 Source code રોજ બદલાય છે. Hermes માં તો બહુ ઝડપથી. "`run_agent.py` ની line 242" આજે એક વાત છે, કાલે બીજી. એટલે આ પુસ્તક એક ચોક્કસ **commit** પર pinned છે:

```text
18e659dfc93ef319771d51441573e3fa31b8f5b7   (main, 2026-11-15)
```

- **Git** = code ના દરેક ફેરફારનો ઇતિહાસ રાખતું tool.
- **Commit** = એક ક્ષણનો ફોટો; તેનું નામ 40 અક્ષરનો hash.

પુસ્તકની દરેક source link આ hash ધરાવે છે, એટલે તે હંમેશા એ જ line બતાવશે. તમારા computer પર એ જ ફોટો ⚠️:

```bash
git clone https://github.com/NousResearch/hermes-agent.git && cd hermes-agent
```

```bash
git checkout --detach 18e659dfc93ef319771d51441573e3fa31b8f5b7
```

🧪 આ પુસ્તકની 106 citations ને `tools/citations.py` એ આ જ checkout સામે ચકાસી છે: દરેક link ની પહેલી line માં અપેક્ષિત શબ્દસમૂહ ("needle") હાજર છે. પૂર્ણ table: [citations.generated.md](../appendix/citations.generated.md).

🔬 **Expert નજર.** Pinning ફક્ત પુસ્તક માટે નથી. Hermes પોતે પોતાની dependencies ને **exact version** પર pin કરે છે, ranges વગર; `pyproject.toml` ની comment કારણ આપે છે — એક supply-chain હુમલો, જેમાં range હોત તો ખરાબ package આપમેળે install થઈ જાત. સિદ્ધાંત એક જ: **"જે તમે ચકાસ્યું નથી, તે આપમેળે અંદર ન આવવું જોઈએ."**

## દૃશ્ય 5 — રિસેપ્શન અને અંદરના ઓરડા: facade + siblings

🎬 પહેલાં શુભમંગલમાં એક જ મોટો ઓરડો હતો; બધા એક જ ટેબલ પર, અને કોઈ કાગળ જડતો નહોતો. સ્મિતાબેને ઑફિસ ફરી ગોઠવી: આગળ **રિસેપ્શન** — ત્યાં ફક્ત નામની તકતીઓ — અને પાછળ નાના ઓરડા: "કેટરિંગ", "મંડપ", "મહેમાન".

❓ "રિસેપ્શન પર કામ કેમ નથી થતું?"

"રિસેપ્શન કહે છે **કોની પાસે જવું**. કામ ઓરડામાં થાય."

💻 Hermes ની source આ જ રીતે ગોઠવાયેલી છે. Guide તેને **"Facade + siblings layout"** કહે છે ([AGENTS.md][agents-facade]) ✅:

- **Facade** = રિસેપ્શન: public entry points અને બીજા packages જે નામ import કરે છે.
- **Siblings** = ઓરડા: `<stem>_<topic>.py`, દરેક એક વિષયનો માલિક.

ઉદાહરણ: `hermes_state.py` facade છે; તેની બાજુમાં `hermes_state_schema.py`, `hermes_state_fts.py`, `hermes_state_search.py` અને બીજા ડઝનો siblings છે. `run_agent.py` માં `AIAgent` class છે ([run_agent.py][aiagent-class]) ✅, પણ loop `agent/conversation_loop.py` અને `agent/turn_*.py` માં રહે છે ([agent/AGENTS.md][agent-shape]) ✅.

**Load-bearing entry points** — પહેલા દિવસે આટલાં નામ પૂરતાં:

| File | ભૂમિકા | વાર્તામાં |
|---|---|---|
| `run_agent.py` | `AIAgent` facade | હર્ષ |
| `agent/conversation_loop.py`, `agent/turn_*.py` | Turn loop અને તેના તબક્કા | હર્ષનો દિવસ |
| `agent/system_prompt.py`, `agent/prompt_builder.py` | System prompt | સૂચના-પાટી |
| `model_tools.py`, `tools/registry.py`, `toolsets.py` | Tools | ઓજાર-કબાટ અને થેલા |
| `hermes_state.py` + siblings | Session DB | રોજમેળ |
| `gateway/` | Messaging gateway | બારીઓ |
| `cron/` | Scheduler | એલાર્મ-ચોપડી |
| `plugins/`, `skills/` | Extensions | કારીગર, રીત-પોથી |

**શોધવાની રીત.** Guide ની સલાહ: facade વાંચીને નહીં, **વિષયથી શોધો** ⚠️:

```bash
grep -rn "def build_system_prompt" agent/
```

દરેક મોટા વિસ્તારની પોતાની `AGENTS.md` છે (`agent/AGENTS.md`, `tools/AGENTS.md`, `gateway/AGENTS.md`…), અને root `AGENTS.md` માં routing table છે કે કયા folder માટે કઈ વાંચવી.

🔬 **Expert નજર.** Size પર **ratchet** છે: નવા function ની cyclomatic complexity ≤ 20, ≤ 300 lines; files ≤ 2,000 lines; જે પહેલેથી મોટાં છે તે ફક્ત **ઘટી** શકે. એક વ્યવહારુ ફાંસો પણ લખેલો છે: sibling function ની અંદર `from <facade> import name` કરે છે, એટલે test માં patch **facade પર** કરવો પડે — "patch where production reads". Defining module પર કરેલો patch "passes silently": test લીલો, પણ કંઈ ચકાસ્યું નથી.

## Source map: આ ક્રમમાં ખોલો

1. [README — Getting Started][readme-getting-started]
2. [AGENTS.md — બે invariants][agents-invariants]
3. [AGENTS.md — Facade + siblings][agents-facade]
4. [hermes_constants.py — `get_hermes_home()`][hermes-home]
5. [Architecture doc — System Overview][doc-architecture]
6. [Architecture doc — Design Principles][doc-arch-principles]

## 🧪 Lab 0 — ઘર ઓળખો (Hermes install વગર પણ)

**ભાગ A — પુસ્તકની labs ચાલે છે?** 🧪

```bash
bash labs/run-all.sh
```

છેલ્લી line: `બધી labs પાસ.` આ command આઠેય labs ચલાવે છે અને outputs `evidence/` માં લખે છે.

**ભાગ B — pinned source વાંચો.** Hermes clone કરીને pin કરો (દૃશ્ય 4), પછી **પહેલાં ધારો, પછી ચલાવો** ⚠️:

```bash
ls hermes_state*.py | wc -l
```

```bash
grep -c "" AGENTS.md
```

પહેલો command `hermes_state` facade ના siblings ગણે છે (ધારો: 5? 20? 60?). બીજો root `AGENTS.md` ની lines ગણે છે; guide કહે છે કે આ file 12k અક્ષરથી મોટી ન થવા દેવાય. કેમ? કારણ કે આ file દરેક AI coding session માં context તરીકે લોડ થાય છે — **પ્રકરણ 2 નો નિયમ, પોતાના પર લાગુ**.

**ભાગ C — Hermes હોય તો** ⚠️: `hermes doctor` ચલાવો અને output ની દરેક line ને ઉપરના `~/.hermes` table સાથે જોડો.

## 🔮 આગાહી કસોટી

તમે `HERMES_HOME=/tmp/test-home hermes chat -q "hi"` ચલાવો છો. નવી `state.db` ક્યાં બનશે: `~/.hermes/state.db` કે `/tmp/test-home/state.db`? દૃશ્ય 3 ના ક્રમ પરથી જવાબ આપો. (જવાબ: [પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch0))

## 🩺 નિષ્ફળતા: "મેં key નાખી, છતાં 'no credentials'"

**લક્ષણ.** `config.yaml` માં `api_key: sk-…` લખ્યું; Hermes કહે છે credentials નથી.

**નિદાન.** દૃશ્ય 2: secrets ની જગ્યા `.env` છે. `hermes setup` કે `hermes model` key ને સાચી જગ્યાએ મૂકે છે. અને બીજું શક્ય કારણ દૃશ્ય 3: તમે બીજી **profile** માં છો, જેની `.env` અલગ છે.

**પાઠ.** "Setting લાગુ ન પડ્યું" નો પહેલો પ્રશ્ન: **કઈ file, કઈ profile?**

## ✅ સાર — ઈશાની નોટબુક

### પાંચ ઘટના, પાંચ નિયમ

| 🎬 ઘટના | 💻 નિયમ |
|---|---|
| નવા માણસને ટેબલ, નંબર, તપાસ | install → `hermes setup` → `hermes doctor` |
| PIN બોર્ડ પરથી ફાડ્યો | `.env` = secrets; `config.yaml` = વર્તન |
| કુરિયર ખોટી શાખાએ | `get_hermes_home()`; કદી hardcode નહીં |
| "ગયા અઠવાડિયા જેવો મંડપ" | Commit pin: `18e659d` |
| રિસેપ્શન અને ઓરડા | Facade + siblings; વિષયથી `grep` |

### નવા શબ્દો

Profile · `HERMES_HOME` · commit · pin · facade · sibling · lint rule · ratchet.

### યાદ-ચાવી

**"તિજોરી – બોર્ડ – રજિસ્ટર – ફોટો – રિસેપ્શન"** = `.env` – `config.yaml` – `get_hermes_home()` – commit – facade.

### સામાન્ય ગેરસમજો

| ગેરસમજ | હકીકત |
|---|---|
| "Hermes હંમેશા `~/.hermes` વાપરે." | Profile અને `HERMES_HOME` પ્રમાણે બદલાય. |
| "`run_agent.py` માં agent નો બધો logic છે." | તે facade છે; loop `agent/` માં છે. |
| "Terminal બંધ કરું તો agent અટકે." | CLI gateway client છે; સ્વીકારેલું કામ gateway પર ચાલુ રહે. |

## 🧠 Mastery check

1. `.env` અને `config.yaml` એક file કેમ નથી? **સુરક્ષા** નું કારણ એક વાક્યમાં.
2. Root `AGENTS.md` પર 12k અક્ષરની મર્યાદા કેમ છે?
3. Test માં તમે `agent/turn_api_call.py` ના function ને patch કર્યો; test પાસ થયો, પણ production bug રહી ગઈ. Guide નો કયો નિયમ તૂટ્યો?

જવાબો: [પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch0).

## 🎬 આગળ શું

ઈશા: "ઘર જોઈ લીધું. હવે હર્ષને **કામ કરતો** જોવો છે. એક સંદેશો આવે, પછી અંદર શું થાય?"

"કાલે એક સંદેશાની પાછળ પાછળ ચાલીશું, દરવાજાથી જવાબ સુધી." → [પ્રકરણ 1 — એક સંદેશાની આખી મુસાફરી](01-ek-sandesh-ni-musafari.md)

<!-- refs:start (generated by tools/citations.py) -->
[agent-shape]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/agent/AGENTS.md#L5-L20
[agents-facade]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/AGENTS.md#L94-L109
[agents-invariants]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/AGENTS.md#L16-L25
[agents-rejected]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/AGENTS.md#L43-L49
[aiagent-class]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/run_agent.py#L215
[doc-arch-principles]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/architecture.md#L260-L270
[doc-architecture]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/architecture.md#L11-L14
[doc-cli-gateway-client]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/cli.md#L175-L177
[doc-memory]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/features/memory.md#L11-L20
[doc-profiles]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/profiles.md#L48
[doc-session-home]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/session-storage.md#L16-L31
[doc-which-file]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/which-file-does-what.md#L11-L24
[hermes-home]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/hermes_constants.py#L206-L211
[readme-getting-started]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/README.md#L107-L119
<!-- refs:end -->
