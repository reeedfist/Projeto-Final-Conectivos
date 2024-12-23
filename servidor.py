import socket
import threading


HOST = '127.0.0.1'
PORT = 12345

clients = []
usernames = {}


def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)


def gerenciamento_cliente(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    usernames[client_socket] = username
    mensagem_de_boas_vindas = f"{username} entrou no chat!"
    print(mensagem_de_boas_vindas)
    broadcast(mensagem_de_boas_vindas, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'sair':
                mensagem_de_saida = f"{username} saiu do chat."
                broadcast(mensagem_de_saida, client_socket)
                remove_client(client_socket)
                break
            elif message.startswith('@'):
                target_username, private_message = message[1:].split(' ', 1)
                enviar_mensagem_privada(target_username, f"[Privado de {username}]: {private_message}", client_socket)
            else:
                broadcast(f"{username}: {message}", client_socket)
        except:
            remove_client(client_socket)
            break


def enviar_mensagem_privada(target_username, message, sender):
    for client, name in usernames.items():
        if name == target_username:
            try:
                client.send(message.encode('utf-8'))
                sender.send(f"[Para {target_username}]: {message}".encode('utf-8'))
                break
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames.pop(client_socket, "Desconhecido")
        print(f"{username} desconectado.")
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor rodando em {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_socket.send("Bem-vindo ao chat! Por favor, insira seu nome.".encode('utf-8'))
        
        thread = threading.Thread(target=gerenciamento_cliente, args=(client_socket,))
        thread.start()

start_server()
