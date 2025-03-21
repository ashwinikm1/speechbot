import asyncio
import os
import uuid
from io import BytesIO
import logging
import time

from google.cloud import speech_v1 as speech
from google.api_core.client_options import ClientOptions

import ffmpeg
import shutil

from util import delete_file  # Ensure you have this file.

LANGUAGE = os.getenv("LANGUAGE", "hi-IN")
API_KEY = "AIzaSyAa1HbCTRBpgnH_l_6b6sl26AccQikKc8w" # Replace with your API key
PROJECT_ID = "tough-buffalo" # Replace with your project ID.

async def transcribe(audio):
    start_time = time.time()
    initial_filepath = f"/tmp/{uuid.uuid4()}{audio.filename}"

    with open(initial_filepath, "wb+") as file_object:
        shutil.copyfileobj(audio.file, file_object)

    converted_filepath = f"/tmp/ffmpeg-{uuid.uuid4()}{audio.filename}"

    logging.debug("running through ffmpeg")
    (
        ffmpeg
        .input(initial_filepath)
        .output(converted_filepath, loglevel="error")
        .run()
    )
    logging.debug("ffmpeg done")

    delete_file(initial_filepath)

    # Use API key for authentication
    client_options = ClientOptions(api_key=API_KEY)
    client = speech.SpeechClient(client_options=client_options)

    with open(converted_filepath, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # Adjust if needed
        sample_rate_hertz=16000, # Adjust if needed
        language_code=LANGUAGE,
    )

    logging.debug("calling Google Cloud Speech API")
    request = speech.RecognizeRequest(config=config, audio=audio)

    try:
        response = client.recognize(request=request)
    except Exception as e:
        logging.error(f"Speech-to-Text API error: {e}")
        return "Error during transcription."

    logging.info("STT response received from Google Cloud Speech in %s seconds", time.time() - start_time)

    # Extract transcript from the response
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    logging.info('Transcript: %s', transcript)

    delete_file(converted_filepath)

    return transcript

class MockAudio:
    def __init__(self, filename, file):
        self.filename = filename
        self.file = file 

async def main():
    audio_file_path = "./test_files/02-15045-01.mp3"  # Replace with your audio file path.
    with open(audio_file_path, "rb") as audio_file:
        audio_content = audio_file.read()

    mock_audio = MockAudio(os.path.basename(audio_file_path), BytesIO(audio_content))

    transcript = await transcribe(mock_audio)
    print("Transcript:", transcript)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())