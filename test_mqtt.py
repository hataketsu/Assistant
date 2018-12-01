import paho.mqtt.client as paho

broker = "broker.hivemq.com"


def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))


client = paho.Client("client-001asa")
client.on_message = on_message
print("connecting to broker ", broker)
client.connect(broker)
print("subscribing ")
client.subscribe("hataketsu")  # subscribe
client.loop_forever()
