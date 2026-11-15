# પરિશિષ્ટ D — Lab solutions અને mastery check જવાબો

પહેલાં જાતે પ્રયત્ન કરો. જવાબ વાંચવાથી શીખાતું નથી; ધારવાથી અને ખોટા પડવાથી શીખાય છે.

<a id="pravesh"></a>

## પ્રવેશ

1. `shastriji()` tool result માંથી `count` વાંચીને અંતિમ જવાબ આપે છે. કારણ: ફાઈલની છેલ્લી entry `tool` છે, એટલે માગેલો ડેટા આવી ગયો; હવે tool માગવાની જરૂર નથી. Model પાસે બીજી કોઈ "યાદ" નથી; તે ફક્ત ફાઈલ જોઈને નક્કી કરે છે.
2. બધા દસ: આગલા નવ turns નો આખો history (system prompt સાથે), વત્તા દસમો સંદેશો. (Compression થયું હોય તો વચ્ચેનો ભાગ સાર રૂપે: પ્રકરણ 4.)
3. Loop તૂટે અને turn નિષ્ફળ જાય. એટલે Hermes નું `dispatch()` દરેક exception ને `{"error": …}` માં ફેરવે છે (પ્રકરણ 3, દૃશ્ય 4).

<a id="ch0"></a>

## પ્રકરણ 0

**આગાહી કસોટી.** `/tmp/test-home/state.db`. `get_hermes_home()` પહેલાં context-local override જુએ, પછી `HERMES_HOME`, અને platform default છેલ્લે. ⚠️ ચલાવીને ચકાસ્યું નથી; ક્રમ pinned doc માંથી.

1. `config.yaml` વહેંચી શકાય (bug report, backup, મિત્ર); `.env` નહીં. એક file હોત તો દરેક વહેંચણી key-ચોરીનું જોખમ.
2. Root `AGENTS.md` દરેક AI coding session માં context તરીકે લોડ થાય છે. મોટી file = દરેક session મોંઘો અને ધ્યાન વેરાયેલું. Hermes પોતાના માટે પણ "પાટી નાની રાખો" પાળે છે.
3. "Patch where production reads." Sibling function facade માંથી નામ import કરે છે, એટલે patch facade પર જોઈએ; defining module પરનો patch "passes silently".

<a id="ch1"></a>

## પ્રકરણ 1

**આગાહી કસોટી.** ના. Interactive tool (`clarify`) હોય ત્યારે execution sequential થાય છે: વપરાશકર્તાને પ્રશ્ન પૂછતી વખતે બીજાં tools પાછળ દોડતાં ન હોવાં જોઈએ.

1. (a) આ turn ના API calls મર્યાદાની અંદર; (b) budget માં ચક્કર બાકી; (c) અથવા એક grace call બાકી. Grace call વગર budget પૂરું થતાં agent વાક્યની વચ્ચે અટકી જાત, અને વપરાશકર્તાને "શું થયું, શું બાકી" નો અહેવાલ ન મળત.
2. Strict role alternation: ચાલુ વાતચીતની વચ્ચે synthetic user message ઘુસાડાય નહીં. (અને cache: chat નો prefix અડાય નહીં.)
3. **250.** સ્રોત: `tools/delegate_tool.py` નો `DEFAULT_MAX_ITERATIONS` અને `config_defaults.py`. Docstring ("50") જૂનો છે; code ચાલે છે, એટલે code.
4. "Results are reinserted in the original tool call order": parallel પરિણામનો ક્રમ પૂરા થવાના ક્રમ પર આધારિત બની જાય, અને model કયું પરિણામ કયા call નું તે ભેળવી શકે.

<a id="ch2"></a>

## પ્રકરણ 2

**આગાહી કસોટી.** શૂન્ય. "Model identity is part of the cache key": cache model (અને account) દીઠ છે. આખો history પૂરા ભાવે.

1. Timestamp દરેક session માં જુદો છે. Stable થરમાં હોત તો તેની **પાછળનું બધું** (ઓળખ, guidance, context files) દરેક નવા session માં cache-miss થાત. Volatile થરમાં તે છેલ્લે છે, એટલે તેની ઉપરનું બધું બચે.
2. Compression વચ્ચેના સંદેશા બદલે જ છે, એટલે cache આમેય તૂટે. એ ક્ષણે system prompt rebuild થાય: memory disk પરથી ફરી લોડ, skills index તાજો, plugin sections ફરી render.
3. હવામાન દર turn બદલાય → system prompt દર turn બદલાય → દરેક turn માં આખો history પૂરા ભાવે. સાચી જગ્યા: એક **tool** (model જરૂર પડે ત્યારે માગે), કે user message સાથેની નોંધ. `pre_llm_call` hook પણ context ઉમેરે છે, system prompt માં નહીં.
4. System prompt ના પહેલા 1292 અક્ષર બંને versions માં સરખા છે: stable + context (1212) અને volatile ની શરૂઆત, memory ની જૂની નોંધ સુધી. નવી નોંધ ત્યાંથી શરૂ થાય છે.

