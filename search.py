"""Web search + page reading. Everything here is free and needs no API key."""

import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# The search library was renamed from "duckduckgo_search" to "ddgs".
# This works with whichever one is installed.
try:
    from ddgs import DDGS
except ImportError:  # pragma: no cover
    from duckduckgo_search import DDGS


class SearchError(Exception):
    """Raised when the web search itself fails."""


# Sites that need JavaScript or a login, so we can't read them.
SKIP_DOMAINS = (
    "youtube.com", "youtu.be", "facebook.com", "instagram.com", "tiktok.com",
    "twitter.com", "x.com", "linkedin.com", "pinterest.com", "quora.com",
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def domain_of(url):
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def search_web(query, max_results=8):
    """Return a list of {title, url, snippet} from DuckDuckGo."""
    try:
        raw = DDGS().text(query, max_results=max_results)
    except Exception as exc:
        raise SearchError(
            "The web search didn't respond. Wait a few seconds and try again. "
            f"(Details: {exc})"
        ) from exc

    results, seen = [], set()
    for item in raw or []:
        url = item.get("href") or item.get("url") or ""
        if not url.startswith("http") or url in seen:
            continue
        if any(domain_of(url).endswith(d) for d in SKIP_DOMAINS):
            continue
        seen.add(url)
        results.append({
            "title": (item.get("title") or domain_of(url)).strip(),
            "url": url,
            "snippet": (item.get("body") or "").strip(),
        })
    return results


def fetch_text(url, max_chars=2200):
    """Open a page and pull out its main readable text. Returns "" on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code >= 400:
            return ""
        if "html" not in resp.headers.get("content-type", "").lower():
            return ""

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "nav", "footer",
                         "header", "aside", "form", "svg", "button"]):
            tag.decompose()

        root = soup.find("article") or soup.find("main") or soup.body or soup
        chunks = [el.get_text(" ", strip=True) for el in root.find_all(["p", "li"])]
        chunks = [c for c in chunks if len(c) >= 60]  # skip menus and captions
        text = re.sub(r"\s+", " ", " ".join(chunks)).strip()
        return text[:max_chars]
    except Exception:
        return ""


def gather_sources(query, want=4, max_chars=2200):
    """Search, read pages in parallel, and return up to `want` usable sources.

    Each source: {id, title, url, domain, text, snippet_only}
    """
    results = search_web(query)
    if not results:
        return []

    with ThreadPoolExecutor(max_workers=6) as pool:
        texts = list(pool.map(lambda r: fetch_text(r["url"], max_chars), results))

    full, fallback = [], []
    for r, text in zip(results, texts):
        if len(text) >= 300:
            full.append({**r, "text": text, "snippet_only": False})
        elif len(r["snippet"]) >= 100:
            fallback.append({**r, "text": r["snippet"], "snippet_only": True})

    chosen = (full + fallback)[:want]
    for i, src in enumerate(chosen, start=1):
        src["id"] = i
        src["domain"] = domain_of(src["url"])
    return chosen


def format_sources(sources):
    """Turn sources into numbered text the AI can read."""
    parts = []
    for s in sources:
        parts.append(f"[{s['id']}] {s['title']} ({s['domain']})\n{s['text']}")
    return "\n\n".join(parts)
