import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


HOST = '127.0.0.1'
PORT = 12345


def send_message():
    message = msg_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        if not message.startswith('@'):
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, f"Você: {message}\n")
            chat_window.config(state=tk.DISABLED)
        msg_entry.delete(0, tk.END)


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, f"{message}\n")
            chat_window.config(state=tk.DISABLED)
        except:
            print("Erro ao receber mensagem.")
            client_socket.close()
            break


def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        username = username_entry.get()
        if username:
            client_socket.send(username.encode('utf-8'))
            username_entry.config(state=tk.DISABLED)
            connect_button.config(state=tk.DISABLED)
            start_gui_chat()
        else:
            messagebox.showerror("Erro", "Nome de usuário não pode estar vazio.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao conectar ao servidor: {e}")


def start_gui_chat():
    thread = threading.Thread(target=receive_messages)
    thread.start()

    main_frame.pack(pady=10)
    input_frame.pack(pady=5)
    msg_entry.focus()


app = tk.Tk()
app.title("Chat")
app.geometry("400x400")


username_frame = tk.Frame(app)
username_frame.pack(pady=10)

tk.Label(username_frame, text="Nome de usuário:").pack(side=tk.LEFT)
username_entry = tk.Entry(username_frame)
username_entry.pack(side=tk.LEFT)
connect_button = tk.Button(username_frame, text="Conectar", command=connect_to_server)
connect_button.pack(side=tk.LEFT)


main_frame = tk.Frame(app)
chat_window = scrolledtext.ScrolledText(main_frame, width=50, height=15, state=tk.DISABLED)
chat_window.pack(pady=5)

input_frame = tk.Frame(app)
msg_entry = tk.Entry(input_frame, width=40)
msg_entry.pack(side=tk.LEFT, padx=5)
send_button = tk.Button(input_frame, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT)

app.mainloop()
