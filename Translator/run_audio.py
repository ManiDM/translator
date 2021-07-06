# import speech
# mytext=str(input("Enter text: "))
# language="en"
# speech.play_text(mytext,language)

# import speech_recognition as sr
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Talk")
#     audio_text = r.listen(source)
#     print("Time over, thanks")  
#     try:
#         print("Text: "+r.recognize_google(audio_text))
#     except:
#          print("Sorry, I did not get that")

import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 4000

with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    # print("Time over, thanks")
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    
    try:
        # using google speech recognition
        print("Text: "+r.recognize_google(audio_text))
    except:
         print("Sorry, I did not get that")