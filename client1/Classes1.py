# ----- !----- !-- Импортируем --! -----! ----- #
import pygame
from random import randint
from time import time, sleep
import math
from socket import *
import threading
import json




# ----- !----- !-- Создаем - инициализируем --! -----! ----- #
# ----- !-- Настройки хоста --! ----- #
HOST = 'localhost'
IP = 8081
# ----- !-----! ----- #


pygame.init() # Инициализируем pygame
pygame.mixer.init() # Инициализируем mixer


screen = pygame.display.set_mode((1300, 700)) # Создаем екран и время
clock = pygame.time.Clock()



# ----- !-- Загружаем картинки --! ----- #
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
        pygame.image.load("Image/Пуля.png").convert_alpha(),
        (600, 300))

projectiles = [] # Список снарядов
players = [] # Список танков



# ----- !-- Загружаем звуки --! ----- #
s = pygame.mixer.Sound("Sound/Shoot.mp3")




# ----- !----- !-- Создаем - класи --! -----! ----- #
# ----- !-- Снаряды --! ----- #
class Projectile:
    def __init__(projectile,
                 x_coord       = 100.0,
                 y_coord       = 100.0,
                 x_coord_speed = 20.0,
                 y_coord_speed = 20.0,
                 speed         = 3.0,
                 rotate        = 0.0,
                 damage      = randint(3000, 8000),
                 penetration = 20,  # %
                 comand      = 'green',
                 image = ''
                 ):

        projectile.x_coord       = x_coord
        projectile.y_coord       = y_coord
        projectile.x_coord_speed = x_coord_speed
        projectile.y_coord_speed = y_coord_speed
        projectile.speed         = speed
        projectile.rotate        = rotate
        projectile.damage      = damage
        projectile.penetration = penetration
        projectile.comand      = comand
        projectile.image = pygame.transform.rotate(image, rotate)
        projectile.projectile = pygame.mask.from_surface(
            pygame.Surface((600, 300)))



    def projectileMove(projectile):
        projectile.x_coord += projectile.x_coord_speed * projectile.speed
        projectile.y_coord += projectile.y_coord_speed * projectile.speed



    def projectileColide(projectile, colide):
        if __class__.colide == 'Tank' and colide.comand != projectile.comand:
            if colide.penetration <= randint(0, 100):
                colide.health -= projectile.damage



    def projectileDraw(projectile, screen):
        projectile_rect = projectile.image.get_rect(center=(projectile.x_coord, projectile.y_coord))
        screen.blit(projectile.image, projectile_rect)



    def projectileUpdate(self, screen, colide=None):
        self.projectileMove()
        # self.projectileColide(colide)
        self.projectileDraw(screen)




