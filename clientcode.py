import os
import socket
import threading
import tkinter as tk
from tkinter import messagebox, colorchooser
import ssl


HOST = "192.168.59.141"
PORT = 5555
BUFFER_SIZE = 1024
color = 'black'
shapes = []

undoing = False

def send_data(data):
    message = data.encode()
    message_length = len(message)
    client_socket.sendall(message_length.to_bytes(4, 'big'))
    client_socket.sendall(message)

def receive_data():
    while True:
        try:
            message_length = int.from_bytes(client_socket.recv(4), 'big')
            data = client_socket.recv(message_length).decode()
            commands = data.split("\n")
            for command in commands:
                parts = command.split()
                if len(parts) == 4:
                    cmd, x, y, color = parts
                    if cmd == "DRAW":
                        draw_on_canvas(int(x), int(y), color)
                elif len(parts) == 1:
                    cmd = parts[0]
                    if cmd == "UNDO":
                        undo()
                else:
                    print(f"Received malformed data: {command}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to receive data from the server: {e}")
            break

def draw_on_canvas(x, y, color):
    shape = canvas.create_oval(x, y, x + 1, y + 1, fill=color)
    shapes.append(shape) 

def on_click(event):
    global color
    x, y = event.x, event.y
    data = f"DRAW {x} {y} {color}"
    send_data(data)
    draw_on_canvas(x, y, color)

def choose_color():
    global color
    color = colorchooser.askcolor()[1] 

def undo():
    if shapes:
        shape = shapes.pop() 
        canvas.delete(shape)  
        send_data("UNDO")

def start_undo(event):
    undo() 

def stop_undo(event):
    pass

def main():
    global canvas, client_socket, root
    root = tk.Tk()
    root.title("Collaborative Whiteboard")

    color_button = tk.Button(root, text="Choose Color", command=choose_color)
    color_button.pack()

    undo_button = tk.Button(root, text="Undo")
    undo_button.pack()
    undo_button.bind("<Button-1>", start_undo) 
    undo_button.bind("<ButtonRelease-1>", stop_undo) 

    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.bind("<B1-Motion>", on_click)

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    client_socket = context.wrap_socket(raw_socket, server_hostname=HOST)
    client_socket.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()