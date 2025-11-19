import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9999))

i = 0

while i < 10:
    data = client_socket.recv(1024)
    print(f"Serveur a envoyer : {data.decode()}")
    i += 1

client_socket.close()
