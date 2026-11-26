# પરિશિષ્ટ F — Verification log

આ પુસ્તકમાં શું ચકાસાયું, કેવી રીતે, અને શું **નથી** ચકાસાયું.

## Environment

| વસ્તુ | કિંમત |
|---|---|
| Hermes Agent commit | `93dd2a4efb0709ceac09969b85d306e768b53815` (`main`, 2026-11-26) |
| પહેલું version | `18e659dfc93ef319771d51441573e3fa31b8f5b7` (`main`, 2026-11-15) |
| Python (labs માટે) | 3.13.18 |
| OS | Linux |
| Hermes install | **ના** — નીચે જુઓ |

## ✅ Source થી ચકાસ્યું

131 citations. `python3 tools/citations.py <checkout>` દરેકનો needle pinned checkout માં શોધે છે અને line range pin કરે છે. Table: [citations.generated.md](citations.generated.md).

મર્યાદા: needle **પહેલી line** ચકાસે છે; range ની અંદરનું અર્થઘટન લેખકનું વાંચન છે.

## 🧪 ચલાવીને ચકાસ્યું

આઠ book labs (`bash labs/run-all.sh`); outputs [`evidence/`](../evidence/) માં. પ્રકરણોમાંના "અપેક્ષિત output" blocks આ files માંથી છે.

આ labs Hermes ના નિયમોની **નકલ** છે, Hermes નો code નથી. તે સાબિત કરે છે કે નિયમ વર્ણવ્યા પ્રમાણે **કામ કરે છે**; તે સાબિત **નથી** કરતી કે Hermes બરાબર એમ જ વર્તે છે.

## ⚠️ ચલાવીને ચકાસ્યું નથી

લેખન environment માં Hermes Agent install કરવાની પરવાનગી નહોતી. એટલે:

- દરેક `hermes …` command અને slash command (પરિશિષ્ટ B).
- `mehmaan-tally` plugin નું ખરા Hermes માં loading (`hermes plugins doctor`).
- `lagna-mehmaan-yadi` skill નું ખરા session માં loading.
- પ્રકરણ 0 ની આગાહી કસોટી (`HERMES_HOME=… hermes chat -q`).
- Compression trigger નું small-window floor (0.75) વર્તન.
- Checkpoints અને `/rollback` (opt-in feature).
- `execute_code` અને Tool Search નું ખરું વર્તન (book lab ફક્ત વિચાર બતાવે છે).
- ખરા provider પર cache hit ના આંકડા.

તમે ચલાવો ત્યારે અહીં ઉમેરો: command, તારીખ, Hermes commit, પરિણામ.

## Update log: 18e659d → 93dd2a4 (2026-11-26)

Re-pin કરતાં `tools/citations.py` એ ચાર citations પર ના પાડી (needle ન મળ્યો): `AGENTS.md` નો "Facade + siblings" વિભાગ, `hermes_state.py` નો `SessionDB`, `hermes_state_fts.py` (file દૂર), અને `tools/checkpoint_manager.py` (ખસી). પછી દરેક cited file નો diff વાંચ્યો, કારણ કે needle મળે છતાં વર્તન બદલાઈ શકે. બદલાયેલા દાવા:

| ફેરફાર | પ્રકરણ |
|---|---|
| Source layout: મોટો topic → `<stem>/__init__.py` facade + `<stem>/<topic>.py`; "Patch where the name is looked up" | 0 |
| Session storage `persistence/` interface (`PersistenceStore`) + `persistence/sqlite/` backend પાછળ; `hermes_state` deprecated stand-in, v0.27.0 માં દૂર | 0, 4 |
| Checkpoints: `agent/checkpoints/manager.py` | 4 |
| `prompt_caching.cache_ttl` default `5m` → `auto` (માણસ: `1h`, machine-paced: `5m`) | 2 |
| નવો `skills.index_desc_limit` (60–1024); authoring standard 60 જ | 5 |
| `dispatch()` નો error text `error_type_name(e)` વાપરે | 3 |
| Nested delegation ઊંડાઈ પરથી; `role` argument અવગણાય | 6 |
| Docs-vs-code: #3 સુધર્યો, #1 અડધો સુધર્યો (નીચે) | 1, 6, 7 |

Labs Hermes ના code પર આધાર રાખતી નથી, એટલે outputs બદલાયાં નથી; ફરી ચલાવીને ચકાસ્યું. 🧪

## Docs અને code વચ્ચેના તફાવતો

| # | Doc/comment કહે છે | Code કરે છે | પ્રકરણ | 2026-11-26 સ્થિતિ |
|---|---|---|---|---|
| 1 | `agent/iteration_budget.py` docstring: parent 500, subagent 50; agent-loop doc: parent 500 | `AIAgent.__init__`: `max_iterations=sys.maxsize`; `config_defaults.py`: `"max_turns": None`; `delegate_tool.py`: `DEFAULT_MAX_ITERATIONS = 250` | 1 | **અડધો સુધર્યો**: doc નો subagent આંકડો 50 → 250 |
| 2 | `agent/AGENTS.md`: "Cron sessions pass `skip_memory=True` by default" | `cron/scheduler.py`: `skip_memory=False` | 6 | બાકી |
| 3 | Delegation doc: subagents માટે `cronjob` blocked | `DELEGATE_BLOCKED_TOOLS` માં `cronjob_manage` | 6 | **સુધર્યો**: doc હવે `cronjob_manage` |
| 4 | MCP user doc: tools `mcp_<server_name>_<tool_name>` (દા.ત. `mcp_github_create_issue`) | `tools/mcp_tool_schema.py`: `MCP_TOOL_NAME_PREFIX = "mcp__"`; નામ `mcp__<server>__<tool>`, 64 અક્ષરે hash suffix સાથે | 7 | બાકી |
| 5 | જૂનું delegation doc: `role="orchestrator"` nesting ચાલુ કરે | `delegate_tool.py`: "The `role` arg is ignored"; role ઊંડાઈ પરથી | 6 | **સુધર્યો** (પહેલા version માં પુસ્તક પોતે જૂના doc ને અનુસર્યું હતું; હવે સુધાર્યું) |
| 6 | Architecture doc: "70+ tools", "~28 toolsets"; README: "40+ tools" | ગણ્યું નથી ⚠️ | — | — |

#2 નો ઇરાદો આ પુસ્તક જાણતું નથી; કયું સાચું "હોવું જોઈએ" તે upstream નો નિર્ણય છે.

## વાર્તા અને ખરા વર્તન વચ્ચેના જાણીતા ફરક

| વાર્તા | ખરું |
|---|---|
| શાસ્ત્રીજી "દસમા ભાગે" ફરી સાંભળે | Cache ના ભાવ અને TTL provider પ્રમાણે જુદા |
| હર્ષ એક માણસ | `AIAgent` અનેક mixins; turn lease; gateway process માં ચાલે |
| રઘુકાકાની એક યાદી | Adapter delegation, group નિયમો, pairing codes |
| લાઈટ જાય તો કામ રહી જાય | `pending_slot` recovery occurrence ને એક વાર પાછો મૂકે |
| હર્ષ "જાતે" રીત લખે | Model નો નિર્ણય, system prompt ની સૂચના પરથી; guarantee નથી |
