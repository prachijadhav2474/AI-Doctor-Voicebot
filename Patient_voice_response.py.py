import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

# Set FFmpeg path
AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Get API Key from Environment (Ensure this is set correctly)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  

# Speech-to-Text Model
stt_model = "whisper-large-v3"

# Audio Recording Function
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert recorded audio to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Transcription Function
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

# 🔹 Main Execution
audio_filepath = "patient_voice_test.mp3"
record_audio(file_path=audio_filepath)

if GROQ_API_KEY:
    transcription_result = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
    print("Transcription:", transcription_result)  # ✅ This will display the transcription output
else:
    logging.error("Groq API key is missing. Set the GROQ_API_KEY environment variable.")

#setup Audio recorder(ffmeg & portaudio)
