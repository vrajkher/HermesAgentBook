# પ્રકરણ 6 — બારીઓ, ઘડિયાળ અને શિખાઉ

> **Level 6 · વાર્તાનો દિવસ 11–12.**
> આજનો પ્રશ્ન: **"એક હર્ષ અનેક જગ્યાએ, અનેક સમયે, અનેક હાથે કેવી રીતે?"**
> ત્રણ જવાબ: **gateway** (અનેક જગ્યા), **cron** (અનેક સમય), **delegation** (અનેક હાથ). ત્રણેયમાં agent core એ જ રહે છે.
> પહેલાં: [પ્રકરણ 5](05-reet-pothi-skills.md). આખો નકશો: [સમગ્ર નકશો](overview-samagra-naksho.md).

## 🎯 આ પ્રકરણ પછી તમે શું કરી શકશો

- Platform પરથી આવેલા સંદેશાનો gateway માં રસ્તો — authorize → session key → agent → delivery — કહી શકશો.
- Authorization નો ક્રમ અને "default: deny" સમજાવી શકશો.
- Cron job નું જીવન અને "at-most-once" ની ગોઠવણ સમજાવી શકશો.
- Subagent ને શું મળે, શું ન મળે, અને parent ને શું પાછું મળે તે કહી શકશો.

## 🗺️ નકશો

| # | દૃશ્ય | Hermes માં |
|---|---|---|
| 1 | ત્રણ બારી, એક હર્ષ | Gateway; platform adapters; platform-agnostic core |
| 2 | રઘુકાકા | User authorization; default deny |
| 3 | કોની ફાઈલ? | Session key |
| 4 | હર્ષ વ્યસ્ત છે | બે message guards; `/stop` |
| 5 | એલાર્મ-ચોપડી | Cron |
| 6 | લાઈટ ગઈ | At-most-once; watchdog |
| 7 | શિખાઉ | `delegate_task`; isolated context |

---

## દૃશ્ય 1 — ત્રણ બારી, એક હર્ષ: gateway

🎬 શુભમંગલની ત્રણ બારી છે: સામે **કાઉન્ટર**, બાજુમાં **WhatsApp** નો ફોન, અને **Telegram** વાળું ટેબ્લેટ. પહેલાં દરેક બારી પર અલગ માણસ હતો, અને દરેક ગ્રાહકને જુદો જવાબ મળતો.

હવે દરેક બારી પર ફક્ત એક **કારકુન** છે, જે બે જ કામ કરે: સંદેશો એક સરખા ફોર્મમાં ઉતારીને અંદર મોકલે, અને જવાબ એ બારીની રીતે બહાર આપે. અંદર **એક જ હર્ષ**: એ જ ડાયરી, એ જ પોથી, એ જ કબાટ.

💻 **Gateway** = લાંબો સમય ચાલતી process, જે 25+ platforms સાથે જોડાય અને દરેક સંદેશાને એ જ `AIAgent` પાસે લઈ જાય ([architecture][doc-architecture]) ✅:

```text
Platform event → Adapter.on_message() → MessageEvent
  → GatewayRunner._handle_message()
    → authorize user
    → resolve session key
    → create AIAgent with session history
    → AIAgent.run_conversation()
    → deliver response back through adapter
```

- **Adapter** = બારીનો કારકુન. Platform ની ભાષા ↔ Hermes નું સામાન્ય `MessageEvent`.
- Bundled platform plugins: Telegram, Discord, Slack, WhatsApp, Signal, Matrix, email, SMS અને બીજા (`plugins/platforms/`).

Design principle ([link][doc-arch-principles]) ✅: **"Platform-agnostic core — One AIAgent class serves CLI, gateway, ACP, batch, and API server. Platform differences live in the entry point, not the agent."**

અને પ્રકરણ 0 ની વાત અહીં પૂરી થાય છે: `hermes chat` પણ એક બારી છે. CLI gateway નો **client** છે ([link][doc-cli-gateway-client]) ✅; terminal બંધ કરો તો "Detached; accepted work continues at the gateway."

