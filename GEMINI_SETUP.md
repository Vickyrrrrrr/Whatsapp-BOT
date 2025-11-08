# Adding Google Gemini AI to Your WhatsApp Bot

## 🤖 What This Does

Your bot can now answer **ANY question** students ask using Google's Gemini AI! 

Examples:
- "What is the admission process?"
- "How do I apply for scholarship?"
- "When do exams start?"
- "Tell me about the university"

The bot will:
1. First check if it's a command (help, notices, events, etc.)
2. Then search your college data
3. **Finally, use Gemini AI to intelligently answer the question**

---

## 🔑 Step 1: Get Your Free Gemini API Key

1. **Go to**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy** the API key (looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX`)

---

## 📝 Step 2: Add API Key to Your Environment

### For Local Development:

Edit your `.env` file and add:
```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
```

### For Cloud Deployment (Render/Railway):

Add this environment variable in your dashboard:
```
GEMINI_API_KEY = AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 📦 Step 3: Install the Package

**Local (already in requirements.txt):**
```powershell
pip install google-generativeai
```

**Cloud:** It will auto-install from `requirements.txt` on next deployment.

---

## 🧪 Step 4: Test It

Restart your bot and send these WhatsApp messages:

1. **"What is University of Lucknow known for?"**
   - Gemini will give an intelligent answer!

2. **"How do I prepare for exams?"**
   - AI-powered study advice!

3. **"notices"**
   - Still uses your predefined data (commands work as before)

---

## 💡 How It Works

```
User Message → Check Commands → Search Data → Ask Gemini AI → Reply
```

**Command** (help, notices, events) → Instant predefined response  
**Keyword match** in data → Returns matching notices  
**General question** → Gemini AI generates intelligent answer with college context

---

## 🎯 Features

✅ **Context-aware**: Gemini knows about your college data (notices, events)  
✅ **Fallback only**: Only used when command/data search fails  
✅ **Character limit**: Responses capped at 1000 chars for WhatsApp  
✅ **Error handling**: Falls back to default message if Gemini fails  
✅ **Free tier**: 60 requests/minute on free plan  

---

## 🔒 Security Notes

- ⚠️ **Never commit** `.env` with your API key to GitHub
- 🔑 Keep your `GEMINI_API_KEY` secret
- 📊 Monitor usage at: https://makersuite.google.com/

---

## 🚀 Optional: Customize AI Behavior

Edit `app.py` around line 95 to change how Gemini responds:

```python
context = f"""You are a helpful assistant for University of Lucknow students.
Be brief, friendly, and helpful. Always end with a positive note.

Recent college info:
...
"""
```

---

## 📊 Gemini Free Tier Limits

- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per day**

Perfect for a university bot! 🎓

---

## 🎉 You're All Set!

Your WhatsApp bot is now **AI-powered**! Students can ask any question and get intelligent answers.

**Need help?** Check the logs for any errors or let me know!
