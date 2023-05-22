import pygame
import Balloon
import Tower


class Player:
    def __init__(self, id):
        self.id = id
        self.health = 10
        self.queue = []
        self.balloons = []
        self.money = 0
        self.towers = []
        self.round = 0
        self.buying = ""
        self.income = 250
        self.round_started = True

    def update(self, window, time):
        """
        updates the time, round, health, money, income, the ENEMY/YOU
        and initiates new rounds every 20 seconds by calling self.next round.
        additionally removes balloons with 0 or below health.
        :returns nothing:
        """
        font = pygame.font.SysFont('arial', 25, True)
        text = font.render('%s:%s' % ((str(time / 60)).zfill(2), (str(time % 60)).zfill(2)), 0, (255, 255, 255))
        window.blit(text, (470, 0))
        text = font.render("Round %s" % str(self.round), 0, (255, 255, 255))
        window.blit(text, (450, 25))
        text = font.render("Health:%s" % str(self.health), 0, (200, 0, 0))
        window.blit(text, (450, 50))
        text = font.render("Money:", 0, (0, 255, 0))
        window.blit(text, (450, 75))
        text = font.render("%s$" % str(self.money), 0, (0, 255, 0))
        window.blit(text, (450, 100))
        text = font.render("Income:", 0, (0, 200, 0))
        window.blit(text, (450, 125))
        text = font.render("%s$" % str(self.income), 0, (0, 200, 0))
        window.blit(text, (450, 150))
        font = pygame.font.SysFont('arial', 20, True)
        if self.id == "1":
            text = font.render("YOU", 0, (255, 255, 255))
            window.blit(text, (250, 0))
            text = font.render("ENEMY", 0, (255, 0, 0))
            window.blit(text, (700, 0))
        else:
            text = font.render("ENEMY", 0, (255, 0, 0))
            window.blit(text, (250, 0))
            text = font.render("YOU", 0, (255, 255, 255))
            window.blit(text, (700, 0))
        # pygame.display.update((450, 0, 100, 150))

        if time % 20 == 0 and (not self.round_started):
            self.next_round()
            self.round_started = True
        elif time % 20 != 0 and self.round_started:
            self.round_started = False

        for b in self.balloons:
            if b.hp <= 0:
                self.balloons.remove(b)

    def next_round(self):
        """
        adds 8 balloons to every player according to the self.round and adds one to self.round
        :returns nothing:
        """
        self.round += 1
        self.money += self.income
        bloons = (8, self.round)
        for bloon in range(bloons[0]):
            self.queue.append(Balloon.Balloon(bloons[1], 100, 0))
            self.queue.append(Balloon.Balloon(bloons[1], 550, 0))

    def check_click(self, pos, window):
        """
        gets the players click position and checks it
        gets the display as well to check if the player clicked on the grass (if he just bought a tower)
        :returns a string according to the position of the click:
        """
        x = pos[0]
        y = pos[1]
        to_return = ""
        if 6 < x < 91:
            cost = 100
            top_y = 41
            bottom_y = 111
            for i in xrange(7):
                if top_y < y < bottom_y and self.money >= cost:
                    if i == 6 and self.money >= 1000:
                        self.money -= 1000
                        self.income += 30
                        if self.id == "1":
                            to_return = "OFFENSE:%s:%s:%s:%s" % ("8", str(self.round), str(550), str(0))
                        else:
                            to_return = "OFFENSE:%s:%s:%s:%s" % ("8", str(self.round), str(100), str(0))
                    else:
                        self.money -= cost
                        self.income += (i+1) * 10
                        if self.id == "1":
                            to_return = "OFFENSE:%s:%s:%s:%s" % ("8", str(i+1), str(550), str(0))
                        else:
                            to_return = "OFFENSE:%s:%s:%s:%s" % ("8", str(i+1), str(100), str(0))
                        break
                cost += 100
                top_y += 85
                bottom_y += 85

        elif self.buying == "":
            if 907 < x < 992:
                if 52 < y < 157 and self.money >= 250:
                    self.money -= 250
                    self.buying = "DART MONKEY"
                elif 265 < y < 370 and self.money >= 500:
                    self.money -= 500
                    self.buying = "TACK SHOOTER"
                elif 478 < y < 583 and self.money >= 1000:
                    self.money -= 1000
                    self.buying = "SUPER MONKEY"
        else:
            x -= 22  # center of the image
            y -= 27  # center of the image
            if self.id == "1":
                if window.get_at(pos) == (34, 177, 76) and x < 500:
                    to_return = "DEFENSE:%s:%s:%s:%s" % (self.buying, str(x), str(y), self.id)
                    self.buying = ""
            elif self.id == "2":
                if window.get_at(pos) == (34, 177, 76) and x > 500:
                    to_return = "DEFENSE:%s:%s:%s:%s" % (self.buying, str(x), str(y), self.id)
                    self.buying = ""
        return to_return

    def handle_data(self, data):
        """
        adds balloons or towers to the main lists of the game according to the data
        :return nothing:
        """
        type = data.split(":")[0]
        if type == "DEFENSE":
            name, x, y, id = data.split(":")[1:]
            self.towers.append(Tower.Tower(name, int(x), int(y), id))
        elif type == "OFFENSE":
            count, hp, x, y = data.split(":")[1:]
            for i in range(int(count)):
                self.queue.append(Balloon.Balloon(int(hp), int(x), int(y)))
