import socket
import threading
import logging


clients = dict()

def handle_client(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} connected.")

    while True:
        msg = conn.recv(1024).decode('utf-8')
        if msg == "!quit":
            break

        if msg.startswith("@response_to_morpheus"):
            print(f"[{addr}] responded: {msg[21:]}")

    clients.pop(addr)
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def send_broadcast(msg):
    for client_conn in clients.values():
        client_conn.send(msg.encode('utf-8'))

def send_private_message(addr, msg):
    if addr in clients:
        clients[addr].send(msg.encode('utf-8'))
    else:
        print(f"[ERROR] No client found with address {addr}")

def morpheus_input():
    while True:
        msg = input("Enter command (broadcast/private [addr]:msg/stop): ")
        if msg == "stop":
            send_broadcast("!server_disconnect")
            break
        elif msg.startswith("broadcast "):
            send_broadcast(msg[10:])
        elif msg.startswith("private "):
            try:
                addr, message = msg[8:].split(':', 1)
                send_private_message(int(addr), message)
            except ValueError:
                print("\n[ERROR] Incorrect format! Use 'private [addr]:msg'")
        elif msg.startswith("clients"):
            print(clients)

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5555))
    server.listen()
    print("[SERVER] listening ...")

    while True:
        conn, addr = server.accept()
        clients[addr] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}")
    
    server.close()

def main():
    input_thread = threading.Thread(target=morpheus_input)
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    input_thread.start()

if __name__ == "__main__":
    main()