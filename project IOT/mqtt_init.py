import paho.mqtt.client as mqtt
import time
import random
import socket

# Configuration
nb = 1  # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com
brokers = [str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com'))]
ports = [80, 1883]
usernames = ['MATZI', '']  # should be modified for HIT
passwords = ['MATZI', '']  # should be modified for HIT
mzs = ['matzi/', '']

# עדכון נושאים עבור הבית החכם
sub_topics = [mzs[nb] + 'sensors/updates', 'pr/home/sensors/#']  # נושאים לתחום הבית החכם
pub_topics = [mzs[nb] + 'test', 'pr/home/sensors/publish']  # נושאים לפרסום נתונים

broker_ip = brokers[nb]  # השתמש בכתובת ה-IP של ה-broker שנבחר
broker_port = ports[nb]
username = usernames[nb]
password = passwords[nb]
sub_topic = sub_topics[nb]
pub_topic = pub_topics[nb]


def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        client.subscribe(sub_topic)  # הירשם לנושא הנכון
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, rc=0):
    print("Disconnected result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received: ", m_decode)


client = mqtt.Client("IOT_client-" + str(random.randint(1000, 9999)), clean_session=True)  # יצירת מופע חדש

client.on_connect = on_connect  # חיבור פונקציית callback
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

if username and password:
    client.username_pw_set(username, password)

print("Connecting to broker ", broker_ip)
client.connect(broker_ip, broker_port)  # התחברות ל-broker

try:
    for x in range(8):
        mylist1 = ['open', 'close']
        b = random.choice(mylist1)
        if b == "open":
            message = "There is an open window on the " + str(x+1) + " floor, Don't worry, the system will close the window for you"
        else:
            message = "There is no open window on the " + str(x+1) + " floor "

        print(f"Publishing message: {message}")
        client.publish(pub_topic, message)
        time.sleep(3)
    client.publish(pub_topic, "Windows test scan finished ")
    for x in range(8):
        mylist1 = ['open', 'close']
        b = random.choice(mylist1)
        if b == "open":
            message = "There is an open shutter on the " + str(x+1) + " floor, Don't worry, the system will close the shutter for you"
        else:
            message = "There is no open shutter on the " + str(x+1) + " floor "

        print(f"Publishing message: {message}")
        client.publish(pub_topic, message)
        time.sleep(3)
    client.publish(pub_topic, "A scan to check the shutters has finished ")
    for x in range(8):
        mylist1 = ['open', 'close']
        b = random.choice(mylist1)
        if b == "open":
            message = "There is a light on on floor number " + str(x+1) + " , Don't worry, the system will close the window for you"
        else:
            message = "There is no light on on floor number " + str(x+1) 

        print(f"Publishing message: {message}")
        client.publish(pub_topic, message)
        time.sleep(3)
    client.publish(pub_topic, "The scan to check the lights is over")
finally:
    print("Disconnecting from broker")
    client.disconnect()  # ניתוק
    print("End publish_client run script")
