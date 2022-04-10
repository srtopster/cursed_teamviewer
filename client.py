import socket
import pyautogui
import numpy as np
import cv2
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",6969))
while True:
    img = pyautogui.screenshot()
    pixel_array = np.array(img)
    frame = cv2.cvtColor(pixel_array, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame,(1024,576),interpolation=cv2.INTER_LINEAR)
    img_bytes = cv2.imencode(".png",frame)[1].tobytes()
    s.send(img_bytes)
    s.send("EOF".encode())
    time.sleep(0.1)