<a id="ch3"></a>

## પ્રકરણ 3

**આગાહી કસોટી.** (c). Cron માં `approvals.cron_mode` નો default `deny` છે; `mode: manual` માણસવાળા sessions માટે છે. Command block થાય અને agent એ બીજો રસ્તો શોધવો પડે.

1. Prompt caching invariant. `tools[]` નો ક્રમ request ના શરૂઆતી ભાગમાં છે; ક્રમ બદલાય તો prefix બદલાય. કોઈ functional test fail ન થાય (tools એ જ છે), પણ વપરાશકર્તાનું બિલ વધે: **શાંત regression**.
2. Session પ્રમાણે `tools[]` બદલાય તો sessions વચ્ચે stable prefix નો લાભ ઘટે, અને "આ tool કેમ દેખાતું નથી?" નું debugging અઘરું બને. `check_fn` ફક્ત reachability/opt-in માટે.
3. પગથિયું 2: **CLI command + skill**. PDF માંથી tables કાઢવાનું `terminal` + એક script થી થાય; skill રીત અને pitfalls આપે. નવું core tool દરેક call માં દરેક વપરાશકર્તાને ખર્ચ કરાવે.
4. Hardline એ "floor that consent cannot lower" છે. તેને config થી બંધ કરી શકાય, તો prompt injection કે ઉતાવળિયો વપરાશકર્તા તેને બંધ કરી શકે; પછી તે floor નથી.

<a id="ch4"></a>

## પ્રકરણ 4

**આગાહી કસોટી.** હા. Compression પછી `invalidate_system_prompt()` memory ને disk પરથી ફરી લોડ કરે છે, એટલે turn 31 નો rebuilt prompt નવી નોંધ ધરાવે. (Turn 6–30 માં તે પાટી પર નહોતી.)

1. Token ગણતરી model/tokenizer પ્રમાણે બદલાય; અક્ષર નહીં. Model બદલો તો પણ મર્યાદાનો અર્થ એ જ રહે.
2. "Per-conversation prompt caching is sacred" — system prompt byte-stable. Lab 2: scenario B માં turn 3 નો ભાવ 385 → 784; C માં 1875. અને ખરી વાતચીતમાં history ઘણો લાંબો હોય.
3. Tool results સૌથી જાડા અને સૌથી ઓછા કામના (model એ તે વાંચી લીધા છે). તેને placeholder થી બદલવું deterministic string operation છે. પહેલો કેમ: મફત → સસ્તું → મોંઘું; ઘણી વાર તે એકલું પૂરતું.
4. હા. Pre-compaction turns એ જ session id નીચે soft-archive (`active=0, compacted=1`) થાય: "still searchable via `session_search` and recoverable, never deleted".

<a id="ch5"></a>

## પ્રકરણ 5

**આગાહી કસોટી.** ફક્ત (b). (a) bundled છે: curator ના LLM review ની બહાર (default માં). (c) pinned: દરેક auto-transition થી મુક્ત.

1. "કેટરર જલારામ" = memory: નાનું, કાયમી, દરેક call માં ~10 tokens પોસાય. "ગણતરી કેવી રીતે મેળવવી" = skill: બે પાનાં; દરેક call માં મૂકો તો સેંકડો tokens નકામા, એટલે ફક્ત સૂચિમાં એક લીટી અને body માગો ત્યારે.
2. અડધી વાંચેલી રીત ખતરનાક: model પાછળનાં pitfalls ચૂકે અને આત્મવિશ્વાસથી ખોટું કરે.
3. "`confirmed` = `maybe` વાળી rows ને મહેમાન ન ગણો, કારણ કે કેટરરને confirmed થાળી દીઠ પૈસા અપાય છે." (તારીખ, નામ, issue number ગયાં; નિયમ + કારણ રહ્યાં.)
4. (a) સીમિત અધિકાર → bundled/hub skills બગડે નહીં; (b) archive, delete નહીં → ખોટો નિર્ણય પાછો વળે; (c) pin → માણસનો veto; (d) pre-run backup → આખો run rollback થાય.

