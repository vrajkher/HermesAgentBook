# labs/ — પુસ્તક-માલિકીનો code

આ folder નો બધો code **આ પુસ્તકનો** છે, Hermes Agent નો નહીં. ફક્ત Python standard library; API key કે internet જોઈતું નથી. Python 3.11+.

```bash
bash labs/run-all.sh
```

| Folder | પ્રકરણ | Hermes નો કયો નિયમ નાના રૂપમાં |
|---|---|---|
| `pravesh/` | પ્રવેશ | Agent loop |
| `01-loop/` | 1 | `IterationBudget`, parallel tool order, role alternation, interrupt |
| `02-prompt/` | 2 | ત્રણ tiers; prefix cache |
| `03-tools/` | 3 | Registry, `check_fn`, dispatch, approval; `mini_exec.py`: `execute_code` નો context લાભ |
| `04-memory/` | 4 | Memory limits + frozen snapshot; SQLite FTS5; compression |
| `05-skills/` | 5 | `SKILL.md` + authoring-standards checker |
| `06-gateway/` | 6 | Authorization order, session key, at-most-once cron, delegation |
| `07-plugin/` | 7 | ખરું Hermes plugin (`mehmaan-tally`) + Hermes વગરનો test |

`07-plugin/mehmaan-tally/` અને `05-skills/lagna-mehmaan-yadi/` ખરા Hermes માં વાપરવા લખાયેલાં છે, પણ ત્યાં ચલાવીને ચકાસાયાં નથી (⚠️ [verification log](../appendix/F-verification-log.md)).
