import pygame
from src.settings import TPS


class Spike:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

        self.rect = pygame.Rect(*self.pos, *self.size)

        self.frames = []
        self.load_images()
        self.frames = [pygame.transform.scale(t, self.size) for t in self.frames]
        self.image = self.frames[10] # 150

    def load_images(self):
        tls = pygame.image.load('./resources/images/world_tileset.png').convert_alpha()
        tw, th = tls.get_size()
        for y in range(0, th, TPS):
            for x in range(0, tw, TPS):
                rect = pygame.Rect(x, y, TPS, TPS)
                ct = tls.subsurface(rect)
                self.frames.append(pygame.transform.scale(ct, self.size))

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.world_x

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
