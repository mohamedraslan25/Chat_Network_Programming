import socket
import threading
import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play

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
    global voice_message_recorded
    if voice_message_recorded:
        message = f"{username_entry.get()} : voice message"
        client_socket.sendall(message.encode())
        voice_message_recorded = False
    else:
        message = f"{username_entry.get()} : {message_entry.get()}"
        client_socket.sendall(message.encode())
    message_entry.delete(0, tk.END)
    

def record_voice():
    global voice_message_recorded
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    
    WAVE_OUTPUT_FILENAME = f"{username_entry.get()}_voice_message.wav"

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    voice_message_recorded = True

def play_voice(file_name):
    voice_message = AudioSegment.from_wav(file_name)
    play(voice_message)

def display_message(message, sender=False):
    tag = "sender" if sender else "responder"
    bg_color = "#E8DFCA"
    
    if ": voice message" in message:
        message_parts = message.split(" : ")
        username = message_parts[0]
        
        chat_box.insert(tk.END, f"{username} : voice message\n", (tag, bg_color))
        
        play_button = ttk.Button(chat_box, text="Play Voice", command=lambda u=username: play_voice(f"{u}_voice_message.wav"))
        chat_box.window_create(tk.END, window=play_button)
        chat_box.insert(tk.END, "\n")
    else:
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
    global client_socket, chat_box, message_entry, username_entry, voice_message_recorded

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Connected to server.")
    
    voice_message_recorded = False

    root.title("Client1")

    chat_frame = tk.Frame(root, bg="#E8DFCA")
    chat_frame.pack(expand=True, fill=tk.BOTH)

    chat_box = tk.Text(chat_frame, wrap="word", font=("Helvetica", 12), height=10, bg="#E8DFCA")
    chat_box.pack(expand=True, fill=tk.BOTH)

    message_entry = tk.Entry(chat_frame, font=("Helvetica", 12), bg="#F5EFE6")
    message_entry.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)
    message_entry.insert(0, 'Write your message')

    username_label = tk.Label(root, text="Enter your username:")
    username_label.pack()

    username_entry = tk.Entry(root, font=("Helvetica", 12), bg="#F5EFE6")
    username_entry.pack(padx=10, pady=5)

    send_button = tk.Button(root, text="Send", command=send_message, bg="#1A4D2E", fg="white", font=("Helvetica", 12), width=15)
    send_button.pack(pady=10, fill=tk.BOTH, expand=True)

    record_button = tk.Button(root, text="Record Voice", command=record_voice, bg="#2196f3", fg="white", font=("Helvetica", 12), width=15)
    record_button.pack(pady=10, fill=tk.BOTH, expand=True)

    emoji_button = tk.Button(root, text="Emojis", command=open_emoji_window, font=("Helvetica", 12), bg="yellow")
    emoji_button.pack(pady=5, fill=tk.BOTH, expand=True)

    clear_chat_button = tk.Button(root, text="Clear Chat", command=clear_chat, bg="#f44336", fg="white", font=("Helvetica", 12))
    clear_chat_button.pack(fill=tk.X)

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
