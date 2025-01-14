from openai import OpenAI
from openai.types import FileObject
from openai.types.beta import Assistant
from openai.types.beta import VectorStore
from dotenv import load_dotenv
import os

# --------------------------------------------------------------
# Configuring OpenAI SDK
# --------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------------------
# Read text file
# --------------------------------------------------------------
def read_text_file(filepath: str, enc: str = 'utf-8') -> str:
    with open(file = filepath, mode = 'r', encoding = enc) as f:
        data = f.read()
    return data

# --------------------------------------------------------------
# Create Vector Store
# --------------------------------------------------------------
def create_vector_store(name: str) -> VectorStore:
    return client.beta.vector_stores.create(name = name)

# --------------------------------------------------------------
# Upload file
# --------------------------------------------------------------
def upload_file(filepath: str, vector_store: VectorStore) -> FileObject:
    file = client.files.create(file=open(filepath, "rb"), purpose="assistants")
    vector_store_file = client.beta.vector_stores.files.create(vector_store_id = vector_store.id, file_id = file.id)
    return file

# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------
def create_assistant(assis_name: str, assis_description: str, assis_instruction: str, openai_model: str, vector_sore: VectorStore) -> Assistant:
    assistant = client.beta.assistants.create(
        name = assis_name,
        description = assis_description,
        instructions = assis_instruction,
        tools = [{"type": "file_search"}],
        model = openai_model,
        response_format = { "type": "json_object" },
        tool_resources = {
            "file_search": {
                "vector_store_ids": [vector_sore.id]
            }
        }
    )
    return assistant

if __name__ == "__main__":
    # --------------------------------------------------------------
    # Creating assistant 01: LLMs4Subjects-all-subjects
    # --------------------------------------------------------------
    print('Creating OpenAI Assistant 01: LLMs4Subjects-all-subjects')
    
    #Setting the assistant paramters
    assistant_name = 'LLMs4Subjects-all-subjects'
    assistant_description = 'A baseline assistant for LLMs4Subject--all-subjects indexing shared task!'
    openai_model = 'gpt-4o'
    vector_store_name = 'vector_store_all_subjects'
    instruction_filepath = './resources/prompts/system-prompt.txt'
    gnd_all_subjects_filepath = './resources/files/GND-Subjects-all.json'
    
    print(f'\nReading the System prompt file: {instruction_filepath}')
    assistant_instruction = read_text_file(instruction_filepath)
    
    print('\nCreating a Vector Store')
    vector_store = create_vector_store(name = vector_store_name)
    print(f'Vector Store created with ID: {vector_store.id}')
    
    print(f'\nUploading the file: {gnd_all_subjects_filepath} to the OpenAI that can be used across various endpoints.')
    all_subjects_file = upload_file(gnd_all_subjects_filepath, vector_store)
    print(f'File uploaded with ID: {all_subjects_file.id}')
    
    print(f'\nCreating the OpenAI Assistant: {assistant_name} with LLM: {openai_model}')
    all_subject_assistant = create_assistant(assistant_name, assistant_description, assistant_instruction, openai_model, vector_store)
    print(f'OpenAI Assistant Created with the following properties:')
    print(f'Name: {all_subject_assistant.name}\nID: {all_subject_assistant.id}')
    
    # --------------------------------------------------------------
    # Creating assistant 02: LLMs4Subjects-tib-core-subjects
    # --------------------------------------------------------------
    print('Creating OpenAI Assistant 02: LLMs4Subjects-tib-core-subjects')
    
    #Setting the assistant paramters
    assistant_name = 'LLMs4Subjects-tib-core-subjects'
    assistant_description = 'A baseline assistant for LLMs4Subject--tib-core-subjects indexing shared task!'
    openai_model = 'gpt-4o'
    vector_store_name = 'vector_store_tib_core_subjects'
    instruction_filepath = './resources/prompts/system-prompt.txt'
    gnd_tib_core_subjects_filepath = './resources/files/GND-Subjects-tib-core.json'
    
    print(f'\nReading the System prompt file: {instruction_filepath}')
    assistant_instruction = read_text_file(instruction_filepath)
    
    print('\nCreating a Vector Store')
    vector_store = create_vector_store(name = vector_store_name)
    print(f'Vector Store created with ID: {vector_store.id}')
    
    print(f'\nUploading the file: {gnd_tib_core_subjects_filepath} to the OpenAI that can be used across various endpoints.')
    tib_core_subjects_file = upload_file(gnd_tib_core_subjects_filepath, vector_store)
    
    print(f'\nCreating the OpenAI Assistant: {assistant_name} with LLM: {openai_model}')
    tib_core_subject_assistant = create_assistant(assistant_name, assistant_description, assistant_instruction, openai_model, vector_store)
    print(f'OpenAI Assistant Created with the following properties:')
    print(f'Name: {tib_core_subject_assistant.name}\nID: {tib_core_subject_assistant.id}')