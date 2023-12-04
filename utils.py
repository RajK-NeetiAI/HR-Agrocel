import json
import uuid
import os
import tempfile

from dotenv import load_dotenv, find_dotenv
from google.cloud import dialogflow

import config


def transcribe_audio(audio_file_path: str) -> str:
    '''Conver the auido into text using Openai APIs

    Parameters:
        - audio_file_path(str): audio file path

    Return:
        - transcriptions of the audio
    '''
    try:
        audio_file = open(audio_file_path, 'rb')
        response = config.openai_client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            language='en'
        )
        transcription = response.text
        return transcription
    except:
        return config.ERROR_MESSAGE


def create_speech(text: str) -> str | None:
    '''Convert teext to audio using Openai APIs

    Parameters:
        - text(str): input text that is converted to audio

    Return:
        - audio file path or None
    '''
    try:
        speech_file_path = os.path.join(
            tempfile.gettempdir(),
            f'{uuid.uuid1()}.mp3'
        )
        response = config.openai_client.audio.speech.create(
            model='tts-1',
            voice='alloy',
            input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path
    except:
        return None


load_dotenv(find_dotenv())

CREDENTIALS = json.loads(os.getenv('CREDENTIALS'))
PROJECT_ID = CREDENTIALS['project_id']

CREDENTIAL_FILE_PATH = os.path.join(
    tempfile.gettempdir(),
    'credentials.json'
)

with open(CREDENTIAL_FILE_PATH, 'w') as file:
    json.dump(CREDENTIALS, file)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_FILE_PATH

session_client = dialogflow.SessionsClient()


def detect_intent(session_id: str, query: str, language_code: str) -> str:
    '''Detect intent of the user query

    Parameters:
        - session_id(str): a unique identifier for the request, this must be same for a conversation
        - query(str): user query
        - language_code(str): language code to detect the intent

    Return:
        - str: response of the detected intent
    '''
    try:
        session = session_client.session_path(PROJECT_ID, session_id)
        text_input = dialogflow.TextInput(
            text=query, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input}
        )
        return response.query_result.fulfillment_text
    except:
        return config.ERROR_MESSAGE


def format_dialogflow_response(messages: list[str], rich_contents: list = [], output_contexts: list[dict] = []) -> dict:
    response_data = {}
    response_data['fulfillmentMessages'] = []
    response_data['fulfillmentMessages'].append(
        {
            'text': {
                'text': messages
            }
        }
    )
    if (len(rich_contents) > 0):
        payload = {}
        payload['payload'] = {}
        payload['payload']['richContent'] = rich_contents
        response_data['fulfillmentMessages'].append(payload)
    if (len(output_contexts) > 0):
        response_data['outputContexts'] = output_contexts
    return response_data


def get_dialogflow_parameters(body: dict, context_name: str) -> dict:
    parameters = {}
    output_contexts = body['queryResult']['outputContexts']
    for oc in output_contexts:
        if context_name in oc['name']:
            parameters = oc['parameters']
    return parameters


def get_error_message():
    error_message = format_dialogflow_response([
        config.ERROR_MESSAGE
    ])
    return error_message
