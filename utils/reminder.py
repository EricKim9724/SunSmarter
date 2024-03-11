import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow as Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def google_authenticate(cred_file_path):
    creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.InstalledAppFlow.from_client_secrets_file(
                cred_file_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        service = build("calendar", "v3", credentials=creds)
    return service


def set_reminder(service, reminder_time):
    # Call the Calendar API
    now = datetime.datetime.now()
    reminder = now + datetime.timedelta(hours=reminder_time)
    reminder_end = reminder + datetime.timedelta(minutes=5)
    event = {
        "summary": "Sunscreen Reminder",
        "start": {
            "dateTime": reminder.isoformat(),
            "timeZone": "Australia/Melbourne",
        },
        "end": {
            "dateTime": reminder_end.isoformat(),
            "timeZone": "Australia/Melbourne",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 10},
                {"method": "popup", "minutes": 5},
            ],
        },
    }
    reminder_event = service.events().insert(calendarId="primary", body=event).execute()
    return reminder_event["id"]


def delete_reminders(service, id):
    service.events().delete(calendarID="primary", eventID=id)

