# Google Sheets Credentials

## Place your service account JSON file here

**File name**: `google-sheets-credentials.json`

**How to get this file**:

1. Follow the instructions in `GOOGLE_SHEETS_SETUP.md` (in project root)
2. Download the JSON key from Google Cloud Console
3. Save it in this folder
4. Update `.env` file with the path:
   ```
   GOOGLE_SHEETS_CREDENTIALS=credentials/google-sheets-credentials.json
   ```

## Security Notes

⚠️ **IMPORTANT**:

- This folder is already in `.gitignore` - credentials will NOT be committed to Git
- Never share these credentials publicly
- If compromised, delete the key in Google Cloud Console and create a new one

## What the file looks like

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "teaching-assistant-bot@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...
}
```

The `client_email` is what you'll share your Google Sheet with!
