# Lockdown Messenger Client

import socket
import threading
 
PORT = 5050     #10.250.41.170
 
 
def receive(sock):
    """Print messages from the server until the connection closes."""
    try:
        for line in sock.makefile("r", encoding="utf-8"):
            print(line.strip())
    except OSError:
        pass
    print("The server closed the connection.")
 
 
def print_no_input_help():
    print(
        "\nThis console cannot accept typed input (it closed the input stream).\n"
        "Run the client from a real terminal instead:  python client.py"
    )
 
 
def main():
    try:
        name = input("Your name: ").strip() or "Anonymous"
        host = input("Server IP (press Enter for this computer): ").strip() or "127.0.0.1"
    except EOFError:
        print_no_input_help()
        return
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, PORT))
    except OSError as e:
        print(f"Could not connect to {host}:{PORT} - {e}")
        return
 
    sock.sendall((name + "\n").encode("utf-8"))
    threading.Thread(target=receive, args=(sock,), daemon=True).start()
    print("Connected. Type a message and press Enter. Type /quit to leave.")
 
    try:
        while True:
            text = input()
            if text.strip() == "/quit":
                break
            if text.strip():
                sock.sendall((text + "\n").encode("utf-8"))
    except EOFError:
        print_no_input_help()
    except (KeyboardInterrupt, OSError):
        pass
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)  # really ends the connection
        except OSError:
            pass
        sock.close()
 
 
if __name__ == "__main__":
    main()