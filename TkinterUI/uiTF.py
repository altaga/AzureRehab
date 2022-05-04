import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import numpy as np
import paho.mqtt.client as mqtt
import base64
import requests

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("ESP-IoT", "qwertyQWERTY0128")
client.connect("20.127.106.220", 1883, 60)

root = tk.Tk()

root.title('Azure Rehab Control')
root.geometry('480x440+50+50')

pixelVirtual = ImageTk.PhotoImage(image=Image.fromarray(cv2.merge((cv2.split(np.zeros((1,1,3), np.uint8)))))) # 1x1 pixel image

def efe():
    global client
    client.publish("/efe", "start")

def al():
    global client
    client.publish("/al", "start")

def ef():
    global client
    client.publish("/ef", "start")

buttonW = tk.Button(
    root, text="Elbow flex-ext",
    width=100, 
    height=35,
    compound="c",
    image=pixelVirtual,
    command=efe
    )
buttonW.place(x=45,y=320+35)

buttonY = tk.Button(
    root, text="Arm Lift",
    width=100, 
    height=35,
    compound="c",
    image=pixelVirtual,
    command=al
    )
buttonY.place(x=100+45*2,y=320+35)

buttonZ = tk.Button(
    root, text="Elbow Flexion",
    width=100, 
    height=35,
    compound="c",
    image=pixelVirtual,
    command=ef
    )
buttonZ.place(x=200+45*3,y=320+35)

#buttonE = tk.Button(root, text="East")
#buttonW.place(x=200,y=320)

def worker():
    global root
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    imgtk = ""
    panel = ""
    blue,green,red = cv2.split(frame)
    img = cv2.merge((red,green,blue))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    panel = tk.Label(root, image= imgtk, width=480, height=320)
    panel.pack()
    while True:
        ret, frame = cap.read()
        if frame is not None:
            retval, buffer = cv2.imencode('.jpg', frame)
            url = "https://azuretf.azurewebsites.net/api/Azure-TFlite?code=waug9kwZ3VLkid0bBfAprjDmaFril53fL0KKyHAUhV6etLOPLvhUJg=="
            payload = base64.b64encode(buffer)
            headers = {
            'Content-Type': 'text/plain'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            decoded_data = base64.b64decode(response.text)
            np_data = np.fromstring(decoded_data, np.uint8)
            img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
            blue,green,red = cv2.split(img)
            img = cv2.merge((red,green,blue))
            im = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)
            panel.configure(image = imgtk)
            panel.image = imgtk

def mqttWorker():
    global client
    rc = 0
    while rc == 0:
        rc = client.loop()


t1 = threading.Thread(name='loop', target=worker)
t1.start()
t2 = threading.Thread(name='mqttloop', target=mqttWorker)
t2.start()

root.mainloop()