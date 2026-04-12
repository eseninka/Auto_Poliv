import os
from dotenv import load_dotenv
import torch
from photo_processing import photo_processing
import paho.mqtt.client as mqtt
from arch_model import Net

load_dotenv()

MQTT_topic_pub = 'kvant/R22/BV/auto_poliv/camera/response'

HOST = os.getenv("HOST")
NAME_USER = os.getenv("NAME_USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
CONNECT = os.getenv("CONNECT")
URL = os.getenv("URL")
UUID = os.getenv("UUID")
User_wqtt = os.getenv("USER_WQTT")
Password_wqtt = os.getenv("PASSWORD_WQTT")
Address_wqtt = os.getenv("ADDRESS_WQTT")
Port_wqtt = int(os.getenv("PORT_WQTT"))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('full_model_v3.pth', map_location=device, weights_only=False)
model.eval()


image_proc = photo_processing(HOST=HOST, NAME_USER=NAME_USER, PASSWORD=PASSWORD, DATABASE=DATABASE, CONNECT=CONNECT, url=URL, uuid=UUID, model=model, device=device)

def on_message(client, userdata, msg):
    print(f"Топик: {msg.topic}, Сообщение: {msg.payload.decode()}, Тип данных {type(msg.payload.decode())}")
    if msg.payload.decode() == 'request':
        image_proc.save_photo()
        resp = image_proc.analiz_image()
        print(resp)
        client.publish(MQTT_topic_pub, resp[0])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message  # Обработчик сообщений
client.username_pw_set(User_wqtt, Password_wqtt)  # Логин и пароль
client.connect(Address_wqtt, Port_wqtt)  # Подключение
client.subscribe('kvant/R22/BV/auto_poliv/camera/status')  # Подписка на топик

client.loop_forever()  # Запуск цикла


