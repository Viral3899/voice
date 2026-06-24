import os
import requests

try:
    import pyttsx3
    HAVE_PYTTSX3 = True
except ImportError:
    HAVE_PYTTSX3 = False

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource
)

from fastapi import UploadFile

from config import settings


# ------------------------
# Deepgram Client
# ------------------------

deepgram = DeepgramClient(
    settings.DEEPGRAM_API_KEY
)


# ------------------------
# Speech To Text
# ------------------------

async def speech_to_text(
    audio: UploadFile
):

    data = await audio.read()

    payload: FileSource = {

        "buffer": data

    }

    options = PrerecordedOptions(

        model="nova-3",

        smart_format=True,

        punctuate=True,

        language="en"

    )

    response = deepgram.listen.rest.v("1").transcribe_file(

        payload,

        options

    )

    transcript = response.results.channels[0]\
        .alternatives[0].transcript

    return {

        "success": True,

        "text": transcript

    }



# ------------------------
# Cartesia TTS
# ------------------------

CARTESIA_URL = "https://api.cartesia.ai/tts/bytes"


def text_to_speech(
    text: str
):
    if HAVE_PYTTSX3:
        engine = pyttsx3.init()
        output_path = "generated_audio.wav"
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return {
            "success": True,
            "audio_file": output_path
        }

    if not settings.CARTESIA_API_KEY:
        return {
            "success": False,
            "message": "No Cartesia API key configured and pyttsx3 is unavailable."
        }

    # Fallback to local pyttsx3 if installed; Cartesia call is deprecated.
    output_path = "generated_audio.wav"
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return {
        "success": True,
        "audio_file": output_path
    }
# ------------------------
# Optional helper
# ------------------------

def delete_audio_file(

    filepath

):

    try:

        if os.path.exists(

            filepath

        ):

            os.remove(

                filepath

            )

    except:

        pass