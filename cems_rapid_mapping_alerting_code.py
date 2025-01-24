import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Email configuration
SMTP_SERVER = ""  # SMTP server - eg. "sender.domain.cctld"
SMTP_PORT = XXX  # TLS port - eg. 587
SENDER_EMAIL = ""  # Sender email address - eg. "alert@sender.domain.cctld"
SENDER_PASSWORD = ""  # Email password or token - "passowrd"
RECIPIENT_EMAILS = ["",""]  # Recipient email addresses - eg. ["email1","email2","email3"]

# Web page URL to monitoring
url = 'https://rapidmapping.emergency.copernicus.eu/backend/staticlist/?name=&category=fire&country=&activationTime__range_min=&activationTime__range_max='

# File to store the last monitored event
last_event_file = "last_event.txt"

# Function to get the last monitored event
def get_last_event():
    try:
        with open(last_event_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None  # If the file does not exist, it means this is the first execution

# Function to update the last monitored event
def update_last_event(event):
    with open(last_event_file, 'w') as file:
        file.write(event)

# Function to send email
def send_email(subject, body, event_name, event_code, activation_date, location):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        msg['Subject'] = subject  # Subject: [Fire alert] Name - Code Event

        # Email body with HTML for bold text
        event_link = f"https://rapidmapping.emergency.copernicus.eu/{event_code}"
        event_link_api = f"https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code={event_code}"
        body_with_link = f"""
        <b>(1) Fire alert</b><br>
        <b>(2) Issued:</b> {activation_date}<br>
        <b>(3) Country:</b> {location}<br>
        <b>(4) Name:</b> {event_name}<br>
        <b>(5) Event code:</b> {event_code}<br>
        <b>(6) Source:</b> CEMS Rapid Mapping<br>
        <b>(7) Resource link:</b> <a href="{event_link}">{event_link}<br></a>
        <b>(8) Resource REST-API:</b> <a href="{event_link_api}">{event_link_api}</a>
        """

        # Add the email body with HTML
        msg.attach(MIMEText(body_with_link, 'html'))

        # Connection to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Activate the encrypted mode
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Email login
            server.send_message(msg)  # Send the message
            print(f"Email successfully sent to: {', '.join(RECIPIENT_EMAILS)}")
    except Exception as e:
        print(f"Error while sending the email: {e}")

# Function to check new events
def check_for_new_event():
    response = requests.get(url)
    if response.status_code == 200:
        # HTML page parsing
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the rows of the table
        rows = soup.find_all('tr')

        # Filter only the wildfire events - double check to filter only wildfire events
        wildfire_events = [
            {
                'code': row.find_all('td')[1].text,
                'name': row.find_all('td')[2].text.strip(),
                'activation time': row.find_all('td')[5].text.strip(),  # Extract the activation date
                'location': row.find_all('td')[6].text.strip()  # Extract the location
            }
            for row in rows
            if len(row.find_all('td')) > 1 and "Wildfire" in row.text
        ]

        # Get the last monitored event
        last_known_event = get_last_event()

        # If there is no last saved event, set a reference event
        if last_known_event is None:
            last_known_event = ''  # Last know event configured - eg. "EMSR769"

        # Check for new wildfire events
        for event in wildfire_events:
            if event['code'] > last_known_event:
                print(f"New wildfire event detected: {event['code']}")
                # Extract the activation date and the location of the event
                activation_date = event['activation time']
                location = event['location']
                send_email(
                    subject=f"[Fire alert] {event['name']} - {event['code']}",
                    body=f"{activation_date}",
                    event_name=event['name'], # Set the event name as a parameter
                    event_code=event['code'],  # Set the event code as a parameter
                    activation_date=activation_date,  # Set the activation date
                    location=location  # Set the location
                )
                update_last_event(event['code'])  # Update the last monitored event
                break

# Main function to perform the periodic check
def main():
    while True:
        check_for_new_event()
        time.sleep(600)  # Check every 10 minutes (600 seconds)

# Run the script
if __name__ == "__main__":
    main()