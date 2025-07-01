import requests
import datetime
import json

LEETCODE_USERNAME = "yunuzcodes"  # Use your username in lowercase

year = datetime.datetime.now().year

headers = {
    'Content-Type': 'application/json',
    'Referer': f'https://leetcode.com/{LEETCODE_USERNAME}/',
    'User-Agent': 'Mozilla/5.0',
}

query = {
    "operationName": "userProgressCalendarV2",
    "variables": {
        "username": LEETCODE_USERNAME,
        "year": year,
        "queryType": "YEARLY"
    },
    "query": """
        query userProgressCalendarV2($username: String!, $year: Int!, $queryType: ProgressCalendarQueryTypeEnum!) {
            userProgressCalendarV2(username: $username, year: $year, queryType: $queryType) {
                dailySubmissionData {
                    date
                    count
                }
            }
        }
    """
}

res = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
data = res.json()

# Debug print
print("Response from LeetCode:")
print(json.dumps(data, indent=2))

# Handle error
if "data" not in data or not data["data"].get("userProgressCalendarV2"):
    print("❌ Error: Failed to fetch calendar. Check username or visibility.")
    exit(1)

submissions = data["data"]["userProgressCalendarV2"]["dailySubmissionData"]

# Convert to date -> count dict
submission_map = {s["date"]: s["count"] for s in submissions}

# Calculate streak
today = datetime.date.today()
streak = 0

for i in range(0, 365):
    date = today - datetime.timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")
    if submission_map.get(date_str, 0) > 0:
        streak += 1
    else:
        break

# Update README.md
README_FILE = "README.md"
START_MARKER = "<!-- LEETCODE-STREAK-START -->"
END_MARKER = "<!-- LEETCODE-STREAK-END -->"

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

new_content = f"{START_MARKER}\n🔥 Current LeetCode Streak: `{streak}` days\n{END_MARKER}"
updated = (
    content.split(START_MARKER)[0]
    + new_content
    + content.split(END_MARKER)[1]
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(updated)

print(f"✅ Updated README with current streak: {streak} days")
