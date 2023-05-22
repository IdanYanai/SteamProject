import Server
import threading
import time
from tcp_by_size import recv_by_size, send_with_size
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("Please enter IP and Token")
    else:
        ip = sys.argv[1]
        token = sys.argv[2]
    port = 6968
    BTD_Server = Server.Server(ip, port)

    BTD_Server.sock.bind(BTD_Server.address)
    BTD_Server.sock.listen(5)
    print "Server started"
    waiting_for_players = True
    id = 0

    while waiting_for_players:
        (client_socket, client_address) = BTD_Server.sock.accept()
        data = recv_by_size(client_socket)
        if data == token:
            id += 1
            BTD_Server.clients.append(client_socket)
            send_with_size(client_socket, str(id))
            print "Player %s connected" % str(id)
            t = threading.Thread(target=BTD_Server.client, args=(client_socket,))
            t.start()
            BTD_Server.threads.append(t)
            if len(BTD_Server.threads) == 2:
                waiting_for_players = False
                BTD_Server.handle_and_send_data("GAME START")
                print "Game start!"
        else:
            send_with_size(client_socket, "")
            client_socket.close()

    while True:
        time.sleep(3.0)
        if len(BTD_Server.clients) == 0:
            break

    for t in BTD_Server.threads:
        t.join()
    print "Bye Bye"
    BTD_Server.sock.close()


if __name__ == '__main__':
    main()
