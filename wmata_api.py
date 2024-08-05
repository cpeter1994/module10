import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "e13626d03d8e4c03ac07f95541b3091b"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []

    # use 'requests' to do a GET request to the WMATA Incidents API
    # retrieve the JSON from the response
    response = requests.get(INCIDENTS_URL, headers=headers)
    data = response.json()

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    for incident in data.get('ElevatorIncidents', []):
        if incident.get('UnitType', '').lower() == unit_type.lower():
            # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
            # -StationCode, StationName, UnitType, UnitName
            incident_dict = {
                'StationCode': incident.get('StationCode'),
                'StationName': incident.get('StationName'),
                'UnitType': incident.get('UnitType'),
                'UnitName': incident.get('UnitName')
            }

            # add each incident dictionary object to the 'incidents' list
            incidents.append(incident_dict)

    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)