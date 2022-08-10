# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com


from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys

import pygame
import os

from pygame.locals import *
from spritesheet import *

max_columns = 20
max_ranks = 12
max_strips = 2

horizontal_offset = 14
vertical_offset = 24
character_stride = 54
strip_stride = 88
rank_stride = 154
pi = False
lcd: pygame.Surface
cell_size = None
cell_off = None

displayinfo = None
character_lookup = None


def clear_rank(rank):
    global displayinfo
    global lcd
    global horizontal_offset
    global vertical_offset
    global strip_stride
    global cell_off
    x, y = get_cell_pos(rank, 0, 0)
    pygame.draw.rect(lcd, (0, 0, 0), (x - horizontal_offset, y - vertical_offset, displayinfo.current_w + horizontal_offset, strip_stride * 2 + vertical_offset))
    for strip in range(2):
        for cell in range(max_columns):
            x, y = get_cell_pos(rank, strip, cell)
            lcd.blit(cell_off, (x, y))


def clear_screen():
    global lcd
    lcd.fill((0, 0, 0))
    for rank in range(12):
        clear_rank(rank)
    flush()


def flush():
    pygame.display.update()


def resize(img):
    w = img.get_width()
    h = img.get_height()
    return pygame.transform.scale(img, (w / 2, h / 2))


def get_cell_pos(rank, strip, cell):
    global horizontal_offset
    global vertical_offset
    global rank_stride
    global strip_stride
    global character_stride
    return horizontal_offset + cell * character_stride, vertical_offset + rank * (rank_stride + strip_stride * 2) + strip * strip_stride


def step_forward(cell, strip):
    global max_columns
    cell += 1
    if cell >= max_columns:
        return newline(strip)
    return cell, strip


def newline(strip):
    strip += 1
    return 0, strip


def vfd_echo_char(ch: object, rank: int, strip: int, cell: int):
    global character_lookup
    global lcd

    img = character_lookup[ch]['img']
    char_x = character_lookup[ch]['x']
    char_y = character_lookup[ch]['y']
    cell_x, cell_y = get_cell_pos(rank, strip, cell)
    if char_x == 0 and char_y == 0:
        cell_x += cell_size[0] / 2 - img.get_width() / 2
        cell_y += cell_size[1] / 2 - img.get_height() / 2
    else:
        cell_x += char_x
        cell_y += char_y

    lcd.blit(img, (int(cell_x), int(cell_y)))


def vfd_print(msg, rank):
    strip = 0
    cell = 0
    for c in msg:
        if c == '\n':
            cell, strip = newline(strip)
            continue

        if c == ' ':
            cell, strip = step_forward(cell, strip)
            continue

        vfd_echo_char(c, rank, strip, cell)
        cell, strip = step_forward(cell, strip)


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


def init():
    global lcd
    global displayinfo
    global pi
    os.putenv('SDL_FBDEV', '/dev/fb0')
    pygame.init()
    displayinfo = pygame.display.Info()
    print(f"Display size = {displayinfo.current_w}x{displayinfo.current_h}")
    if displayinfo.current_w == 1100:
        lcd = pygame.display.set_mode((1100, 3840))
        pi = True
    else:
        lcd = pygame.display.set_mode((550, 1920))


