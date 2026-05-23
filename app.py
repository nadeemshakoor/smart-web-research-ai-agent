# ============================================================
# Smart Web Research Agent - Backend Server
# File: app.py
# Description: Main Flask server that connects frontend to agent
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import ResearchAgent

# Initialize Flask app
app = Flask(__name__)

# Allow frontend to communicate with backend (CORS fix)
CORS(app, resources={r"/*": {"origins": "*"}})

# Create one agent instance
agent = ResearchAgent()


# ── ROUTE: Health Check ──────────────────────────────────────
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "message": "Smart Web Research Agent Backend is live!"
    })


# ── ROUTE: Main Research Endpoint ───────────────────────────
@app.route('/research', methods=['POST'])
def research():
    """
    Accepts a POST request with a user query.
    Returns a structured research result.
    """

    # Get JSON data from frontend
    data = request.get_json()

    # STEP 1: Validate the query
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400

    query = data['query'].strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    if len(query) < 3:
        return jsonify({"error": "Query is too short. Please be more specific."}), 400

    print(f"\n[REQUEST] Query received: {query}")

    # Run the full agent pipeline
    result = agent.run(query)

    # Check if agent returned an error
    if "error" in result:
        return jsonify(result), 500

    print(f"[SUCCESS] Result ready for: {query}")
    return jsonify(result), 200


# ── START SERVER ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  Smart Web Research Agent - Backend")
    print("  Running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)


import os
port = int(os.environ.get("PORT", 7860))