import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 65432))

while True:
    message = input("Message à envoyer : ")
    if message.lower() == "quit":
        break
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print(f"Serveur a répondu : {data.decode()}")

client_socket.close()
