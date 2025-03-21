from google.cloud import texttospeech
import os

# Replace with your API key and project ID or set GOOGLE_APPLICATION_CREDENTIALS
API_KEY = "AIzaSyAa1HbCTRBpgnH_l_6b6sl26AccQikKc8w" # Replace with your API key
PROJECT_ID = "tough-buffalo" # Replace with your project ID.

def text_to_speech(text, output_filename="output.mp3"):
    """Converts text to speech and saves it to an MP3 file."""

    client = texttospeech.TextToSpeechClient(client_options={"api_key": API_KEY})

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code='hi-IN',
        name='hi-IN-Neural2-C',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file: {output_filename}')

# Example usage
text_to_convert = "Namashkar, Yeh ek asaann bhasa mai samjhane ki koshish hai. Asha karta hu aapko samajh aaya hoga"
text_to_speech(text_to_convert)