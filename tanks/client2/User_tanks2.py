from Options2 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))



while True:
    new_event = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            new_event = 'MOUSEBUTTONDOWN'


    screen.fill((255, 255, 255))


    try:
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()





            # if event.type == pygame.KEYMAPCHANGED:
        if keys[pygame.K_w]:           new_event = 'K_w'
        if keys[pygame.K_s]:           new_event = 'K_s'
        if keys[pygame.K_a]:           new_event = 'K_a'
        if keys[pygame.K_d]:           new_event = 'K_d'

        socket_player.send(
            json.dumps(
                (new_event, mouse_x, mouse_y)
            ).encode()
        )

        information_received = socket_player.recv(1024).decode().strip()
        information_received = json.loads(information_received)
        print(information_received)
        drawTank(information_received)


    except Exception as ex:
        print(ex)



    pygame.display.flip()
    clock.tick(60)