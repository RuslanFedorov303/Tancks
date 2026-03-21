from Options2 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        screen.fill((255, 255, 255))

        try:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            socket_player.send(
                json.dumps(
                    (event, mouse_x, mouse_y)
                ).encode()
            )

            information_received = socket_player.recv(1024).decode().strip()
            information_received = json.loads(information_received)
            if information_received:
                drawTank(information_received)


        except Exception as ex:
            print(ex)




    pygame.display.flip()
    clock.tick(60)