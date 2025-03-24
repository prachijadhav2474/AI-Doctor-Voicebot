# AI-Doctor-Voicebot

Overview

AI-Doctor Voicebot is an AI-powered medical assistant that processes voice and image inputs to provide health-related guidance. It utilizes Groq API for AI-driven responses, ElevenLabs & gTTS for text-to-speech, and Whisper for speech recognition.

Features

Speech-to-Text: Converts patient speech into text using Whisper (via Groq API).

Text Analysis & Diagnosis: AI-generated responses based on user symptoms.

Image Processing: Analyzes uploaded images for skin-related issues.

Text-to-Speech: Converts AI-generated responses to voice output using gTTS & ElevenLabs.

Interactive UI: Built with Gradio for easy interaction.

Tech Stack

Python

Gradio (for UI)

Groq API (for AI analysis & transcription)

gTTS & ElevenLabs (for voice synthesis)

SpeechRecognition & pydub (for audio processing)

Base64 (for image encoding)

Dotenv (for API key management)
