import pygame


class Tower:
    def __init__(self, name, x, y, id):
        self.name = name
        if self.name.upper() == "DART MONKEY":
            self.damage = 1
            self.attack_speed = 2
            self.radius = 100
            self.image = pygame.image.load("Dart_Monkey.png").convert()
        elif self.name.upper() == "TACK SHOOTER":
            self.damage = 1
            self.attack_speed = 4
            self.radius = 50
            self.image = pygame.image.load("Tack_Shooter.png").convert()
        elif self.name.upper() == "SUPER MONKEY":
            self.damage = 1
            self.attack_speed = 1
            self.radius = 500
            self.image = pygame.image.load("Super_Monkey.png").convert()
        self.x = x
        self.y = y
        self.center_x = x+22
        self.center_y = y+27
        self.id = id
        self.image.set_colorkey((255, 255, 255))

    def draw(self, window):
        """
        draws the tower
        :return nothing:
        """
        window.blit(self.image, (self.x, self.y))

    def attack(self, balloons):
        """
        gets the list of balloons from the player and then attacks balloons
        according to the tower's name
        :return nothing:
        """
        if self.name.upper() == "DART MONKEY" or self.name.upper() == "SUPER MONKEY":
            for b in balloons:
                if b.x < 500 and self.id == "1":
                    if self.center_x - self.radius < b.x < self.center_x + self.radius:
                        if self.center_y - self.radius < b.y < self.center_y + self.radius:
                            b.hp -= self.damage
                            break
                elif b.x > 500 and self.id == "2":
                    if self.center_x - self.radius < b.x < self.center_x + self.radius:
                        if self.center_y - self.radius < b.y < self.center_y + self.radius:
                            b.hp -= self.damage
                            break
        elif self.name.upper() == "TACK SHOOTER":
            for b in balloons:
                if b.x < 500 and self.id == "1":
                    if self.center_x - self.radius < b.x < self.center_x + self.radius:
                        if self.center_y - self.radius < b.y < self.center_y + self.radius:
                            b.hp -= self.damage
                elif b.x > 500 and self.id == "2":
                    if self.center_x - self.radius < b.x < self.center_x + self.radius:
                        if self.center_y - self.radius < b.y < self.center_y + self.radius:
                            b.hp -= self.damage
