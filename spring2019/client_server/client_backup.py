import socket

HOST = 'localhost'
PORT = 11130

print("Client started....")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

inputFile = s.makefile('rb', 0)
outputFile = s.makefile('wb', 0)

while True:
    path = input("Enter a path for backup: ")
    if path:
        outputFile.write(bytes(path, encoding = "utf-8") + b"\n")

        answ = str(inputFile.readline().strip(), encoding = "utf-8")
        if(answ == "No"):
            print("There is no path like this, try again")
        else:
            print("Backup created!!!")
            s.shutdown(2)
            break
s.close()