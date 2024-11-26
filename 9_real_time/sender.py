import time
import socket

from random import randint

HOST = "127.0.0.1"
PORT = 5050

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        random_number = randint(1, 100)
        s.sendall(str(random_number).encode())
        print(f"Sending: {random_number}")
        time.sleep(5)
