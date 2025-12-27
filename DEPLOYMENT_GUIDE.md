# 🚀 Deployment Guide - AI Teaching Assistant

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- ✅ OpenAI API key with active billing
- ✅ Google Sheets credentials (service account JSON)
- ✅ All dependencies in `requirements.txt`
- ✅ `.env` file configured (will need to set environment variables on server)

---

## 🎯 Deployment Options

### **Option 1: Streamlit Cloud (Recommended for Dashboard)**

**Best for:** Non-technical users, free tier available, easiest setup

#### Steps:

1. **Push to GitHub**

   ```powershell
   git init
   git add .
   git commit -m "Initial commit - AI Teaching Assistant"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-teaching-assistant.git
   git push -u origin main
   ```

2. **Create `.streamlit/secrets.toml`**

   ```powershell
   mkdir .streamlit
   ```

   Create `.streamlit/secrets.toml`:

   ```toml
   OPENAI_API_KEY = "sk-proj-your-key-here"
   GOOGLE_SHEET_ID = "your-sheet-id-here"

   # Paste entire Google Sheets credentials JSON
   [gcp_service_account]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@project.iam.gserviceaccount.com"
   client_id = "123456789"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
   ```

3. **Update `google_sheets.py` for Streamlit Cloud**
   Add this at the top of `get_sheets_client()`:

   ```python
   # Check if running on Streamlit Cloud
   if 'gcp_service_account' in st.secrets:
       credentials = Credentials.from_service_account_info(
           st.secrets["gcp_service_account"],
           scopes=["https://www.googleapis.com/auth/spreadsheets",
                   "https://www.googleapis.com/auth/drive"]
       )
   else:
       # Local development - use JSON file
       credentials = Credentials.from_service_account_file(
           credentials_path,
           scopes=["https://www.googleapis.com/auth/spreadsheets",
                   "https://www.googleapis.com/auth/drive"]
       )
   ```

4. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repository
   - Set main file: `dashboard.py`
   - Paste secrets from `.streamlit/secrets.toml` into Streamlit Cloud secrets
   - Click "Deploy"

**Cost:** FREE (with limitations: 1 app, community support)

---

### **Option 2: Heroku (For Flask API + Dashboard)**

**Best for:** Full-stack deployment, REST API access, custom domain

#### Steps:

1. **Create `Procfile`**

   ```powershell
   New-Item -Path "Procfile" -ItemType File
   ```

   Add to `Procfile`:

   ```
   web: gunicorn main:app
   ```

2. **Install Gunicorn**

   ```powershell
   venv\Scripts\pip.exe install gunicorn
   venv\Scripts\pip.exe freeze > requirements.txt
   ```

3. **Create `runtime.txt`**

   ```
   python-3.11.9
   ```

   (Heroku doesn't support Python 3.14 yet - use 3.11.x)

4. **Update `.gitignore`**
   Ensure these are excluded:

   ```
   .env
   credentials/
   *.json
   ```

5. **Deploy to Heroku**

   ```powershell
   # Install Heroku CLI first: https://devcenter.heroku.com/articles/heroku-cli

   heroku login
   heroku create ai-teaching-assistant

   # Set environment variables
   heroku config:set OPENAI_API_KEY=sk-proj-your-key-here
   heroku config:set GOOGLE_SHEET_ID=your-sheet-id-here

   # Upload Google Sheets credentials (as base64)
   $creds = Get-Content credentials\google-sheets-credentials.json -Raw
   $encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($creds))
   heroku config:set GOOGLE_SHEETS_CREDENTIALS_BASE64=$encoded

   # Deploy
   git push heroku main
   heroku open
   ```

6. **Update `google_sheets.py` for Heroku**
   Add this to handle base64 credentials:

   ```python
   import base64
   import json

   # In get_sheets_client():
   creds_base64 = os.getenv("GOOGLE_SHEETS_CREDENTIALS_BASE64")
   if creds_base64:
       creds_json = base64.b64decode(creds_base64).decode('utf-8')
       creds_dict = json.loads(creds_json)
       credentials = Credentials.from_service_account_info(
           creds_dict,
           scopes=["https://www.googleapis.com/auth/spreadsheets",
                   "https://www.googleapis.com/auth/drive"]
       )
   else:
       # Local development
       credentials = Credentials.from_service_account_file(...)
   ```

**Cost:** FREE tier available (550-1000 dyno hours/month)

---

### **Option 3: Render (Modern Alternative to Heroku)**

**Best for:** Free tier, automatic deployments, easier than Heroku

#### Steps:

1. **Create `render.yaml`**

   ```yaml
   services:
     - type: web
       name: ai-teaching-assistant
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn main:app
       envVars:
         - key: OPENAI_API_KEY
           sync: false
         - key: GOOGLE_SHEET_ID
           sync: false
         - key: GOOGLE_SHEETS_CREDENTIALS_BASE64
           sync: false
   ```

2. **Push to GitHub** (same as Option 1)

3. **Deploy on Render**
   - Go to https://dashboard.render.com
   - Click "New Web Service"
   - Connect GitHub repository
   - Select `render.yaml` configuration
   - Add environment variables in dashboard
   - Click "Create Web Service"

**Cost:** FREE tier available (auto-sleep after 15 min inactivity)

---

### **Option 4: Railway (Simplest Deployment)**

**Best for:** Zero-config deployment, modern developer experience

#### Steps:

1. **Push to GitHub**

2. **Deploy on Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and installs dependencies
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `GOOGLE_SHEET_ID`
     - `GOOGLE_SHEETS_CREDENTIALS_BASE64` (base64-encoded JSON)
   - Click "Deploy"

**Cost:** FREE $5 credit/month (enough for small projects)

---

### **Option 5: AWS EC2 (Full Control)**

**Best for:** Production-grade, scalable, custom configurations

#### Quick Setup:

1. **Launch EC2 Instance** (Ubuntu 22.04)

2. **SSH and Setup**

   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y

   # Clone repository
   git clone https://github.com/YOUR_USERNAME/ai-teaching-assistant.git
   cd ai-teaching-assistant

   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Setup environment variables
   nano .env
   # Add your API keys

   # Install Gunicorn
   pip install gunicorn

   # Run with Gunicorn
   gunicorn --bind 0.0.0.0:8000 main:app
   ```

3. **Configure Nginx** (reverse proxy)

4. **Setup Systemd** (auto-restart service)

**Cost:** FREE tier 750 hours/month (t2.micro), then ~$5-10/month

---

## 🎯 **Recommended Path for You**

### **For Dashboard Only:**

→ **Streamlit Cloud** (Option 1)

- Free
- Zero server management
- Perfect for teachers
- Deploy in 5 minutes

### **For Full API + Dashboard:**

→ **Railway** (Option 4)

- Easiest full-stack deployment
- Free tier sufficient for testing
- Auto-deployment on GitHub push
- Can scale later

---

## 📝 **Next Steps**

1. **Choose deployment platform** (I recommend Streamlit Cloud for dashboard)
2. **Create GitHub repository** (if not already)
3. **Add deployment-specific configuration** (I can help with this)
4. **Set environment variables** on chosen platform
5. **Deploy and test**

**Which option sounds best for your use case?** I can walk you through the detailed steps for your chosen platform.

---

## 🔒 **Security Reminders**

- ✅ Never commit `.env` file
- ✅ Never commit `credentials/*.json` files
- ✅ Use environment variables on all platforms
- ✅ Rotate API keys if accidentally exposed
- ✅ Enable 2FA on all deployment accounts
