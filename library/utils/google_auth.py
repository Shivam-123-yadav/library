import os, json
from google.oauth2 import service_account

def get_google_credentials():
    """
    Render ke environment variable se Google credentials load karega
    """
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise ValueError("GOOGLE_CREDENTIALS environment variable not found!")

    creds_dict = json.loads(creds_json)
    return service_account.Credentials.from_service_account_info(creds_dict)
