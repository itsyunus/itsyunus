import requests
import datetime
import json

LEETCODE_USERNAME = "your_leetcode_username"

# Headers for GraphQL
headers = {
    'Content-Type': 'application/json',
    'Referer': f'https://leetcode.com/YunuZCodes/',
    'User-Agent': 'Mozilla/5.0',
}

# GraphQL query to fetch user streak dat
query = {
    "operationName": "userCalendar",
    "variables": {"username": LEETCODE_USERNAME},
    "query": """
        query userCalendar($username: String!) {
            userCalendar(username: $username) {
                submissionCalendar
            }
        }
    """
}

# Send the POST request
res = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
data = res.json()

calendar = json.loads(data["data"]["userCalendar"]["submissionCalendar"])

# Calculate current streak
dates = sorted(int(day) for day in calendar.keys())
today = datetime.date.today()
streak = 0

for i in range(len(dates) - 1, -1, -1):
    date = datetime.datetime.fromtimestamp(dates[i]).date()
    if date == today or date == today - datetime.timedelta(days=streak):
        streak += 1
    else:
        break

# Update README.md between markers
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
