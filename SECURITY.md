# 🔒 Security Guide - API Key Management

## ✅ Current Security Status

Your project is configured securely:

- `.env` file is gitignored ✅
- `credentials/*.json` files are gitignored ✅
- No sensitive data in repository ✅

---

## 🚨 Security Checklist Before Deployment

### 1. **Verify Gitignore is Working**

```powershell
# Check that sensitive files are NOT staged
git status

# Should NOT see:
# - .env
# - credentials/google-sheets-credentials.json
```

### 2. **Rotate Your OpenAI API Key (IMPORTANT!)**

Your current API key has been used in development and may have been logged. **Best practice: Create a new production key**

**Steps:**

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "AI Teaching Assistant - Production"
4. Copy the new key
5. Update `.env` with new key
6. **Delete the old key** from OpenAI dashboard

### 3. **Check for Accidental Key Exposure**

```powershell
# Search for hardcoded API keys in code
Select-String -Path "*.py" -Pattern "sk-proj-" -Recurse -Exclude "venv"
Select-String -Path "*.py" -Pattern "private_key" -Recurse -Exclude "venv"
```

If any matches found (should be NONE), remove them immediately.

### 4. **Verify No Keys in Git History**

```powershell
# Check what would be committed
git diff --cached

# Should NOT contain:
# - sk-proj-...
# - private_key
# - service_account credentials
```

---

## 🔐 Environment Variable Management by Platform

### **Streamlit Cloud**

Store secrets in `.streamlit/secrets.toml` (local only, gitignored):

```toml
OPENAI_API_KEY = "sk-proj-NEW-KEY-HERE"
GOOGLE_SHEET_ID = "your-sheet-id"

[gcp_service_account]
type = "service_account"
project_id = "your-project"
# ... rest of credentials
```

Then add to Streamlit Cloud dashboard → Settings → Secrets

### **Heroku**

```powershell
heroku config:set OPENAI_API_KEY=sk-proj-NEW-KEY-HERE
heroku config:set GOOGLE_SHEET_ID=your-sheet-id

# For Google credentials (base64 encoded)
$creds = Get-Content credentials\google-sheets-credentials.json -Raw
$encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($creds))
heroku config:set GOOGLE_SHEETS_CREDENTIALS_BASE64=$encoded
```

### **Railway / Render**

Add in web dashboard:

- Navigate to Environment Variables section
- Add `OPENAI_API_KEY`, `GOOGLE_SHEET_ID`, and `GOOGLE_SHEETS_CREDENTIALS_BASE64`

### **AWS EC2**

```bash
# SSH into server
nano .env

# Add variables
OPENAI_API_KEY=sk-proj-NEW-KEY-HERE
GOOGLE_SHEET_ID=your-sheet-id

# Secure the file
chmod 600 .env
```

---

## 🛡️ Additional Security Best Practices

### **1. Enable Rate Limiting**

Add to `main.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/generate/lesson', methods=['POST'])
@limiter.limit("10 per minute")
def generate_lesson():
    # ... existing code
```

### **2. Add API Authentication**

For production, add simple API key authentication:

```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_SECRET_KEY'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/generate/lesson', methods=['POST'])
@require_api_key
def generate_lesson():
    # ... existing code
```

### **3. Enable HTTPS Only**

In production, force HTTPS:

```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

### **4. Rotate Keys Regularly**

- OpenAI API key: Every 90 days
- Google Service Account: Every 180 days
- Set calendar reminders

### **5. Monitor API Usage**

- Check OpenAI dashboard weekly: https://platform.openai.com/usage
- Set spending limits in OpenAI billing settings
- Alert if unusual usage detected

---

## ⚠️ What to Do If Keys Are Exposed

### **If OpenAI Key is Leaked:**

1. **Immediately revoke** at https://platform.openai.com/api-keys
2. Create new key
3. Update all environments (local + production)
4. Check OpenAI usage logs for unauthorized use

### **If Google Credentials are Leaked:**

1. Go to Google Cloud Console
2. IAM & Admin → Service Accounts
3. Delete compromised service account
4. Create new service account
5. Download new credentials
6. Re-share Google Sheet with new account
7. Update all environments

### **If Committed to Git:**

```powershell
# Remove from Git history (DESTRUCTIVE - use carefully)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (if already pushed to remote)
git push origin --force --all
```

Then immediately rotate ALL exposed keys.

---

## 📋 Pre-Deployment Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] `credentials/*.json` is in `.gitignore`
- [ ] No API keys in code (grep search confirms)
- [ ] No API keys in git history (`git log -p` review)
- [ ] OpenAI API key rotated for production
- [ ] Google Sheet shared with service account only
- [ ] Environment variables configured on deployment platform
- [ ] HTTPS enabled in production
- [ ] Rate limiting configured
- [ ] OpenAI spending limit set ($10/month recommended for testing)
- [ ] Monitoring/alerts configured

---

## 🔗 Security Resources

- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Google Cloud Security](https://cloud.google.com/security/best-practices)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Secrets Scanning](https://docs.github.com/en/code-security/secret-scanning)

---

## 📞 Security Contact

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Rotate compromised credentials immediately
3. Document the incident
4. Review logs for unauthorized access
