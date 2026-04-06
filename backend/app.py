import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests.
    Expected JSON: { "message": "user message", "history": [...] }
    Returns: { "reply": "bot response", "history": [...] }
    """
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Build messages array for API call
        messages = []

        # Add conversation history
        if isinstance(history, list):
            for msg in history:
                if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                    messages.append(msg)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Groq API via HTTP
        headers = {
            "Authorization": "Bearer " + GROQ_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            error_text = response.text
            return jsonify({
                "error": "Groq API error",
                "details": error_text,
                "status_code": response.status_code
            }), 500

        api_response = response.json()

        # Extract the assistant's reply
        if 'choices' not in api_response or not api_response['choices']:
            return jsonify({"error": "Invalid response from Groq API"}), 500

        bot_reply = api_response['choices'][0]['message']['content']

        # Build updated history
        updated_history = history.copy() if isinstance(history, list) else []
        updated_history.append({
            "role": "user",
            "content": user_message
        })
        updated_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({
            "reply": bot_reply,
            "history": updated_history
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Groq API timed out"}), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Network error",
            "details": str(e)
        }), 500

    except ValueError as e:
        return jsonify({
            "error": "Invalid JSON or missing API key",
            "details": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
