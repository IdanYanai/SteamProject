import pygame


class Balloon:
    def __init__(self, hp, x, y):
        self.hp = hp
        self.speed = 5
        self.x = x
        self.y = y
        self.last_hp = 0
        self.image = pygame.image.load("red.png").convert()
        self.image.set_colorkey((195, 195, 195))
        self.last_position = (x, y, 19, 25)

    def draw(self, window):
        """
        draws the balloon according to its HP
        :return nothing:
        """
        if self.hp != self.last_hp:
            if self.hp == 1:
                self.image = pygame.image.load("red.png").convert()
            elif self.hp == 2:
                self.image = pygame.image.load("blue.png").convert()
            elif self.hp == 3:
                self.image = pygame.image.load("green.png").convert()
            elif self.hp == 4:
                self.image = pygame.image.load("yellow.png").convert()
            elif self.hp == 5:
                self.image = pygame.image.load("pink.png").convert()
            elif self.hp == 6:
                self.image = pygame.image.load("black.png").convert()
            elif self.hp >= 7:
                self.image = pygame.image.load("rainbow.png").convert()
            self.image.set_colorkey((195, 195, 195))
        self.last_position = window.blit(self.image, (self.x, self.y))

    def move(self, player_id):
        """
        moves the balloon according to its position and in a fixed way
        if the balloon gets past the red line it returns its self.hp otherwise and sets it to 0
        gets players id so it can return the hp of balloons for only this player
        """
        if self.y >= 385:
            hp = self.hp
            self.hp = 0
            if self.x < 500 and player_id == "1":
                return hp
            elif self.x > 500 and player_id == "2":
                return hp
            return 0
        turns = {(100, 25): "+x", (430, 125): "-x", (100, 225): "+x", (430, 325): "-x", (100, 425): "+x",
                 (430, 525): "-x", (100, 625): "+x", (430, 725): "-x", (430, 25): "+y", (100, 125): "+y",
                 (430, 225): "+y", (100, 325): "+y", (430, 425): "+y", (100, 525): "+y", (430, 625): "+y",
                 (100, 725): "+y",  # player 1 turns
                 (550, 25): "+x", (880, 125): "-x", (550, 225): "+x", (880, 325): "-x", (550, 425): "+x",
                 (880, 525): "-x", (550, 625): "+x", (880, 725): "-x", (880, 25): "+y", (550, 125): "+y",
                 (880, 225): "+y", (550, 325): "+y", (880, 425): "+y", (550, 525): "+y", (880, 625): "+y",
                 (550, 725): "+y"  # player 2 turns
                 }

        pos = (self.x, self.y)
        if pos in turns:
            action = turns[pos]
            if action[1] == "x":
                if action[0] == '-':
                    self.x -= self.speed
                else:
                    self.x += self.speed
            else:
                self.y += self.speed

        elif self.y % 200 == 25:
            self.x += self.speed
        elif self.y % 100 == 25:
            self.x -= self.speed

        elif self.x < 500:
            if self.x == 100:
                self.y += self.speed
            elif self.x == 430:
                self.y += self.speed

        elif self.x > 500:
            if self.x == 550:
                self.y += self.speed
            elif self.x == 880:
                self.y += self.speed
        return 0



