import socket
import sys
import signal

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


filename = input(">> ")

if filename in "a":
    print(filename)
else:
    f = open(filename, "r")
    msg = f.read()
    f.close()
    client_socket.send(filename.encode())
    sys.stdout.write("File terkirim ke client 2 dan client 3")

reply = client_socket.recv(1024).decode()
sys.stdout.write(reply)

client_socket.close()
sys.exit(0)