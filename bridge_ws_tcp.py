import asyncio
import websockets
import socket
import json

# --- CONFIGURATION ---
WS_URL = "ws://127.0.0.1:8000/ws"  # serveur WebSocket
TCP_HOST = "127.0.0.1"              # adresse locale pour Spark
TCP_PORT = 9999                      # port pour Spark

# --- Création du socket TCP serveur ---
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((TCP_HOST, TCP_PORT))
tcp_server_socket.listen()
print(f"[TCP] En écoute sur {TCP_HOST}:{TCP_PORT}…")

# Accepter la connexion d'un client Spark
conn, addr = tcp_server_socket.accept()
print(f"[TCP] Client connecté : {addr}")

# --- Fonction bridge WebSocket -> TCP ---
async def websocket_to_tcp():
    async with websockets.connect(WS_URL) as ws:
        print(f"[WebSocket] Connecté à {WS_URL}")
        while True:
            try:
                # Recevoir un message depuis le WebSocket
                message = await ws.recv()
                
                # Si le message est JSON, on peut le formater ou l'envoyer tel quel
                try:
                    data = json.loads(message)
                    # Transformer en chaîne JSON pour TCP
                    message_tcp = json.dumps(data)
                except json.JSONDecodeError:
                    # si ce n'est pas du JSON, envoyer tel quel
                    message_tcp = message
                
                # Envoyer sur le socket TCP
                conn.sendall((message_tcp + "\n").encode())  # ajout d'un \n pour Spark
                
                # Affichage console pour debug
                print(f"[Bridge] Transmis à TCP : {message_tcp}")

            except websockets.ConnectionClosed:
                print("[WebSocket] Connexion fermée")
                break
            except Exception as e:
                print(f"[Erreur] {e}")
                break

# --- Lancer le bridge ---
asyncio.run(websocket_to_tcp())
