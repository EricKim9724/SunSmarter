import datetime
import pandas as pd
from utils.authentication import get_connection
from google.auth.transport.requests import Request
import  google_auth_oauthlib.flow as Flow
from googleapiclient.discovery import build
import streamlit as st


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

def set_reminder(service, activity_type):
    # Call the Calendar API
    now = datetime.datetime.now()
    act_to_interval = {"Swimming/Water Activity":1,
                       "High Intensity Sports":1.5,
                       "Low Intensity Sports":2}
    reminder_time = act_to_interval[activity_type]
    reminder = now + datetime.timedelta(hours= reminder_time)
    reminder_end = reminder + datetime.timedelta(minutes= 5)
    event = {
        'summary': 'Sunscreen Reminder',
        'start': {
            'dateTime': reminder.isoformat(),
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': reminder_end.isoformat(),
            'timeZone': 'Australia/Melbourne',
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {
                    "method": "email",
                    "minutes": 10
                },
                {
                    "method": "popup",
                    "minutes": 5
                }
            ]
        }
    }
    reminder_event = service.events().insert(calendarId='primary', body=event).execute()
    return reminder_event

def delete_reminders(service, id):
    service.events().delete(calendarID = 'primary', eventID = id)

def display_reminder_history(email):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT date,activity  FROM reminder WHERE email = %s",(email))
        result = cursor.fetchall()
    connection.close()
    if result:
        df = pd.DataFrame(list(result), columns=['Date', 'Actvity'])
        st.write(df)
    else:
       st.subheader("No Reminder History...")

def start_outdoor_session(activity_type):
    service = google_authenticate("./utils/desktop_cred.json")
    reminder = set_reminder(service, activity_type)
    email = reminder['creator']['email']
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS reminder (date VARCHAR(30),email VARCHAR(30),activity VARCHAR(30))")
        cursor.execute("INSERT INTO reminder (date,email,activity) VALUES (%s,%s,%s)",(reminder['start']['dateTime'],email,activity_type))  
    connection.commit()
    connection.close()



