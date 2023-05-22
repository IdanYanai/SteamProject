import sqlite3


class Users(object):
    def __init__(self, username, password, nickname, email, money=0, id=None):
        self.ID = id
        self.Username = username
        self.Password = password
        self.Nickname = nickname
        self.Email = email
        self.Money = money


class Games(object):
    def __init__(self, name, path, price, description, release_date, id=None):
        self.ID = id
        self.Name = name
        self.Path = path
        self.Price = price
        self.Description = description
        self.Release_date = release_date


class GamesOwned(object):
    def __init__(self, UserID, GameID):
        self.UserID = UserID
        self.GameID = GameID


class Friends(object):
    def __init__(self, UserID, FriendID):
        self.UserID = UserID
        self.FriendID = FriendID


class FriendRequests(object):
    def __init__(self, sender, receiver):
        self.Sender = sender
        self.Receiver = receiver


class DataBaseORM:
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('Database.db')
        self.current = self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def AddUser(self, user):
        self.open_DB()

        sql = "SELECT MAX(ID) FROM Users"
        res = self.current.execute(sql)
        maxID = res.fetchone()[0]
        if maxID is None:
            maxID = 0
        maxID = int(maxID) + 1

        print(maxID, user.Username, user.Password, user.Nickname, user.Email, user.Money)

        sql = "INSERT INTO Users (ID, Username, Password, Nickname, Email, Money) VALUES " \
              "(%d, '%s', '%s', '%s', '%s', %d)" % (maxID, user.Username, user.Password, user.Nickname,
                                                          user.Email, user.Money)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def AddGame(self, game):
        self.open_DB()

        sql = "SELECT MAX(ID) FROM Games"
        res = self.current.execute(sql)
        maxID = res.fetchone()[0]
        if maxID is None:
            maxID = 0
        maxID = int(maxID) + 1

        sql = "INSERT INTO Games (ID, Name, Path, Price, Description, Release_Date) VALUES " \
              "(%d, '%s', %s, '%s', '%s', %d)" % \
              (maxID, game.Name, game.Path, game.Price, game.Description, game.Release_Date)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def AddGameOwned(self, gameOwned):
        self.open_DB()

        sql = "INSERT INTO GamesOwned (UserID, GameID) VALUES " \
              "(%d, %d)" % (gameOwned.UserID, gameOwned.GameID)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def SendFriendRequest(self, friend_rq):
        self.open_DB()

        sql = "INSERT INTO FriendRequests (Sender, Receiver) VALUES " \
              "(%d, %d)" % (friend_rq.Sender, friend_rq.Receiver)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def FriendList(self, id):
        self.open_DB()

        sql = "SELECT FriendID FROM Friends WHERE UserID = %d" % id
        res = self.current.execute(sql)
        ids = res.fetchall()

        f_list = []
        for friend_id in ids:
            sql = "SELECT * FROM Users WHERE ID = %d" % friend_id
            res = self.current.execute(sql)
            f = res.fetchone()
            f_list.append(f)

        self.close_DB()
        return f_list

    def GamesOwnedList(self, id):
        self.open_DB()

        sql = "SELECT GameID FROM GamesOwned WHERE UserID = %d" % id
        res = self.current.execute(sql)
        ids = res.fetchall()

        g_list = []
        for game_id in ids:
            sql = "SELECT * FROM Games WHERE ID = %d" % game_id
            res = self.current.execute(sql)
            g = res.fetchone()
            g_list.append(g)

        self.close_DB()
        return g_list

    def GamesList(self):
        self.open_DB()

        sql = "SELECT * FROM Games"
        res = self.current.execute(sql)
        data = res.fetchall()

        self.close_DB()
        return data

    def GetPassword(self, username):
        self.open_DB()

        sql = "SELECT Password FROM Users WHERE Username = '%s'" % username
        res = self.current.execute(sql)
        data = res.fetchone()[0]

        self.close_DB()
        return data

    def GetUserInfo(self, username):
        self.open_DB()

        sql = "SELECT ID, Nickname, Email, Money FROM Users WHERE Username = '%s'" % username
        res = self.current.execute(sql)
        data = res.fetchone()

        self.close_DB()
        return data

    def GetID(self, nickname):
        self.open_DB()

        sql = "SELECT ID FROM Users WHERE Nickname = '%s'" % nickname
        res = self.current.execute(sql)
        data = res.fetchone()[0]

        self.close_DB()
        return data

    def FriendRequests(self, id):
        self.open_DB()

        sql = "SELECT Sender FROM FriendRequests Requests WHERE Receiver = %d" % id
        res = self.current.execute(sql)
        ids = res.fetchall()

        f_list = []
        for friend_id in ids:
            sql = "SELECT * FROM Users WHERE ID = %d" % friend_id
            res = self.current.execute(sql)
            f = res.fetchone()
            f_list.append(f)

        self.close_DB()
        return f_list

    def AcceptFriendRQ(self, Sender, Receiver):
        self.open_DB()

        sql = "INSERT INTO Friends (UserID, FriendID) VALUES (%d, %d)" % (Sender, Receiver)
        res = self.current.execute(sql)
        sql = "INSERT INTO Friends (UserID, FriendID) VALUES (%d, %d)" % (Receiver, Sender)
        res = self.current.execute(sql)
        sql = "DELETE FROM FriendRequests WHERE Sender = %d AND Receiver = %d" % (Sender, Receiver)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def DenyFriendRQ(self, Sender, Receiver):
        self.open_DB()

        sql = "DELETE FROM FriendRequests WHERE Sender = %d AND Receiver = %d" % (Sender, Receiver)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def AddCash(self, id, amount):
        self.open_DB()

        sql = "SELECT Money FROM Users WHERE ID = %d" % id
        res = self.current.execute(sql)
        money = res.fetchone()[0]
        new_money = float(money) + float(amount)
        sql = "UPDATE Users SET Money = %d WHERE ID = %d" % (new_money, id)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def Purchase(self, UserID, Game):
        self.open_DB()

        sql = "SELECT Price FROM Games WHERE Name = '%s'" % Game
        res = self.current.execute(sql)
        Price = res.fetchone()[0]
        sql = "SELECT Money FROM Users WHERE ID = %d" % UserID
        res = self.current.execute(sql)
        Money = res.fetchone()[0]

        if Money >= Price:
            sql = "SELECT ID FROM Games WHERE Name = '%s'" % Game
            res = self.current.execute(sql)
            GameID = res.fetchone()[0]
            sql = "UPDATE Users SET Money = %d WHERE ID = %d" % ((Money - Price), UserID)
            res = self.current.execute(sql)
            sql = "INSERT INTO GamesOwned (UserID, GameID) VALUES (%d, %d)" % (UserID, GameID)
            res = self.current.execute(sql)
        else:
            return b"ERROR - Not enough money"

        self.commit()
        self.close_DB()

        return b"CMPLT|" + Game.encode() + b"|" + (str(Money-Price)).encode()
