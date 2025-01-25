import os
import time
import json
import requests
from dotenv import load_dotenv

# --------------------------------------------------------------
# Configuring OpenAI SDK
# --------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = 'https://api.openai.com/v1'

# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(request_body: dict) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }

    # Run the assistant
    run = requests.post(f'{OPENAI_BASE_URL}/threads/runs', headers = headers, data=json.dumps(request_body))

    if run.status_code != 200:
        print(f"Error: {run.status_code} - {run.text}")
        return None
    
    run = run.json()
    run_id = run['id']
    thread_id = run['thread_id']

    # Wait for completion
    while run.get("status") != "completed":
        time.sleep(0.5)
        run = requests.get(f'{OPENAI_BASE_URL}/threads/{thread_id}/runs/{run_id}', headers = headers)
        run = run.json()

    # Retrieve the Messages
    messages = requests.get(f'{OPENAI_BASE_URL}/threads/{thread_id}/messages', headers = headers)
    messages = messages.json()
    new_message = messages['data'][0]['content'][0]['text']['value']
    
    return new_message

# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body: str, assistant_id: str) -> str:
    #Create a thread with the message for OpenAI Assistant
    request_body = {
        "assistant_id": assistant_id,
        "thread": {
            "messages": [
                {
                    "role": "user",
                    "content": message_body
                }
            ]
        }
    }

    # Run the assistant
    new_message = run_assistant(request_body)
    return new_message

# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------
assistant_id = 'asst_zMq4YoycnKBDkE6FmXd0eBYV'
title = 'Modellierung sektoren\u00fcbergreifender Systemdienstleistungen bei gekoppelt betriebenem Strom- und Gassektor'
abstract = 'Aufgrund der steigenden Einspeisung elektrischer Leistung durch erneuerbare Energieanlagen und der gleichzeitig voranschreitenden schrittweisen Abschaltung von konventionellen Kohlekraftwerken, steigen die Anforderungen an eine zuverl\u00e4ssige, kosteng\u00fcnstige und klimafreundliche Bereitstellung von Flexibilit\u00e4ten zum Erhalt der Systemstabilit\u00e4t. Mit der Gesamtsystembetrachtung aus Strom- und Gassektor k\u00f6nnen durch die Kopplung neue Freiheitsgrade erschlossen werden. In diesem Beitrag wird vorgestellt, wie eine sektoren\u00fcbergreifende Erbringung von Systemdienstleistungen vom Strom- zum Gasnetz in einem dynamischen Energiesystemmodell im Zeitbereich der Mittelzeitdynamik abgebildet werden kann. Anhand von numerischen Fallstudien wird am Beispiel von Th\u00fcringen f\u00fcr verschiedene Szenarien ausgewertet, inwiefern durch eine sektoren\u00fcbergreifende Betrachtung Flexibilit\u00e4tspotenziale realisiert und die Betriebsgrenzen und somit die Stabilit\u00e4tsbedingungen beider Sektoren eingehalten werden k\u00f6nnen.'
message_body = f'"title": {title}\n"abstract": {abstract}'

gnd_tags = generate_response(message_body, assistant_id)
print(f'GND Tags:\n{json.dumps(json.loads(gnd_tags), indent=4)}')