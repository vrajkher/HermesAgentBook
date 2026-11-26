# પરિશિષ્ટ B — Command reference

> ⚠️ આ પરિશિષ્ટના `hermes …` commands pinned README અને docs માંથી લીધેલા છે; આ પુસ્તક લખતી વખતે ચલાવ્યા નથી. 🧪 વાળા ચલાવેલા છે.

## પુસ્તકની labs 🧪

| Command | શું |
|---|---|
| `bash labs/run-all.sh` | આઠેય labs; outputs `evidence/` માં |
| `python3 labs/pravesh/toy_agent.py` | 45-line agent |
| `python3 labs/01-loop/mini_loop.py` | Budget, parallel order, alternation |
| `python3 labs/02-prompt/cache_sim.py` | Prefix cache ના ત્રણ scenarios |
| `python3 labs/03-tools/mini_registry.py` | Registry, `check_fn`, dispatch, approval |
| `python3 labs/03-tools/mini_exec.py` | એક-એક ઓજાર vs એક script |
| `python3 labs/04-memory/mini_memory.py` | Memory, FTS5, compression |
| `python3 labs/05-skills/check_skill.py <SKILL.md>` | Skill standards checker |
| `python3 labs/06-gateway/mini_gateway.py` | Authz, session key, cron, delegation |
| `python3 labs/07-plugin/test_plugin.py` | Plugin test, નકલી `ctx` સાથે |
| `python3 tools/citations.py [checkout]` | Citations pin + verify |

## Hermes: રોજના commands ⚠️

| Command | શું | પ્રકરણ |
|---|---|---|
| `hermes` | વાતચીત શરૂ | 0 |
| `hermes chat -q "…"` | એક પ્રશ્ન, બહાર | 0 |
| `hermes setup` | Setup wizard | 0 |
| `hermes doctor` | તપાસ | 0 |
| `hermes model` | Provider અને model | 0 |
| `hermes tools` | Tools ચાલુ/બંધ | 3 |
| `hermes config set` / `get` / `edit` | Settings | 0 |
| `hermes logs` | Logs | 0 |
| `hermes profile create <name>` | નવી profile | 0, 7 |
| `hermes -p <name>` | Profile સાથે ચલાવો | 0 |
| `hermes gateway setup` / `start` | Messaging gateway | 6 |
| `hermes cron list\|add\|edit\|pause\|resume\|run\|remove` | Scheduled jobs | 6 |
| `hermes skills install official/<category>/<skill>` | Optional skill | 5 |
| `hermes curator status\|run\|pin\|unpin\|archive\|restore\|rollback` | Skill lifecycle | 5 |
| `hermes plugins install\|list\|enable\|doctor\|validate` | Plugins | 7 |
| `hermes update` | Update | — |

## Slash commands (વાતચીતની અંદર) ⚠️

| Command | શું | પ્રકરણ |
|---|---|---|
| `/new`, `/reset` | નવું session (memory ની સીમા) | 4 |
| `/model [provider:model]` | Model બદલો — cache શૂન્ય થશે | 2 |
| `/compress` | હમણાં compress | 4 |
| `/usage`, `/insights` | વપરાશ | 2 |
| `/retry`, `/undo` | છેલ્લો turn | — |
| `/stop` | ચાલુ કામ રોકો (messaging) | 1, 6 |
| `/approve`, `/deny` | જોખમી command નો જવાબ | 3, 6 |
| `/yolo` | Approval prompts bypass (hardline સિવાય) | 3 |
| `/skills`, `/<skill-name>` | Skills | 5 |
| `/cron add "<schedule>" "<prompt>"` | Job ઉમેરો | 6 |
| `/personality [name]` | Session-level overlay | 2 |
| `/rollback`, `/rollback <N>`, `/rollback diff <N>` | Checkpoint પર પાછા (`checkpoints.enabled` જોઈએ) | 4 |

## Config keys જે આ પુસ્તકમાં આવ્યા ✅

| Key | Default | પ્રકરણ |
|---|---|---|
| `agent.max_turns` | `None` (અમર્યાદ) | 1 |
| `approvals.mode` | `smart` | 3 |
| `approvals.cron_mode` | `deny` | 3, 6 |
| `memory.memory_char_limit` / `user_char_limit` | `2200` / `1375` | 4 |
| `compression.threshold` | `0.50` | 4 |
| `compression.protect_last_n` | `20` | 4 |
| `compression.in_place` | `true` | 4 |
| `delegation.max_iterations` | `250` | 6 |
| `delegation.max_concurrent_children` | `10` | 6 |
| `prompt_caching.cache_ttl` | `auto` (`1h` માણસ સાથે, `5m` machine-paced) | 2 |
| `skills.index_desc_limit` | `60` (60–1024) | 5 |
| `agent.api_max_retries` | `3` | 1 |
| `checkpoints.enabled` | `false` | 4 |