def load_assets():
    global cell_off
    global character_lookup
    global cell_size
    global pi
    global horizontal_offset
    global vertical_offset
    global character_stride
    global strip_stride
    global rank_stride

    spritesheet = Spritesheet("./assets/sprite-sheet")
    cell_off = spritesheet.get_by_name('vfd-cell-off')
    # upper case letters
    # letter_uppercase_a = pygame.image.load("./assets/letter-uppercase-a.png")
    # letter_uppercase_b = pygame.image.load("./assets/letter-uppercase-b.png")
    # letter_uppercase_c = pygame.image.load("./assets/letter-uppercase-c.png")
    # letter_uppercase_d = pygame.image.load("./assets/letter-uppercase-d.png")
    # letter_uppercase_e = pygame.image.load("./assets/letter-uppercase-e.png")
    # letter_uppercase_f = pygame.image.load("./assets/letter-uppercase-f.png")
    # letter_uppercase_g = pygame.image.load("./assets/letter-uppercase-g.png")
    # letter_uppercase_h = pygame.image.load("./assets/letter-uppercase-h.png")
    # letter_uppercase_i = pygame.image.load("./assets/letter-uppercase-i.png")
    # letter_uppercase_j = pygame.image.load("./assets/letter-uppercase-j.png")
    # letter_uppercase_k = pygame.image.load("./assets/letter-uppercase-k.png")
    # letter_uppercase_l = pygame.image.load("./assets/letter-uppercase-l.png")
    # letter_uppercase_m = pygame.image.load("./assets/letter-uppercase-m.png")
    # letter_uppercase_n = pygame.image.load("./assets/letter-uppercase-n.png")
    # letter_uppercase_o = pygame.image.load("./assets/letter-uppercase-o.png")
    # letter_uppercase_p = pygame.image.load("./assets/letter-uppercase-p.png")
    # letter_uppercase_q = pygame.image.load("./assets/letter-uppercase-q.png")
    # letter_uppercase_r = pygame.image.load("./assets/letter-uppercase-r.png")
    # letter_uppercase_s = pygame.image.load("./assets/letter-uppercase-s.png")
    # letter_uppercase_t = pygame.image.load("./assets/letter-uppercase-t.png")
    # letter_uppercase_u = pygame.image.load("./assets/letter-uppercase-u.png")
    # letter_uppercase_v = pygame.image.load("./assets/letter-uppercase-v.png")
    # letter_uppercase_w = pygame.image.load("./assets/letter-uppercase-w.png")
    # letter_uppercase_x = pygame.image.load("./assets/letter-uppercase-x.png")
    # letter_uppercase_y = pygame.image.load("./assets/letter-uppercase-y.png")
    # letter_uppercase_z = pygame.image.load("./assets/letter-uppercase-z.png")
    #
    # # numbers
    # number_0 = pygame.image.load("./assets/number-0.png")
    # number_1 = pygame.image.load("./assets/number-2.png")
    # number_2 = pygame.image.load("./assets/number-2.png")
    # number_3 = pygame.image.load("./assets/number-3.png")
    # number_4 = pygame.image.load("./assets/number-4.png")
    # number_5 = pygame.image.load("./assets/number-5.png")
    # number_6 = pygame.image.load("./assets/number-6.png")
    # number_7 = pygame.image.load("./assets/number-7.png")
    # number_8 = pygame.image.load("./assets/number-8.png")
    # number_9 = pygame.image.load("./assets/number-9.png")
    #
    # symbol_minus = pygame.image.load("./assets/symbol-minus.png")
    # symbol_plus = pygame.image.load("./assets/symbol-plus.png")
    # symbol_at = pygame.image.load("./assets/symbol-at.png")
    # symbol_dollar = pygame.image.load("./assets/symbol-dollar.png")
    # symbol_slash = pygame.image.load("./assets/symbol-slash.png")
    # symbol_bang = pygame.image.load("./assets/symbol-bang.png")
    # symbol_hash = pygame.image.load("./assets/symbol-hash.png")
    # symbol_percentage = pygame.image.load("./assets/symbol-percentage.png")

    character_lookup = {
        # '.': {'img': None, 'x': 0, 'y': 0},
        # ',': {'img': None, 'x': 0, 'y': 0},
        # ';': {'img': None, 'x': 0, 'y': 0},
        # '\'': {'img': None, 'x': 0, 'y': 0},
        # '-': {'img': None, 'x': 0, 'y': 0},
        'A': {'img': spritesheet.get_by_name("letter-uppercase-a"), 'x': 0, 'y': 0},
        'B': {'img': spritesheet.get_by_name("letter-uppercase-b"), 'x': 0, 'y': 0},
        'C': {'img': spritesheet.get_by_name("letter-uppercase-c"), 'x': 0, 'y': 0},
        'D': {'img': spritesheet.get_by_name("letter-uppercase-d"), 'x': 0, 'y': 0},
        'E': {'img': spritesheet.get_by_name("letter-uppercase-e"), 'x': 0, 'y': 0},
        'F': {'img': spritesheet.get_by_name("letter-uppercase-f"), 'x': 0, 'y': 0},
        'G': {'img': spritesheet.get_by_name("letter-uppercase-g"), 'x': 0, 'y': 0},
        'H': {'img': spritesheet.get_by_name("letter-uppercase-h"), 'x': 0, 'y': 0},
        'I': {'img': spritesheet.get_by_name("letter-uppercase-i"), 'x': 0, 'y': 0},
        'J': {'img': spritesheet.get_by_name("letter-uppercase-j"), 'x': 0, 'y': 0},
        'K': {'img': spritesheet.get_by_name("letter-uppercase-k"), 'x': 0, 'y': 0},
        'L': {'img': spritesheet.get_by_name("letter-uppercase-l"), 'x': 0, 'y': 0},
        'M': {'img': spritesheet.get_by_name("letter-uppercase-m"), 'x': 0, 'y': 0},
        'N': {'img': spritesheet.get_by_name("letter-uppercase-n"), 'x': 0, 'y': 0},
        'O': {'img': spritesheet.get_by_name("letter-uppercase-o"), 'x': 0, 'y': 0},
        'P': {'img': spritesheet.get_by_name("letter-uppercase-p"), 'x': 0, 'y': 0},
        'Q': {'img': spritesheet.get_by_name("letter-uppercase-q"), 'x': 0, 'y': 0},
        'R': {'img': spritesheet.get_by_name("letter-uppercase-r"), 'x': 0, 'y': 0},
        'S': {'img': spritesheet.get_by_name("letter-uppercase-s"), 'x': 0, 'y': 0},
        'T': {'img': spritesheet.get_by_name("letter-uppercase-t"), 'x': 0, 'y': 0},
        'U': {'img': spritesheet.get_by_name("letter-uppercase-u"), 'x': 0, 'y': 0},
        'V': {'img': spritesheet.get_by_name("letter-uppercase-v"), 'x': 0, 'y': 0},
        'W': {'img': spritesheet.get_by_name("letter-uppercase-w"), 'x': 0, 'y': 0},
        'X': {'img': spritesheet.get_by_name("letter-uppercase-x"), 'x': 0, 'y': 0},
        'Y': {'img': spritesheet.get_by_name("letter-uppercase-y"), 'x': 0, 'y': 0},
        'Z': {'img': spritesheet.get_by_name("letter-uppercase-z"), 'x': 0, 'y': 0},
        '0': {'img': spritesheet.get_by_name("number-0"), 'x': 0, 'y': 0},
        '1': {'img': spritesheet.get_by_name("number-1"), 'x': 0, 'y': 0},
        '2': {'img': spritesheet.get_by_name("number-2"), 'x': 0, 'y': 0},
        '3': {'img': spritesheet.get_by_name("number-3"), 'x': 0, 'y': 0},
        '4': {'img': spritesheet.get_by_name("number-4"), 'x': 0, 'y': 0},
        '5': {'img': spritesheet.get_by_name("number-5"), 'x': 0, 'y': 0},
        '6': {'img': spritesheet.get_by_name("number-6"), 'x': 0, 'y': 0},
        '7': {'img': spritesheet.get_by_name("number-7"), 'x': 0, 'y': 0},
        '8': {'img': spritesheet.get_by_name("number-8"), 'x': 0, 'y': 0},
        '9': {'img': spritesheet.get_by_name("number-9"), 'x': 0, 'y': 0},
        '-': {'img': spritesheet.get_by_name("symbol-minus"), 'x': 0, 'y': 0},
        '+': {'img': spritesheet.get_by_name("symbol-plus"), 'x': 0, 'y': 0},
        '@': {'img': spritesheet.get_by_name("symbol-at"), 'x': 0, 'y': 0},
        '$': {'img': spritesheet.get_by_name("symbol-dollar"), 'x': 0, 'y': 0},
        '/': {'img': spritesheet.get_by_name("symbol-slash"), 'x': 0, 'y': 0},
        '!': {'img': spritesheet.get_by_name("symbol-bang"), 'x': 0, 'y': 0},
        '#': {'img': spritesheet.get_by_name("symbol-hash"), 'x': 0, 'y': 0},
        '%': {'img': spritesheet.get_by_name("symbol-percentage"), 'x': 0, 'y': 0},
    }

    if not pi:
        print("Not a raspberry pi")
        cell_off = resize(cell_off)
        for character in character_lookup:
            character_lookup[character]['img'] = resize(character_lookup[character]['img'])
            character_lookup[character]['x'] /= 2
            character_lookup[character]['y'] /= 2

        horizontal_offset /= 2
        vertical_offset /= 2
        character_stride /= 2
        strip_stride /= 2
        rank_stride /= 2
    else:
        print("Running on the raspberry pi")

    cell_size = cell_off.get_size()


init()
load_assets()
clear_screen()

vfd_print('CLEAN DOWNSTAIRS\nCAT LITTER', 0)
vfd_print('CLEAN UPSTAIRS\nCAT LITTER', 1)
vfd_print('WATER BASIL PLANTS', 2)
vfd_print('WATER ROSEMARY PLANT', 3)
vfd_print('ADVANCE LAUNDRY', 4)
vfd_print('EMPTY DISHWASHER', 5)
vfd_print('LOAD DISHWASHER', 6)
vfd_print('EMPTY RECYCLING BIN', 7)
vfd_print('WASH MICROWAVE', 8)
vfd_print('CHANGE BED LINENS', 9)

flush()
wait()
pygame.display.quit()
pygame.quit()
exit()
