# CEMS Rapid Mapping alerting code

This Python script monitors wildfire events using the Copernicus Emergency Management Service (CEMS) API and sends email notifications when new events are detected.  

## Features

- Monitors wildfire events using the CEMS API.
- Sends email notifications for new events.
- Stores the last monitored event to avoid duplicate notifications.
- Configurable email settings.

## Requirements

- Python 3.x
- `smtplib` library
- `requests` library

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:
   ```bash
   pip install requests

# Configuration:  
Open the script file and configure the following settings:  
SMTP_SERVER: The SMTP server address (e.g., "smtp.example.com").  
SMTP_PORT: The SMTP server port (e.g., 587).  
SENDER_EMAIL: The sender's email address (e.g., "alert@example.com").  
SENDER_PASSWORD: The sender's email password or token.  
RECIPIENT_EMAILS: A list of recipient email addresses (e.g., ["email1@example.com", "email2@example.com"]).  
API_URL: The API URL to monitor events (default: "https://mapping.emergency.copernicus.eu/activations/api/activations/").  
LAST_EVENT_FILE: The file to store the last monitored event (default: "last_event.txt").  

# Usage:  
Run the script:  
python(3) cems_rapid_mapping_alerting_v2.py  
The script will periodically check for new wildfire events every 10 minutes and send email notifications if new events are detected.

# Functions
get_last_event(): Retrieves the last monitored event from the file.  
update_last_event(event_code): Updates the last monitored event in the file.  
send_email(subject, event_name, event_code, activation_date, location): Sends an email notification about a new wildfire event.  
check_for_new_event(): Checks for new wildfire events using the API.  
main(): Main function to perform the periodic check.  

# This is an alert example:  
(1) Fire alert  
(2) Issued: 2025-01-16  
(3) Country: France  
(4) Name: Wildfire in Amsterdam Island, France  
(5) Event code: EMSR785  
(6) Source: CEMS Rapid Mapping  
(7) Resource link: https://rapidmapping.emergency.copernicus.eu/EMSR785  
(8) Resource REST-API: https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR785

# License
GNU General Public License v3.0.

# Acknowledgments:  
Copernicus Emergency Management Service (CEMS) for providing the API.

# Contact:  
Consiglio Nazionale delle Ricerche - Istituto di Metodologie per l'Analisi Ambientale (CNR-IMAA)
ACTRIS-ARES DC Unit  
Ermann Ripepi - ermann.ripepi@cnr.it  
Michele Volini - michele.volini@cnr.it