🔬 **Expert નજર.** આ ફરી narrow waist છે, બીજા ખૂણેથી: N platforms અને M ક્ષમતાઓ હોય, તો સીધા જોડાણમાં N×M code જોઈએ; વચ્ચે એક સામાન્ય ફોર્મ (`MessageEvent`) હોય તો N+M. નવું platform ઉમેરવા agent ને અડવું પડતું નથી; નવી ક્ષમતા ઉમેરવા adapters ને અડવું પડતું નથી. Guide તેને નિયમ બનાવે છે: platform ના ખાસ વર્તન માટે core માં "name check" નહીં; plugin જાતે `PlatformEntry` પર ગુણધર્મ સેટ કરે.

## દૃશ્ય 2 — રઘુકાકા: default deny

🎬 એક રાત્રે અજાણ્યા નંબર પરથી WhatsApp આવે છે: "પટેલ લગ્નનું બુકિંગ રદ કરો અને advance પાછું મોકલો." હર્ષ કામ શરૂ કરવા જાય છે.

ચોકીદાર **રઘુકાકા** રોકે છે. તેમની પાસે એક યાદી છે, અને એક ક્રમ:

1. આ બારી બધા માટે ખુલ્લી જાહેર કરી છે?
2. આ માણસ પાસે સ્મિતાબેને આપેલી **ઓળખ-પરચી** છે?
3. આ બારીની યાદીમાં નામ છે?
4. ઑફિસની સામાન્ય યાદીમાં નામ છે?
5. આખી ઑફિસ બધા માટે ખુલ્લી જાહેર કરી છે?
6. **નહીં તો: ના.**

💻 શબ્દશઃ એ જ ક્રમ ([Authorization Check Order][doc-security-authz]) ✅ — `_is_user_authorized()` ([authz_mixin.py][gateway-authz]) ✅:

1. Per-platform allow-all flag (દા.ત. `DISCORD_ALLOW_ALL_USERS=true`)
2. **DM pairing** approved list (pairing code થી મંજૂર)
3. Platform allowlist (દા.ત. `TELEGRAM_ALLOWED_USERS=12345,67890`)
4. Global allowlist (`GATEWAY_ALLOWED_USERS`)
5. Global allow-all (`GATEWAY_ALLOW_ALL_USERS=true`)
6. **Default: deny**

Allowlists `~/.hermes/.env` માં રહે છે: તે ઓળખની વાત છે, એટલે તિજોરીમાં.