<a id="ch6"></a>

## પ્રકરણ 6

**આગાહી કસોટી.** `clarify` subagent માટે blocked છે, એટલે tool તેની યાદીમાં નથી. સાચી design: child પોતાના સારમાં "આ માહિતી ખૂટે છે" લખે; **parent** વપરાશકર્તાને પૂછે અને જરૂર પડે તો નવું delegation કરે.

1. Agent મંજૂરીની રાહમાં blocked છે; `/approve` કતારમાં જાય તો agent ના પૂરા થવાની રાહ જુએ: deadlock. Test માં ન પકડાય કારણ કે તે ફક્ત "agent blocked + નવો સંદેશો" ના સંયોગમાં થાય, અને સામાન્ય tests sequential છે.
2. દલીલ બંને તરફ: invoice બે વાર જાય તો ગ્રાહક ગૂંચવાય (at-most-once); ન જાય તો પૈસા મોડા (at-least-once). સારો જવાબ: at-most-once + ચૂકી ગયેલા slot ની **દેખાતી** નોંધ, અથવા job ને idempotent બનાવો (મોકલતાં પહેલાં "આજે મોકલ્યું?" તપાસો). મુખ્ય વાત: પસંદગી **કામના પરિણામ** પરથી.
3. "No writes to shared MEMORY.md". પ્રકરણ 4: "એક ઘર, એક agent" — અનેક writers એકબીજાની entries ભેળવે. દસ parallel children દસ writers હોત.
4. Links: `agent/AGENTS.md` ની line અને `cron/scheduler.py` ની line. પ્રશ્ન: "કયું ઇરાદાપૂર્વકનું છે: doc કે code?" (Fix સૂચવતાં પહેલાં ઇરાદો પૂછો: "verify the claim AND the intent".)

<a id="ch7"></a>

## પ્રકરણ 7

**Debugging challenge.** ક્રમ: (1) Plugin enable છે અને `register()` crash વગર ચાલ્યું? (`hermes plugins doctor`) (2) Tool model ને દેખાય છે — toolset `mehmaan` આ platform પર ચાલુ છે? (3) Install ચાલુ session માં કર્યું? નવું session. (4) Description: model ને ખબર છે **ક્યારે** વાપરવું? સસ્તી તપાસ પહેલાં.

<a id="mastery"></a>

## Mastery પરીક્ષા

1. **Trace.** Adapter `on_message` → `MessageEvent` → `GatewayRunner._handle_message` → `_is_user_authorized` → `build_session_key` → `AIAgent` (session history સાથે) → `run_conversation` → system prompt (cache માંથી) → `while` loop → model call → `run_tool_round` → `handle_function_call` → `registry.dispatch` → tool result `messages` માં → ફરી model call → `finish_text_response` → `state.db` માં persist → adapter delivery.
2. (a) caching; (b) caching; (c) narrow waist નહીં, **security** (untrusted input) — ફાંસો! બેમાંથી એકમાં ન બેસે તે ઓળખવું પણ કુશળતા છે; (d) caching; (e) narrow waist.
3. Inbox access: MCP server કે plugin tool (API integration → tool). "સાર કેવો જોઈએ": skill. "દર કલાકે": cron, Telegram delivery સાથે. Core tool નહીં.
4. (i) `/model` બદલ્યો કે fallback થયો → cache શૂન્ય; (ii) વાતચીત ખૂબ લાંબી, `/new` નથી; (iii) plugin/tools વધ્યાં → દરેક call મોટો; (iv) agent loop માં અટક્યો, મર્યાદા અમર્યાદ; (v) nested delegation; (vi) cache TTL કરતાં લાંબા વિરામ.
5. Reject. `agent/AGENTS.md` Message-flow invariants: system prompt byte-stable; `build_system_prompt` "only rebuilt after compression"; timestamp પહેલેથી volatile થરમાં session-start વખતે છે. વિકલ્પ: tool કે user-message નોંધ. અને prompt-surface snapshot test fail થશે.
6. (i) Iteration budget: docstring/doc "500/50" vs code "unlimited/250"; (ii) cron `skip_memory`: `agent/AGENTS.md` "True" vs `scheduler.py` `False`; (iii) delegation doc `cronjob` vs code `cronjob_manage`. દરેકમાં: code ને હકીકત માનો; ચલાવીને ખાતરી કરો; (i) અને (iii) માટે doc-fix PR; (ii) માટે પહેલાં ઇરાદો પૂછતો issue.

**Rubric:** [પરિશિષ્ટ E](E-mastery-rubric.md).
