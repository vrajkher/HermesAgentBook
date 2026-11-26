# પરિશિષ્ટ A — Source index

Pinned commit: `93dd2a4efb0709ceac09969b85d306e768b53815` (`main`, 2026-11-26). પહેલું version: `18e659d` (2026-11-15); ફેરફારો [verification log](F-verification-log.md) માં. પૂર્ણ generated table, દરેક line range સાથે: [citations.generated.md](citations.generated.md).

## પ્રકરણ પ્રમાણે મુખ્ય files

| પ્રકરણ | Hermes files | શું જોવું |
|---|---|---|
| 0 | `AGENTS.md`, `hermes_constants.py`, `website/docs/developer-guide/architecture.md` | બે invariants; `get_hermes_home()`; facade અને topic folders; `hermes_state.py` deprecation |
| 1 | `run_agent.py`, `agent/turn_facade.py`, `agent/conversation_loop.py`, `agent/iteration_budget.py`, `agent/AGENTS.md` | `AIAgent`; `chat()`; `while`; `IterationBudget`; message-flow invariants |
| 2 | `agent/system_prompt.py`, `agent/prompt_builder.py`, `agent/prompt_caching.py`, `agent/subdirectory_hints.py` | ત્રણ tiers; `invalidate_system_prompt()`; cache breakpoints |
| 3 | `tools/registry.py`, `toolsets.py`, `model_tools.py`, `tools/approval_detection.py`, `tools/todo_tool.py` | discovery; `register`; `get_definitions`; `dispatch`; patterns |
| 4 | `tools/memory_tool.py`, `tools/memory_tool_store.py`, `persistence/core/backend.py`, `persistence/sqlite/`, `agent/context_compressor.py`, `agent/checkpoints/manager.py`, `hermes_cli/config_defaults.py` | મર્યાદા; snapshot; `SessionDB`; FTS5; compression defaults |
| 5 | `skills/AGENTS.md`, `agent/skill_utils.py`, `website/docs/user-guide/features/skills.md` | authoring standards; description limit; curator |
| 6 | `gateway/authz_mixin.py`, `gateway/session.py`, `gateway/AGENTS.md`, `cron/AGENTS.md`, `cron/scheduler.py`, `tools/delegate_tool*.py` | authorization; session key; guards; cron invariants; blocked tools |
| 7 | `plugins/AGENTS.md`, `hermes_cli/plugins_context.py`, `website/docs/developer-guide/plugins/index.md` | "never touch core"; `register_tool`; hooks; rubric |

## Citations ફરી બનાવવા અને ચકાસવા

```bash
python3 tools/citations.py <pinned hermes-agent checkout>
```

દરેક citation એક "needle" (શબ્દસમૂહ) થી બંધાયેલું છે. Script checkout માં needle શોધે છે, line range pin કરે છે, દરેક file ના અંતે reference links ફરી લખે છે, અને દરેક reference-style citation અને relative link ચકાસે છે. Needle ન મળે તો script fail થાય: એટલે બીજા commit પર pin બદલો તો ખબર પડે કે કયો દાવો ફરી તપાસવો.