🔬 **Expert નજર.** તમારા agent પાસે terminal છે. જે તેને સંદેશો મોકલી શકે, તે **તમારા computer પર command ચલાવી શકે**. એટલે authorization security નું **પહેલું** સ્તર છે (પ્રકરણ 3 ના આઠમાંનું #1), અને default "ના" છે. "Default allow" વાળી system માં ભૂલી જવું = ખુલ્લું; "default deny" માં ભૂલી જવું = બંધ. **ભૂલ થાય ત્યારે કઈ બાજુ પડવું, તે પહેલેથી નક્કી કરો.** અને એક પૂરક નિયમ gateway guide માં: user content INFO+ logs માં **કદી નહીં** — logs `hermes debug share` થી બહાર જાય છે; body ને બદલે `len(text)` કે hash લખો.

## દૃશ્ય 3 — કોની ફાઈલ?: session key

🎬 પટેલ કાકા Telegram પર પૂછે છે: "મારું શું થયું?" એ જ ક્ષણે શાહ કાકી WhatsApp પર: "મારું શું થયું?" હર્ષ બંનેને **એક જ ફાઈલ** માંથી જવાબ આપી દે, તો? પટેલનું બજેટ શાહને.

નિયમ: દરેક ફાઈલ પર એક **લેબલ**: કઈ બારી, કેવી વાત (અંગત કે જૂથ), કોણ.

💻 **Session key** ([gateway internals][doc-gateway-key]) ✅:

```text
agent:{namespace}:{platform}:{chat_type}:{chat_id}
```

ઉદાહરણ: `agent:main:telegram:private:123456789`. `namespace` default profile માટે `main`; multiplexing માં profile નું નામ.

Doc ની ચેતવણી: **"Never construct session keys manually"** — હંમેશા `build_session_key()` ([session.py][gateway-session-key]) ✅. કેમ? Thread-aware platforms (Telegram forum topics, Discord/Slack threads) chat_id ભાગમાં thread id ઉમેરે છે, અને નિયમો platform પ્રમાણે જુદા છે. હાથે બનાવેલી key એક કિસ્સો ચૂકે, અને બે વાતચીત ભળી જાય.

⚠️ Session key (gateway ની: "આ chat કોની?") અને session id (`state.db` ની: "આ transcript કઈ?") જુદી વસ્તુ છે. `/new` પછી key એ જ રહે, session id નવી.

🔬 **Expert નજર.** "હાથે ન બનાવો; એક function વાપરો" આ પુસ્તકમાં ત્રીજી વાર આવ્યું: `get_hermes_home()` (પ્રકરણ 0), `registry.register()` (પ્રકરણ 3), `build_session_key()`. નમૂનો: **જે વસ્તુના નિયમો ઝીણા હોય અને ભૂલનું પરિણામ ચૂપ હોય, તેને બનાવવાની એક જ જગ્યા રાખો.** Cross-session isolation security નું સાતમું સ્તર છે; તેની ચાવી આ એક string છે.

## દૃશ્ય 4 — હર્ષ વ્યસ્ત છે: બે ચોકી અને `/stop`

🎬 હર્ષ પટેલ કાકાનું કામ કરે છે (ફોન 2 ચાલુ). કાકા ત્રણ સંદેશા મોકલે છે:

1. "અને કેટરર પણ જો." → કારકુન **કતારમાં** મૂકે; હર્ષ હાલનું કામ પૂરું કરીને લેશે.
2. "હા, મંજૂર." (હર્ષે પૂછેલી મંજૂરીનો જવાબ) → આ કતારમાં જાય, તો હર્ષ **કાયમ રાહ જુએ**: તે મંજૂરી વગર આગળ વધી શકતો નથી, અને મંજૂરી તેની પાછળ કતારમાં છે!
3. "રોકાઈ જા!" → આ પણ કતારમાં જાય, તો નકામું.

💻 Gateway guide નું શીર્ષક પોતે નિયમ છે ([link][gateway-guards]) ✅: **"The gateway has TWO message guards — both must bypass approval/control commands."**

Agent ચાલતો હોય ત્યારે આવતો સંદેશો બે ચોકીમાંથી પસાર થાય:

1. **Base adapter** — session active હોય તો સંદેશો `_pending_messages` માં કતારમાં.
2. **Runner** — `/stop`, `/new`, `/queue`, `/status`, `/approve`, `/deny` ને `running_agent.interrupt()` સુધી પહોંચતાં પહેલાં પકડે.

જે નવો command agent **blocked** હોય ત્યારે runner સુધી પહોંચવો જ જોઈએ, તેણે **બંને** ચોકી bypass કરવી પડે અને inline dispatch થવું પડે.

🔬 **Expert નજર.** વાર્તાનો સંદેશો 2 એ **deadlock** છે: A, B ની રાહ જુએ; B, A ની પાછળ કતારમાં. આ concurrency ની ક્લાસિક bug છે, અને તે ફક્ત ત્યારે દેખાય જ્યારે બે વસ્તુ એકસાથે બને — એટલે સામાન્ય test માં નહીં. Guide તેને મોટા અક્ષરે લખે છે કારણ કે તે **એક વાર થઈ ચૂકી છે**. સારા project ની `AGENTS.md` એ ઘાવના નિશાનોની યાદી છે: દરેક "MUST" પાછળ એક incident.

## દૃશ્ય 5 — એલાર્મ-ચોપડી: cron

🎬 સ્મિતાબેન: "રોજ સવારે 8 વાગ્યે કેટરરને આજનાં કામ યાદ અપાવ, અને મને WhatsApp પર અહેવાલ મોકલ."

હર્ષ **એલાર્મ-ચોપડી** માં લખે છે: સમય, કામ, કઈ રીત વાપરવી, જવાબ કઈ બારીએ. સવારે 8 વાગ્યે એલાર્મ વાગે; હર્ષ **કોરી ફાઈલ** લઈને કામ કરે અને અહેવાલ મોકલે.

💻 **Cron** = નિશ્ચિત સમયે ચાલતાં agent tasks. Architecture doc: "First-class agent tasks (not shell tasks)" ✅.

**ચાર schedule રૂપ** ([Scheduling Model][doc-cron-schedule]) ✅:

| રૂપ | ઉદાહરણ | વર્તન |
|---|---|---|
| Relative delay | `30m`, `2h`, `1d` | એક વાર |
| Interval | `every 2h` | વારંવાર |
| Cron expression | `0 9 * * *` | 5-field cron |
| ISO timestamp | `2025-01-15T09:00:00` | એક વાર, ચોક્કસ સમયે |

**ત્રણ દરવાજા** ([cron doc][doc-cron-usage]) ✅ ⚠️:

```text
/cron add "every 2h" "Check server status"
/cron add "every 1h" "Summarize new feed items" --skill blogwatcher
```

```bash
hermes cron create "every 2h" "Check server status"
```

અને model પોતે: `cronjob_manage` tool (actions: `create`, `list`, `update`, `pause`, `resume`, `run`, `remove`).

Jobs `~/.hermes/cron/jobs.json` માં, **atomic write** સાથે: temp file માં લખો, પછી rename. અડધી લખાયેલી file કદી ન દેખાય.

**Job ચાલે ત્યારે** ([architecture][doc-architecture]) ✅: fresh `AIAgent` (history વગર) → attached skills context તરીકે → prompt ચલાવો → target platform પર deliver → `next_run` update.

Cron agent કેવી રીતે બને તે code માં ([scheduler.py][cron-agent-build]) ✅:

```python
# Repository code — cron/scheduler.py
# Project context files only with a configured workdir; SOUL.md always.
skip_context_files=not bool(workdir),
load_soul_identity=True,
skip_memory=False,
skip_background_review=True,  # Cron has no human-in-the-loop need for skill/memory review forks (~30K tok/event)
platform="cron",
```

- Project context files ફક્ત `workdir` સેટ હોય તો; `SOUL.md` હંમેશા.
- અને પ્રકરણ 3: જોખમી command પર `approvals.cron_mode` નો default `deny`. રાત્રે કોઈ નથી → ના.

### ⚠️ ફરી docs અને code: `skip_memory`

`agent/AGENTS.md` લખે છે: "Cron sessions pass `skip_memory=True` by default — memory providers intentionally do not run during cron." ([link][agent-cron-memory-doc]) ✅. ઉપરનો code એ જ commit પર `skip_memory=False` આપે છે ✅.

આ પુસ્તક તેનું **કારણ** જાણતું નથી, અને અનુમાન કરતું નથી. પ્રકરણ 1 નો પાઠ: code ચાલે છે, એટલે તે હકીકત છે; doc દાવો છે. તમારા cron job માં memory લોડ થાય છે કે નહીં, તે જાણવાનો રસ્તો **ચલાવીને જોવું** છે (⚠️ ચલાવ્યું નથી).

🔬 **Expert નજર.** Cron job **કોરી ફાઈલ** થી કેમ શરૂ થાય, ચાલુ chat માં કેમ નહીં? બે invariants: (1) alternation — chat ની વચ્ચે synthetic user message ઘુસાડાય નહીં (પ્રકરણ 1, દૃશ્ય 4); (2) cache — chat નો prefix અડાય નહીં. એટલે cron નો **પોતાનો session**. અને તેથી prompt **સ્વયંપૂર્ણ** હોવો જોઈએ: "ગઈકાલે કહ્યું તેમ" cron job માટે અર્થહીન છે.

## દૃશ્ય 6 — લાઈટ ગઈ: એક વાર, કે એક પણ વાર નહીં

🎬 સવારે 8:00 વાગ્યે એલાર્મ વાગે છે. હર્ષ કેટરરને સંદેશો મોકલે છે. 8:01 વાગ્યે **લાઈટ જાય છે**; હર્ષે ચોપડીમાં "થઈ ગયું" લખ્યું નહોતું. 8:05 વાગ્યે લાઈટ આવે છે. હર્ષ ચોપડી જુએ છે: "8 વાગ્યાનું કામ બાકી." ફરી સંદેશો. કેટરરને **બે** સંદેશા. (અને જો કામ "advance ચૂકવો" હોત?)

સ્મિતાબેન: "પહેલાં ચોપડીમાં **આવતી કાલનો** સમય લખ. **પછી** કામ કર. લાઈટ જાય તો આજનું કામ કદાચ રહી જાય; પણ **બે વાર** કદી નહીં થાય."

💻 Cron guide ના "Hardening invariants" — દરેક વિશે લખ્યું છે "each guards a real failure" ([link][cron-agents]) ✅. મુખ્ય ([link][cron-atmostonce]) ✅:

> "`tick()` advances `next_run_at` BEFORE dispatch (at-most-once across a mid-run crash)…"

- **At-most-once** = વધુમાં વધુ એક વાર. Crash થાય તો કામ રહી જાય, પણ બેવડાય નહીં.
- વિકલ્પ, **at-least-once** = ઓછામાં ઓછું એક વાર; crash પછી ફરી ચાલે, એટલે બેવડાઈ શકે.

પણ Hermes "રહી જાય" ને પણ ચૂપ નથી રાખતું: એ જ save માં `pending_slot` stamp થાય છે; પછીનો scan stamp ને મૃત માલિક સાથે જુએ તો instant **એક વાર** પાછો મૂકે. અને નિયમ: "Never drop a slot silently."

બીજા બચાવ:

- **Inactivity watchdog:** default 600 સેકન્ડ **idle** (wall-clock નહીં). અટકેલું session hard-interrupt થાય; લાંબું-પણ-સક્રિય job કદી કપાય નહીં.
- **Catch-up window:** period નો અડધો, 120 સેકન્ડ થી 2 કલાકની વચ્ચે. Computer બંધ હતું અને job ચૂકી ગયું? આ બારીની અંદર હોય તો ચલાવો.
- **Tick lock:** `<home>/cron/.tick.lock` — બે processes એક જ store પર એકસાથે tick ન કરે.

🔬 **Expert નજર.** Distributed systems નો પાયાનો પ્રશ્ન: crash ગમે ત્યારે થઈ શકે, તો **કયા ક્રમમાં લખવું**? "કામ, પછી નોંધ" = at-least-once. "નોંધ, પછી કામ" = at-most-once. "Exactly once" મફતમાં મળતું નથી. સાચી પસંદગી **કામ પર** આધાર રાખે છે: યાદ અપાવવાનો સંદેશો બે વાર જાય તો ચાલે; payment બે વાર ન ચાલે. Hermes agent jobs માટે at-most-once પસંદ કરે છે, કારણ કે agent ગમે તે કરી શકે — અને ગમે તે બે વાર થાય તે જોખમી છે. Watchdog માં "idle, wall-clock નહીં" પણ એ જ ઝીણવટ: **સાચી વસ્તુ માપો** — "કેટલો સમય થયો" નહીં, "કેટલા સમયથી કંઈ થયું નથી".

## દૃશ્ય 7 — શિખાઉ: delegation

🎬 લગ્નના આગલા દિવસે ત્રણ કામ એકસાથે: હોલ શોધવા, ફૂલવાળા સરખાવવા, બેન્ડ નક્કી કરવું. હર્ષ બે **શિખાઉ** — જય અને પરી — ને મોકલે છે.

પહેલી વાર, જય પાછો આવીને **આખા દિવસની વાત** કરે છે: કયા રસ્તે ગયો, કોણે ચા પીવડાવી, 40 હોલની દરેક વિગત. હર્ષની ફાઈલ 40 પાનાં જાડી થઈ જાય છે, અને શાસ્ત્રીજીનો ફોન મોંઘો.

નવા નિયમ:

1. શિખાઉ **કોરી ફાઈલ** લઈને જાય: ફક્ત કામ અને જરૂરી સંદર્ભ.
2. પાછો આવીને **ફક્ત સાર** આપે.
3. શિખાઉ **ન કરી શકે**: બીજા શિખાઉ રાખવા, ગ્રાહકને સીધો પ્રશ્ન પૂછવો, ઑફિસની ડાયરીમાં લખવું, ગ્રાહકોને સંદેશા મોકલવા, એલાર્મ ગોઠવવા.
4. શિખાઉને હર્ષ પાસે છે તેનાથી **વધુ ઓજાર ન મળે**.

💻 **`delegate_task`** ([delegation doc][doc-delegation]) ✅:

> "spawns child AIAgent instances with isolated context, inherited tool access, and their own terminal sessions. Each child gets a fresh conversation and works independently — only its final summary enters the parent's context."

નિયમ 3 શબ્દશઃ code માં ([delegate_tool_toolsets.py][delegate-blocked]) ✅:

```python
# Repository code — tools/delegate_tool_toolsets.py
DELEGATE_BLOCKED_TOOLS = frozenset(
    [
        "delegate_task",  # no recursive delegation
        "clarify",  # no user interaction
        "memory",  # no writes to shared MEMORY.md
        "send_message",  # no cross-platform side effects
        "cronjob_manage",  # no scheduling more work in the parent's name
    ]
)
```

⚠️ ત્રીજો નાનો docs-vs-code ફરક: delegation doc ની યાદીમાં છેલ્લું નામ `cronjob` લખ્યું છે; code માં tool નું ખરું નામ `cronjob_manage` છે.

નિયમ 4: `delegate_task` પાસે model-facing `toolsets` parameter **નથી**; દરેક subagent parent ના enabled toolsets વારસામાં લે છે, "so the model cannot grant a child capabilities that the parent does not have" ✅.

**Defaults:**

| Setting | Default | Source |
|---|---|---|
| એકસાથે children | 10 | [`_DEFAULT_MAX_CONCURRENT_CHILDREN`][delegate-concurrent] ✅ |
| Child દીઠ iterations | 250 | [`DEFAULT_MAX_ITERATIONS`][delegate-maxiter], [config default][delegate-config-default] ✅ |
| Nesting depth | 1 (flat) | delegation doc ✅ |

દરેક child નું **પોતાનું** `IterationBudget` છે (પ્રકરણ 1, દૃશ્ય 5). Budget પૂરું થાય તો child `exit_reason: max_iterations` અને `truncated: true` સાથે પાછું આવે, જેથી parent "પૂરું થયું" અને "કપાઈ ગયું" નો ફરક જાણે.

Nested delegation opt-in છે: `role="orchestrator"` અને `max_spawn_depth` વધારો. Docs ની ચેતવણી: depth 3 અને 3 concurrent → 3×3×3 = **27** leaf agents એકસાથે.

🔬 **Expert નજર.** Delegation નો ખરો લાભ ઝડપ નથી; **context ની સ્વચ્છતા** છે. શોધખોળનું કામ ઘોંઘાટવાળું છે: 40 web pages, 200 file reads, જેમાંથી 3 કામનાં. Child એ ઘોંઘાટ પોતાના context માં રાખે અને parent ને ફક્ત 3 આપે. Parent નો context નાનો રહે: સસ્તો, અને model નું ધ્યાન કેન્દ્રિત. અને નિયમ 4 સુરક્ષાનો સિદ્ધાંત છે: **privilege કદી નીચે જતાં વધે નહીં.** નહીં તો model પોતે પોતાને એક child મારફતે વધુ અધિકાર આપી શકે.

## Source map: આ ક્રમમાં ખોલો

1. [Architecture — System Overview અને data flows][doc-architecture]
2. [Security doc — Authorization Check Order][doc-security-authz]
3. [session.py — `build_session_key()`][gateway-session-key]
4. [gateway/AGENTS.md — TWO message guards][gateway-guards]
5. [Cron internals — Scheduling Model][doc-cron-schedule]
6. [cron/AGENTS.md — Hardening invariants][cron-agents]
7. [scheduler.py — cron agent construction][cron-agent-build]
8. [delegate_tool_toolsets.py — `DELEGATE_BLOCKED_TOOLS`][delegate-blocked]

## 🧪 Lab 6 — ત્રણ વિચાર, 100 lines

[`labs/06-gateway/mini_gateway.py`](../labs/06-gateway/mini_gateway.py)

**પહેલાં ધારો:**

1. Config: Telegram allowlist માં `111`; paired `222`. User `999`?
2. એ જ user `111`, Telegram અને WhatsApp પર: એક session કે બે?
3. Job t=100 પર due. ચાલતાં crash. t=101 પર restart: ફરી ચાલશે?
4. Parent પાસે 6 tools (તેમાં `memory`, `delegate_task`, `clarify`). Child ને કેટલાં?

```bash
python3 labs/06-gateway/mini_gateway.py
```

અપેક્ષિત output 🧪 ([evidence](../evidence/06-mini-gateway.out)):

```text
1) telegram user 111: (True, 'platform allowlist')
1) telegram user 222: (True, 'DM pairing')
1) telegram user 999: (False, 'default: deny')
2) keys: agent:main:telegram:private:111 | agent:main:whatsapp:private:111
3)
   agent:main:telegram:private:111 ← 'હોલ શોધ' turn શરૂ
   agent:main:telegram:private:111 ← 'અને કેટરર પણ' કતારમાં
   agent:main:telegram:private:111 ← /stop (તરત પહોંચ્યો)
4) t=90 : due નથી | t=100: ચાલતાં crash | restart t=101: due નથી | t=160: ચાલ્યું | કુલ runs: 1
5) બાળકનાં tools: ['read_file', 'terminal', 'web_search']
   બાળકની ફાઈલ: 41 સંદેશા | parent ની ફાઈલ: 6 → 7 (ફક્ત સાર ઉમેરાયો)
```

**વાંચો:** line 4 માં t=100 નો occurrence crash માં ગયો, અને restart પર **ફરી ચાલ્યો નહીં**: at-most-once. Line 5: બાળકે 41 સંદેશાનું કામ કર્યું; parent ની ફાઈલ ફક્ત **એક** વધી.

**પ્રયોગ.** `cron_tick` માં `job["next_run"] += job["every"]` ને `job["runs"] += 1` ની **પછી** ખસેડો (crash ની return પહેલાં નહીં). હવે line 4 માં restart પર શું થાય? તમે at-least-once બનાવ્યું.

⚠️ Lab `pending_slot` recovery બતાવતી નથી; ખરા Hermes માં crash થયેલો occurrence એક વાર પાછો મુકાય છે. Lab નું authorization પણ સરળ છે; ખરામાં adapter delegation અને group નિયમો છે.

## 🔮 આગાહી કસોટી

Subagent ને કામ દરમિયાન વપરાશકર્તાને એક પ્રશ્ન પૂછવાની જરૂર લાગે છે. તે `clarify` બોલાવે છે. શું થશે, અને સાચી design શું છે? ([પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch6))

## 🩺 નિષ્ફળતા: "Cron job ચાલ્યું, પણ કંઈ કર્યું નહીં"

1. **Prompt સ્વયંપૂર્ણ છે?** Job કોરી ફાઈલ થી શરૂ થાય; "પેલું કામ" તેને ખબર નથી.
2. **જોખમી command?** `cron_mode: deny` એ block કર્યું; agent ને બીજો રસ્તો ન મળ્યો (પ્રકરણ 3).
3. **Project context?** `workdir` વગર `AGENTS.md` લોડ થતી નથી (દૃશ્ય 5).
4. **Gateway ચાલે છે?** Guide: headless tick (`hermes cron tick`) gateway વગર agent jobs **refuse** કરે છે, નવો daemon spawn કરતું નથી; `last_fire_error` જુઓ ⚠️.
5. **Delivery?** Job ચાલ્યું પણ જવાબ ખોટી બારીએ ગયો.

**પાઠ.** Unattended કામમાં માણસ નથી જે "કેમ અટક્યો?" પૂછે. એટલે **દરેક ના પાડવાનું કારણ લખાયેલું** હોવું જોઈએ — અને તમારે તે ક્યાં લખાય છે તે જાણવું જોઈએ.

## ✅ સાર — ઈશાની નોટબુક

### સાત ઘટના, સાત નિયમ

| 🎬 ઘટના | 💻 નિયમ | તૂટે તો |
|---|---|---|
| ત્રણ બારી, એક હર્ષ | Platform-agnostic core; adapters | N×M code; દરેક બારીએ જુદું વર્તન |
| અજાણ્યો નંબર | Authorization ક્રમ; default deny | કોઈ પણ તમારું agent ચલાવે |
| કોની ફાઈલ? | `build_session_key()` | વાતચીતો ભળે |
| "હા, મંજૂર" કતારમાં | બે guards; control commands bypass | Deadlock |
| એલાર્મ-ચોપડી | Cron: fresh session, સ્વયંપૂર્ણ prompt | Alternation/cache તૂટે |
| લાઈટ ગઈ | `next_run_at` BEFORE dispatch | એક કામ બે વાર |
| જયનો લાંબો અહેવાલ | Subagent: isolated context, ફક્ત સાર; blocked tools | Parent context ભરાય; privilege વધે |

### નવા શબ્દો

Gateway · adapter · `MessageEvent` · allowlist · DM pairing · session key · deadlock · cron · atomic write · at-most-once · watchdog · delegation · subagent · orchestrator.

### યાદ-ચાવીઓ

- **"બારી અનેક, હર્ષ એક."**
- **"યાદીમાં નથી → ના."**
- **"પહેલાં ચોપડી, પછી કામ."**
- **"કોરી ફાઈલ લઈ જા, સાર લઈ આવ."**

### સામાન્ય ગેરસમજો

| ગેરસમજ | હકીકત |
|---|---|
| "Telegram પરનો Hermes અલગ agent છે." | એ જ `AIAgent`; ફક્ત adapter જુદો. |
| "Cron job મારી ચાલુ chat માં ચાલે." | પોતાના અલગ session માં. |
| "Subagent parent નો history જુએ." | ના; fresh conversation + આપેલો context. |
| "Subagents વધુ = હંમેશા ઝડપી." | દરેક child પોતાના tokens ખર્ચે; depth ગુણાકાર કરે. |

### પુનરાવર્તન કાર્ડ

| પ્રશ્ન | જવાબ |
|---|---|
| Authorization નું છેલ્લું પગથિયું? | Default: deny |
| Session key નું રૂપ? | `agent:{namespace}:{platform}:{chat_type}:{chat_id}` |
| Cron jobs ક્યાં? | `<hermes home>/cron/jobs.json` |
| Subagent ના blocked tools? | `delegate_task`, `clarify`, `memory`, `send_message`, `cronjob_manage` |
| Subagent default iterations? | 250 |

## 🧠 Mastery check

1. `/approve` ને gateway ની બંને guards કેમ bypass કરવી પડે? ન કરે તો કઈ bug થાય, અને તે test માં કેમ ન પકડાય?
2. At-most-once અને at-least-once: "રોજ સવારે ગ્રાહકોને invoice મોકલ" job માટે કયું સારું? તમારી દલીલ.
3. Subagent ને `memory` tool કેમ નથી? પ્રકરણ 4 ની કઈ ચેતવણી સાથે આ જોડાય છે?
4. દૃશ્ય 5 ના `skip_memory` વિરોધાભાસ વિશે તમે issue ફાઈલ કરો છો. તેમાં કઈ બે links, અને કયો **એક પ્રશ્ન** હશે?

જવાબો: [પરિશિષ્ટ D](../appendix/D-lab-solutions.md#ch6).

## 🎬 આગળ શું

લગ્નને ચાર દિવસ બાકી. ઈશા રોજ સાંજે મહેમાન-યાદી અને કેટરરની ગણતરી મેળવે છે: skill છે, પણ દર વખતે model CSV હાથે ગણે છે, ધીમે, અને એક વાર તો ખોટું.

"મામા, આ ગણતરી **code** કરે તો? એક સાચું ઓજાર."

"હા. પણ Hermes ના કબાટમાં નહીં — કબાટ નાનો રાખવાનો છે. તું **બહારની કારીગર** બનીશ."

→ [પ્રકરણ 7 — પોતાનું ઓજાર અને mastery](07-potanu-ojar-ane-mastery.md)

<!-- refs:start (generated by tools/citations.py) -->
[agent-cron-memory-doc]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/agent/AGENTS.md#L127-L128
[cron-agent-build]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/cron/scheduler.py#L2505-L2510
[cron-agents]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/cron/AGENTS.md#L20-L25
[cron-atmostonce]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/cron/AGENTS.md#L38-L42
[delegate-blocked]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/tools/delegate_tool_toolsets.py#L14-L23
[delegate-concurrent]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/tools/delegate_tool_config.py#L19
[delegate-config-default]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/hermes_cli/config_defaults.py#L1310
[delegate-maxiter]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/tools/delegate_tool.py#L106
[doc-arch-principles]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/architecture.md#L260-L270
[doc-architecture]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/architecture.md#L11-L14
[doc-cli-gateway-client]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/cli.md#L175-L177
[doc-cron-schedule]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/cron-internals.md#L22-L34
[doc-cron-usage]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/features/cron.md#L64-L75
[doc-delegation]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/features/delegation.md#L7-L11
[doc-gateway-key]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/developer-guide/gateway-internals.md#L688
[doc-security-authz]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/website/docs/user-guide/security.md#L473-L482
[gateway-authz]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/gateway/authz_mixin.py#L855-L857
[gateway-guards]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/gateway/AGENTS.md#L19-L27
[gateway-session-key]: https://github.com/NousResearch/hermes-agent/blob/18e659dfc93ef319771d51441573e3fa31b8f5b7/gateway/session.py#L722-L725
<!-- refs:end -->
