import socket

HOST = 'localhost'
PORT = 2018
print("Client started....")

path =r"C:\Users\Stas\Documents\em.txt"
file = open(path, "r")
fileData = file.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        input("Press Enter to sent data...")
        s.sendall(bytes(fileData, encoding='utf-8'))
        data = s.recv(1024)
        print()
        print(str(data, encoding='utf-8'))

