# Lockdown Messenger Server
# Made by Yamniel Negroni Febus and Adrian Castillo Morales

import socket
import threading
 
HOST = "0.0.0.0"
PORT = 5050
 
clients = {}
lock = threading.Lock()
 
 
def broadcast(text, sender=None):
    data = (text + "\n").encode("utf-8")
    dead = []
    with lock:
        for sock in clients:
            if sock is sender:
                continue
            try:
                sock.sendall(data)
            except OSError:
                dead.append(sock)
        for sock in dead:
            clients.pop(sock, None)
 
 
def handle_client(sock, address):
    name = None
    try:
        reader = sock.makefile("r", encoding="utf-8")
        name = reader.readline().strip()[:20]
        if not name:
            return
        with lock:
            clients[sock] = name
        print(f"[+] {name} connected from {address[0]}")
        broadcast(f"* {name} joined the chat", sender=sock)
 
        for line in reader:  # one message per line
            line = line.strip()
            if line:
                print(f"{name}: {line}")
                broadcast(f"{name}: {line}", sender=sock)
    except (OSError, UnicodeDecodeError):
        pass
    finally:
        with lock:
            clients.pop(sock, None)
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()
        if name:
            print(f"[-] {name} disconnected")
            broadcast(f"* {name} left the chat")
 
 
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on port {PORT}. Press Ctrl+C to stop.")
    try:
        while True:
            sock, address = server.accept()
            threading.Thread(
                target=handle_client, args=(sock, address), daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.close()
 
 
if __name__ == "__main__":
    main()