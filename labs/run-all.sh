#!/usr/bin/env bash
# બધી book labs ચલાવો અને outputs evidence/ માં લખો. Repository root માંથી: bash labs/run-all.sh
set -euo pipefail
mkdir -p evidence
run() { echo "== $1"; shift; "$@" | tee "evidence/$OUT"; }
OUT=pravesh-toy-agent.out  run "પ્રવેશ"    python3 labs/pravesh/toy_agent.py
OUT=01-mini-loop.out       run "પ્રકરણ 1"  python3 labs/01-loop/mini_loop.py
OUT=02-cache-sim.out       run "પ્રકરણ 2"  python3 labs/02-prompt/cache_sim.py
OUT=03-mini-registry.out   run "પ્રકરણ 3"  python3 labs/03-tools/mini_registry.py
OUT=04-mini-memory.out     run "પ્રકરણ 4"  python3 labs/04-memory/mini_memory.py
OUT=05-check-skill.out     run "પ્રકરણ 5"  python3 labs/05-skills/check_skill.py labs/05-skills/lagna-mehmaan-yadi/SKILL.md
OUT=06-mini-gateway.out    run "પ્રકરણ 6"  python3 labs/06-gateway/mini_gateway.py
OUT=07-test-plugin.out     run "પ્રકરણ 7"  python3 labs/07-plugin/test_plugin.py
echo "બધી labs પાસ."
