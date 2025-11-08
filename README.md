# University of Lucknow — WhatsApp Info Bot

This project is a scaffold for a WhatsApp chatbot that helps University of Lucknow students get the latest college information (notices, events, contacts, timetable, etc.). It uses Twilio's WhatsApp API for messaging and a small Flask webhook to respond.

Features
- Responds to commands: `help`, `notices`, `events`, `contacts`, `timetable`, `latest <keyword>`
- Local JSON data store (`data/college_info.json`) which can be updated by an admin script
- Instructions for Twilio setup and local testing using ngrok
- Simple unit test for message parsing

Quick start (local, Windows PowerShell)
1. Install Python 3.9+ and create a venv:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Create a `.env` file with the following values:

```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1415XXXXXXX   # Twilio sandbox or registered WA number
ADMIN_TOKEN=some-secret-token
FLASK_ENV=development
```

3. Run the Flask app:

```powershell
python app.py
```

4. Expose your local server with ngrok and configure Twilio webhook to point to `https://<ngrok>.ngrok.io/webhook` (POST).

5. Use WhatsApp to message your Twilio WhatsApp number. Try `help`.

Admin: update data
- To update notices/events/contacts, run `python admin_update.py new_data.json --token <ADMIN_TOKEN>`

Testing
- Run `pytest -q`

Notes
- This scaffold uses Twilio for messaging; you'll need a Twilio account and WhatsApp sandbox or a registered number to send/receive messages.
- If you prefer an unofficial WhatsApp Web library (e.g., Baileys or yowsup), that can be integrated instead of Twilio.

Next steps
- Hook into University of Lucknow official feeds (RSS, website scraping, Google Sheets) to fetch live updates automatically.
- Add authentication for admin actions via a web UI.

