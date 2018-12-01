import os
import time

import paho.mqtt.client as paho
import speech_recognition as sr
from gtts import gTTS

client = paho.Client("rasp-001asa" + str(time.time()))
client.connect("broker.hivemq.com")


def speak(audioString, lang='vi'):
    print(audioString)
    tts = gTTS(text=audioString, lang=lang, )
    tts.save("audio.mp3")
    os.system("mpv audio.mp3")


def recordAudio():
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

    return data.strip().lower()


def jarvis(data):
    if len(data) == 0:
        return
    if data == "thư ký":
        speak("Sẵn sàng")
    else:
        speak("Bạn nói: " + data)
        if data.startswith("bật đèn"):
            number = data[8]
            command = '0:'
            client.publish('hataketsucontrol/in', command + number)
        elif data.startswith("tắt đèn"):
            number = data[8]
            command = '1:'
            client.publish('hataketsucontrol/in', command + number)


speak("Xin chào, tôi có thể giúp gì cho bạn?")
while 1:
    data = recordAudio()
    jarvis(data)
