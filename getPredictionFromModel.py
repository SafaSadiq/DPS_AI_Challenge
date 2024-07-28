import requests
import json

payload = {
    "year": "2021",
    "month": "01"
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
url = "https://us-central1-dpsaichallenge.cloudfunctions.net/dpsaichallenge"
response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)