"""Tool schema — model આ description વાંચીને નક્કી કરે છે કે tool ક્યારે વાપરવું."""

MEHMAAN_TALLY = {
    "name": "mehmaan_tally",
    "description": (
        "Compare a wedding RSVP CSV (columns: family,event,confirmed,count) with a caterer CSV "
        "(columns: event,plates) and return, per event, confirmed guests, plates and the "
        "difference. Read-only: never edits either file. Use it when the user asks whether the "
        "guest list and the catering order match."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "rsvp_path": {"type": "string", "description": "Path to the RSVP CSV file"},
            "caterer_path": {"type": "string", "description": "Path to the caterer CSV file"},
        },
        "required": ["rsvp_path", "caterer_path"],
    },
}
