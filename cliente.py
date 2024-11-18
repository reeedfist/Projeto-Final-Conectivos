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
