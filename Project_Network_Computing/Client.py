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

def receive_messages():
    while True:
        data = client_socket.recv(1024).decode()
        display_message(data, sender=True)

def send_message():
    message = message_entry.get()
    client_socket.sendall(message.encode())
    display_message("You: " + message, sender=True)
    message_entry.delete(0, tk.END)

def display_message(message, sender=False):
    tag = "sender" if sender else "responder"
    bg_color = "#E8DFCA"
    for code, emoji in EMOJIS.items():
        message = message.replace(code, emoji)
    chat_box.insert(tk.END, message + "\n", (tag, bg_color))

def clear_chat():
    chat_box.delete('1.0', tk.END)

def open_emoji_window():
    emoji_window = tk.Toplevel(root)
    emoji_window.title("Select Emoji")

    for code, emoji in EMOJIS.items():
        emoji_button = ttk.Button(emoji_window, text=emoji, command=lambda e=emoji: insert_emoji(e))
        emoji_button.pack(padx=5, pady=5)

def insert_emoji(emoji):
    message_entry.insert(tk.END, emoji)

def main():
    global client_socket, chat_box, message_entry

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Connected to server.")

    # GUI setup
    root.title("Simple Chat")

    chat_frame = tk.Frame(root, bg="#E8DFCA")
    chat_frame.pack(expand=True, fill=tk.BOTH)

    chat_box = tk.Text(chat_frame, wrap="word", font=("Helvetica", 12), height=10, bg="#E8DFCA")
    chat_box.pack(expand=True, fill=tk.BOTH)

    message_entry = tk.Entry(chat_frame, font=("Helvetica", 12), bg="#F5EFE6")
    message_entry.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)
    message_entry.insert(0, 'Write your message')

    send_button = tk.Button(root, text="Send", command=send_message, bg="#1A4D2E", fg="white", font=("Helvetica", 12), width=15)
    send_button.pack(pady=10, fill=tk.BOTH, expand=True)

    emoji_button = tk.Button(root, text="Emojis", command=open_emoji_window, font=("Helvetica", 12), bg="yellow")
    emoji_button.pack(pady=5, fill=tk.BOTH, expand=True)

    clear_chat_button = tk.Button(root, text="Clear Chat", command=clear_chat, bg="#f44336", fg="white", font=("Helvetica", 12))
    clear_chat_button.pack(fill=tk.X)

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()


# import socket
# import threading
# import tkinter as tk
# from tkinter import ttk
# import sounddevice as sd
# import soundfile as sf

# root = tk.Tk()

# def receive_messages():
#     while True:
#         data = client_socket.recv(1024).decode()
#         if data.startswith("REC"):
#             record_audio()
#         else:
#             display_message(data, sender=True)

# def send_message():
#     message = message_entry.get()
#     client_socket.sendall(message.encode())
#     display_message("You: " + message, sender=True)
#     message_entry.delete(0, tk.END)

# def display_message(message, sender=False):
#     tag = "sender" if sender else "responder"
#     chat_box.insert(tk.END, message + "\n", (tag,))

# def clear_chat():
#     chat_box.delete('1.0', tk.END)

# def record_audio():
#     duration = 5  # Recording duration in seconds
#     fs = 44100  # Sample rate
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
#     sd.wait()  # Wait until recording is finished
#     sf.write('record.wav', recording, fs)  # Save the recorded audio to a file
#     display_message("You: [Recorded an audio message]", sender=True)

# def main():
#     global client_socket, chat_box, message_entry

#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('localhost', 12345))

#     print("Connected to server.")

#     # GUI setup
#     root.title("Simple Chat")

#     chat_frame = tk.Frame(root)
#     chat_frame.pack(expand=True, fill=tk.BOTH)

#     chat_box = tk.Text(chat_frame, wrap="word", font=("Helvetica", 12), height=10)
#     chat_box.pack(expand=True, fill=tk.BOTH)

#     message_entry = tk.Entry(chat_frame, font=("Helvetica", 12))
#     message_entry.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)
#     message_entry.insert(0, 'Write your message')

#     send_button = tk.Button(root, text="Send", command=send_message)
#     send_button.pack(pady=10)

#     record_button = tk.Button(root, text="Record", command=record_audio)
#     record_button.pack(pady=5)

#     clear_chat_button = tk.Button(root, text="Clear Chat", command=clear_chat)
#     clear_chat_button.pack()

#     # Start a thread to receive messages
#     receive_thread = threading.Thread(target=receive_messages)
#     receive_thread.daemon = True
#     receive_thread.start()

#     root.mainloop()

# if __name__ == "__main__":
#     main()
