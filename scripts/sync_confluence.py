import os
import base64
import requests

CONFLUENCE_BASE_URL = os.environ["CONFLUENCE_BASE_URL"]  # e.g. https://quickbase.atlassian.net/wiki
CONFLUENCE_EMAIL = os.environ["CONFLUENCE_EMAIL"]
CONFLUENCE_API_TOKEN = os.environ["CONFLUENCE_API_TOKEN"]
GH_TOKEN = os.environ["GH_TOKEN"]
GH_REPO = os.environ["GH_REPO"]  # e.g. "Hankh005/Test-2"

OWNER, REPO = GH_REPO.split("/")

PAGE_IDS = ["6429147235", "6429769806"]


def fetch_page_markdown(page_id):
    url = f"{CONFLUENCE_BASE_URL}/api/v2/pages/{page_id}"
    params = {"body-format": "markdown"}
    resp = requests.get(
        url,
        params=params,
        auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("body", {}).get("markdown", {}).get("value", "")


def get_existing_sha(path):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def push_to_github(path, content, commit_message):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }

    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    body = {
        "message": commit_message,
        "content": encoded,
    }

    sha = get_existing_sha(path)
    if sha:
        body["sha"] = sha

    resp = requests.put(url, headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()


def sync_page(page_id):
    content = fetch_page_markdown(page_id)
    path = f"skills/{page_id}.md"
    push_to_github(path, content, f"sync: page {page_id}")
    print(f"Synced page {page_id}")


def main():
    for page_id in PAGE_IDS:
        sync_page(page_id)


if __name__ == "__main__":
    main()
