import json
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone


API_URL = (
    "https://api.interschoolscoding.com"
    "/api/v1/practice/leaderboard/"
    "?limit=20&offset=0"
)

TARGET_NAME = "Akampurira Moris"


def fetch_leaderboard():
    request = Request(
        API_URL,
        headers={
            "User-Agent": "ISCC-Portfolio-Tracker/1.0"
        },
    )

    with urlopen(request, timeout=30) as response:
        return json.load(response)


def extract_moris(data):
    for student in data["leaderboard"]:
        if student["student_name"] == TARGET_NAME:
            return student

    raise RuntimeError(f"{TARGET_NAME} was not found in leaderboard.")


def build_snapshot(data, student):
    return {
        "rank": student["rank"],
        "student_name": student["student_name"],
        "school_name": student["school_name"],
        "total_points": student["total_points"],
        "challenges_solved": student["challenges_solved"],
        "total_students": data["pagination"]["total_count"],
        "submissions_this_week": student["recent_activity"][
            "submissions_this_week"
        ],
        "points_this_week": student["recent_activity"][
            "points_this_week"
        ],
        "last_updated": student["last_updated"],
        "synced_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    data = fetch_leaderboard()
    student = extract_moris(data)
    snapshot = build_snapshot(data, student)

    output = Path("src/data/iscc.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()