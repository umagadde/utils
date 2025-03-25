# 6️⃣ Priority ↔ Status
# Critical issues are usually not in Backlog for too long.
# Low-priority issues may sit in Backlog longer.

# 7️⃣ Assignee ↔ Status
# If an issue is assigned to someone, it's probably not in Backlog.
# If an issue is In Progress, it must have an assignee.

# 8️⃣ Sprint ↔ Rank
# If an issue is in Backlog, its rank should be lower (e.g., > 100).
# If an issue is in an Active Sprint, it should have a high rank (e.g., 1-50).
# '''


# Fixing all the dependencies here ..... 

import pandas as pd
import random
from datetime import datetime, timedelta

# Helper function to generate a start date for future sprints
def future_start_date():
    return datetime.today() + timedelta(days=random.randint(5, 30))

# Define 6 sprints with fixed start/end dates & consistent states
sprint_data = {
    "Sprint 1": {"state": "Completed", "start_date": datetime(2024, 1, 1), "end_date": datetime(2024, 1, 14)},
    "Sprint 2": {"state": "Completed", "start_date": datetime(2024, 1, 15), "end_date": datetime(2024, 1, 28)},
    "Sprint 3": {"state": "Active", "start_date": datetime(2024, 2, 1), "end_date": datetime(2024, 2, 14)},
    "Sprint 4": {"state": "Active", "start_date": datetime(2024, 2, 15), "end_date": datetime(2024, 2, 28)},
    "Sprint 5": {"state": "Future", "start_date": future_start_date(), "end_date": None},  # Will be calculated below
    "Sprint 6": {"state": "Future", "start_date": future_start_date(), "end_date": None},  # Will be calculated below
}

# Calculate end dates for future sprints (2-week duration)
for sprint in ["Sprint 5", "Sprint 6"]:
    sprint_data[sprint]["end_date"] = sprint_data[sprint]["start_date"] + timedelta(days=14)

# Define possible values
projects = ["E-Commerce", "Banking App", "Healthcare System", "Logistics Platform"]
statuses = ["Backlog", "To Do", "In Progress", "Review", "Done"]
assignees = ["Alice", "Bob", "Charlie", "David", "Eve", None]  # None for unassigned
priorities = ["High", "Medium", "Low", "Critical"]
issue_types = ["Story", "Bug", "Task", "Epic"]
epics = ["EPIC-1", "EPIC-2", "EPIC-3", "EPIC-4"]
resolutions = ["Fixed", "Won't Fix", "Duplicate", None]

# Create dataset
data = []
for i in range(1, 201):
    project = random.choice(projects)

    # Pick a sprint and use its predefined details
    sprint_name = random.choice(list(sprint_data.keys()))
    sprint_details = sprint_data[sprint_name]

    sprint_state = sprint_details["state"]
    sprint_start = sprint_details["start_date"]
    sprint_end = sprint_details["end_date"]

    # Assign a status based on sprint state
    if sprint_state == "Future":
        status = random.choice(["Backlog", "To Do"])
    elif sprint_state == "Completed":
        status = "Done"
    else:  # Active
        status = random.choice(["To Do", "In Progress", "Review", "Done"])

    # Resolution: Only for "Done" status
    resolution = random.choice(resolutions) if status == "Done" else None

    # Issue Type & Story Points Logic
    issue_type = random.choice(issue_types)
    story_points = random.choice([1, 2, 3, 5, 8, 13]) if issue_type in ["Story", "Epic"] else None

    # Epic Link: Epics do NOT have an epic link, but other types may
    epic_link = None if issue_type == "Epic" else random.choice(epics)

    # Priority & Status Interdependency
    priority = random.choice(priorities)
    if priority == "Critical" and status in ["Backlog", "To Do"]:
        status = "In Progress"

    # Assignee Logic: "In Progress" must have an assignee
    assignee = random.choice(assignees) if status != "Backlog" else None

    # Rank Logic: Higher rank for backlog issues, lower rank for active sprint issues
    rank = random.randint(101, 200) if status == "Backlog" else random.randint(1, 50)

    # Create entry
    data.append({
        "id": i,
        "key": f"{project[:3].upper()}-{i}",
        "project": project,
        "summary": f"Task {i} for {project}",
        "description": f"Description for task {i} in {project}",
        "status": status,
        "assignee": assignee,
        "reporter": random.choice(assignees),
        "priority": priority,
        "issuetype": issue_type,
        "created": (datetime.today() - timedelta(days=random.randint(5, 90))).strftime("%Y-%m-%d"),
        "updated": (datetime.today() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
        "resolution": resolution,
        "labels": random.choice([["backend"], ["frontend"], ["bugfix"], ["enhancement"], ["UI"], []]),
        "components": random.choice([["Auth Service"], ["Payment Service"], ["UI"], ["API"], ["Database"]]),
        "sprint": sprint_name if status != "Backlog" else None,  # Backlog issues have no sprint
        "sprintId": random.randint(10, 50) if status != "Backlog" else None,
        "sprintState": sprint_state if status != "Backlog" else None,
        "sprintStartDate": sprint_start.strftime("%Y-%m-%d") if status != "Backlog" else None,
        "sprintEndDate": sprint_end.strftime("%Y-%m-%d") if status != "Backlog" else None,
        "storyPoints": story_points,
        "epicLink": epic_link,
        "rank": rank,
        "column": status if status != "Backlog" else "Backlog",
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("new_custom.csv", index=False)

