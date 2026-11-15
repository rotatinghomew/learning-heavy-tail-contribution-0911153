from app.contributions import contribution_profile
from collections import defaultdict
from app.protocol import finite, unique


def validate(packet):
    if not packet["revision"]:
        raise ValueError("missing revision")
    unique(packet["roster"], "person")
    people = {row["person"] for row in packet["roster"]}
    for row in packet["sessions"]:
        if row["person"] not in people:
            raise ValueError("unknown contributor")
        if row["hours"] is not None and finite(row["hours"], "hours") < 0:
            raise ValueError("negative hours")
        if row["capped"] and row["hours"] != row["cap"]:
            raise ValueError("invalid capped observation")


def recorded_hours(packet, options):
    totals = defaultdict(float)
    capped = missing = 0
    for row in packet["sessions"]:
        if row["hours"] is None:
            missing += 1
        else:
            totals[row["person"]] += row["hours"]
        capped += row["capped"]
    ordered = sorted(totals.values(), reverse=True)
    total = sum(ordered)
    return {"source_profile": contribution_profile(packet), "roster_size": len(packet["roster"]), "recorded_hours": total,
            "capped_records": capped, "missing_records": missing,
            "top_five_recorded_share": sum(ordered[:5]) / total if total else None,
            "interpretation": "Recorded hours retain caps and missingness; this is neither true total nor future capacity."}


ANALYSES = {"recorded_hours": recorded_hours}