# ----- !-- Танки --! ----- #
class Tank:
    def __init__(self,
                 x_coord = 100.0,
                 y_coord = 100.0,
                 speed   = 3.0,
                 __body_rotate       = 0.0,
                 __turret_rotate     = 0.0,
                 body_rotate_speed   = 1.0,
                 turret_rotate_speed = 1.2,
                 health           = 10_000,
                 damage           = (3000, 8000), # От - до
                 penetration      = 20, # %
                 recharge         = 3,
                 projectile_speed = 70,
                 comand           = 'green',
                 player_ID        = 1,
                 body_image       = '',
                 turret_image     = '',
                 gun_image        = '',
                 projectile_image = ''
                 ):

        self.x_coord = x_coord
        self.y_coord = y_coord
        self.speed   = speed
        self.body_rotate         = __body_rotate
        self.turret_rotate       = __turret_rotate
        self.body_rotate_speed   = body_rotate_speed    / 5
        self.turret_rotate_speed = turret_rotate_speed / 5
        self.health           = health
        self.damage           = damage
        self.penetration      = penetration
        self.recharge         = recharge
        self.projectile_speed = projectile_speed
        self.comand           = comand
        self.player_ID        = player_ID
        self.body_image       = body_image
        self.turret_image     = turret_image
        self.gun_image        = gun_image
        self.projectile_image = projectile_image


        self.recharging_long_start = recharge # Настройки перезарядки
        self.recharging_long_exit  = 0.0


        self.position_vector         = pygame.Vector2((self.x_coord, self.y_coord))
        self.body_direction_vector   = pygame.Vector2((1, 0))
        self.turret_direction_vector = pygame.Vector2((1, 0))
        self.gun_direction_vector    = pygame.Vector2((1, 0))

        self.gun_offset_animate = 0.0



    def _bodyMove(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.position_vector += self.body_direction_vector * self.speed
        if keys[pygame.K_s]: self.position_vector -= self.body_direction_vector * self.speed



    def _bodyRotate(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.body_rotate   += self.body_rotate_speed
            self.turret_rotate += self.body_rotate_speed

            self.body_direction_vector.rotate_ip(-self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(-self.body_rotate_speed)


        if keys[pygame.K_d]:
            self.body_rotate   -= self.body_rotate_speed
            self.turret_rotate -= self.body_rotate_speed

            self.body_direction_vector.rotate_ip(self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(self.body_rotate_speed)


        self.x_coord = self.position_vector.x
        self.y_coord = self.position_vector.y



    def _colideWalls(self):
        pass



    def _turretRotate(self, mouse_x, mouse_y):
        rel_x = mouse_x - self.x_coord
        rel_y = mouse_y - self.y_coord

        target_angle = math.degrees(math.atan2(-rel_y, rel_x))
        angle_degrees = (target_angle - self.turret_rotate + 180) % 360 - 180


        if abs(angle_degrees) > self.turret_rotate_speed:
            if angle_degrees > 0:
                self.turret_rotate += self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(-self.turret_rotate_speed)
                # self.gun_direction_vector.rotate_ip(-self.turret_rotate_speed)

            else:
                self.turret_rotate -= self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(self.turret_rotate_speed)
                # self.gun_direction_vector.rotate_ip(self.turret_rotate_speed)



    def _gunShoot(self, event):
        self.recharging_long_exit = time()


        if (event.type == pygame.MOUSEBUTTONDOWN
        and self.recharging_long_exit - self.recharging_long_start >= self.recharge):
            self.gun_offset_animate += 50.0


            projectiles.append(Projectile(x_coord       = self.x_coord,
                                          y_coord       = self.y_coord,
                                          x_coord_speed = self.turret_direction_vector.x,
                                          y_coord_speed = self.turret_direction_vector.y,
                                          speed         = self.projectile_speed,
                                          rotate        = self.turret_rotate,
                                          damage      = randint(self.damage[0], self.damage[1]),
                                          penetration = self.penetration,
                                          comand      = self.comand,
                                          image = self.projectile_image
                                          ))
            self.recharging_long_start = time()

        if self.gun_offset_animate > 0:
            self.gun_offset_animate -= 5 / self.recharge



    def _tankDraw(self, screen):
        rotated_body = pygame.transform.rotate(self.body_image, self.body_rotate)
        body_rect = rotated_body.get_rect(center=(self.x_coord, self.y_coord))
        screen.blit(rotated_body, body_rect)


        rotated_gun = pygame.transform.rotate(self.gun_image, self.turret_rotate)
        gun_rect = rotated_gun.get_rect(center=(self.x_coord, self.y_coord))
        screen.blit(rotated_gun, gun_rect)


        rotated_turret = pygame.transform.rotate(self.turret_image, self.turret_rotate)
        turret_rect = rotated_turret.get_rect(center=(self.x_coord, self.y_coord))
        screen.blit(rotated_turret, turret_rect)



    def tankUpdate(self, screen, event, mouse_x, mouse_y):
        self._bodyMove()
        self._bodyRotate()
        self._colideWalls()
        self._turretRotate(mouse_x, mouse_y)
        self._gunShoot(event)
        self._tankDraw(screen)



    def get_data(self):
        return {
            'x_coord'       : self.x_coord,
            'y_coord'       : self.y_coord,
            'body_rotate'   : self.body_rotate,
            'turret_rotate' : self.turret_rotate,
            'health'        : self.health,
            'comand'        : self.comand,
            'player_ID'     : self.player_ID
        }













