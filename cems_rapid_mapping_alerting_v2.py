import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
from datetime import datetime

# Email configuration
SMTP_SERVER = ""  # SMTP server - e.g. "sender.domain.cctld"
SMTP_PORT = XXX  # TLS port - e.g. 587
SENDER_EMAIL = ""  # Sender email address - e.g. "alert@sender.domain.cctld"
SENDER_PASSWORD = r""  # Email password or token - e.g. "passowrd"
RECIPIENT_EMAILS = ["", ""]  # Recipient emails - e.g. ["email1","email2","email3"]

# API URL to monitor events
API_URL = "https://mapping.emergency.copernicus.eu/activations/api/activations/"

# File to store the last monitored event
LAST_EVENT_FILE = "last_event.txt"

# Function to get the last monitored event
def get_last_event():
    """Retrieve the last monitored event from file."""
    try:
        with open(LAST_EVENT_FILE, 'r') as file:
            last_event = file.read().strip()
            print(f"📄 Last monitored event: {last_event}")
            return last_event
    except FileNotFoundError:
        print("⚠️ No previous event found, creating a new file.")
        return None

# Function to update the last monitored event
def update_last_event(event_code):
    """Update the last monitored event in the file."""
    with open(LAST_EVENT_FILE, 'w') as file:
        file.write(event_code)
    print(f"✅ Updated last monitored event: {event_code}")

# Function to send email
def send_email(subject, event_name, event_code, activation_date, location):
    """Send an email notification about a new wildfire event."""
    try:
        print(f"📧 Sending email for event: {event_name} - {event_code}")
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        msg['Subject'] = subject

        # Email body with HTML for bold text
        event_link = f"https://rapidmapping.emergency.copernicus.eu/{event_code}"
        event_link_api = f"https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code={event_code}"
        
        body = f"""
        <b>(1) Fire alert</b><br>
        <b>(2) Issued:</b> {activation_date}<br>
        <b>(3) Country:</b> {location}<br>
        <b>(4) Name:</b> {event_name}<br>
        <b>(5) Event code:</b> {event_code}<br>
        <b>(6) Source:</b> CEMS Rapid Mapping<br>
        <b>(7) Resource link:</b> <a href="{event_link}">{event_link}</a><br>
        <b>(8) Resource REST-API:</b> <a href="{event_link_api}">{event_link_api}</a>
        """
        
        # Add the email body with HTML
        msg.attach(MIMEText(body, 'html'))
        
        # Connection to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Activate the encrypted mode
            server.login(SENDER_EMAIL, SENDER_PASSWORD) # Email login
            server.send_message(msg) # Send the message
        
        print(f"✅ Email successfully sent to: {', '.join(RECIPIENT_EMAILS)}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Function to check new events
def check_for_new_event():
    """Check for new wildfire events using the API."""
    print("🔍 Fetching events from API...")
    
    params = {
        'categories': 'fire,volcan,earthquake,mass,storm,flood,humanitarian,industrial,environment,other',
        'activationTime': '2012-01,2025-2',
        'limit': 500
    }
    
    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        print("✅ API request successful, processing data...")
        data = response.json()
        
        # Filter wildfire events
        wildfire_events = [
            {
                'code': event['code'],
                'name': event['name'],
                'activation_time': event['activationTime'],
                'location': ', '.join([country['short_name'] for country in event['countries']])
            }
            for event in data['results']
            if 'Wildfire' in event['name']
        ]
        
        print(f"🔥 Wildfire events found: {len(wildfire_events)}")
        
        # Get the last monitored event
        last_known_event = get_last_event() or 'EMSN212'  # Default reference event
        
        # Check for new wildfire events
        for event in wildfire_events:
            if event['code'] > last_known_event:
                print(f"🚨 New wildfire event detected: {event['code']} - {event['name']}")
                
                send_email(
                    subject=f"[Fire alert] {event['name']} - {event['code']}",
                    event_name=event['name'], # Set the event name as a parameter
                    event_code=event['code'], # Set the event code as a parameter
                    activation_date=event['activation_time'], # Set the activation date
                    location=event['location'] # Set the location
                )
                
                update_last_event(event['code']) # Update the last monitored event
                break
    else:
        print(f"❌ API request error, status code: {response.status_code}")

# Main function to perform the periodic check
def main():
    """Main function to periodically check for new events."""
    print("🚀 Starting event monitoring...")
    while True:
        check_for_new_event()
        print("⏳ Waiting 10 minutes before the next check...")
        time.sleep(600)  # Check every 10 minutes (600 seconds)


if __name__ == "__main__":
    main()
