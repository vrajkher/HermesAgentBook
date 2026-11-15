---
name: lagna-mehmaan-yadi
description: Reconcile a wedding guest list with caterer counts.
version: 1.0.0
author: Isha (Shubhmangal Wedding Planners), Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wedding, guests, csv, reconciliation]
    category: productivity
---

# Lagna Mehmaan Yadi Skill

Compares the RSVP guest list with the caterer's plate count for one event and reports the
difference. It does not message guests or change either file.

## When to Use

- The user asks whether the guest list and the caterer's count match.
- A wedding event (mehndi, sangeet, lagna, reception) is within seven days.

## Prerequisites

- `rsvp.csv` with columns `family,event,confirmed,count`.
- `caterer.csv` with columns `event,plates`.

## How to Run

1. Read both files with `read_file`. Never guess a count that is not in a file.
2. Add `count` for rows where `confirmed` is `yes`, per event.
3. Compare each event total with `plates` in `caterer.csv`.

## Quick Reference

| Result | Meaning |
|---|---|
| `plates - guests >= 0` and under 5% | OK, normal buffer |
| `plates - guests < 0` | Shortage: tell the user first |
| buffer over 10% | Waste: suggest a lower plate count |

## Procedure

1. List every event found in either file. An event in only one file is itself a finding.
2. Report one line per event: guests, plates, difference.
3. Ask before any follow-up action; this skill only reports.

## Pitfalls

- Rows with `confirmed` = `maybe` are not guests yet: counting them hides a shortage,
  because the caterer is paid per confirmed plate.
- The same family can appear once per event: totals are per event, never per family.

## Verification

- The per-event guest totals add up to the grand total of confirmed `count` values.
- Every number in the report can be traced to a row in one of the two files.
