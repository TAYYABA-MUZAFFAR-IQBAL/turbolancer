import socket
import threading
import time

HEADER_LENGTH = 10
PORT = 8080
IP_ADDRESS = "127.0.0.1"

def handle_client(client_socket):
    username = receive_message(client_socket)
    print("Client connected: " + username)

    while True:
        message = receive_message(client_socket)
        print("Received message from " + username + ": " + message)

        send_message(client_socket, "Message received")

def receive_message(client_socket):
    header = client_socket.recv(HEADER_LENGTH)
    message_length = int(header.decode("utf-8"))
    message = client_socket.recv(message_length)
    return message.decode("utf-8")

def send_message(client_socket, message):
    message = message.encode("utf-8")
    message_length = len(message)
    header = str(message_length).encode("utf-8")
    client_socket.send(header + message)

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
