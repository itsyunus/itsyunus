import requests, datetime, json

LEETCODE_USERNAME = "yunuzcodes"  # lowercase
year = datetime.date.today().year

query = {
    "operationName": "userProfileCalendar",
    "variables": {"username": LEETCODE_USERNAME, "year": year},
    "query": """
      query userProfileCalendar($username: String!, $year: Int) {
        matchedUser(username: $username) {
          userCalendar(year: $year) {
            streak
            submissionCalendar
          }
        }
      }
    """
}

res = requests.post("https://leetcode.com/graphql", json=query, headers={
    "Content-Type": "application/json",
    "Referer": f"https://leetcode.com/{LEETCODE_USERNAME}/",
})
data = res.json()
print(json.dumps(data, indent=2))

# Validate response
cal = data.get("data", {}).get("matchedUser", {}).get("userCalendar")
if not cal:
    print("❌ Failed to fetch userCalendar. Check username or visibility.")
    exit(1)

current_streak = cal.get("streak", 0)
# Optionally parse calendar JSON if you want daily details
# submission_map = json.loads(cal["submissionCalendar"])

# Update README
with open("README.md", "r+") as f:
    content = f.read()
    start, end = "<!-- LEETCODE-STREAK-START -->", "<!-- LEETCODE-STREAK-END -->"
    new_section = f"{start}\n🔥 Current LeetCode Streak: `{current_streak}` days\n{end}"
    updated = content.split(start)[0] + new_section + content.split(end)[1]
    f.seek(0); f.write(updated); f.truncate()

print(f"✅ Updated streak: {current_streak}")
