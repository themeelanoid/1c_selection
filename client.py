import socket
import threading

START_CHAT = False

def receive(server):
    global START_CHAT
    while True:
        msg = server.recv(1024).decode('utf-8')
        START_CHAT = True
        print(msg)
        if msg == "!server_disconnect":
            break

def client(server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect((server_ip, 5555))

    receive_thread = threading.Thread(target=receive, args=(client,), daemon=True)
    receive_thread.start()

    while not START_CHAT:
        msg = input("Type !quit to quit. Type try to try to start dialog with morpheus\n")
        if msg == "!quit" or not receive_thread.is_alive():
            client.send(msg.encode('utf-8'))
            break
    
    while START_CHAT:
        msg = input("Enter a message to send Morpheus: ")
        if msg == "!quit" or not receive_thread.is_alive():
            client.send(msg.encode('utf-8'))
            break
        else:
            msg = "@response_to_morpheus" + msg
            client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    client(input("Enter Morpheus server IP: "))
