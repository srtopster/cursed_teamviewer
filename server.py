import socket
import io
import PySimpleGUI as sg
from PIL import Image
import threading

sg.theme("DarkGrey10")
end = False
def get_image(window):
    global end
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("192.168.0.100",1337))
    s.listen()
    print("server iniciado")
    client, addr = s.accept()
    print(f"Conexão: {addr}")
    while True:
        img_bytes = io.BytesIO()
        with img_bytes as f:
            while True:
                data = client.recv(1024)
                if data == b"":
                    end = True
                    break
                f.write(data)
                if data.endswith(b"EOF"):
                    break
            if end == True:
                client.close()
                break
            im = Image.open(io.BytesIO(img_bytes.getvalue()))
            im.thumbnail((1024,576))
            img_bytes2 = io.BytesIO()
            im.save(img_bytes2,"PPM")
            window["img"].update(data=img_bytes2.getvalue())
    print("acabou")

layout = [
    [sg.Image(size=(1024,576),key="img")],
    [sg.Button("Start Server",key="b1"),sg.Button("Stop server",key="b2",disabled=True)]
]
window = sg.Window(title="TeamViewer do paraguay",layout=layout)
while True:
    event, values = window.read()
    if event == "b1":
        end = False
        threading.Thread(target=get_image,args=[window]).start()
        window["b1"].update(disabled=True)
        window["b2"].update(disabled=False)
    if event == "b2":
        end = True
        window["b1"].update(disabled=False)
        window["b2"].update(disabled=True)
    if event == sg.WIN_CLOSED:
        break