# Import necessary libraries
import logging  # For logging messages to console and file
import smtplib  # For sending emails via SMTP
from email.mime.text import MIMEText  # For formatting email content as plain text or HTML
from email.mime.multipart import MIMEMultipart  # For creating emails with multiple parts (e.g., HTML + attachments)
import requests  # For making HTTP requests to the API
import time  # For adding delays between checks
from datetime import datetime  # For handling date and time

# Configure logging to output to both console and a log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler("/var/log/CEMS_RAPID_MAPPING/cems_rapid_mapping.log")  # Output to log file
    ]
)

# Email configuration variables
SMTP_SERVER = ""  # SMTP server address (e.g., "smtp.example.com")
SMTP_PORT = XXX  # SMTP port for TLS (e.g., 587)
SENDER_EMAIL = ""  # Email address used to send alerts
SENDER_PASSWORD = r""  # Password or token for the sender email
RECIPIENT_EMAILS = ["", ""]  # List of recipient email addresses
API_URL = "https://mapping.emergency.copernicus.eu/activations/api/activations/"  # API endpoint for event data
LAST_EVENT_FILE = "last_event.txt"  # File to store the last processed event code


# Read the last processed event code from file
def get_last_event():
    try:
        with open(LAST_EVENT_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "EMSR000"  # Default value if file doesn't exist
# Update the last processed event code in the file
def update_last_event(code):
    with open(LAST_EVENT_FILE, 'w') as file:
        file.write(code)


# Send an email with event details
def send_email(subject, event_name, event_code, activation_date, location):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(RECIPIENT_EMAILS)
    msg['Subject'] = subject

    # Generate links to the event page and API
    event_link = f"https://rapidmapping.emergency.copernicus.eu/{event_code}"
    event_link_api = f"https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code={event_code}"

    # Email body in HTML format
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

    # Attach the HTML body to the email
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Start TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login to the SMTP server
        server.send_message(msg)  # Send the email

    logging.info(f"✅ Email sent for {event_code} - {event_name}")


# Check the API for new fire-related events
def check_for_new_event():
    params = {
        'categories': 'fire',  # Filter for fire-related events
        'limit': 500  # Maximum number of events to retrieve
    }

    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        logging.error(f"❌ API error: {response.status_code}")
        return

    data = response.json()

    # Extract relevant event information and filter for fire/wildfire events
    events = [
        {
            'code': e['code'],
            'name': e['name'],
            'activation_time': e['activationTime'],
            'location': ', '.join([c['short_name'] for c in e['countries']])
        }
        for e in data['results']
        if 'fire' in e['name'].lower() or 'wildfire' in e['name'].lower()
    ]

    # Sort events by numeric part of the code (e.g., EMSR123)
    events.sort(key=lambda x: int(x['code'][4:]))

    last_code = get_last_event()
    logging.info(f"📄 Last monitored event: {last_code}")

    # Check if there are new events with a higher code number
    for event in events:
        current_code = event['code']
        if int(current_code[4:]) > int(last_code[4:]):
            send_email(
                subject=f"[Fire alert] {event['name']} - {event['code']}",
                event_name=event['name'],
                event_code=event['code'],
                activation_date=event['activation_time'],
                location=event['location']
            )
            update_last_event(current_code)  # Save the new event code
            break  # Only notify for the first new event


# Main loop: continuously check for new events every 10 minutes
def main():
    logging.info("🚀 Wildfire monitoring started...")
    while True:
        check_for_new_event()
        logging.info("⏳ Waiting 10 minutes...")
        time.sleep(600)  # Wait for 600 seconds (10 minutes)


# Entry point of the script
if __name__ == "__main__":
    main()
