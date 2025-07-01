import requests
import json

LEETCODE_USERNAME = "yunuzcodes"  # Lowercase for GraphQL

headers = {
    'Content-Type': 'application/json',
    'Referer': f'https://leetcode.com/{LEETCODE_USERNAME}/',
    'User-Agent': 'Mozilla/5.0',
}

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

res = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
data = res.json()

# Debug print to inspect response
print("Response from LeetCode:")
print(json.dumps(data, indent=2))

if "data" not in data or not data["data"].get("userCalendar"):
    print("❌ Error: Failed to fetch calendar. Check username or visibility.")
    exit(1)

calendar = json.loads(data["data"]["userCalendar"]["submissionCalendar"])
