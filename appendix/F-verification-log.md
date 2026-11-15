# પરિશિષ્ટ F — Verification log

આ પુસ્તકમાં શું ચકાસાયું, કેવી રીતે, અને શું **નથી** ચકાસાયું.

## Environment

| વસ્તુ | કિંમત |
|---|---|
| Hermes Agent commit | `18e659dfc93ef319771d51441573e3fa31b8f5b7` (`main`, 2026-11-15) |
| Python (labs માટે) | 3.13.18 |
| OS | Linux |
| Hermes install | **ના** — નીચે જુઓ |

## ✅ Source થી ચકાસ્યું

106 citations. `python3 tools/citations.py <checkout>` દરેકનો needle pinned checkout માં શોધે છે અને line range pin કરે છે. Table: [citations.generated.md](citations.generated.md).

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
- ખરા provider પર cache hit ના આંકડા.

તમે ચલાવો ત્યારે અહીં ઉમેરો: command, તારીખ, Hermes commit, પરિણામ.

## Docs અને code વચ્ચેના તફાવતો (pinned commit પર)

| # | Doc/comment કહે છે | Code કરે છે | પ્રકરણ |
|---|---|---|---|
| 1 | `agent/iteration_budget.py` docstring અને agent-loop doc: parent default 500, subagent 50 | `AIAgent.__init__`: `max_iterations=sys.maxsize`; `config_defaults.py`: `"max_turns": None`; `delegate_tool.py`: `DEFAULT_MAX_ITERATIONS = 250` | 1 |
| 2 | `agent/AGENTS.md`: "Cron sessions pass `skip_memory=True` by default" | `cron/scheduler.py`: `skip_memory=False` | 6 |
| 3 | Delegation doc: subagents માટે `cronjob` blocked | `DELEGATE_BLOCKED_TOOLS` માં `cronjob_manage` | 6 |
| 4 | Architecture doc: "70+ tools", "~28 toolsets"; README: "40+ tools" | ગણ્યું નથી ⚠️ | — |

#2 નો ઇરાદો આ પુસ્તક જાણતું નથી; કયું સાચું "હોવું જોઈએ" તે upstream નો નિર્ણય છે.

## વાર્તા અને ખરા વર્તન વચ્ચેના જાણીતા ફરક

| વાર્તા | ખરું |
|---|---|
| શાસ્ત્રીજી "દસમા ભાગે" ફરી સાંભળે | Cache ના ભાવ અને TTL provider પ્રમાણે જુદા |
| હર્ષ એક માણસ | `AIAgent` અનેક mixins; turn lease; gateway process માં ચાલે |
| રઘુકાકાની એક યાદી | Adapter delegation, group નિયમો, pairing codes |
| લાઈટ જાય તો કામ રહી જાય | `pending_slot` recovery occurrence ને એક વાર પાછો મૂકે |
| હર્ષ "જાતે" રીત લખે | Model નો નિર્ણય, system prompt ની સૂચના પરથી; guarantee નથી |
