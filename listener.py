import os

import speech_recognition as sr
from gtts import gTTS


def speak(audioString, lang='vi'):
    print(audioString)
    tts = gTTS(text=audioString, lang=lang, )
    tts.save("audio.mp3")
    os.system("mpv audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio, language='vi-VN')
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


def jarvis(data):
    if len(data.strip()) == 0:
        return
    if data.lower() == "thư ký":
        speak("Sẵn sàng")
    else:
        speak("Bạn nói: " + data)
        if "khỏe không" in data:
            speak("Khỏe v l")
            speak("Phịch nhau đi em")


speak("Xin chào, tôi có thể giúp gì cho bạn?")
while 1:
    data = recordAudio()
    jarvis(data)
