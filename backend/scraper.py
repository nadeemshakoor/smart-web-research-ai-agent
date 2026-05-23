# ============================================================
# Smart Web Research Agent - Scraper Module
# File: scraper.py
# Description: Visits URLs and extracts clean text content
# ============================================================

import requests
from bs4 import BeautifulSoup


# Browser headers to avoid being blocked
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_url(url: str, timeout: int = 8) -> str:
    """
    STEP 3: WEB SCRAPING
    Visits a single URL and extracts clean body text.
    Ignores ads, menus, footers, and irrelevant elements.

    Args:
        url    : The webpage URL to scrape
        timeout: Max seconds to wait for page load

    Returns:
        Extracted clean text as a string (empty if failed)
    """

    try:
        print(f"[SCRAPER] Visiting: {url}")

        # Send HTTP GET request
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted HTML tags
        for tag in soup(['script', 'style', 'nav', 'header',
                         'footer', 'aside', 'form', 'iframe',
                         'noscript', 'ads', 'advertisement']):
            tag.decompose()

        # Extract main text content
        text = soup.get_text(separator=' ', strip=True)

        # Clean up extra whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = ' '.join(lines)

        # Only return if meaningful content found
        if len(clean_text) > 200:
            print(f"[SCRAPER] Extracted {len(clean_text)} characters")
            return clean_text[:5000]  # Limit to 5000 chars per page
        else:
            print(f"[SCRAPER] Too little content, skipping.")
            return ""

    except Exception as e:
        # If URL fails, skip it automatically
        print(f"[SCRAPER] Skipped {url} — Reason: {e}")
        return ""


def scrape_all(search_results: list) -> tuple:
    """
    Scrapes all URLs from search results.

    Args:
        search_results: List of dicts with url, title, snippet

    Returns:
        Tuple of (combined_text, sources_list)
    """

    all_text = []
    sources  = []

    for result in search_results:
        url   = result.get("url", "")
        title = result.get("title", "Unknown")

        if not url:
            continue

        # Scrape content from this URL
        content = scrape_url(url)

        if content:
            all_text.append(content)
            sources.append({"title": title, "url": url})

    # Combine all scraped content
    combined = "\n\n".join(all_text)
    print(f"[SCRAPER] Total content: {len(combined)} characters from {len(sources)} sources")

    return combined, sources
