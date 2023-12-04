import uuid
import os
import tempfile

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
