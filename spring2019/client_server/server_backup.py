import socketserver
import shutil
import datetime


class Server(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)


class RequestHandler(socketserver.StreamRequestHandler):

    def handle(self):

        while True:
            path = str(self.rfile.readline().strip(), encoding="utf-8")
            print(path)
            try:
                shutil.make_archive("backup(" + str(datetime.datetime.now()) + ")", 'zip', path)
                self.wfile.write(bytes("Yes", encoding="utf-8") + b"\n")
                break
            except FileNotFoundError:
                self.wfile.write(bytes("No", encoding="utf-8") + b"\n")

        self.request.shutdown(2)


HOST = ''
PORT = 11130

print("Server started....")
Server((HOST, PORT), RequestHandler).serve_forever()    