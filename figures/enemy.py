import time

import pygame

import cfg
import os


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, name, x, y, direction='right' ):
        super(self.__class__, self).__init__()
        self.images = []
        dir = ''
        d=''
        if name == 'anubis':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\AnubisWalking'
            d = 'AnubisWalking'
        if name == 'vampire':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\VampireWalking'
            d = 'VampireWalking'
        if name == 'black_wizard':
            dir = r'C:\Users\sagiv\PycharmProjects\lilfighter\BlackWizardWalking'
            d = 'BlackWizardWalking'
        for filename in os.listdir(dir):
            if filename.endswith('.png'):
                self.images.append(pygame.image.load(f'{d}\{filename}'))
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.name = name
        self.health = 100
        self.mana = 100
        self.type = type
        self.is_alive = True

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57)

        self.__vx = 3
        self.direction = direction
        self.prev_direction = 'right'
        self.is_animating = True
        self.following = False

    def animate(self):
        if self.is_animating == True:
            self.current_image += 0.35
            if self.current_image > 23:
                self.current_image = 0
            self.image = pygame.transform.scale(self.images[int(self.current_image)], (80, 80))


    def update(self):
        self.is_animating = True

    def stop_animate(self):
        self.is_animating = False

    def blitme(self):
        if self.direction == 'right':
            cfg.display.blit(self.image, self.get_pos())
        elif self.direction == 'left':
            cfg.display.blit(pygame.transform.flip(self.image, True, False), self.get_pos())
        if self.direction == 'up' or self.direction == 'down':
            if self.prev_direction == 'left':
                cfg.display.blit(pygame.transform.flip(self.image, True, False), self.get_pos())
            if self.prev_direction == 'right':
                cfg.display.blit(self.image, self.get_pos())
        color = (0,128,0)
        if self.health < 33:
            color=(255,0,0)
        pygame.draw.rect(cfg.display, (0,0,0), (self.hitbox[0]-26, self.hitbox[1]-10, 100, 6))
        pygame.draw.rect(cfg.display, color, (self.hitbox[0]-25, self.hitbox[1]-10, int(self.health-2), 5))

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

    def get_pos(self):
        return self.rect.x, self.rect.y

    def move(self, direction, number):
        if direction == 'up' or direction == 'down':
            if not self.direction == 'up' and not self.direction == 'down':
                self.prev_direction = self.direction
                self.direction = direction
        if direction == 'right' or direction == 'left':
            self.prev_direction = self.direction
            self.direction = direction
        if self.direction == 'right':
            self.move_right_by(number)
        elif self.direction == 'left':
            self.move_left_by(number)
        elif self.direction == 'up':
            self.jump_by(number)
        elif self.direction == 'down':
            self.down_by(number)

    def update_velocity(self, vx, vy):
        self.__vx = vx
        # self__vy=vy

    def update_location(self,character):
        if self.following:
            if character.rect.x-90 > self.rect.x:
                self.direction = 'right'
            elif character.rect.x+90<self.rect.x:
                self.direction = 'left'

        if self.direction == 'right':
            if self.rect.x + self.__vx < cfg.WIDTH - 70:
                self.rect.x += self.__vx
            else:
                self.direction = 'left'

        if self.direction == 'left':
            if self.rect.x - self.__vx > 20:
                self.rect.x -= self.__vx
            else:
                self.direction = 'right'

        if self.direction == 'up':
            if self.rect.y - self.__vx > 30:
                self.rect.y -= self.__vx
            else:
                self.direction = 'down'

        if self.direction == 'down':
            if self.rect.y - self.__vx < cfg.HEIGHT - 30:
                self.rect.y += self.__vx
            else:
                self.direction = 'up'

        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57)
        # self.rect.y =+ self.__vy

    def get_velocity(self):
        return self.__vx
    def hit(self,character, dmg):
        if self.rect.colliderect(character.rect) and (character.is_animating or character.skill):
            if character.skill:
                dmg*=2
            self.health-=dmg
            # return True
        # if self.rect.colliderect(character.skill_rect) and character.skill:
        #     self.health-=2*dmg
            return True
        return False

    def die(self, character, bad_guys):
        damage = character.level/2 # increase damage every level by 0.5
        if self.hit(character,damage):
            self.following=True
            if self.health<=0:
                self.kill()
                self.is_alive = False
                bad_guys.remove(self)

                return True
        return False
