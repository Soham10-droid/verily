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


# Search engines tried in order. Cloud hosts (like Streamlit Cloud) are often
# blocked or rate-limited by one engine while another still answers, so we
# don't rely on a single one.
BACKENDS = ("auto", "duckduckgo", "bing", "brave", "mojeek", "yahoo")


def _metasearch(query, max_results):
    for backend in BACKENDS:
        try:
            raw = DDGS().text(query, max_results=max_results, backend=backend)
        except TypeError:
            # older library version without the backend option
            try:
                raw = DDGS().text(query, max_results=max_results)
            except Exception:
                raw = []
        except Exception:
            continue  # this engine refused or errored; try the next one
        if raw:
            return raw
    return []


def _wikipedia_search(query, max_results=5):
    """Last-resort fallback: Wikipedia's free public search API, which
    doesn't block cloud servers. Returns results in the same shape."""
    try:
        resp = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": query,
                    "format": "json", "srlimit": max_results},
            headers={"User-Agent": "Verily/1.0 (student research project)"},
            timeout=8,
        )
        hits = resp.json().get("query", {}).get("search", [])
    except Exception:
        return []
    return [{
        "title": h["title"],
        "href": "https://en.wikipedia.org/wiki/" + h["title"].replace(" ", "_"),
        "body": re.sub(r"<[^>]+>", "", h.get("snippet", "")),
    } for h in hits]


def search_web(query, max_results=8):
    """Return a list of {title, url, snippet}, trying several engines and
    falling back to Wikipedia so a blocked engine doesn't stop the app."""
    raw = _metasearch(query, max_results) or _wikipedia_search(query)
    if not raw:
        raise SearchError(
            "None of the search engines returned results. Try rewording the "
            "question, or wait a minute and try again."
        )

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
