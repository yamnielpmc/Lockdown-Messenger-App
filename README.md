# Lockdown Messenger

A desktop messaging application that lets multiple users communicate in real time over a local Wi-Fi network using TCP sockets. The long-term goal is a secure messenger with a modern graphical interface and AES encryption, built to demonstrate secure data transmission between computers.

**Team:** Adrian J. Castillo Morales and Yamniel Negroni Febus
**Language:** Python 3
**Course:** Final class project

---

## Current status

The project is being built in stages. Right now the **networking foundation** is done and working.

| Stage | Status |
|---|---|
| TCP server that relays messages between many clients | Done |
| Terminal client (send and receive in real time) | Done |
| Join and leave notices | Done |
| Automated test of the server and client | Done |
| Encryption (AES) | Planned |
| Graphical interface | Planned |
| Standout features (see roadmap) | Planned |

**Important:** messages are currently sent as plain text. Encryption is the next major milestone, so do not treat the current version as secure.

---

## Requirements

- Python 3.8 or newer
- No extra packages. The current version uses only Python's standard library, so there is nothing to install.

Check your Python version with:

```
python --version
```

(On Mac or Linux the command may be `python3`.)

---

## Project structure

```
lockdown_basic/
  server.py        The server: accepts clients and relays messages
  client.py        The terminal client: connect, send, receive
  test_basic.py    Optional automated test (not needed to chat)
  README.md        This file
```

---

## How to run

### On one computer (quick test)

1. Open a terminal in the project folder and start the server:
   ```
   python server.py
   ```
2. Open a second terminal and start a client:
   ```
   python client.py
   ```
   Enter a name, then press Enter to use the default server address (this computer).
3. Open a third terminal and start another client with a different name.
4. Type a message in either client and it appears in the other. Type `/quit` to leave.

### On two or more computers (the real use case)

1. Connect all computers to the **same Wi-Fi network**.
2. On the computer acting as the server, find its local IP address:
   - Windows: run `ipconfig` and look for the IPv4 address
   - Mac: run `ipconfig getifaddr en0`
   - Linux: run `hostname -I`
3. On that computer, run `python server.py`.
4. On every other computer, run `python client.py` and enter the server's IP address when asked.

The server listens on **port 5050**. If clients cannot connect, allow Python or port 5050 through the server computer's firewall.

---

## How it works

### Architecture

The app uses a client-server model. Every client connects to the server over TCP, and the server relays each message to all other connected clients.

```
  Client A  <----\                /---->  Client C
                  \              /
                   +-- Server --+
                  /              \
  Client B  <----/                \---->  Client D
```

### Server (`server.py`)

- Listens on all network interfaces at port 5050.
- Starts one thread per connected client, so many users can chat at once.
- Reads the client's name from its first line, announces that they joined, then relays each message as `name: text` to everyone except the sender.
- Announces when a client leaves and removes it from the list of connected clients.
- A lock protects the shared client list because several threads use it.

### Client (`client.py`)

- Asks for a name and the server's IP address.
- Connects to the server and sends the name as its first line.
- Uses two parts at once: a background thread prints incoming messages, while the main loop reads what you type and sends it.
- Typing `/quit` closes the connection cleanly.

### Message format

Messages are plain text, one message per line, ending with a newline character. This newline marks where one message ends, which matters because TCP is a continuous stream of bytes and does not keep message boundaries by itself.

1. The first line a client sends is its **name** (trimmed to 20 characters by the server).
2. Every following line is a **chat message**.

---

## Testing

`test_basic.py` is an optional script that checks the server and client work. It starts the server in the background, connects two test clients, sends messages in both directions, and checks that the join and leave notices appear.

```
python test_basic.py
```

It prints `basic chat ok` when everything passes. It is not needed to run the chat, but it is a quick way to confirm nothing broke after changing the code.

**Still to test manually:** chatting between two real computers over Wi-Fi, three or more clients at once, and what happens when the server stops while clients are connected.

---

## Troubleshooting

**The client disconnects right after I enter my name.**
Some IDE "Run" buttons (for example Code Runner's output panel) cannot accept typed input. The client will print "This console cannot accept typed input." Run it from a real terminal instead (`python client.py`).

**"Could not connect" error.**
- Make sure `server.py` is running first.
- Check that the IP address is the server computer's address on the Wi-Fi network.
- Make sure both computers are on the same network.
- Allow Python or port 5050 through the server computer's firewall.

**"Address already in use" when starting the server.**
Another copy of the server is still running, or the port is busy. Close the other terminal, or wait a few seconds and try again.

**Import errors in an IDE.**
The current version needs no extra packages. If an IDE reports missing imports, it is usually using a different Python interpreter than the one you run from the terminal. Select the correct interpreter in your IDE settings.

---

## Roadmap

Planned work, in the order we intend to build it:

1. **Basics polish:** reject duplicate usernames, add timestamps, add a `/users` command, clearer connection errors.
2. **Encryption:** AES-256-GCM so messages are encrypted and tamper-proof, with a key exchange (X25519) so no key is hardcoded. This will need an extra library such as `cryptography` or `pycryptodome`, pending approval for the class.
3. **Graphical interface:** a modern chat window on top of the same networking code.
4. **Standout features:**
   - Attacker View: a toggle showing the raw ciphertext next to the decrypted message
   - Fingerprint verification so users can confirm who they are talking to
   - Lockdown button that wipes keys and chat history
   - Replay protection with message counters
   - Peer auto-discovery on the local network
   - Online/offline status and typing indicators
5. **Stretch goals:** encrypted file transfer, self-destructing messages, encrypted local chat history.

---

## Known limitations

- Messages are not encrypted yet.
- Two users can currently choose the same name.
- There is no authentication, so anyone on the network who knows the server's address can join.
- The server only relays messages and does not store history.
- The terminal client is a temporary interface until the GUI is built.

---

## Development notes

Early on we started with a peer-to-peer design that used a GUI library and the `cryptography` package. We restarted with a simpler client-server design using only the standard library, to make setup easy and to get a reliable networking base before adding encryption and the interface.