import os
import socket
import threading
import ssl



HOST = ""
PORT = 5555
BUFFER_SIZE = 1024
CERTFILE_PATH = "server.crt"
KEYFILE_PATH = "server.pem"

clients = {}

def handle_client(client_socket, address):
    print(f"New connection from {address}")
    try:
        while True:
            message_length = int.from_bytes(client_socket.recv(4), 'big')
            data = client_socket.recv(message_length).decode()
            if not data:
                break
            broadcast(data, client_socket)
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        del clients[client_socket]

def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                message = message.encode()
                message_length = len(message)
                client_socket.sendall(message_length.to_bytes(4, 'big'))
                client_socket.sendall(message)
            except Exception as e:
                print(f"Error broadcasting to a client: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE_PATH, keyfile=KEYFILE_PATH)
    server_socket = context.wrap_socket(server_socket, server_side=True)

    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            clients[client_socket] = address
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()