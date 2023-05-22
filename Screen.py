import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
import time
import Games

widgets = None
input_function = None
Popup = None
info = None
got_info = False
got_msg = None
chats = {}


class Screen:
    def __init__(self, func):
        global widgets, input_function
        input_function = func

        app = QApplication(sys.argv)
        widgets = QtWidgets.QStackedWidget()

        login = Login()
        widgets.addWidget(login)
        register = Register()
        widgets.addWidget(register)

        widgets.setFixedHeight(600)
        widgets.setFixedWidth(800)

        p = widgets.palette()
        p.setColor(widgets.backgroundRole(), QtCore.Qt.darkCyan)
        widgets.setPalette(p)

        widgets.show()

        self.worker = Poper()
        self.worker.start()
        self.worker.popup.connect(lambda: show_popup(Popup))
        self.worker.login.connect(load_user)
        self.worker.chatter.connect(update_chat)

        try:
            sys.exit(app.exec_())
        except:
            print("Shutting down...")
            input_function("DISCO")


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("uis/login.ui", self)
        self.setWindowTitle("Steam")
        self.register_bt.clicked.connect(self.GoToRegister)
        self.login_bt.clicked.connect(self.CheckLogin)

    def GoToRegister(self):
        widgets.setCurrentIndex(1)

    def CheckLogin(self):
        global input_function
        username = self.username.text()
        password = self.password.text()

        if username == "" or password == "":
            show_popup("Please fill all the fields")
        else:
            data = "LOGIN|" + username + "|" + password
            input_function(data)

        self.username.setText("")
        self.password.setText("")


class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("uis/register.ui", self)
        self.setWindowTitle("Steam")
        self.login_bt1.clicked.connect(self.GoToLogin)
        self.register_bt1.clicked.connect(self.CheckRegister)

    def GoToLogin(self):
        widgets.setCurrentIndex(0)

    def CheckRegister(self):
        global input_function
        username = self.username.text()
        password = self.password.text()
        email = self.email.text()
        nickname = self.nickname.text()

        if username == "" or password == "" or email == "" or nickname == "":
            show_popup("Please fill all the fields")
        else:
            data = "REGIS|" + username + "|" + password + "|" + nickname + "|" + email
            input_function(data)

        self.username.setText("")
        self.password.setText("")
        self.email.setText("")
        self.nickname.setText("")


class Chat(QDialog):
    def __init__(self, user, friend):
        global chats
        super(Chat, self).__init__()
        loadUi("uis/chat.ui", self)
        self.setWindowTitle("Steam")
        self.nickname.setText("Logged in - " + user)
        self.friendNick.setText("Chatting with - " + friend)

        self.friend = friend

        if friend in chats.keys():
            print(chats[friend])
            for msg in chats[friend]:
                if msg.startswith("F:"):
                    self.chat.addItem(friend + ": " + msg[2:])
                else:
                    self.chat.addItem("You: " + msg[4:])

        self.back.clicked.connect(self.GoBack)
        self.send.clicked.connect(self.SendMessage)

    def SendMessage(self):
        global input_function, chats
        msg = self.to_send.text()
        if msg != "":
            data = "MSGFR|" + self.friend + "|" + msg
            self.to_send.setText("")
            if self.friend in chats.keys():
                chats[self.friend].append("To: " + msg)
            else:
                chats[self.friend] = ["To: " + msg]
            self.chat.addItem("You: " + msg)
            input_function(data)

    def GoBack(self):
        global widgets, info
        widgets.setCurrentIndex(2)


