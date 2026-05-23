# ============================================================
# Smart Web Research Agent - Core Agent
# File: agent.py
# Description: Orchestrates all steps of the research pipeline
# ============================================================

from search     import search_web
from scraper    import scrape_all
from summarizer import summarize


class ResearchAgent:
    """
    The main AI Agent that coordinates all research steps:
    Search → Scrape → Process → Summarize → Return
    """

    def run(self, query: str) -> dict:
        """
        Runs the full research pipeline for a given query.
        """

        print(f"\n{'='*50}")
        print(f"  AGENT STARTED: {query}")
        print(f"{'='*50}")

        # ── STEP 1: RECEIVE & CLEAN QUERY ───────────────────
        print("\n[STEP 1] Cleaning query...")
        query = ' '.join(query.strip().split())
        print(f"[STEP 1] Clean query: {query}")

        # ── STEP 2: WEB SEARCH ──────────────────────────────
        print("\n[STEP 2] Searching the web...")
        search_results = search_web(query, max_results=5)

        # If search fails use AI knowledge directly
        if not search_results:
            search_results = [
                {
                    "title"  : "AI Knowledge Base",
                    "url"    : "https://wikipedia.org",
                    "snippet": query
                }
            ]

        # ── STEP 3: WEB SCRAPING ────────────────────────────
        print("\n[STEP 3] Scraping web pages...")
        combined_text, sources = scrape_all(search_results)

        # If scraping failed use snippets as fallback
        if not combined_text or len(combined_text) < 100:
            print("[STEP 3] Using search snippets as fallback...")
            combined_text = "\n\n".join([
                f"{r['title']}: {r['snippet']}"
                for r in search_results if r.get('snippet')
            ])
            sources = [
                {"title": r["title"], "url": r["url"]}
                for r in search_results
            ]

        # ── STEP 4: CONTENT PROCESSING ──────────────────────
        print("\n[STEP 4] Processing content...")
        combined_text = self._process_content(combined_text)

        # ── STEP 5 & 6: SUMMARIZE & RETURN ──────────────────
        print("\n[STEP 5] Generating AI summary...")
        result = summarize(query, combined_text, sources)

        print("\n[AGENT DONE] Research complete!")
        return result


    def _process_content(self, text: str) -> str:
        """
        STEP 4: CONTENT PROCESSING
        Removes duplicate sentences and cleans the text.
        """

        sentences  = text.replace('\n', ' ').split('. ')
        seen       = set()
        unique     = []

        for sentence in sentences:
            normalized = sentence.strip().lower()
            if len(normalized) < 20:
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            unique.append(sentence.strip())

        processed = '. '.join(unique)
        print(f"[STEP 4] {len(sentences)} → {len(unique)} unique sentences")

        return processed