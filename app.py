import os
import json
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'college_info.json')

app = Flask(__name__)

# --- Helpers ---

def load_data():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"notices": [], "events": [], "contacts": {}, "timetable": {}}


def build_reply(text, data):
    """Given an incoming text and the data dict, return a string reply."""
    text = (text or "").strip()
    lc = text.lower()
    if lc in ('help', 'hi', 'hello'):
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

    # fallback: try to search notices for keyword
    notices = data.get('notices', [])
    matches = [n for n in notices if lc in (n.get('title','')+n.get('content','')).lower()]
    if matches:
        lines = [f"{m['date']} - {m['title']}" for m in matches[:5]]
        return "I found these notices:\n" + "\n".join(lines)

    return "Sorry, I didn't understand. Send 'help' for commands."


# --- Flask webhook ---
@app.route('/', methods=['GET'])
def index():
    return "University of Lucknow WhatsApp Bot is running! 🎓"

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming = request.form.get('Body', '')
    sender = request.form.get('From', '')
    data = load_data()
    reply_text = build_reply(incoming, data)

    resp = MessagingResponse()
    resp.message(reply_text)
    return Response(str(resp), mimetype='application/xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
