import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 65432
server_socket.bind((host, port))
server_socket.listen()
print(f"Serveur TCP en écoute sur {host}:{port}...")

conn, addr = server_socket.accept()
print(f"Connexion établie avec {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Reçu : {data.decode()}")
    conn.sendall(data)

conn.close()
server_socket.close()