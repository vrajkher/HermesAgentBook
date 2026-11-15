"""Tool handler. નિયમ: args dict લો, JSON string પાછી આપો, ક્યારેય raise ન કરો, **kwargs સ્વીકારો."""
import csv
import json


def _rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mehmaan_tally(args: dict, **kwargs) -> str:
    rsvp_path, caterer_path = args.get("rsvp_path"), args.get("caterer_path")
    if not rsvp_path or not caterer_path:
        return json.dumps({"error": "Need rsvp_path and caterer_path"})
    try:
        guests: dict[str, int] = {}
        maybe = 0
        for row in _rows(rsvp_path):
            status = row["confirmed"].strip().lower()
            if status == "yes":
                guests[row["event"]] = guests.get(row["event"], 0) + int(row["count"])
            elif status == "maybe":
                maybe += int(row["count"])
        plates = {row["event"]: int(row["plates"]) for row in _rows(caterer_path)}
    except (OSError, KeyError, ValueError) as e:
        return json.dumps({"error": f"Cannot read input: {type(e).__name__}: {e}"})

    events = []
    for event in sorted(set(guests) | set(plates)):
        g, p = guests.get(event), plates.get(event)
        if g is None or p is None:
            status = "missing_in_rsvp" if g is None else "missing_in_caterer"
        elif p < g:
            status = "shortage"
        elif (p - g) > 0.10 * g:
            status = "waste"
        else:
            status = "ok"
        events.append({"event": event, "guests": g, "plates": p,
                       "difference": None if g is None or p is None else p - g, "status": status})
    return json.dumps({"events": events, "unconfirmed_maybe": maybe,
                       "all_ok": all(e["status"] == "ok" for e in events)}, ensure_ascii=False)
