import socket
import Player
import pygame
from tcp_by_size import recv_by_size, send_with_size
import sys
import os


def main():
    if len(sys.argv) != 3:
        sys.exit("Please enter IP and Token")
    else:
        ip = sys.argv[1]
        token = sys.argv[2]
    port = 6968

    sock = socket.socket()
    sock.connect((ip, port))
    send_with_size(sock, token)
    player_id = recv_by_size(sock)
    if player_id == "":
        sock.close()
        sys.exit("Wrong token")
    print "Connected - player number %s" % player_id
    game_start = recv_by_size(sock)
    if game_start == "GAME START":
        print "GAME START"
    print(os.getcwd() + "\Games\Bloons TD Battles\Client")
    os.chdir(os.getcwd() + "\Games\Bloons TD Battles\Client")
    pygame.init()
    window = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("BTD Battles")
    map = pygame.image.load("Map.png").convert_alpha()
    window.blit(map, (0, 0))

    p = Player.Player(player_id)
    running = True
    sock.settimeout(0.1)
    pygame.display.update()
    clock = pygame.time.Clock()
    p.next_round()
    match = ""
    while running:
        try:
            clock.tick(4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    send_with_size(sock, "SHUT DOWN")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    to_send = p.check_click(pos, window)
                    if to_send != "":
                        send_with_size(sock, to_send)
            timer = pygame.time.get_ticks() / 1000

            window.blit(map, (0, 0))

            p.update(window, timer)

            if p.queue:
                p.balloons.append(p.queue[0])
                del p.queue[0]

            for b in p.balloons:
                p.health -= b.move(p.id)
                b.draw(window)

            for tower in p.towers:
                if timer % tower.attack_speed == 0:
                    tower.attack(p.balloons)
                tower.draw(window)

            pygame.display.update()

            if p.health <= 0:
                print "MATCH END"
                match = "YOU LOSE"
                send_with_size(sock, "MATCH END")
                break

            data = recv_by_size(sock)
            if data:
                if data == "SHUT DOWN":
                    running = False
                elif "MATCH END" in data:
                    running = False
                    match = "YOU WIN"
                print data
                p.handle_data(data)
            else:
                running = False
                print "Server disconnected"

        except socket.timeout:
            continue

    if match != "":
        font = pygame.font.SysFont('arial', 200, True)
        if match == "YOU WIN":
            text = font.render("YOU WIN", 0, (0, 230, 0))
        else:
            text = font.render("YOU LOSE", 0, (230, 0, 0))
        window.blit(text, (20, 150))
        pygame.display.update()
        pygame.time.wait(5 * 1000)

    pygame.quit()
    sock.close()


if __name__ == '__main__':
    main()
