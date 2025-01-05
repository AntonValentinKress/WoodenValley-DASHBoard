import segno
import rystavariables as rysta
import time
import socket

def RystaPermaQR():
    print("Creating QR-Code")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip = s.getsockname()[0]
    print(f"Current IP: {ip}")

    s.close()

    url = f"http://{ip}:{rysta.port}"

    qrcode = segno.make(url)

    print("Save QR-Code as .svg-File")

    qrcode.save('assets/Dashboard.svg', scale = 10, dark='white')

    print("Waiting...")

RystaPermaQR()