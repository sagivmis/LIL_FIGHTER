import pygame
import time
import random
import math

pygame.init()

from figures.character import Character
from figures.enemy import Enemy
import cfg

clock = pygame.time.Clock()


def score(score):
    value = cfg.score_font.render(f"Defeated: {score}", True, cfg.score_color)
    cfg.display.blit(value, [5, 0])
    v = cfg.score_font.render(f"LIL FIGHTER", True, cfg.title_color)
    cfg.display.blit(v, [cfg.WIDTH / 2.4, 50])
    # w = cfg.score_font.render(f"Wins: {wins}", True, cfg.green)
    # cfg.display.blit(w, [670, 0])


def generate_enemies(size):
    # enemies = pygame.sprite.Group()
    enemies = []
    for i in range(size):
        if i % 2 == 0:
            dir = 'right'
        else:
            dir = 'left'

        if i % 3 == 0:
            name = 'anubis'
        elif i % 3 == 1:
            name = 'vampire'
        else:
            name = 'black_wizard'
        enemies.append(Enemy('water', name=name, x=random.randrange(0, cfg.WIDTH - 80), y=600, direction=dir))
    return enemies


def generate_character():
    character = pygame.sprite.Group()
    character.add(Character("sagiv", 100, 600))
    return character


all_figures = pygame.sprite.Group()



def show_character(char):
    cfg.display.blit(char.image, char.get_pos())


def blit_all(figures):
    for fig in figures:
        fig.blitme()


def blit_bad_guys(bad_guys,character):
    for bad in bad_guys:
        if bad.is_alive:
            bad.update_location(character)
            bad.blitme()

def choose_character():
    cfg.display.fill(cfg.black)
    value = cfg.lvl_font.render(f'Choose your character', True, cfg.score_color)
    char = None
    while not char:
        knight = pygame.image.load('MedievalSlashing/idle/Idle_000.png')
        ninja = pygame.image.load('NinjaSlashing/idle/Idle_000.png')
        thug = pygame.image.load('ThugSlashing/idle/Idle_000.png')
        cfg.display.blit(value, [cfg.WIDTH / 2-120, cfg.HEIGHT / 2-100])
        cfg.display.blit(knight, [cfg.WIDTH/1.67-30, cfg.HEIGHT/2+100])
        cfg.display.blit(cfg.lvl_font.render('Knight - k',True,cfg.score_color), [cfg.WIDTH/1.67-40,cfg.HEIGHT/2+50])
        cfg.display.blit(ninja, [cfg.WIDTH/2-30, cfg.HEIGHT/2+100])
        cfg.display.blit(cfg.lvl_font.render('Ninja - n',True,cfg.score_color), [cfg.WIDTH/2-40,cfg.HEIGHT/2+50])
        cfg.display.blit(thug, [cfg.WIDTH/2.5-30, cfg.HEIGHT/2+100])
        cfg.display.blit(cfg.lvl_font.render('Thug - t',True,cfg.score_color), [cfg.WIDTH/2.5-40,cfg.HEIGHT/2+50])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    char='knight'
                if event.key == pygame.K_n:
                    char='ninja'
                if event.key == pygame.K_t:
                    char='thug'
        pygame.display.flip()
    return char



def game():
    game_esc = False
    character_name = choose_character()
    my_first_char = Character(character_name, 100, 600)
    game_on = True
    num_of_enemies = 5
    bad_guys = generate_enemies(num_of_enemies)

    my_score = 0
    while game_on:
        while game_esc:
            character_name = choose_character()
            game_esc = False
            my_first_char = Character(character_name,100,600)
        if len(bad_guys) == 0:
            num_of_enemies += 5
            bad_guys = generate_enemies(num_of_enemies)
            my_first_char.level+=1
        background = pygame.image.load('beach.png')
        cfg.display.blit(background, (0, 0))
        score(my_score)
        my_first_char.blitme()
        blit_bad_guys(bad_guys, my_first_char)
        my_first_char.animate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    my_first_char.move('left', 45)
                if event.key == pygame.K_RIGHT:
                    my_first_char.move('right', 45)
                if event.key == pygame.K_UP:
                    my_first_char.move('up', 45)
                if event.key == pygame.K_DOWN:
                    my_first_char.move('down', 45)
                if event.key == pygame.K_c:
                    my_first_char.update(bad_guys)
                if event.key == pygame.K_a:
                    if my_first_char.level>0:
                        my_first_char.skill = True
                        my_first_char.animate()
                if event.key == pygame.K_ESCAPE:
                    game_esc = True


        for baddie in bad_guys:
            baddie.animate()
            if baddie.is_alive:
                if baddie.die(my_first_char, bad_guys):
                    my_score += 1
                    print(score)

        clock.tick(30)
        pygame.display.flip()

    pygame.quit()
    quit()

game()