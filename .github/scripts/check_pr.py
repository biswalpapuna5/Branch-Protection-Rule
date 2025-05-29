import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_REF").split("/")[-1]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Get PR details
pr_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
pr_response = requests.get(pr_url, headers=headers)
pr_data = pr_response.json()

# Check if it's from a feature branch
source_branch = pr_data['head']['ref']
target_branch = pr_data['base']['ref']

if not source_branch.startswith("feature/") or target_branch != "dev":
    print(f"❌ PR not from feature/* to dev. Source: {source_branch}, Target: {target_branch}")
    exit(1)

# Check combined status
sha = pr_data['head']['sha']
status_url = f"https://api.github.com/repos/{REPO}/commits/{sha}/status"
status_response = requests.get(status_url, headers=headers)
status_data = status_response.json()

state = status_data['state']
print(f"✅ Combined status for {sha}: {state}")

if state != "success":
    print("❌ Not all status checks passed.")
    exit(1)

print("✅ All required checks passed. Ready to merge.")
