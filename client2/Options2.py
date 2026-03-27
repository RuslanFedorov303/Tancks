import pygame
from socket import *
import json


HOST = 'localhost'
IP = 8081


screen = pygame.display.set_mode((1300, 1000)) # Создаем екран и время
clock = pygame.time.Clock()


body_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_body.png").convert_alpha(),
        (600, 300))

turret_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_turret.png").convert_alpha(),
        (600, 300))

gun_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_gun.png").convert_alpha(),
        (600, 300))

projectile_image = pygame.transform.scale(
        pygame.image.load("Image/Projectile.png").convert_alpha(),
        (600, 300))

bush_image = pygame.transform.scale(
        pygame.image.load("Image/Bush.png").convert_alpha(),
        (600, 300))



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
    print(True)