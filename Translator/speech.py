from gtts import gTTS
import os
from playsound import playsound

def play_text(text,language):
    tts = gTTS(text, lang=language)
    tts.save("static/speech.mp3")
    return playsound('static/speech.mp3'),os.remove("static/speech.mp3")  

# mytext="good morning"
# language="en"
# play_text(mytext, language)