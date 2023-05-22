import socket
from Protocol import recv_by_size, send_with_size
import sys
from Crypto.PublicKey import RSA
import Chat
import Screen
import threading
import time
import os


input = None
login = False


def main():
    global login
    if len(sys.argv) == 1:
        sys.exit("Please enter IP argument")
    else:
        ip = sys.argv[1]
    port = 6969

    os.makedirs("Games", exist_ok=True)

    sock = socket.socket()
    sock.connect((ip, port))

    pkey = recv_by_size(sock)
    chat = Chat.Chat(RSA.import_key(pkey, passphrase=None))

    t = threading.Thread(target=Screen.Screen, args=(user_input,))
    t.start()
    t = threading.Thread(target=async_recv, args=(sock, chat))
    t.start()

    to_send = ""
    while True:
        args = wait_for_input()
        print(args)

        if args.upper() == "DISCO":
            send_with_size(sock, b"DISCO")
            break
        elif args.upper() == "LGOUT":
            to_send = b"LGOUT"
            login = False
        elif args == "ACPTG":
            t = threading.Thread(target=chat.start_game, args=(False,))
            t.start()
            to_send = args.encode()
        elif args == "DENYG":
            to_send = args.encode() + b"|" + chat.P2P[1].encode()
        elif not login:
            to_send = chat.encrypt_password(args)
        else:
            to_send = args.encode()

        send_with_size(sock, to_send)
        print(b"SENT - " + to_send)


def async_recv(sock, chat):
    global login

    while True:
        try:
            data = recv_by_size(sock).decode()
        except socket.error:
            break
        print(data)

        if data == "":
            print("Server Disconnected")
            break
        elif data.startswith("UINFO"):
            login = True
            print("Logged in")

        chat.handle_message(data)

    sock.close()


def wait_for_input():
    global input
    while input is None:
        time.sleep(1)
    save = input
    input = None
    return save


def user_input(data):
    global input
    input = data


if __name__ == '__main__':
    main()
