import speech_recognition as SRG
import time
import speech
import json

def speech_to_text(src):
    store = SRG.Recognizer()
    store.energy_threshold = 4000
    print("Text recognizing...")
    print(src)

    try:
        with SRG.Microphone() as s:
            store.adjust_for_ambient_noise(s, duration=1)
            # audio_input = store.record(s, timeout=2)
            audio_input = store.listen(s, timeout=2)
        text_output = store.recognize_google(audio_input, language=src)
        # print(text_output)
        return text_output

    except SRG.WaitTimeoutError as e:
        response="Sorry about that, I didn't hear anything."
        return response
    except SRG.UnknownValueError:
        response="Sorry about that, I didn't hear anything."
        return response
    except SRG.RequestError as e:
        response="Sorry about that, I didn't hear anything."
        return response

# src="en"
# speech_to_text(src)


# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     recognizer.adjust_for_ambient_noise(source, duration=1)
#     print("Recording for 4 seconds")
#     recorded_audio = recognizer.listen(source, timeout=4)
#     print("Done recording")

# try:
#     text = recognizer.recognize_google(recorded_audio, language="en-US")
#     print(text)
# except Exception as ex:
#     print(ex)