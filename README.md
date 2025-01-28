# CEMS Rapid Mapping alerting code

This Python script detects if there is a new WildFire event on the CEMS Rapid Mapping portal and sends an email containing the following information:  

(1) Fire alert  
(2) Issued:   
(3) Country:   
(4) Name:   
(5) Event code:   
(6) Source:   
(7) Resource link:   
(8) Resource REST-API: 

This is an example:

(1) Fire alert  
(2) Issued: 2025-01-16  
(3) Country: France  
(4) Name: Wildfire in Amsterdam Island, France  
(5) Event code: EMSR785  
(6) Source: CEMS Rapid Mapping  
(7) Resource link: https://rapidmapping.emergency.copernicus.eu/EMSR785  
(8) Resource REST-API: https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/?code=EMSR785  

CEMS Rapid Mapping portal: https://rapidmapping.emergency.copernicus.eu/backend/staticlist/?name=&category=fire&country=&activationTime__range_min=&activationTime__range_max=

As soon as possible, we will integrate other information related to the description of the script.  

Contact:  
ACTRIS-ARES DC Unit
Ermann Ripepi - ermann.ripepi@cnr.it
