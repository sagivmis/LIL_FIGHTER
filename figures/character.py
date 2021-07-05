import os

import pygame
import time
import random
import math

import cfg


class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super(self.__class__, self).__init__()
        self.images = []
        dir = ''
        d = ''
        if name == 'thug':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\ThugSlashing'
            d = 'ThugSlashing'
        if name == 'knight':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\MedievalSlashing'
            d = 'MedievalSlashing'
        if name == 'ninja':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\NinjaSlashing'
            d = 'NinjaSlashing'

        for file in os.listdir(dir):
            if file.endswith('.png'):
                self.images.append(pygame.image.load(f'{d}\{file}'))

        self.idle_image = pygame.image.load(f'{d}/idle/Idle_000.png')
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[int(self.current_image)], (80, 80))
        self.image.set_colorkey((113, 102, 79))
        self.skill_images = []
        self.current_skill_image = 0
        dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\Skill'

        for file in os.listdir(dir):
            if file.endswith('.png'):
                self.skill_images.append(pygame.image.load(f'Skill\{file}'))

        self.skill_image = self.skill_images[self.current_skill_image]
        self.name = name
        self.health = 100
        self.mana = 100
        self.level = 1

        self.skill_rect = self.skill_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.skill_rect.x = x
        self.skill_rect.y = y-50
        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57)

        self.__vx = 1
        self.direction = 'right'
        self.prev_direction = 'right'
        self.is_animating = False
        self.skill = False

        self.following = False
        # self.__vy=5

    def animate(self):
        if self.is_animating:
            self.current_image += 0.6
            if self.current_image > 11:
                self.is_animating = False
                self.current_image = 0
            self.image = pygame.transform.scale(self.images[int(self.current_image)], (80, 80))
            self.image.set_colorkey((113, 102, 79))
        if self.skill:
            self.current_skill_image += 0.7
            if self.current_skill_image > 30:
                self.skill = False
                self.current_skill_image = 0
            self.skill_image = self.skill_images[int(self.current_skill_image)]
            self.skill_image.set_colorkey((60, 63, 65))
        if not self.is_animating and not self.skill:
            self.image=self.idle_image
        pygame.display.update()

    def update(self, enemies):
        self.is_animating = True
        self.animate()

    def blitme(self):
        (posx, posy) = self.get_pos()
        if self.direction == 'right':
            cfg.display.blit(self.image, self.get_pos())
            if self.skill:
                cfg.display.blit(self.skill_image,(posx, posy-50))
        elif self.direction == 'left':
            cfg.display.blit(pygame.transform.flip(self.image, True, False), self.get_pos())
            if self.skill:
                cfg.display.blit(self.skill_image,(posx-100, posy-50))
        if self.direction == 'up' or self.direction == 'down':
            if self.prev_direction == 'left':
                cfg.display.blit(pygame.transform.flip(self.image, True, False), self.get_pos())
                if self.skill:
                    cfg.display.blit(self.skill_image, (posx-100, posy - 50))
            if self.prev_direction == 'right':
                cfg.display.blit(self.image, self.get_pos())
                if self.skill:
                    cfg.display.blit(self.skill_image, (posx, posy - 50))

        color = (0, 128, 0)
        if self.health < 33:
            color = (255, 0, 0)
        pygame.draw.rect(cfg.display, cfg.black, (62, cfg.HEIGHT - 30, 5 * 100, 30))  # health
        pygame.draw.rect(cfg.display, color, (63, cfg.HEIGHT - 30, 5 * int(self.health) - 2, 29))  # health
        pygame.draw.rect(cfg.display, cfg.black, (62, cfg.HEIGHT - 35, 5 * 100, 5))  # mana
        pygame.draw.rect(cfg.display, cfg.blue, (63, cfg.HEIGHT - 35, 5 * int(self.mana) - 2, 4))  # mana
        pygame.draw.rect(cfg.display, cfg.black, (0, cfg.HEIGHT - 30, 62, 30))  # lvl
        level = cfg.lvl_font.render(f"LV. {self.level}", True, cfg.score_color)  # lvl
        cfg.display.blit(level, [3, cfg.HEIGHT - 30])  # lvl

    def move(self, direction, number):
        if direction == 'up' or direction == 'down':
            if not self.direction == 'up' and not self.direction == 'down':
                self.prev_direction = self.direction
                self.direction = direction
        if direction == 'right' or direction == 'left':
            self.prev_direction = self.direction
            self.direction = direction
        if direction == 'right':
            self.move_right_by(number)
        elif direction == 'left':
            self.move_left_by(number)
        elif direction == 'up':
            self.jump_by(number)
        elif direction == 'down':
            self.down_by(number)

    def update_velocity(self, vx, vy):
        self.__vx = vx
        # self__vy=vy

    def update_location(self):
        if self.direction == 'right':
            self.rect.x += self.__vx

        if self.direction == 'left':
            self.rect.x -= self.__vx

        if self.direction == 'up':
            self.rect.y -= self.__vx

        if self.direction == 'down':
            self.rect.y += self.__vx
        # self.rect.y =+ self.__vy

    def get_velocity(self):
        return self.__vx

    def get_pos(self):
        return self.rect.x, self.rect.y

    def move_right_by(self, num):
        self.rect.x = self.rect.x + num
        pygame.display.flip()

    def move_left_by(self, num):
        self.rect.x = self.rect.x - num
        pygame.display.flip()

    def jump_by(self, num):
        self.rect.y = self.rect.y - num
        pygame.display.flip()

    def down_by(self, num):
        self.rect.y = self.rect.y + num
        pygame.display.flip()

    def hit(self, bad_guys, dmg):
        for bad in bad_guys:
            if self.rect.colliderect(bad.rect) and not self.is_animating:
                self.health -= dmg
                return True
        return False
