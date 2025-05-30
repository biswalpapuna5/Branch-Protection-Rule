import os
import requests

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_pr_commit_sha():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["head"]["sha"]

def get_commit_status(sha):
    url = f"{GITHUB_API}/repos/{REPO}/commits/{sha}/status"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["state"]

def enable_auto_merge():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}/merge"
    data = {
        "merge_method": "merge"
    }
    resp = requests.put(url, headers=headers, json=data)
    if resp.status_code == 200:
        print("✅ Merge successful.")
    else:
        print(f"⚠️ Merge not done: {resp.status_code} - {resp.text}")

def main():
    sha = get_pr_commit_sha()
    status = get_commit_status(sha)
    print(f"Status for commit {sha}: {status}")
    
    if status == "success":
        print("✔️ Status checks passed. Attempting to merge.")
        enable_auto_merge()
    else:
        print("❌ Status checks failed. Merge is disabled.")

if __name__ == "__main__":
    main()
