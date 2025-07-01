import requests
import datetime
import json

LEETCODE_USERNAME = "yunuzcodes"  # your username (lowercase)

headers = {
    'Content-Type': 'application/json',
    'Referer': f'https://leetcode.com/{LEETCODE_USERNAME}/',
    'User-Agent': 'Mozilla/5.0',
}

query = {
    "operationName": "userProgressCalendarV2",
    "variables": {"username": LEETCODE_USERNAME},
    "query": """
        query userProgressCalendarV2($username: String!) {
            userProgressCalendarV2(username: $username) {
                submissionCalendar
            }
        }
    """
}

res = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
data = res.json()

# Debug print
print("Response from LeetCode:")
print(json.dumps(data, indent=2))

# Error check
if "data" not in data or not data["data"].get("userProgressCalendarV2"):
    print("❌ Error: Failed to fetch calendar. Check username or visibility.")
    exit(1)

calendar_str = data["data"]["userProgressCalendarV2"]["submissionCalendar"]
calendar = json.loads(calendar_str)

# Calculate streak
dates = sorted(int(day) for day in calendar.keys())
today = datetime.date.today()
streak = 0

for i in range(len(dates) - 1, -1, -1):
    date = datetime.datetime.fromtimestamp(dates[i]).date()
    if date == today or date == today - datetime.timedelta(days=streak):
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

print(f"✅ Streak updated: {streak} days")
