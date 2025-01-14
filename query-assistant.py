from openai import OpenAI
from openai.types.beta import Thread
from dotenv import load_dotenv
import os
import time
import json

# --------------------------------------------------------------
# Configuring OpenAI SDK
# --------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread: Thread, assistant_id: str) -> str:
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistant_id)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    return new_message

# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body: str, assistant_id: str) -> str:
    #Create a thread with the message for OpenAI Assistant
    thread = client.beta.threads.create(messages=[
        {
            "role": "user",
            "content": message_body
        }
    ])

    # Run the assistant
    new_message = run_assistant(thread, assistant_id)
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