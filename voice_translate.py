import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import time
import os


# Initialize
recognizer = sr.Recognizer()

SAMPLE_RATE = 44100
DURATION = 5   # Recording time in seconds


# Record voice
def record_audio():

    print("🎤 Speak in English (5 seconds)...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("input.wav", SAMPLE_RATE, recording)


# Convert voice to text
def listen_english():

    record_audio()

    with sr.AudioFile("input.wav") as source:

        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text

        except:
            print("❌ Could not understand. Try again.")
            return None


# Translate English to Kannada
def translate_to_kannada(text):

    translator = GoogleTranslator(source="en", target="kn")

    return translator.translate(text)


# Speak Kannada safely
def speak_kannada(text):

    tts = gTTS(text=text, lang="kn")

    filename = "kannada.mp3"

    tts.save(filename)

    pygame.mixer.init()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait till audio finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Wait for Windows to release file
    time.sleep(1)

    # Delete file safely
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            pass


# ================= MAIN PROGRAM =================

print("======================================")
print(" English ➜ Kannada Voice Translator ")
print(" Python 3.13 Compatible Version ")
print(" Say 'exit' to stop ")
print("======================================\n")


while True:

    english_text = listen_english()

    if english_text:

        if english_text.lower() == "exit":
            print("Program Closed.")
            break

        kannada_text = translate_to_kannada(english_text)

        print("Kannada:", kannada_text)

        speak_kannada(kannada_text)

    print("----------------------------------\n")