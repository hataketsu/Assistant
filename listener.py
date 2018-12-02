import os
import time

import paho.mqtt.client as paho
import speech_recognition as sr
from gtts import gTTS

client = paho.Client("rasp-001asa" + str(time.time()))

flag_connected = 0


def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1


def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0


client.on_connect = on_connect
client.on_disconnect = on_disconnect
print('connecting')
client.connect("broker.hivemq.com")
print('connected')


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
                int(number)
                speak("Bạn nói: " + data)
                command = '0:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("tắt đèn"):
            try:
                number = data[8]
                int(number)
                speak("Bạn nói: " + data)
                command = '1:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("chớp đèn"):
            try:
                number = data[8]
                int(number)
                speak("Bạn nói: " + data)
                command = '-1:'
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")
        elif data.startswith("làm mờ đèn") and data.endswith("%"):
            try:
                number = data[11]
                percent = data[13:15].strip()
                percent = int(percent)
                command = str(percent / 100.0) + ':'
                speak("Bạn nói: " + data)
                send_cmd(command, number)
            except Exception:
                speak("câu lệnh lỗi")


def send_cmd(command, number):
    while flag_connected == 0:
        client.connect("broker.hivemq.com")
        time.sleep(0.1)
        client.loop()
    client.publish('hataketsucontrolx/in', command + number)


speak("Xin chào, tôi có thể giúp gì cho bạn?")
while 1:
    client.loop()
    data = recordAudio()
    jarvis(data)
