import time
import socket
import threading
import tkinter as tk
import customtkinter as ctk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(("81.169.141.81", 8888))
client.connect(("localhost", 7777))

root = ctk.CTk()
root.geometry("400x300")
root.resizable(True, True)
root.title("OnlineBanking")

frame = ctk.CTkFrame(root)
frame.pack(pady=50)

message_label = ctk.CTkLabel(frame)
message_label.pack()

message_entry = ctk.CTkEntry(root)
message_entry.pack(anchor='center')


def send_message(event=None):
    message = message_entry.get()
    if message.lower() == "register":
        register()
    else:
        client.send(message.encode())
    message_entry.delete(0, tk.END)


message_entry.bind("<Return>", send_message)

message_queue = []


def receive_messages():
    while True:
        message = client.recv(1024).decode()
        message_queue.append(message)
        time.sleep(2)


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


def update_message_label():
    if message_queue:
        message_label.configure(text=message_queue.pop(0))

    root.after(100, update_message_label)


root.after(100, update_message_label)


# Register function
def register():
    client.send("register".encode())


# Register button
register_button = ctk.CTkButton(root, text="Register", command=register)
register_button.place(x=10, y=10)

root.mainloop()
