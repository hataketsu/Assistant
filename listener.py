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
    os.system("mpv --ao=jack audio.mp3")


def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
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
        if data.startswith("bật đèn"):
            try:
                number = data[8]
                speak("Bạn nói: " + data)
                int(number)
                command = '0:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("tắt đèn"):
            try:
                number = data[8]
                speak("Bạn nói: " + data)
                int(number)
                command = '1:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("chớp đèn"):
            try:
                number = data[8]
                speak("Bạn nói: " + data)
                int(number)
                command = '-1:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("làm mờ đèn") and data.endswith("%"):
            try:
                number = data[11]
                percent = data[13:15].strip()
                speak("Bạn nói: " + data)
                percent = int(percent)
                command = str(percent / 100.0) + ':'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")


def send_cmd(command, number):
    client.publish('hataketsucontrolx/in', command + number)


speak("Xin chào, tôi có thể giúp gì cho bạn?")
while 1:
    data = recordAudio()
    jarvis(data)
