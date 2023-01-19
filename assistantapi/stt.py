import io
import os

import numpy as np
from google.cloud import speech
from scipy.io import wavfile

from assistantapi.config import GOOGLE_APPLICATION_CREDENTIALS

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


def transcribe_file(speech_file, fs=48000):
    """Transcribe the given audio file."""

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=fs,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    return {"transcript": response.results[0].alternatives[0].transcript}


def transcribe(content, fs=48000):
    """Transcribe the given audio file."""

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=fs,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    total_result = ""
    for result in response.results:
        total_result += result.alternatives[0].transcript
    return total_result


def transcribe_bytes(data, fs=48000):
    data_bytes = io.BytesIO()
    wavfile.write(data_bytes, fs, data)
    try:
        transcription = transcribe(data_bytes.read(), fs)
    except Exception:
        abort(500)
    return transcription
