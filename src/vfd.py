import pygame

from src.spritesheet import Spritesheet
from src.util import is_raspberrypi


class VFD:
    def __init__(self):
        self.max_columns = 20
        self.max_ranks = 12
        self.max_strips = 2
        self.horizontal_offset = 14
        self.vertical_offset = 24
        self.character_stride = 54
        self.strip_stride = 88
        self.rank_stride = 154
        self.cell_size = None
        self.cell_off = None
        self.displayinfo = None
        self.character_lookup = None
        self.spritesheet = None
        self.displayinfo = None
        self.displayinfo = pygame.display.Info()
        print(f"Display size = {self.displayinfo.current_w}x{self.displayinfo.current_h}")
        if is_raspberrypi():
            self.lcd = pygame.display.set_mode((1100, 3840))
        else:
            self.lcd = pygame.display.set_mode((550, 1920))

    def clr(self, rank):
        # global displayinfo
        # global lcd
        # global horizontal_offset
        # global vertical_offset
        # global strip_stride
        # global cell_off
        x, y = self.get_cell_pos(rank, 0, 0)
        pygame.draw.rect(self.lcd, (0, 0, 0), (x - self.horizontal_offset, y - self.vertical_offset, self.displayinfo.current_w + self.horizontal_offset, self.strip_stride * 2 + self.vertical_offset))
        for strip in range(2):
            for cell in range(self.max_columns):
                x, y = self.get_cell_pos(rank, strip, cell)
                self.lcd.blit(self.cell_off, (x, y))

    def cls(self):
        self.lcd.fill((0, 0, 0))
        for rank in range(12):
            self.clr(rank)
        self.flush()

    @staticmethod
    def flush():
        pygame.display.update()

    @staticmethod
    def resize(img):
        w = img.get_width()
        h = img.get_height()
        return pygame.transform.scale(img, (w / 2, h / 2))

    def get_cell_pos(self, rank, strip, cell):
        return self.horizontal_offset + cell * self.character_stride, self.vertical_offset + rank * (self.rank_stride + self.strip_stride * 2) + strip * self.strip_stride

    def step_forward(self, cell, strip):
        cell += 1
        if cell >= self.max_columns:
            return self.newline(strip)
        return cell, strip

    @staticmethod
    def newline(strip):
        strip += 1
        return 0, strip

    def echo_char(self, ch: object, rank: int, strip: int, cell: int):
        img = self.character_lookup[ch]['img']
        char_x = self.character_lookup[ch]['x']
        char_y = self.character_lookup[ch]['y']
        cell_x, cell_y = self.get_cell_pos(rank, strip, cell)
        if char_x == 0 and char_y == 0:
            cell_x += self.cell_size[0] / 2 - img.get_width() / 2
            cell_y += self.cell_size[1] / 2 - img.get_height() / 2
        else:
            cell_x += char_x
            cell_y += char_y

        self.lcd.blit(img, (int(cell_x), int(cell_y)))

    def print(self, msg, rank):
        strip = 0
        cell = 0
        for c in msg:
            if c == '\n':
                cell, strip = self.newline(strip)
                continue

            if c == ' ':
                cell, strip = self.step_forward(cell, strip)
                continue

            self.echo_char(c, rank, strip, cell)
            cell, strip = self.step_forward(cell, strip)

    def load_assets(self):
        self.spritesheet = Spritesheet("./assets/sprite-sheet")
        self.cell_off = self.spritesheet.get_by_name('vfd-cell-off')
        self.character_lookup = {
            # '.': {'img': None, 'x': 0, 'y': 0},
            # ',': {'img': None, 'x': 0, 'y': 0},
            # ';': {'img': None, 'x': 0, 'y': 0},
            # '\'': {'img': None, 'x': 0, 'y': 0},
            # '-': {'img': None, 'x': 0, 'y': 0},
            'A': {'img': self.spritesheet.get_by_name("letter-uppercase-a"), 'x': 0, 'y': 0},
            'B': {'img': self.spritesheet.get_by_name("letter-uppercase-b"), 'x': 0, 'y': 0},
            'C': {'img': self.spritesheet.get_by_name("letter-uppercase-c"), 'x': 0, 'y': 0},
            'D': {'img': self.spritesheet.get_by_name("letter-uppercase-d"), 'x': 0, 'y': 0},
            'E': {'img': self.spritesheet.get_by_name("letter-uppercase-e"), 'x': 0, 'y': 0},
            'F': {'img': self.spritesheet.get_by_name("letter-uppercase-f"), 'x': 0, 'y': 0},
            'G': {'img': self.spritesheet.get_by_name("letter-uppercase-g"), 'x': 0, 'y': 0},
            'H': {'img': self.spritesheet.get_by_name("letter-uppercase-h"), 'x': 0, 'y': 0},
            'I': {'img': self.spritesheet.get_by_name("letter-uppercase-i"), 'x': 0, 'y': 0},
            'J': {'img': self.spritesheet.get_by_name("letter-uppercase-j"), 'x': 0, 'y': 0},
            'K': {'img': self.spritesheet.get_by_name("letter-uppercase-k"), 'x': 0, 'y': 0},
            'L': {'img': self.spritesheet.get_by_name("letter-uppercase-l"), 'x': 0, 'y': 0},
            'M': {'img': self.spritesheet.get_by_name("letter-uppercase-m"), 'x': 0, 'y': 0},
            'N': {'img': self.spritesheet.get_by_name("letter-uppercase-n"), 'x': 0, 'y': 0},
            'O': {'img': self.spritesheet.get_by_name("letter-uppercase-o"), 'x': 0, 'y': 0},
            'P': {'img': self.spritesheet.get_by_name("letter-uppercase-p"), 'x': 0, 'y': 0},
            'Q': {'img': self.spritesheet.get_by_name("letter-uppercase-q"), 'x': 0, 'y': 0},
            'R': {'img': self.spritesheet.get_by_name("letter-uppercase-r"), 'x': 0, 'y': 0},
            'S': {'img': self.spritesheet.get_by_name("letter-uppercase-s"), 'x': 0, 'y': 0},
            'T': {'img': self.spritesheet.get_by_name("letter-uppercase-t"), 'x': 0, 'y': 0},
            'U': {'img': self.spritesheet.get_by_name("letter-uppercase-u"), 'x': 0, 'y': 0},
            'V': {'img': self.spritesheet.get_by_name("letter-uppercase-v"), 'x': 0, 'y': 0},
            'W': {'img': self.spritesheet.get_by_name("letter-uppercase-w"), 'x': 0, 'y': 0},
            'X': {'img': self.spritesheet.get_by_name("letter-uppercase-x"), 'x': 0, 'y': 0},
            'Y': {'img': self.spritesheet.get_by_name("letter-uppercase-y"), 'x': 0, 'y': 0},
            'Z': {'img': self.spritesheet.get_by_name("letter-uppercase-z"), 'x': 0, 'y': 0},
            '0': {'img': self.spritesheet.get_by_name("number-0"), 'x': 0, 'y': 0},
            '1': {'img': self.spritesheet.get_by_name("number-1"), 'x': 0, 'y': 0},
            '2': {'img': self.spritesheet.get_by_name("number-2"), 'x': 0, 'y': 0},
            '3': {'img': self.spritesheet.get_by_name("number-3"), 'x': 0, 'y': 0},
            '4': {'img': self.spritesheet.get_by_name("number-4"), 'x': 0, 'y': 0},
            '5': {'img': self.spritesheet.get_by_name("number-5"), 'x': 0, 'y': 0},
            '6': {'img': self.spritesheet.get_by_name("number-6"), 'x': 0, 'y': 0},
            '7': {'img': self.spritesheet.get_by_name("number-7"), 'x': 0, 'y': 0},
            '8': {'img': self.spritesheet.get_by_name("number-8"), 'x': 0, 'y': 0},
            '9': {'img': self.spritesheet.get_by_name("number-9"), 'x': 0, 'y': 0},
            '-': {'img': self.spritesheet.get_by_name("symbol-minus"), 'x': 0, 'y': 0},
            '+': {'img': self.spritesheet.get_by_name("symbol-plus"), 'x': 0, 'y': 0},
            '@': {'img': self.spritesheet.get_by_name("symbol-at"), 'x': 0, 'y': 0},
            '$': {'img': self.spritesheet.get_by_name("symbol-dollar"), 'x': 0, 'y': 0},
            '/': {'img': self.spritesheet.get_by_name("symbol-slash"), 'x': 0, 'y': 0},
            '!': {'img': self.spritesheet.get_by_name("symbol-bang"), 'x': 0, 'y': 0},
            '#': {'img': self.spritesheet.get_by_name("symbol-hash"), 'x': 0, 'y': 0},
            '%': {'img': self.spritesheet.get_by_name("symbol-percentage"), 'x': 0, 'y': 0},
        }

        if not is_raspberrypi():
            self.cell_off = self.resize(self.cell_off)
            for character in self.character_lookup:
                self.character_lookup[character]['img'] = self.resize(self.character_lookup[character]['img'])
                self.character_lookup[character]['x'] /= 2
                self.character_lookup[character]['y'] /= 2

            self.horizontal_offset /= 2
            self.vertical_offset /= 2
            self.character_stride /= 2
            self.strip_stride /= 2
            self.rank_stride /= 2

        self.cell_size = self.cell_off.get_size()
