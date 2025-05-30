import os
import requests

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_latest_commit_sha():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["head"]["sha"]

def get_commit_status(sha):
    url = f"{GITHUB_API}/repos/{REPO}/commits/{sha}/status"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["state"]

def comment_on_pr(message):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    data = { "body": message }
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    print("💬 Comment posted on PR.")

def main():
    sha = get_latest_commit_sha()
    status = get_commit_status(sha)
    print(f"🔍 Status for commit {sha}: {status}")

    if status == "success":
        comment_on_pr("✅ All status checks passed. Ready to merge.")
    elif status in ["failure", "error"]:
        comment_on_pr("❌ Status checks failed. Please fix the issues before merging.")
    elif status == "pending":
        comment_on_pr("⏳ Status checks are still pending. Please wait until they complete.")
    else:
        comment_on_pr(f"⚠️ Unknown status: {status}. Manual review needed.")

if __name__ == "__main__":
    main()
