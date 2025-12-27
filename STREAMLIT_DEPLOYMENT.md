# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Access Streamlit Cloud

Go to: **https://share.streamlit.io**

### 2. Create New App

- Click **"New app"**
- Sign in with GitHub if not already signed in
- **Repository**: `kmgmedia/ai-teaching-assistant`
- **Branch**: `main`
- **Main file path**: `dashboard.py`
- **App URL**: Choose your custom subdomain (e.g., `ai-teacher-assistant`)

### 3. Configure Secrets

Click **"Advanced settings"** → **"Secrets"** and paste this configuration:

```toml
# Google Gemini API Key
GOOGLE_API_KEY = "your-google-gemini-api-key-here"

# Google Gemini Model Settings
GOOGLE_MODEL = "gemini-1.5-flash"
GOOGLE_TEMPERATURE = "0.7"
GOOGLE_MAX_TOKENS = "1000"

# Google Sheet ID (from your Google Sheet URL)
GOOGLE_SHEET_ID = "your-google-sheet-id-here"

# Google Cloud Service Account Credentials
# Copy these values from your service account JSON file
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

### 4. Deploy!

Click **"Deploy"** and wait 2-3 minutes for your app to build and launch.

---

## 📊 What's Included

Your deployed app will have these features:

✅ **6 Full Pages**:

- 🏠 Home - Welcome and overview
- 📊 Analytics - Performance metrics and insights
- 📝 Lesson Generator - AI-powered lesson planning
- 📊 Report Generator - Automated student reports
- ✉️ Parent Message - Parent communication templates
- 👥 View Students - Student data management

✅ **Multi-Teacher Support**:

- Teacher selector dropdown
- Filtered data by teacher
- Teacher performance comparison

✅ **Real-time Google Sheets Integration**:

- 132 student records
- 3 teachers assigned
- Automatic data synchronization

---

## 🔒 Security Notes

- ✅ Credentials are stored securely in Streamlit Secrets
- ✅ Never commit `.env` or `credentials/*.json` files to GitHub
- ✅ Service account has limited permissions (Sheets + Drive only)
- ✅ API keys can be rotated using `rotate_api_key.ps1`

---

## 🔄 Auto-Updates

Your Streamlit app automatically redeploys when you:

1. Push code changes to `main` branch on GitHub
2. Update any files in the repository

No manual redeployment needed!

---

## 🌐 Access Your App

Once deployed, your app will be available at:
**`https://your-subdomain.streamlit.app`**

Share this URL with teachers to access the AI Teaching Assistant!

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Repo**: https://github.com/kmgmedia/ai-teaching-assistant
- **Issues**: Report bugs via GitHub Issues

---

## ✅ Pre-Deployment Checklist

- [x] GitHub repository is public
- [x] `requirements.txt` includes all dependencies
- [x] `dashboard.py` is the main entry point
- [x] Code supports both local `.env` and Streamlit secrets
- [x] All 6 pages tested and working
- [x] Multi-teacher filtering operational
- [x] Analytics dashboard displaying correctly
