"""
Pulls every page from a Confluence space and writes it as Markdown under skills/,
mirroring the Confluence page hierarchy as nested folders (a page with children
becomes a folder containing README.md + its children; a leaf page becomes a file).

Runs inside GitHub Actions — see .github/workflows/confluence-sync.yml.

Required env vars:
  CONFLUENCE_BASE_URL    e.g. https://quickbase.atlassian.net/wiki
  CONFLUENCE_EMAIL       the Atlassian account email tied to the API token
  CONFLUENCE_API_TOKEN   https://id.atlassian.com/manage-profile/security/api-tokens
  CONFLUENCE_SPACE_ID    numeric space ID only, e.g. 6386384916 (no labels/parentheses)
"""
import os
import re
import sys
import requests
from collections import defaultdict
from markdownify import markdownify

BASE_URL = os.environ["CONFLUENCE_BASE_URL"].rstrip("/")
AUTH = (os.environ["CONFLUENCE_EMAIL"], os.environ["CONFLUENCE_API_TOKEN"])
SPACE_ID = os.environ["CONFLUENCE_SPACE_ID"]
OUTPUT_DIR = "skills"


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


def page_to_markdown(page: dict) -> str:
    storage_html = page.get("body", {}).get("storage", {}).get("value", "")
    if not storage_html.strip():
        return ""
    return markdownify(storage_html, heading_style="ATX").strip()


def unique_slug(title: str, used: set) -> str:
    """De-dupe slugs within a single directory only (siblings), not globally."""
    base = slugify(title)
    slug = base
    n = 1
    while slug in used:
        n += 1
        slug = f"{base}-{n}"
    used.add(slug)
    return slug


def write_page(page: dict, dir_path: str, sibling_slugs: set, children_map: dict) -> int:
    """Writes one page (as a file or folder+README) and recurses into its children.
    Returns count of files written."""
    written = 0
    title = page["title"]
    slug = unique_slug(title, sibling_slugs)
    children = children_map.get(page["id"], [])
    md = page_to_markdown(page)
    header = f"<!-- Synced from Confluence page {page['id']}: {title} -->\n\n"

    if children:
        folder = os.path.join(dir_path, slug)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "README.md"), "w") as f:
            f.write(header + (md + "\n" if md else ""))
        written += 1

        child_slugs: set = set()
        for child in sorted(children, key=lambda p: p["title"]):
            written += write_page(child, folder, child_slugs, children_map)
    else:
        path = os.path.join(dir_path, f"{slug}.md")
        with open(path, "w") as f:
            f.write(header + (md + "\n" if md else ""))
        written += 1

    return written


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages = get_all_pages()
    by_id = {p["id"]: p for p in pages}

    children_map = defaultdict(list)
    roots = []
    for p in pages:
        parent_id = p.get("parentId")
        if parent_id and parent_id in by_id:
            children_map[parent_id].append(p)
        else:
            # parentId missing, null, or points outside this page set (e.g. the space homepage)
            roots.append(p)

    total_written = 0
    root_slugs: set = set()

    for root in sorted(roots, key=lambda p: p["title"]):
        # Write the root page's own content (e.g. the space homepage) as skills/README.md,
        # then place its children directly under skills/ rather than nesting an extra folder.
        md = page_to_markdown(root)
        header = f"<!-- Synced from Confluence page {root['id']}: {root['title']} -->\n\n"
        if md:
            with open(os.path.join(OUTPUT_DIR, "README.md"), "w") as f:
                f.write(header + md + "\n")
            total_written += 1

        for child in sorted(children_map.get(root["id"], []), key=lambda p: p["title"]):
            total_written += write_page(child, OUTPUT_DIR, root_slugs, children_map)

    print(f"Synced {total_written} file(s)/folder(s) from {len(pages)} Confluence page(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
