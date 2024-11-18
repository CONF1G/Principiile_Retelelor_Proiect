import socket
import tkinter as tk
from tkinter import messagebox

TCP_IP = '127.0.0.1'
TCP_PORT = 12345

def send_guess():
    guess = entry.get()
    client_socket.send(guess.encode())
    response = client_socket.recv(1024).decode()
    if "Felicitari" in response:
        messagebox.showinfo("Rezultat", response)
        root.quit()
    else:
        label_response.config(text=response)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((TCP_IP, TCP_PORT))

root = tk.Tk()
root.title("Guess the Number")

label = tk.Label(root, text="Ghiceste un număr între 1 și 100:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Trimite", command=send_guess)
button.pack()

label_response = tk.Label(root, text="")
label_response.pack()

root.mainloop()
client_socket.close()
