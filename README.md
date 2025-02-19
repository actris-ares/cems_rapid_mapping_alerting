# CEMS Rapid Mapping alerting code

This Python script detects if there is a new WildFire event on the CEMS Rapid Mapping portal and sends an email containing the following information:  

# Prerequisites
Python 3.x  
pandas library  
netCDF4 library  
requests library  
BeautifulSoup library  

You can install the required libraries using pip:
pip install pandas netCDF4 requests beautifulsoup4  

# Configuration
Before running the script, you need to configure the email settings and the URL to monitor.

1. Email Configuration:  
SMTP_SERVER: The SMTP server address (e.g., "smtp.domain.com").
SMTP_PORT: The SMTP server port (e.g., 587).
SENDER_EMAIL: The sender's email address.
SENDER_PASSWORD: The sender's email password or token.
RECIPIENT_EMAILS: A list of recipient email addresses.

2. Webpage URL:
url: The URL of the webpage to monitor for wildfire events.

3. File to Store the Last Monitored Event:
last_event_file: The file where the last monitored event code will be stored.

# Usage

1. Clone the Repository:
git clone https://github.com/yourusername/wildfire-alert-system.git
cd wildfire-alert-system

2. Configure the Script: Open the script and update the email configuration and URL to monitor.
Run the Script:
python wildfire_alert_system.py
The script will check the webpage for new wildfire events every 10 minutes and send an email alert if a new event is detected.

# Functions
- get_last_event(): Reads the last monitored event from the file.
- update_last_event(event): Updates the last monitored event in the file.
- send_email(subject, body, event_name, event_code, activation_date, location): Sends an email alert with the event details.
- check_for_new_event(): Checks the webpage for new wildfire events and sends an email alert if a new event is detected.
- main(): The main function that performs the periodic check for new events.

# License
GNU General Public License v3.0.

# This is an alert example:

(1) Fire alert  
(2) Issued: 2025-01-16  
(3) Country: France  
(4) Name: Wildfire in Amsterdam Island, France  
(5) Event code: EMSR785  
(6) Source: CEMS Rapid Mapping  
(7) Resource link: https://rapidmapping.emergency.copernicus.eu/EMSR785  
(8) Resource REST-API: https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR785  

CEMS Rapid Mapping portal: https://rapidmapping.emergency.copernicus.eu/backend/staticlist/?name=&category=fire&country=&activationTime__range_min=&activationTime__range_max=

# Contact:  
ACTRIS-ARES DC Unit  
Ermann Ripepi - ermann.ripepi@cnr.it  
Michele Volini - michele.volini@cnr.it