class Main(QDialog):
    def __init__(self, user, f_list, g_list, games_owned, friend_rq):
        super(Main, self).__init__()
        loadUi("uis/main.ui", self)

        self.nickname.setText("Logged in - " + user.Nickname)
        self.name = user.Nickname
        self.money.setText("Money - " + str(user.Money))
        self.email.setText("Email - " + user.Email)

        for i in f_list:
            self.friends.addItem(str(i[3]))
        for i in games_owned:
            self.gamesOwned.addItem(str(i[1]))
        for i in g_list:
            if i not in games_owned:
                self.games.addItem(str(i[1]) + "(" + str(i[2]) + ")")
        for i in friend_rq:
            self.friendRequests.addItem(str(i[3]))

        self.logout.clicked.connect(self.Logout)
        self.send.clicked.connect(self.SendRequest)
        self.accept.clicked.connect(self.AcceptRq)
        self.deny.clicked.connect(self.DenyRq)
        self.addCash.clicked.connect(self.AddMoney)
        self.purchase.clicked.connect(self.PurchaseGame)
        self.invite.clicked.connect(self.Invite)
        self.chat.clicked.connect(self.GoChat)
        self.uninstall.clicked.connect(self.UninstallGame)
        self.install.clicked.connect(self.InstallGame)

    def Logout(self):
        global input_function, info
        info = None
        widgets.setCurrentIndex(0)
        input_function("LGOUT")

    def SendRequest(self):
        global input_function
        in_friends = False
        in_requests = False
        friend_name = self.friendName.text()
        rows = self.friends.count()
        for i in range(rows):
            if friend_name == self.friends.item(i).text():
                in_friends = True
        rows = self.friendRequests.count()
        for i in range(rows):
            if friend_name == self.friendRequests.item(i).text():
                in_requests = True
        if friend_name != "":
            if not in_friends:
                if not in_requests:
                    data = "FREQU|" + friend_name
                    input_function(data)
                else:
                    show_popup("A request from this user is already pending")
            else:
                show_popup("This user is already your friend")
        self.friendName.setText("")

    def AcceptRq(self):
        global input_function
        row = self.friendRequests.currentRow()
        if row != -1:
            friend = self.friendRequests.takeItem(row).text()
            self.friends.addItem(friend)
            data = "RQACC|" + friend
            input_function(data)

    def DenyRq(self):
        global input_function
        row = self.friendRequests.currentRow()
        if row != -1:
            friend = self.friendRequests.takeItem(row).text()
            data = "RQDEN|" + friend
            input_function(data)

    def AddMoney(self):
        global input_function
        to_add = self.cash.text()
        money = self.money.text().split()[2]
        if to_add != "" or to_add.isnumeric():
            new_money = float(money) + float(to_add)
            self.money.setText("Money - " + str(new_money))
            data = "MONEY|" + to_add
            self.cash.setText("")
            input_function(data)

    def PurchaseGame(self):
        global input_function
        row = self.games.currentRow()
        if row != -1:
            game_name = self.games.item(row).text()[:-6]
            game = self.games.item(row).text()
            money = self.money.text().split()[2]
            game_cost = game.split("(")[1]
            game_cost = game_cost[:-1]
            print("Cost:" + game_cost)
            if float(money) >= float(game_cost):
                take = self.games.takeItem(row)
                data = "PURCH|" + game_name
                input_function(data)
            else:
                show_popup("Not enough money to purchase game")

    def Invite(self):
        global input_function
        friend_row = self.friends.currentRow()
        game_row = self.gamesOwned.currentRow()
        if friend_row != -1 and game_row != -1:
            friend = self.friends.currentItem().text()
            game = self.gamesOwned.currentItem().text()
            data = "INVIT|" + friend + "|" + game
            input_function(data)

    def GoChat(self):
        friend_row = self.friends.currentRow()
        if friend_row != -1:
            friend = self.friends.currentItem().text()
            chat = Chat(self.name, friend)
            widgets.insertWidget(3, chat)
            widgets.setCurrentIndex(3)

    def UninstallGame(self):
        game_row = self.gamesOwned.currentRow()
        if game_row != -1:
            game = self.gamesOwned.currentItem().text()
            if Games.check_install(game):
                Games.uninstall_game(game)
                show_popup("Successfully removed game")
            else:
                show_popup("Game not installed")

    def InstallGame(self):
        global input_function
        game_row = self.gamesOwned.currentRow()
        if game_row != -1:
            game = self.gamesOwned.currentItem().text()
            if Games.check_install(game):
                show_popup("Game already installed")
            else:
                input_function("DOWNL|" + game)


class Poper(QtCore.QThread):
    popup = QtCore.pyqtSignal()
    login = QtCore.pyqtSignal()
    chatter = QtCore.pyqtSignal()

    def run(self):
        global Popup, got_info, got_msg
        while True:
            while Popup is None and not got_info and got_msg is None:
                time.sleep(1)
            if got_info:
                self.login.emit()
            elif got_msg:
                self.chatter.emit()
            elif Popup:
                self.popup.emit()
            time.sleep(1)
            Popup = None
            got_info = False
            got_msg = None


def update_chat():
    global widgets, got_msg
    user, friend = got_msg.split()
    if widgets.currentIndex() == 3:
        chat = Chat(user, friend)
        widgets.insertWidget(3, chat)
        widgets.setCurrentIndex(3)


def load_user():
    global widgets, info
    user, f_list, g_list, games_owned, friend_rq = info
    main = Main(user, f_list, g_list, games_owned, friend_rq)
    widgets.insertWidget(2, main)
    widgets.setCurrentIndex(2)


def show_popup(pop):
    msg = QMessageBox()
    if "invited" in pop:
        msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        msg.setWindowTitle("Server")
        msg.setText(pop)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(popup_clicked)
    else:
        msg.setWindowTitle("Server")
        msg.setText(pop)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)

    x = msg.exec_()


def popup_clicked(press):
    global input_function
    print("PRESSED")
    press = press.text()
    print(press)
    if "Yes" in press:
        input_function("ACPTG")
    else:
        input_function("DENYG")
