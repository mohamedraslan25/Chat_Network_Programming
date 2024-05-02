import socket
import threading
import tkinter as tk
from tkinter import ttk

EMOJIS = {
    ":)": "😊",
    ":(": "😞",
    ":D": "😄",
    ":P": "😛",
    "<3": "❤️",   # Heart
    ":heart_eyes:": "😍",  # Heart eyes
    ":heartpulse:": "💓",  # Heart pulse
}

root = tk.Tk()

clients = []

def receive_messages(conn):
    while True:
        data = conn.recv(1024).decode()
        broadcast(data)

def broadcast(message):
    for client_conn in clients:
        client_conn.sendall(message.encode())

def client_handler(conn, addr):
    clients.append(conn)
    print("Connected to", addr)

    receive_thread = threading.Thread(target=receive_messages, args=(conn,))
    receive_thread.daemon = True
    receive_thread.start()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()

    print("Server is running. Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        client_handler(conn, addr)

if __name__ == "__main__":
    main()
