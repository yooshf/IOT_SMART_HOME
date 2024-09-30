import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt

from mqtt_init import username, password, broker_port, broker_ip

# MQTT and GUI configurations
clientname = "IOT_client-Id-" + str(random.randrange(1, 10000000))
relay_topic = 'pr/home/' + str(random.randrange(1, 10000000)) + '/sts'
ON = False


class MqttClient:

    def __init__(self):
        self.broker = ''
        self.port = 1883
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.client = None
        self.on_connected_to_form = None

    # Setters and getters
    def set_on_connected_to_form(self, callback):
        self.on_connected_to_form = callback

    def set_broker(self, broker):
        self.broker = broker

    def set_port(self, port):
        self.port = port

    def set_clientname(self, clientname):
        self.clientname = clientname

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def connect_to(self):
        self.client = mqtt.Client(self.clientname, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
        except Exception as e:
            print(f"Connection failed: {e}")

    def disconnect_from(self):
        self.client.disconnect()

    def on_log(self, client, userdata, level, buf):
        print(f"log: {buf}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected OK")
            if self.on_connected_to_form:
                self.on_connected_to_form()
        else:
            print(f"Bad connection, returned code={rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}")

    def on_message(self, client, userdata, msg):
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print(f"Message from {msg.topic}: {m_decode}")
        mainwin.connectionDock.update_btn_state(m_decode)

    def subscribe_to(self, topic):
        self.client.subscribe(topic)

    def publish_to(self, topic, message):
        self.client.publish(topic, message)


class ConnectionDock(QDockWidget):

    def __init__(self, mc):
        super().__init__()
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)

        self.init_ui()

    def init_ui(self):
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(relay_topic)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.ePushtbtn = QPushButton("", self)
        self.ePushtbtn.setStyleSheet("background-color: gray")

        formLayout = QFormLayout()
        formLayout.addRow("Turn On/Off", self.eConnectbtn)
        formLayout.addRow("Sub topic", self.eSubscribeTopic)
        formLayout.addRow("Status", self.ePushtbtn)

        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientname(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.subscribe_to(self.eSubscribeTopic.text())

    def update_btn_state(self, text):
        global ON
        if ON:
            self.ePushtbtn.setStyleSheet("background-color: gray")
            ON = False
        else:
            self.ePushtbtn.setStyleSheet("background-color: red")
            ON = True


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mc = MqttClient()
        self.init_ui()

    def init_ui(self):
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setGeometry(30, 300, 300, 150)
        self.setWindowTitle('RELAY')
        self.connectionDock = ConnectionDock(self.mc)
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
