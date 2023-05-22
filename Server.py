import socket
import threading
from Protocol import recv_by_size, send_with_size
import sys
import Manager


users = {}
lock = threading.Lock()


def main():
    if len(sys.argv) == 1:
        sys.exit("Please enter IP argument")
    else:
        ip = sys.argv[1]
    port = 6969

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print("Server started")

    running = True
    Threads = []

    while running:
        (client_socket, client_address) = server_socket.accept()
        print("Client connected")
        t = threading.Thread(target=handle_client, args=(client_socket, client_address))
        t.start()
        Threads.append(t)

    for t in Threads:
        t.join()
    print("RIP")
    server_socket.close()


def handle_client(sock, address):
    global users
    MG = Manager.Manager(sock, address)
    to_send = ""
    send_with_size(sock, MG.Enc.PKey.exportKey(format='PEM', passphrase=None, pkcs=1))

    while True:
        try:
            data = recv_by_size(sock).decode()
        except ConnectionError:
            print("Client crashed")
            if MG.user is not None:
                user_logout(MG.user.Nickname)
            break
        print(data)

        if data == "" or data.upper() == "DISCO":
            print("Client disconnected")
            if MG.user is not None:
                user_logout(MG.user.Nickname)
            break
        elif data.startswith("LGOUT"):
            user_logout(MG.user.Nickname)

        to_send = MG.handle_message(data, users)

        if to_send.startswith(b"UINFO"):
            update_users(MG.user.Nickname, sock)
        send_with_size(sock, to_send)
        print(b"SENT - " + to_send)

    sock.close()


def update_users(nickname, socket):
    global users, lock
    with lock:
        users[nickname] = socket
    print("---- Online Users ------")
    for user in users:
        print(user)
    print("")


def user_logout(nickname):
    global users, lock
    with lock:
        del users[nickname]
    print("---- Online Users ------")
    for user in users:
        print(user)
    print("")


if __name__ == '__main__':
    main()
