import socket
import re


def find_emails(data):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    rez = re.findall(pattern, data)
    str_rez = str()
    for i in range(len(rez)):
        str_rez += rez[i] +"\n"
    return str_rez


HOST = ''
PORT = 2018
print("Server started....")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)

        if not data: break
        tempData = str(data, encoding='utf-8')

        result = bytes(find_emails(tempData), encoding='utf-8')
        print(result)

        conn.sendall(result)

    conn.close()