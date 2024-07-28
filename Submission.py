import requests
import json

github_repo = "https://github.com/SafaSadiq/DPS_AI_Challenge"
email = "safasadiq999@gmail.com"
submission_url = "https://us-central1-dpsaichallenge.cloudfunctions.net/dpsaichallenge"

payload = {
    "github": github_repo,
    "email": email,
    "url": submission_url
}

headers = {
    "Content-Type": "application/json"
}

url = "https://dps-challenge.netlify.app/.netlify/functions/api/challenge"
response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)