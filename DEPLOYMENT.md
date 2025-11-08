# Cloud Deployment Guide - University of Lucknow WhatsApp Bot

## Deploy to Render (Recommended - FREE)

### Step 1: Push to GitHub
```powershell
cd "c:\Documents\GitHub\Whatsapp BOT"
git add .
git commit -m "Ready for cloud deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository: `Vickyrrrrrr/Whatsapp-BOT`
4. Configure:
   - **Name**: `lucknow-whatsapp-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

### Step 3: Add Environment Variables
In Render dashboard, add these environment variables:
```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
ADMIN_TOKEN=your-secret-admin-token
PORT=10000
```

### Step 4: Get Your Webhook URL
- After deployment, Render gives you a URL like: `https://lucknow-whatsapp-bot.onrender.com`
- Your webhook endpoint: `https://lucknow-whatsapp-bot.onrender.com/webhook`

### Step 5: Configure Twilio
1. Go to Twilio Console → WhatsApp Sandbox
2. Set webhook URL: `https://your-render-url.onrender.com/webhook`
3. Method: **POST**

---

## Deploy to Railway

### Quick Deploy
1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub**
3. Select your repository
4. Add environment variables (same as above)
5. Railway auto-detects Python and deploys

---

## Deploy to Heroku

### Prerequisites
```powershell
# Install Heroku CLI
winget install Heroku.HerokuCLI
```

### Deploy
```powershell
cd "c:\Documents\GitHub\Whatsapp BOT"
heroku login
heroku create lucknow-whatsapp-bot
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
heroku config:set ADMIN_TOKEN=your-admin-token
git push heroku main
```

Webhook URL: `https://lucknow-whatsapp-bot.herokuapp.com/webhook`

---

## Deploy to AWS EC2 (Advanced)

### Launch EC2 Instance
1. Login to AWS Console
2. Launch Ubuntu t2.micro (Free Tier)
3. Security Group: Allow port 80, 443, 22

### Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip nginx -y

# Clone repository
git clone https://github.com/Vickyrrrrrr/Whatsapp-BOT.git
cd Whatsapp-BOT

# Install packages
pip3 install -r requirements.txt

# Create .env file
nano .env  # Add your environment variables

# Run with gunicorn
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Setup Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Important Notes

### Environment Variables Required
All cloud platforms need these environment variables:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER`
- `ADMIN_TOKEN`
- `PORT` (usually auto-set by platform)

### Free Tier Limitations
- **Render**: May sleep after 15 min of inactivity (wakes on request)
- **Railway**: $5/month free credit
- **Heroku**: No free tier anymore (starts $5/month)
- **AWS/GCP/Azure**: Free tier for 12 months

### Keep Bot Awake (for Render/Railway)
Create a cron job to ping your bot every 10 minutes:
- Use https://cron-job.org (free)
- Ping URL: `https://your-bot-url.onrender.com/webhook`

---

## Recommended Approach

**For students/testing**: Use **Render** (free, easy, no credit card)
**For production**: Use **Railway** or **AWS EC2** with proper scaling

Your bot is now ready for cloud deployment! 🚀
