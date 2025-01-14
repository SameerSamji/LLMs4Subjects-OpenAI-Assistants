# LLMs4Subjects -- Creating Baseline OpenAI Assistants

## 💡 About

This repository contains scripts to programmatically create and query OpenAI Assistants. It demonstrates this process using the [LLMs4Subjects](https://sites.google.com/view/llms4subjects/home) shared task use case.

## 🧪 Installation

Install all the necessary Python packages listed in the [requirements.txt](requirements.txt) file.

```bash
pip install -r requirements.txt
```

## 🧑‍💻 Tool Usage

### 🛠️ Configuration

Parameters such as API keys and model settings are managed using a dedicated environment file. The .env file has to be saved at the root directory of this project.

### Creating the OpenAI Assistants

The [script](create-assistant.py) script demonstrates the creation of OpenAI Assistants for the LLMs4Subjects use case. Two different assistants are created:

1. GND all-subjects
2. GND tib-core-subjects

The file [GND-Subjects-all.json](resources/files/GND-Subjects-all.json) contains the GND subjects for all subjects while [GND-Subjects-tib-core.json](resources/files/GND-Subjects-tib-core.json) contains the GND subjects for TIB Core related subjects. These files are uploaded to the OpenAI vector store, allowing them to be accessed by the Assistants.

```bash
$ create-assistant.py
Creating OpenAI Assistant 01: LLMs4Subjects-all-subjects

Reading the System prompt file: ./resources/prompts/system-prompt.txt

Creating a Vector Store
Vector Store created with ID: vs_ioziLiY0eaylEfTPrywoA5Bf

Uploading the file: ./resources/files/GND-Subjects-all.json to the OpenAI that can be used across various endpoints.
File uploaded with ID: file-C1NaousD3zRcMvhmjjALo7

Creating the OpenAI Assistant: LLMs4Subjects-all-subjects with LLM: gpt-4o
OpenAI Assistant Created with the following properties:
Name: LLMs4Subjects-all-subjects
ID: asst_zMq4YoycnKBDkE6FmXd0eBYV
```

### Querying the OpenAI Assistants

The [script](query-assistant.py) script demonstrates how to query an assistant with a user message. For the LLMs4Subjects use case, the relevant assistant ID, along with the title and abstract of an article, is provided to obtain the corresponding GND labels.

Example usage for the LLMs4Subjects-all-subjects assistant:

```python
assistant_id = 'asst_zMq4YoycnKBDkE6FmXd0eBYV'
title = 'Modellierung sektoren\u00fcbergreifender Systemdienstleistungen bei gekoppelt betriebenem Strom- und Gassektor'
abstract = 'Aufgrund der steigenden Einspeisung elektrischer Leistung durch erneuerbare Energieanlagen und der gleichzeitig voranschreitenden schrittweisen Abschaltung von konventionellen Kohlekraftwerken, steigen die Anforderungen an eine zuverl\u00e4ssige, kosteng\u00fcnstige und klimafreundliche Bereitstellung von Flexibilit\u00e4ten zum Erhalt der Systemstabilit\u00e4t. Mit der Gesamtsystembetrachtung aus Strom- und Gassektor k\u00f6nnen durch die Kopplung neue Freiheitsgrade erschlossen werden. In diesem Beitrag wird vorgestellt, wie eine sektoren\u00fcbergreifende Erbringung von Systemdienstleistungen vom Strom- zum Gasnetz in einem dynamischen Energiesystemmodell im Zeitbereich der Mittelzeitdynamik abgebildet werden kann. Anhand von numerischen Fallstudien wird am Beispiel von Th\u00fcringen f\u00fcr verschiedene Szenarien ausgewertet, inwiefern durch eine sektoren\u00fcbergreifende Betrachtung Flexibilit\u00e4tspotenziale realisiert und die Betriebsgrenzen und somit die Stabilit\u00e4tsbedingungen beider Sektoren eingehalten werden k\u00f6nnen.'
message_body = f'"title": {title}\n"abstract": {abstract}'

gnd_tags = generate_response(message_body, assistant_id)
print(f'GND Tags:\n{json.dumps(json.loads(gnd_tags), indent=4)}')
```

```bash
$ query-assistant.py
GND Tags:
{
    "GND_subject_codes": [
        {
            "code": "4299793-6",
            "name": "Energiesysteme"
        },
        {
            "code": "4034873-7",
            "name": "Stromerzeugung"
        },
        {
            "code": "4034879-9",
            "name": "Gaswirtschaft"
        },
        {
            "code": "4551504-6",
            "name": "Systemdienstleistung"
        },
        {
            "code": "4617977-3",
            "name": "Erneuerbare Energie"
        },
        {
            "code": "4696286-6",
            "name": "Sektor\u00fcbergreifende Zusammenarbeit"
        }
    ]
}
```