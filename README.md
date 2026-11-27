# Hermes Agent: 12મા ધોરણથી Expert Developer સુધી

એક ગુજરાતી પુસ્તક, જે એક જ વાર્તા — વડોદરાનું **"શુભમંગલ વેડિંગ પ્લાનર્સ"** — માં [Hermes Agent](https://github.com/NousResearch/hermes-agent) ને અંદરથી શીખવે છે. વાર્તા શણગાર નથી: ઑફિસની દરેક ઘટના Hermes નો એક નિયમ છે, તેના કારણ સાથે.

- **વિષય:** [Hermes Agent](https://github.com/NousResearch/hermes-agent) — Nous Research નો "self-improving AI agent": agent loop, prompt caching, tools, memory, skills, messaging gateway, cron, subagents, plugins.
- **Pinned commit:** [`93dd2a4`](https://github.com/NousResearch/hermes-agent/tree/93dd2a4efb0709ceac09969b85d306e768b53815) (`main`, 2026-11-26). દરેક source link આ commit પર pinned છે. પહેલું version `18e659d` (2026-11-15) પર હતું; શું બદલાયું તે [verification log](appendix/F-verification-log.md) અને [પ્રકરણ 0, દૃશ્ય 6](book/00-paayo-ane-pratham-run.md) માં.
- **વાચક:** 12મું ધોરણ પાસ કરેલો કોઈ પણ વિદ્યાર્થી, programming ન આવડતું હોય તો પણ. [પ્રવેશ પ્રકરણ](book/pravesh-shunya-thi-shuruaat.md) શૂન્યથી શરૂ કરે છે; પ્રકરણ 7 ના અંતે તમે plugin લખો છો અને maintainer ની જેમ PR આંકો છો.
- **API key જરૂરી નથી.** બધી labs ફક્ત Python standard library પર ચાલે છે.

> 📖 **Web આવૃત્તિ — online વાંચો:** <https://claude.ai/artifact/PB9WSBnZxSWUF7Bm96eEUZ>
> આખું પુસ્તક એક પાનામાં: દરેક પ્રકરણનું ચિત્ર, રંગીન વાર્તા-ખાનાં, વિષયસૂચિ, light/dark mode, અક્ષરનું કદ નાનું-મોટું, phone પર પણ. આ પાનું [`tools/build-artifact.py`](tools/build-artifact.py) આ repository ની files પરથી બનાવે છે.

> **Verification marks:** ✅ pinned source વાંચીને ચકાસ્યું · 🧪 આ પુસ્તક લખતી વખતે ચલાવીને ચકાસ્યું · ⚠️ ચકાસ્યું નથી.
>
> **પ્રામાણિક નોંધ:** આ પુસ્તક જ્યાં લખાયું ત્યાં Hermes Agent install કરવાની પરવાનગી નહોતી. એટલે પુસ્તકની પોતાની labs 🧪 છે; `hermes …` commands docs/source માંથી ✅ છે, પણ ચલાવેલા નથી ⚠️. વિગત: [verification log](appendix/F-verification-log.md).
>
> Hermes model એ બનાવેલા commands ચલાવી શકે છે. વાપરતાં પહેલાં upstream [SECURITY.md](https://github.com/NousResearch/hermes-agent/blob/93dd2a4efb0709ceac09969b85d306e768b53815/SECURITY.md) વાંચો.

## વાર્તા એક ફકરામાં

**ઈશા** 12મું પાસ કરીને college ની રાહ જુએ છે; તેની મમ્મી **સ્મિતાબેન** વેડિંગ-પ્લાનિંગ ઑફિસ ચલાવે છે, અને ડિસેમ્બરમાં પટેલ પરિવારનાં લગ્ન છે. Software engineer **નિખિલમામા** 14 દિવસ રોજ એક પગથિયું શીખવે છે, અને ઑફિસ જ પ્રયોગશાળા બને છે: **શાસ્ત્રીજી** = AI model (કાશીમાં; ફક્ત ફોન પર; શબ્દ દીઠ ફી; ફોન મૂકતાં જ બધું ભૂલે), **હર્ષ** = agent loop, **સૂચના-પાટી** = system prompt, **ફી-માફી** = prompt cache, **ઓજાર-કબાટ** = tool registry, **સ્મિતાબેનની સહી** = approval, **ખિસ્સા-ડાયરી** = memory, **રોજમેળ** = session DB, **રીત-પોથી** = skills, **બારીઓ** = gateway, **એલાર્મ-ચોપડી** = cron, **શિખાઉ** = subagents, **બહારના કારીગર** = plugins. છેલ્લે ઈશા ખરો પ્રશ્ન ઉકેલે છે: મહેમાન-યાદી અને કેટરરની થાળી મેળવવી.

આખું પુસ્તક Hermes ની **બે invariants** પર ઊભું છે:

1. *"Per-conversation prompt caching is sacred."* → **"પાટી દિવસભર અડશો નહીં."**
2. *"The core is a narrow waist; capability lives at the edges."* → **"કબાટ નાનો રાખો; નવું ઓજાર બહારના કારીગર લાવે."**

## વિષયસૂચિ

શરૂઆત [સમગ્ર નકશો](book/overview-samagra-naksho.md) થી કરો.

| Level | દિવસ | પ્રકરણ | મુખ્ય lab |
|---|---|---|---|
| — | — | **[સમગ્ર નકશો — આખું પુસ્તક એક નજરે](book/overview-samagra-naksho.md)** | પાત્રો, 14 ઘટના → 14 નિયમ, બે invariants |
| −1 | 1 | [પ્રવેશ — શૂન્યથી શરૂઆત](book/pravesh-shunya-thi-shuruaat.md) | terminal, JSON/YAML, model/API/token; 45-line રમકડા-agent |
| 0 | 2 | [પાયો અને પ્રથમ run](book/00-paayo-ane-pratham-run.md) | `~/.hermes` નું ઘર, commit pinning અને re-pin, facade અને topic folders |
| 1 | 3–4 | [એક સંદેશાની આખી મુસાફરી](book/01-ek-sandesh-ni-musafari.md) | Turn vs iteration, `while` loop, budget, alternation, interrupt |
| 2 | 5 | [સૂચના-પાટી: prompt અને cache](book/02-suchna-pati-prompt-ane-cache.md) | ત્રણ tiers; એક લીટીનો ભાવ (cache simulation) |
| 3 | 6–7 | [ઓજાર-કબાટ: tools](book/03-ojar-kabat-tools.md) | Registry, `check_fn`, dispatch, footprint ladder, approval |
| 4 | 8–9 | [યાદ: memory, sessions, compression](book/04-yaad-memory-sessions.md) | Frozen snapshot, SQLite FTS5, compression ના 4 તબક્કા |
| 5 | 10 | [રીત-પોથી: skills](book/05-reet-pothi-skills.md) | `SKILL.md` લખો અને standards સામે તપાસો; curator |
| 6 | 11–12 | [બારીઓ, ઘડિયાળ અને શિખાઉ](book/06-bario-ghadiyal-shikhau.md) | Gateway authz, session key, at-most-once cron, delegation |
| 7 | 13–14 | [પોતાનું ઓજાર અને mastery](book/07-potanu-ojar-ane-mastery.md) | `mehmaan-tally` plugin, contribution rubric, mastery પરીક્ષા, [expert ની દસ ટેવો](book/07-potanu-ojar-ane-mastery.md#upsanhar) |

### પરિશિષ્ટ

- [A — Source index](appendix/A-source-index.md) (પૂર્ણ generated table: [citations.generated.md](appendix/citations.generated.md))
- [B — Command reference](appendix/B-command-reference.md)
- [C — ગુજરાતી–English glossary](appendix/C-glossary.md) (દરેક શબ્દ વાર્તાની ઉપમા સાથે)
- [D — Lab solutions અને mastery check જવાબો](appendix/D-lab-solutions.md)
- [E — Mastery rubric](appendix/E-mastery-rubric.md)
- [F — Verification log](appendix/F-verification-log.md) (શું ચકાસ્યું, શું નહીં, docs-vs-code તફાવતો)

## આ પુસ્તક કેવી રીતે શીખવે છે

દરેક પ્રકરણ **દૃશ્યો** માં ચાલે છે, અને દરેક દૃશ્ય ચાર પગથિયાંમાં:

| નિશાન | પગથિયું | ઉદાહરણ (પ્રકરણ 4) |
|---|---|---|
| 🎬 | **ઘટના** — ઑફિસમાં કંઈક બને છે | હર્ષે ડાયરીમાં લખ્યું; દસ મિનિટ પછી પાટી પર તે નથી. |
| ❓ | **ઈશાનો પ્રશ્ન** | "હમણાં જ લખ્યું હતું! ક્યાં ગયું?" |
| 💻 | **Code માં** — એ જ નિયમ pinned source માં | Memory = frozen snapshot: session શરૂઆતમાં એક વાર; `_system_prompt_snapshot`. |
| 🔬 | **Expert નજર** — નિયમ કેમ બન્યો, તૂટે તો શું બગડે | Bug જેવું લાગે છે તે cache invariant નું અનિવાર્ય પરિણામ છે. |

દરેક પ્રકરણનો ક્રમ: 🎯 શું કરી શકશો → 🗺️ નકશો → દૃશ્યો → Source map → 🧪 Lab ("પહેલાં ધાર, પછી ચલાવ") → 🔮 આગાહી કસોટી → 🩺 નિષ્ફળતા અને નિદાન → ✅ સાર (ઘટના → નિયમ, શબ્દો, યાદ-ચાવીઓ, ગેરસમજો, પુનરાવર્તન કાર્ડ) → 🧠 Mastery check → 🎬 આગળ શું.

Code હંમેશા ઓળખાવેલો છે: **repository code** (Hermes નો, pinned link સાથે) કે **book lab code** (આ પુસ્તકનો).

## Repository layout

| Folder | શું છે |
|---|---|
| `book/` | સમગ્ર નકશો, પ્રવેશ, પ્રકરણ 0–7 |
| `appendix/` | પરિશિષ્ટ A–F અને generated citation table |
| `labs/` | પુસ્તક-માલિકીનો code: આઠ runnable labs, એક skill, એક plugin — [labs/README.md](labs/README.md) |
| `evidence/` | Labs નાં ચલાવેલાં outputs |
| `book/images/chapters/` | દરેક પ્રકરણનું ચિત્ર (SVG), `tools/make-illustrations.py` થી બનેલું |
| `tools/` | `citations.py` (citations pin + links ચકાસણી), `make-illustrations.py` (ચિત્રો), `build-artifact.py` (web આવૃત્તિ) |

## Labs ઝડપથી શરૂ કરો

```bash
python3 labs/pravesh/toy_agent.py
```

અપેક્ષિત છેલ્લી line: `જવાબ: પટેલ પરિવારના લગ્નમાં 5 પ્રસંગ છે.`

બધી labs એકસાથે:

```bash
bash labs/run-all.sh
```

Windows (PowerShell) પર, કે bash વગર ગમે ત્યાં:

```powershell
py labs\run_all.py
```

અપેક્ષિત છેલ્લી line: `બધી labs પાસ.` Windows પર Hermes install કરવાનાં પગલાં: [પ્રકરણ 0 — Windows પર](book/00-paayo-ane-pratham-run.md).

## પુસ્તક ચકાસવું (maintainers માટે)

```bash
git clone https://github.com/NousResearch/hermes-agent.git && git -C hermes-agent checkout --detach 93dd2a4efb0709ceac09969b85d306e768b53815
```

```bash
python3 tools/citations.py hermes-agent
```

આ command દરેક citation ને pinned checkout સામે ફરી pin કરે છે, reference links ફરી લખે છે, અને દરેક citation key અને relative link ચકાસે છે. Checkout વગર (`python3 tools/citations.py`) તે lock file વાપરીને ફક્ત links ચકાસે છે.

Web આવૃત્તિ ફરી બનાવવા:

```bash
python3 tools/make-illustrations.py
```

```bash
python3 tools/build-artifact.py book.html
```

## License

આ પુસ્તકનો text અને `labs/` નો code આ repository ના [LICENSE](LICENSE) હેઠળ છે. Hermes Agent ના quoted excerpts upstream MIT license હેઠળ છે.
