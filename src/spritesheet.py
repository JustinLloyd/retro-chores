import pygame
import json


class Spritesheet:
    def __init__(self, spritesheet_name):
        self.spritesheet_name = spritesheet_name
        with open(self.spritesheet_name + '.json') as f:
            data = json.load(f)
        f.close()
        self.meta_data = data['meta']
        self.frames = data['frames']
        print(self.meta_data['image'])
        self.image = pygame.image.load('./assets/' + self.meta_data['image']).convert()

    def get_by_pos(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey(((0, 0, 0)))
        sprite.blit(self.image, (0, 0), (x, y, w, h))
        return sprite

    def get_by_name(self, name):
        sprite = self.frames[name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_by_pos(x, y, w, h)
        return image
