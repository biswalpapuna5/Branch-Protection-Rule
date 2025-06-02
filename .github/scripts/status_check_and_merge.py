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

def comment_on_pr(message):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    data = {"body": message}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 201:
        print(f"❌ Failed to post comment: {resp.status_code} - {resp.text}")
        resp.raise_for_status()
    print("💬 Comment posted on PR.")

def main():
    sha = get_pr_commit_sha()
    status = get_commit_status(sha)
    print(f"🔍 Status for commit {sha}: {status}")

    if status == "success":
        comment_on_pr("✅ All required status checks have passed. You can now manually merge this pull request.")
    elif status in ["failure", "error"]:
        comment_on_pr("❌ Status checks failed. Please fix the issues before merging.")
        exit(1)  # Fail the job to block merge if checks fail
    elif status == "pending":
        comment_on_pr("⏳ Status checks are still pending. Please wait until they complete before merging.")
        exit(1)  # Fail the job to block merge until status is success
    else:
        comment_on_pr(f"⚠️ Unknown status: `{status}`. Manual review may be required.")
        exit(1)

if __name__ == "__main__":
    main()
