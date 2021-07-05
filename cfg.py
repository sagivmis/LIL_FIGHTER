import pygame

# colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (59, 168, 96)
blue = (50, 153, 213)
back_color = (239, 239, 239)
score_color = (255, 209, 103)
title_color = (119, 0, 21)
red_to_ignore = (237, 28, 36)
score_font = pygame.font.SysFont("comicsansms", 35)
font_style = pygame.font.SysFont("bahnschrift", 23)
lvl_font = pygame.font.Font('Roboto-Regular.ttf', 26)

# mouse events
LEFT = 1
SCROLL = 2
RIGHT = 3

# dimensions
WIDTH = 1280
HEIGHT = 750
DIMENSIONS = (WIDTH, HEIGHT)
display = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("LILFIGHTER")

# location
x_change = 0
y_change = 0
mouse_list = []

# global vars
TILESIZE = 16

