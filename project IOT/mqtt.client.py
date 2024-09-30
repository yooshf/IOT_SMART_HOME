import paho.mqtt.client as mqtt  # import the client
import time
import random

# broker list
brokers = ["iot.eclipse.org", "broker.hivemq.com", "test.mosquitto.org"]

broker = brokers[1]  # אפשר לשנות לברוקר הרצוי

# עדכון נושא לפרסום
pub_topic = 'pr/home/sensors/windows'  # עדכן את הנושא כך שיתאים למערכת שלך


def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
        client.subscribe(pub_topic)
        print(f"Subscribed to {pub_topic}")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received: ", m_decode)


client = mqtt.Client("IOT_client_" + str(random.randint(1000, 9999)), clean_session=True)  # create new client instance

client.on_connect = on_connect  # bind call back function
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message
print("Connecting to broker ", broker)
port = 1883
client.connect(broker, port)  # connect to broker

client.loop_start()

try:
    for x in range(21):
        mylist1 = ['open', 'close']
        b = random.choice(mylist1)
        if b == "open":
            message = "There are open windows on floor " + str(x) + ". The system will close the windows :)"
        else:
            message = "There are no open windows on the floor " + str(x)

        print(f"Publishing message: {message}")
        client.publish(pub_topic, message)
        print(f"Published message to {pub_topic}: {message}")
        time.sleep(5)

    client.publish(pub_topic, "The scan is finished :)")
    print(f"Published message to {pub_topic}: The scan is finished :)")
finally:
    print("Disconnecting from broker")
    client.disconnect()  # disconnect
    client.loop_stop()
    print("End publish_client run script")
