from Classes1 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))

tank = Tank(body_image       = body_image,
            turret_image     = turret_image,
            gun_image        = gun_image,
            projectile_image = projectile_image,
            x_coord=200, y_coord=200)


def drawTank(dataPlayer):
    rotated_body = pygame.transform.rotate(body_image, dataPlayer['body_rotate'])
    body_rect = rotated_body.get_rect(center=(dataPlayer['x_coord'], dataPlayer['y_coord']))
    screen.blit(rotated_body, body_rect)

    rotated_gun = pygame.transform.rotate(gun_image, dataPlayer['turret_rotate'])
    gun_rect = rotated_gun.get_rect(center=(dataPlayer['x_coord'], dataPlayer['y_coord']))
    screen.blit(rotated_gun, gun_rect)

    rotated_turret = pygame.transform.rotate(turret_image, dataPlayer['turret_rotate'])
    turret_rect = rotated_turret.get_rect(center=(dataPlayer['x_coord'], dataPlayer['y_coord']))
    screen.blit(rotated_turret, turret_rect)


while True:
    try:
        socket_player.send(
            json.dumps(
                tank.get_data()
            ).encode()
        )


        information_received = socket_player.recv(1024).decode().strip()
        information_received = json.loads(information_received)
        if information_received:
            drawTank(information_received)


    except Exception as ex:
        print(ex)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    screen.fill((255, 255, 255))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    tank.tankUpdate(screen, event, mouse_x, mouse_y)

    pygame.display.flip()
    clock.tick(60)