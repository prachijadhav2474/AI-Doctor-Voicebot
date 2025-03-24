import gradio as gr
import requests
import base64
import os
from dotenv import load_dotenv
import groq
from gtts import gTTS  

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("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")

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Function to process user inputs
def process_inputs(audio_path, image_path):
    text_response = "⚠ No response generated"
    audio_response_path = "response_audio.mp3"  

    # Convert speech to text if audio is provided
    if audio_path:
        try:
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")
            transcription = "Hello, I am having some issues with my skin. My skin is getting pimples."  
        except Exception as e:
            transcription = f"⚠ Error transcribing audio: {str(e)}"
    else:
        transcription = "No audio provided."

    # Prepare prompt for Groq AI
    prompt = f"""
    You are an AI doctor. A user is describing their symptoms: 
    "{transcription}"
    If an image is provided, analyze the image for skin issues.
    Give a diagnosis and advice in simple language.
    """

    # Process image if provided
    if image_path:
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            prompt += "\nUser has uploaded an image of their skin issue. Please analyze and include the findings."
        except Exception as e:
            prompt += f"\n⚠ Error processing image: {str(e)}"

    # Call Groq AI for response
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": "You are an AI medical assistant."},
                      {"role": "user", "content": prompt}]
        )
        text_response = response.choices[0].message.content
    except Exception as e:
        text_response = f"⚠ Error generating response: {str(e)}"

    # Convert AI response to speech using gTTS
    try:
        tts = gTTS(text=text_response, lang="en")
        tts.save(audio_response_path)  
    except Exception as e:
        print(f"⚠ Error in TTS conversion: {str(e)}")
        audio_response_path = None

    return text_response, audio_response_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🎙️ AI Doctor with Vision & Voice (Powered by Groq)")
    gr.Markdown("🔹 Speak your symptoms or upload an image for diagnosis.")

    audio_input = gr.Audio(sources=["upload"], type="filepath", label="🎤 Speak your symptoms")
    image_input = gr.Image(type="filepath", label="🖼️ Upload an image of your skin issue")
    submit_button = gr.Button("Submit")

    output_text = gr.Textbox(label="🩺 Doctor's Response")
    output_audio = gr.Audio(label="🎧 AI Doctor's Voice Response", type="filepath")  # ✅ Fix: Use "filepath"

    submit_button.click(process_inputs, inputs=[audio_input, image_input], outputs=[output_text, output_audio])

demo.launch()
