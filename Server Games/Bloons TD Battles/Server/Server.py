import socket
import threading
from tcp_by_size import recv_by_size, send_with_size


class Server:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ip, port)
        self.lock = threading.Lock()
        self.clients = []
        self.threads = []

    def client(self, client_socket):
        """
        main thread
        """
        running = True
        error = ""
        while running:
            try:
                data = recv_by_size(client_socket)
                if data:
                    print data
                    if data == "SHUT DOWN" or data == "MATCH END":
                        running = False
                    self.handle_and_send_data(data)
                else:
                    print "Client disconnected"
                    running = False
            except socket.error as error:
                print error
                running = False
        self.clients.remove(client_socket)
        if error:
            self.handle_and_send_data("SHUT DOWN")

    def handle_and_send_data(self, data):
        """
        gets data and sends it to all clients (all the 2)
        :return nothing:
        """
        self.lock.acquire()
        for client in self.clients:
            send_with_size(client, data)
        self.lock.release()
