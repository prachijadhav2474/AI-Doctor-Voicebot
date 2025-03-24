import os
import platform
import subprocess
import logging
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from pydub import AudioSegment  # Needed for MP3 to WAV conversion

# Load environment variables from .env file
load_dotenv()

# Get API key securely
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def play_audio(output_filepath):
    """Plays the generated audio file across different operating systems."""
    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])  # Works on Linux

        elif os_name == "Windows":  # Windows
            # Try playing MP3 directly with mpg123
            try:
                subprocess.run(['mpg123', output_filepath])
            except FileNotFoundError:
                logging.warning("mpg123 not found! Converting MP3 to WAV for playback...")
                
                # Convert MP3 to WAV if mpg123 is not installed
                wav_filepath = output_filepath.replace(".mp3", ".wav")
                sound = AudioSegment.from_mp3(output_filepath)
                sound.export(wav_filepath, format="wav")

                # Play WAV file using PowerShell
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])

        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        logging.error(f"Error playing audio: {e}")


def text_to_speech_with_gtts(input_text, output_filepath="gtts_output.mp3"):
    """Convert text to speech using Google TTS (gTTS)."""
    try:
        logging.info("Generating speech with gTTS...")
        language = "en"
        audioobj = gTTS(text=input_text, lang=language, slow=False)
        audioobj.save(output_filepath)
        logging.info(f"Audio saved as {output_filepath}")

        # Play the generated audio
        play_audio(output_filepath)

    except Exception as e:
        logging.error(f"gTTS error: {e}")


def text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_output.mp3"):
    """Convert text to speech using ElevenLabs API."""
    if not ELEVENLABS_API_KEY:
        logging.error("ElevenLabs API key is missing! Please set ELEVENLABS_API_KEY in your environment.")
        return

    try:
        logging.info("Generating speech with ElevenLabs...")
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        logging.info(f"Audio saved as {output_filepath}")

        # Play the generated audio
        play_audio(output_filepath)

    except Exception as e:
        logging.error(f"ElevenLabs error: {e}")


# Example usage
if __name__ == "__main__":
    input_text = "Hello! This is an AI-powered voice test."

    # Uncomment the desired function to test
    text_to_speech_with_gtts(input_text, output_filepath="gtts_test.mp3")
    # text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_test.mp3")


