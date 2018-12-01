import time

import paho.mqtt.client as paho


def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))


client = paho.Client("rasp-001asa"+str(time.time()))
client.on_message = on_message
client.connect("broker.hivemq.com")
client.subscribe("hataketsu")
# client.loop_forever()
while True:
    time.sleep(1)
    client.publish('hataketsu','fuck')