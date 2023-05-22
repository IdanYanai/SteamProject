import pickle
import Database
import RSA
import base64
import bcrypt
import Games
import secrets
from Protocol import send_with_size


class Manager:
    def __init__(self, sock, address):
        self.db = Database.DataBaseORM()
        self.Enc = RSA.Encryptor()
        self.user = None
        self.sock = sock
        self.address = address

    def handle_message(self, msg, users):
        to_return = "ACKNW"
        command = msg.split("|")[0]
        print("Command: " + command)

        if command == "LOGIN":
            try:
                username = msg.split("|")[1]
                print("Username: " + username)
                password = msg[7 + len(username):]
                print("Encrypted: " + password)
                password = self.Enc.rsa_decrypt(password)
                print("Decrypted: " + password)
                hashed_password = self.db.GetPassword(username).encode()
                print(hashed_password)
                if bcrypt.checkpw(password.encode(), hashed_password):
                    uinfo = self.get_info(username)
                    to_return = b"UINFO|" + uinfo
                else:
                    to_return = b"ERROR - Username or password are incorrect"
            except Exception as err:
                print(err)
                to_return = b"ERROR - Username or password are incorrect"

        elif command == "REGIS":
            try:
                if len(msg.split("|")) > 5:
                    plength = len(msg.split("|")) - 4
                    password = " ".join(msg[2:2+plength])
                    username, username = msg.split("|")[:2]
                    nickname, email = msg.split("|")[2+plength:]
                else:
                    command, username, password, nickname, email = msg.split("|")

                print(command, username, password, nickname, email)

                password = self.Enc.rsa_decrypt(password)
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
                print(hashed_password)

                user = Database.Users(username, hashed_password, nickname, email)
                self.db.AddUser(user)
                uinfo = self.get_info(username)
                to_return = b"UINFO|" + uinfo

            except Exception as err:
                err = str(err)
                print(err)
                if "Username" in err:
                    to_return = b"ERROR - Username already taken"
                elif "Email" in err:
                    to_return = b"ERROR - Email already exists"
                elif "Nickname" in err:
                    to_return = b"ERROR - Nickname already taken"

        elif command == "LGOUT":
            self.user = None
            to_return = b"ACKNW"

        elif command == "MONEY":
            money = msg.split("|")[1]
            self.db.AddCash(self.user.ID, money)
            self.user.Money += float(money)
            to_return = b"ACKNW"

        elif command == "FREQU":
            nickname = msg.split("|")[1]
            id = self.db.GetID(nickname)
            fr = Database.FriendRequests(self.user.ID, id)
            self.db.SendFriendRequest(fr)
            if nickname in users.keys():
                other_client = users[nickname]
                message = "REQUF|" + self.user.Nickname
                send_with_size(other_client, message.encode())
            to_return = b"ACKNW"

        elif command == "RQACC":
            nickname = msg.split("|")[1]
            id = self.db.GetID(nickname)
            self.db.AcceptFriendRQ(id, self.user.ID)
            if nickname in users.keys():
                other_client = users[nickname]
                message = "ACCRQ|" + self.user.Nickname
                send_with_size(other_client, message.encode())
            to_return = b"ACKNW"

        elif command == "RQDEN":
            nickname = msg.split("|")[1]
            id = self.db.GetID(nickname)
            self.db.DenyFriendRQ(id, self.user.ID)
            to_return = b"ACKNW"
        
        elif command == "PURCH":
            game = msg.split("|")[1]
            id = self.db.GetID(self.user.Nickname)
            to_return = self.db.Purchase(id, game)

        elif command == "MSGFR":
            nick = msg.split("|")[1]
            msg = msg.split("|")[2]
            if nick in users.keys():
                other_client = users[nick]
                message = "FRMSG|" + self.user.Nickname + "|" + msg
                send_with_size(other_client, message.encode())
                to_return = b"ACKNW"
            else:
                to_return = b"ERROR - Friend not online"

        elif command == "INVIT":
            nick = msg.split("|")[1]
            game = msg.split("|")[2]
            if nick in users.keys():
                id = self.db.GetID(nick)
                games = self.db.GamesOwnedList(id)
                owns = False
                for g in games:
                    if game in g:
                        owns = True
                if owns:
                    token = secrets.token_hex(32)
                    print(token)
                    other_client = users[nick]
                    invite = "PINVI|" + self.user.Nickname + "|" + game + "|" + self.address[0] + "|" + token
                    send_with_size(other_client, invite.encode())
                    to_return = b"START|" + game.encode() + b"|" + self.address[0].encode() + b"|" + token.encode()
                else:
                    to_return = b"ERROR - Friend does not own this game"
            else:
                to_return = b"ERROR - Friend not online"

        elif command == "DOWNL":
            game = msg.split("|")[1]
            files = Games.send_game(game)
            for file in files:
                file = base64.b64encode(file)
                to_send = b"FILES|" + game.encode() + b"|" + file
                send_with_size(self.sock, to_send)
            to_return = b"Download complete"

        elif command == "DENYG":
            nick = msg.split("|")[1]
            if nick in users.keys():
                other_client = users[nick]
                message = "DENYG|" + nick
                send_with_size(other_client, message.encode())
                to_return = b"ACKNW"

        elif command == "ACPTG":
            to_return = b"ACKNW"

        else:
            to_return = b"Unknown command"

        return to_return

    def get_info(self, username):
        id, nickname, email, money = self.db.GetUserInfo(username)
        self.user = Database.Users(username, 0, nickname, email, money, id)
        fl = self.db.FriendList(self.user.ID)
        go = self.db.GamesOwnedList(self.user.ID)
        gl = self.db.GamesList()
        fr = self.db.FriendRequests(self.user.ID)

        data = pickle.dumps(self.user) + b"|" + pickle.dumps(fl) + b"|" + pickle.dumps(go) + b"|" + pickle.dumps(gl) \
               + b"|" + pickle.dumps(fr)
        print(data)
        return base64.b64encode(data)
