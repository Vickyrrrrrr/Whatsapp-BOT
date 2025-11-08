"""
Telegram Bot Version - Alternative to Twilio
Use this if you want to switch from WhatsApp to Telegram

Setup:
1. Create bot: Talk to @BotFather on Telegram
2. Get bot token
3. Set webhook: https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-render-url.com/webhook
4. Add TELEGRAM_BOT_TOKEN to .env
"""

import os
import json
import requests
from flask import Flask, request, Response
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'college_info.json')

app = Flask(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# --- Same helper functions from app.py ---
def load_data():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"notices": [], "events": [], "contacts": {}, "timetable": {}}


def build_reply(text, data):
    """Same logic as WhatsApp version - NO CHANGES NEEDED!"""
    text = (text or "").strip()
    lc = text.lower()
    
    if lc in ('help', 'hi', 'hello', '/start'):
        return (
            "Hi! I'm the University of Lucknow Info Bot. Commands:\n"
            "- notices: latest notices\n"
            "- events: upcoming events\n"
            "- contacts: important numbers\n"
            "- timetable: department timetables\n"
            "- latest <keyword>: search notices for a keyword\n"
            "Example: latest exam"
        )

    if lc == 'notices':
        notices = data.get('notices', [])
        if not notices:
            return "No notices found."
        lines = [f"{n['date']} - {n['title']}" for n in notices[:5]]
        return "Latest notices:\n" + "\n".join(lines)

    if lc == 'events':
        events = data.get('events', [])
        if not events:
            return "No upcoming events."
        lines = [f"{e['date']} - {e['title']} @ {e.get('location','TBA')}" for e in events[:5]]
        return "Upcoming events:\n" + "\n".join(lines)

    if lc == 'contacts':
        contacts = data.get('contacts', {})
        if not contacts:
            return "No contact information available."
        lines = [f"{k}: {v}" for k, v in contacts.items()]
        return "Important contacts:\n" + "\n".join(lines)

    if lc == 'timetable':
        tt = data.get('timetable', {})
        if not tt:
            return "No timetable data available."
        lines = [f"{dept}: {when}" for dept, when in tt.items()]
        return "Timetables:\n" + "\n".join(lines)

    if lc.startswith('latest '):
        q = lc.split(' ', 1)[1]
        notices = data.get('notices', [])
        matches = [n for n in notices if q in (n.get('title','')+n.get('content','')).lower()]
        if not matches:
            return f"No notices found containing '{q}'."
        lines = [f"{m['date']} - {m['title']}" for m in matches[:5]]
        return f"Notices matching '{q}':\n" + "\n".join(lines)

    # Use Gemini AI for general questions
    if model and len(text) > 3:
        try:
            context = f"""You are a helpful assistant for University of Lucknow students. 
Answer the student's question briefly and helpfully."""
            
            prompt = f"{context}\n\nStudent question: {text}\n\nAnswer:"
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()[:4000]  # Telegram allows longer messages
        except Exception:
            pass

    return "Sorry, I didn't understand. Send 'help' for commands or ask a question!"


# --- ONLY THIS PART IS DIFFERENT - Telegram webhook instead of Twilio ---
@app.route('/', methods=['GET'])
def index():
    return "University of Lucknow Telegram Bot is running! 🎓"


@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook - different format than Twilio"""
    data = request.get_json()
    
    # Extract message from Telegram format
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        incoming = data['message'].get('text', '')
        
        # Get reply using same logic
        college_data = load_data()
        reply_text = build_reply(incoming, college_data)
        
        # Send reply via Telegram API
        telegram_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        requests.post(telegram_url, json={
            'chat_id': chat_id,
            'text': reply_text
        })
    
    return Response('ok', status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
