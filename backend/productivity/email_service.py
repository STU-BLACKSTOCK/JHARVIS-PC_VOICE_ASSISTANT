import os
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

# Secure absolute path resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOKEN_PATH = os.path.join(ROOT_DIR, 'token.json')
CREDS_PATH = os.path.join(ROOT_DIR, 'credentials.json')

_cached_service = None

def get_gmail_service():
    global _cached_service
    if _cached_service:
        return _cached_service

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except Exception as e:
        print(f"Notice: Google API libraries not initialized ({e}). Gmail features disabled.")
        return None

    creds = None
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception:
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        else:
            if not os.path.exists(CREDS_PATH):
                return None
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception:
                return None
        if creds:
            try:
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
            except Exception:
                pass

    if not creds:
        return None

    try:
        _cached_service = build('gmail', 'v1', credentials=creds)
        return _cached_service
    except Exception as error:
        print(f"An error occurred connecting to Gmail: {error}")
        return None

def read_latest_emails(max_results=3):
    service = get_gmail_service()
    if not service:
        return "Gmail API is not configured. Missing credentials."
    
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            return "You have no unread messages."
        
        summaries = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
            summaries.append(f"From {sender.split('<')[0].strip()}: {subject}")
            
        return "Here are your latest emails. " + ". ".join(summaries)
    except Exception as e:
        return f"Error reading emails: {e}"
