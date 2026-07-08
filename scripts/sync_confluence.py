"""
Pulls every page from a Confluence space and writes it as a Markdown file under skills/.
Runs inside GitHub Actions — see .github/workflows/confluence-sync.yml.

Required env vars:
  CONFLUENCE_BASE_URL    e.g. https://quickbase.atlassian.net/wiki
  CONFLUENCE_EMAIL       the Atlassian account email tied to the API token
  CONFLUENCE_API_TOKEN   https://id.atlassian.com/manage-profile/security/api-tokens
  CONFLUENCE_SPACE_ID    numeric space ID (e.g. 6386384916 for IAS)
"""
import os
import re
import sys
import requests
from markdownify import markdownify

BASE_URL = os.environ["CONFLUENCE_BASE_URL"].rstrip("/")
AUTH = (os.environ["CONFLUENCE_EMAIL"], os.environ["CONFLUENCE_API_TOKEN"])
SPACE_ID = os.environ["CONFLUENCE_SPACE_ID"]
OUTPUT_DIR = "skills"

# Titles to skip — structural/container pages that aren't actual skill content.
# Edit this list to match your space's navigation pages.
SKIP_TITLES = {
    "Internal AI Skills",
    "Enterprise Skills",
    "Team Skills",
    "Template - How-to guide",
    "Template - Troubleshooting article",
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled"


def get_all_pages() -> list[dict]:
    pages = []
    url = f"{BASE_URL}/api/v2/spaces/{SPACE_ID}/pages"
    params = {"limit": 100, "body-format": "storage"}

    while url:
        r = requests.get(url, params=params, auth=AUTH, timeout=30)
        r.raise_for_status()
        data = r.json()
        pages.extend(data["results"])

        next_link = data.get("_links", {}).get("next")
        if next_link:
            url = f"{BASE_URL}{next_link}" if next_link.startswith("/") else next_link
            params = {}  # next_link already has query params baked in
        else:
            url = None

    return pages


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages = get_all_pages()

    written, skipped = 0, 0
    seen_slugs = {}

    for page in pages:
        title = page["title"]
        if title in SKIP_TITLES:
            skipped += 1
            continue

        storage_html = page.get("body", {}).get("storage", {}).get("value", "")
        if not storage_html.strip():
            skipped += 1
            continue

        md_body = markdownify(storage_html, heading_style="ATX").strip()

        slug = slugify(title)
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            slug = f"{slug}-{seen_slugs[slug]}"
        else:
            seen_slugs[slug] = 0

        path = os.path.join(OUTPUT_DIR, f"{slug}.md")
        with open(path, "w") as f:
            f.write(f"<!-- Synced from Confluence page {page['id']}: {title} -->\n\n")
            f.write(md_body + "\n")

        written += 1

    print(f"Synced {written} page(s), skipped {skipped}.", file=sys.stderr)


if __name__ == "__main__":
    main()
