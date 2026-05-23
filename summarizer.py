import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a research summarizer. Based on the content provided, generate a structured JSON response.

Return ONLY a valid JSON object with NO markdown, NO backticks, NO extra text. Just pure JSON like this:
{
  "summary": ["paragraph 1", "paragraph 2", "paragraph 3"],
  "key_points": ["point 1", "point 2", "point 3", "point 4", "point 5"]
}

Rules:
- summary: array of 2 to 4 clear paragraphs explaining the topic
- key_points: array of 5 to 8 important facts as plain strings
- Be factual, neutral, and concise
- Never make up facts. Only use the content provided.
- Return ONLY the JSON object, nothing else."""


def summarize(query: str, content: str, sources: list) -> dict:
    try:
        print("[SUMMARIZER] Sending content to Groq AI...")

        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

        user_message = f"""Research Query: {query}

Web Content Collected:
{content[:8000]}

Based on the above content, generate a structured summary."""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_message}
                ],
                "max_tokens": 1500
            },
            timeout=30
        )

        if response.status_code != 200:
            print(f"[SUMMARIZER ERROR] Groq API Error: {response.status_code} - {response.text}")
            return {"error": f"Groq API error {response.status_code}: {response.text}"}

        resp_json = response.json()

        if "choices" not in resp_json:
            print(f"[SUMMARIZER ERROR] Unexpected response: {resp_json}")
            return {"error": f"Unexpected Groq response: {resp_json}"}

        raw_text = resp_json["choices"][0]["message"]["content"].strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        ai_result = json.loads(raw_text)

        print("[SUMMARIZER] AI summary generated successfully")

        return {
            "summary"   : ai_result.get("summary", []),
            "key_points": ai_result.get("key_points", []),
            "sources"   : sources
        }

    except json.JSONDecodeError as e:
        print(f"[SUMMARIZER ERROR] JSON parse failed: {e}")
        return {"error": "AI returned invalid format. Please try again."}

    except Exception as e:
        print(f"[SUMMARIZER ERROR] {e}")
        return {"error": f"Summarization failed: {str(e)}"}