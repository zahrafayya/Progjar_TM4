import select
import socket
import sys
import threading

fileReceived = 1

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
            

	# close all threads
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.client = id[0]
        self.address = id[1]
        self.size = 1024

    def run(self):
        global fileReceived
        while fileReceived:
            filename = self.client.recv(self.size)
            if filename:
                print ('recv: '+str(self.address)+str(filename))
                fileReceived = 0
        reply = "yes"
        self.client.send(reply.encode())

if __name__ == "__main__":
    s = Server()
    s.run()
