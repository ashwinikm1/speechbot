import logging
import os
import time
import uuid

from google.cloud import texttospeech
from deep_translator import GoogleTranslator
from google.api_core.client_options import ClientOptions

from util import delete_file



LANGUAGE = os.getenv("LANGUAGE", "hi-IN")
API_KEY = "AIzaSyAa1HbCTRBpgnH_l_6b6sl26AccQikKc8w" # Replace with your API key
PROJECT_ID = "tough-buffalo" # Replace with your project ID.

TTS_PROVIDER = os.getenv("TTS_PROVIDER", "googleTTS")


async def to_speech(text, background_tasks):
    if TTS_PROVIDER == "googleTTS":
        return await _google_text_to_speech(text, background_tasks)
    else:
        raise ValueError(f"env var TTS_PROVIDER set to unsupported value: {TTS_PROVIDER}")


async def _google_text_to_speech(text, background_tasks):
    start_time = time.time()

    # Instantiates a client
    # Use API key for authentication
    client_options = ClientOptions(api_key=API_KEY)
    client = texttospeech.TextToSpeechClient(client_options=client_options)


    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US")
    # and the ssml voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code='hi-IN',
        name='hi-IN-Chirp3-HD-Aoede',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(request={"input": synthesis_input, "voice": voice, "audio_config": audio_config})

    # The response's audio_content is binary.
    filepath = f"/tmp/{uuid.uuid4()}.wav"
    with open(filepath, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ')

    background_tasks.add_task(delete_file, filepath)

    logging.info('TTS time: %s %s', time.time() - start_time, 'seconds')
    return filepath