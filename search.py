import time
import requests


def search_web(query: str, max_results: int = 5) -> list:
    results = []

    try:
        print(f"[SEARCH] Searching for: {query}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        # DuckDuckGo Lite — more reliable
        url = f"https://lite.duckduckgo.com/lite/?q={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers, timeout=15)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links from DuckDuckGo Lite
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            title = a_tag.get_text(strip=True)

            if (href.startswith('http')
                    and 'duckduckgo.com' not in href
                    and title
                    and len(title) > 10):

                results.append({
                    "title"  : title,
                    "url"    : href,
                    "snippet": ""
                })

            if len(results) >= max_results:
                break

        print(f"[SEARCH] Found {len(results)} results")

    except Exception as e:
        print(f"[SEARCH ERROR] {e}")

    return results