from collections import defaultdict


def contribution_profile(packet):
    people = {row["person"]: {"lower_recorded_hours": 0.0, "observed_records": 0, "capped_records": 0, "missing_records": 0}
              for row in packet["roster"]}
    teams = defaultdict(lambda: {"people": set(), "recorded_hours": 0.0, "events": set()})
    for session in packet["sessions"]:
        person = people[session["person"]]
        team = teams[session["team"]]
        team["people"].add(session["person"])
        team["events"].add(session["team_event"])
        if session["hours"] is None:
            person["missing_records"] += 1
        else:
            person["observed_records"] += 1
            person["lower_recorded_hours"] += session["hours"]
            team["recorded_hours"] += session["hours"]
        person["capped_records"] += session["capped"]
    by_person = [{"person": identity, **values} for identity, values in sorted(people.items())]
    return {"people": by_person,
            "teams": [{"team": identity, "people": len(values["people"]), "events": len(values["events"]),
                       "recorded_hours": values["recorded_hours"]} for identity, values in sorted(teams.items())],
            "current_roster": len(people), "next_roster": len(packet["scenario_roster"]),
            "next_roster_recorded_hours": sum(people[identity]["lower_recorded_hours"] for identity in packet["scenario_roster"]),
            "interpretation": "Person and team records are descriptive; no finite upper tail or future promise is asserted."}
