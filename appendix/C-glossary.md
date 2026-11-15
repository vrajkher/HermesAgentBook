# પરિશિષ્ટ C — ગુજરાતી–English glossary

દરેક શબ્દ: વાર્તાની ઉપમા, એક લીટીનો અર્થ, અને પ્રકરણ.

| English | વાર્તામાં | અર્થ | પ્રકરણ |
|---|---|---|---|
| Adapter | બારીનો કારકુન | Platform ની ભાષા ↔ Hermes નું `MessageEvent` | 6 |
| Agent | હર્ષ | Model + loop + tools + memory | પ્રવેશ |
| Agent loop | હર્ષનો દિવસ | ફોન → ચિઠ્ઠી → ઓજાર → ફરી ફોન | 1 |
| Allowlist | રઘુકાકાની યાદી | મંજૂર users (કે commands) ની યાદી | 3, 6 |
| API | ફોન નંબર | Model સાથે વાત કરવાનો રસ્તો | પ્રવેશ |
| API key | ખાતાની ઓળખ | ગુપ્ત; `.env` માં | 0 |
| Approval | સ્મિતાબેનની સહી | જોખમી command પહેલાં મંજૂરી | 3 |
| AST | — | Code નું બંધારણ, ચલાવ્યા વગર | 3 |
| At-most-once | પહેલાં ચોપડી, પછી કામ | Crash માં કામ રહી જાય, બેવડાય નહીં | 6 |
| Behaviour-contract test | — | Test જે વચન તપાસે, લખાણ નહીં | 7 |
| Byte-stable | પાટી અડાય નહીં | એક અક્ષર પણ ન બદલાય | 2 |
| Cache (prompt) | ફી-માફી | સરખી શરૂઆત સસ્તી | 2 |
| `check_fn` | બેટરી છે? | Tool અત્યારે ચાલી શકે તેમ છે? | 3 |
| Commit | એ દિવસનો ફોટો | Code ની એક ક્ષણ; 40 અક્ષરનો hash | 0 |
| Compression | સાર-નોંધ | લાંબા history નો વચ્ચેનો ભાગ ટૂંકો | 4 |
| Context file | પ્રોજેક્ટની પહેલી નોંધ | `AGENTS.md`, `.hermes.md`… | 2 |
| Context window | એક ફોનની મર્યાદા | એક call માં કેટલા tokens | પ્રવેશ |
| Cron | એલાર્મ-ચોપડી | નિશ્ચિત સમયે agent task | 6 |
| Curator | પોથીની સફાઈ | Agent-created skills ની જાળવણી | 5 |
| Deadlock | મંજૂરી કતારમાં | બે વસ્તુ એકબીજાની રાહ જુએ | 6 |
| Default deny | યાદીમાં નથી → ના | સ્પષ્ટ મંજૂરી વગર ના | 3, 6 |
| Delegation | શિખાઉ | Subagent ને કામ સોંપવું | 6 |
| Dispatch | ઓજાર હાથમાં લેવું | નામથી tool handler ચલાવવો | 3 |
| Facade | રિસેપ્શન | Public entry points વાળી file | 0 |
| Fail closed | શંકા હોય તો ના | ભૂલમાં સલામત બાજુ પડવું | 3 |
| Fallback provider | બીજા પંડિત | Primary fail થાય ત્યારે | 7 |
| Footprint ladder | ઓજાર ક્યાં મૂકવું | નવી ક્ષમતા માટે પગથિયાંનો ક્રમ | 3 |
| Frozen snapshot | સવારની નકલ | Session શરૂઆતની memory, પાટી પર સ્થિર | 4 |
| FTS5 | અનુક્રમણિકા | SQLite નું full-text search | 4 |
| Gateway | બારીઓ | અનેક platforms, એક agent | 6 |
| Handler | ઓજાર પોતે | Tool નું કામ કરતું function | 3 |
| Hardline | તિજોરી: સહીથી પણ નહીં | મંજૂરીથી પણ ન ખૂલે તેવી blocklist | 3 |
| `HERMES_HOME` | ઑફિસનું સરનામું | Hermes નું ઘર | 0 |
| Hook | કબાટની ઘંટડી | Lifecycle ની ક્ષણે બોલાવાતું plugin function | 7 |
| Interrupt | "રોકાઈ જા!" | ચાલુ call/tool રોકવું | 1 |
| Invariant | કદી ન તૂટતો નિયમ | Design નો પાયો | નકશો |
| Iteration | એક ફોન | Loop નું એક ચક્કર | 1 |
| Iteration budget | ચક્કર-મર્યાદા | એક agent ના iterations ની મર્યાદા | 1 |
| JSON / YAML | છાપેલું ફોર્મ / હાથની નોંધ | મશીન માટે / settings માટે | પ્રવેશ |
| MCP | બહારની દુકાનની બારી | બહારનાં tool servers જોડવાનો protocol | 7 |
| Memory | ખિસ્સા-ડાયરી, ગ્રાહક-કાર્ડ | `MEMORY.md`, `USER.md` | 4 |
| Model (LLM) | શાસ્ત્રીજી | Text વાંચી text લખે; stateless | પ્રવેશ |
| Narrow waist | નાનો કબાટ | પાતળું, સ્થિર core | 3 |
| Plugin | બહારનો કારીગર | Core ને અડ્યા વગર tools/hooks ઉમેરે | 7 |
| Prefix | ફાઈલની શરૂઆત | Request નો શરૂઆતી ભાગ; cache તેના પર | 2 |
| Profile | શાખા | અલગ ઘર: config, memory, sessions | 0, 7 |
| Progressive disclosure | સૂચિ → પાનું → પરિશિષ્ટ | જરૂર પડે તેટલું જ લોડ | 5 |
| Registry | ઓજાર-કબાટ | નામથી નોંધણી અને શોધ | 3 |
| Role alternation | પ્રશ્ન પછી જવાબ | સંદેશાના roles નો કડક ક્રમ | 1 |
| Schema | ઓજારની ચિઠ્ઠી | Model જે વાંચે: description + parameters | 3 |
| Session | એક ફાઈલ | એક વાતચીત | 4 |
| Session key | ફાઈલનું લેબલ | Gateway: આ chat કોની | 6 |
| Sibling | અંદરનો ઓરડો | `<stem>_<topic>.py` | 0 |
| Skill | રીત-પોથીનું પાનું | `SKILL.md`: procedure | 5 |
| `SOUL.md` | ડ્રોઅરનું કાર્ડ | Agent ની ઓળખ | 2 |
| Subagent | શિખાઉ | Isolated context વાળો child agent | 6 |
| System prompt | સૂચના-પાટી | `messages` ની પહેલી entry | 2 |
| Tier | પાટીનો થર | stable / context / volatile | 2 |
| Token | શબ્દનો ટુકડો | બિલનો એકમ | પ્રવેશ |
| Tool call | ચિઠ્ઠી | Model ની "આ tool ચલાવો" માગ | પ્રવેશ |
| Toolset | થેલો | Tools નું નામવાળું જૂથ | 3 |
| Turn | એક કામ | સંદેશાથી અંતિમ જવાબ સુધી | 1 |
| Watchdog | — | અટકેલું કામ પકડતો ચોકીદાર | 6 |
