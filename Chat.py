import RSA
import pickle
import base64
import Screen
import Games
import subprocess
import threading


class Chat:
    def __init__(self, pkey):
        self.user = None
        self.friend_list = None
        self.game_list = None
        self.games_owned = None
        self.friend_requests = None
        self.RSA = RSA.Encryptor(pkey)
        self.processes = []
        self.P2P = []

    def encrypt_password(self, args):
        to_return = ""
        command = args.split("|")[0]
        parameters = args.split("|")[1:]

        if command == "LOGIN":
            username, password = parameters
            e_password = self.RSA.rsa_encrypt(password)
            to_return = username.encode() + b"|" + e_password

        elif command == "REGIS":
            username, password, nickname, email = parameters
            e_password = self.RSA.rsa_encrypt(password)
            to_return = username.encode() + b"|" + e_password + b"|" + nickname.encode() + b"|" + email.encode()

        print(command, to_return)
        return command.encode() + b"|" + to_return

    def handle_message(self, msg):
        command = msg.split("|")[0]

        if msg.startswith("UINFO"):
            msg = base64.b64decode(msg.split("|")[1])
            user, fl, go, gl, fr = msg.split(b"|")
            self.friend_list = pickle.loads(fl)
            print("Friend list: ")
            print(self.friend_list)

            self.game_list = pickle.loads(gl)
            print("Game list: ")
            print(self.game_list)

            self.games_owned = pickle.loads(go)
            print("Games Owned: ")
            print(self.games_owned)

            self.friend_requests = pickle.loads(fr)
            print("Friend Requests: ")
            print(self.friend_requests)

            self.user = pickle.loads(user)
            print("User Info: " + self.user.Username + " - " + self.user.Nickname)
            Screen.got_info = True
            Screen.info = [self.user, self.friend_list, self.game_list, self.games_owned, self.friend_requests]

        elif command == "FRMSG":
            name = msg.split("|")[1]
            msg = "F:" + msg.split("|")[2]
            if name in Screen.chats.keys():
                Screen.chats[name].append(msg)
            else:
                Screen.chats[name] = [msg]
            Screen.got_msg = self.user.Nickname + " " + name

        elif command == "CMPLT":
            game = msg.split("|")[1]
            new_money = msg.split("|")[2]
            user, f_list, g_list, games_owned, friend_rq = Screen.info
            for g in g_list:
                if game in g:
                    games_owned.append(g)
            user.Money = new_money
            Screen.got_info = True
            Screen.info = [user, f_list, g_list, games_owned, friend_rq]

        elif msg.startswith("FILES"):
            game = msg.split("|")[1]
            data = msg.split("|", 2)[2]
            data = base64.b64decode(data)
            Games.install(data, game)

        elif msg.startswith("REQUF"):
            nickname = msg.split("|")[1]
            user, f_list, g_list, games_owned, friend_rq = Screen.info
            friend_rq.append((None, None, None, nickname))
            Screen.got_info = True
            Screen.info = [user, f_list, g_list, games_owned, friend_rq]

        elif msg.startswith("ACCRQ"):
            nickname = msg.split("|")[1]
            user, f_list, g_list, games_owned, friend_rq = Screen.info
            f_list.append((None, None, None, nickname))
            Screen.got_info = True
            Screen.info = [user, f_list, g_list, games_owned, friend_rq]

        elif command == "START":
            command, game, address, token = msg.split("|")
            self.P2P = command, None, game, address, token
            if game == "Bloons TD Battles":
                t = threading.Thread(target=self.start_game, args=(True,))
                t.start()
                t = threading.Thread(target=self.start_game, args=(False,))
                t.start()

            elif game == "Chess":
                print("nope")

        elif command == "DENYG":
            print(self.processes)
            for process in self.processes:
                process.kill()
                self.processes.remove(process)

        elif command == "PINVI":
            command, nick, game, address, token = msg.split("|")
            self.P2P = command, nick, game, address, token
            Screen.Popup = nick + " has invited you to play " + game

        elif command == "ACKNW":
            print("GOOD!")
        else:
            Screen.Popup = msg

    def start_game(self, server=False):
        command, nick, game, address, token = self.P2P

        if game == "Bloons TD Battles":
            if server:
                to_run = ["py", "-2.7", "Games/Bloons TD Battles/Server/BTD_Server.py", address, token]
                server = subprocess.Popen(to_run)
                self.processes.append(server)
                print("Server started")
                server_out, server_err = server.communicate()
            else:
                to_run = ["py", "-2.7", "Games/Bloons TD Battles/Client/BTD_Client.py", address, token]
                client = subprocess.Popen(to_run)
                self.processes.append(client)
                print("Client started")
                client_out, client_err = client.communicate()

