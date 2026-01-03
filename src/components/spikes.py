import pygame
from src.settings import TPS


class Spike:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

        self.rect = pygame.Rect(*self.pos, *self.size)
        self.tile = pygame.Rect(*self.pos, *self.size)

        self.v_y = 2
        self.d_y = 1

        self.frames = []
        self.load_images()
        self.frames = self.frameHlp(self.size, self.frames)
        self.image = self.frames[33]  # 150

        # Spike
        tls = pygame.image.load(
            './resources/images/spike.png'
        ).convert_alpha()
        ptr = tls.get_bounding_rect()
        pti = tls.subsurface(ptr)
        self.spike = pygame.transform.scale(pti, self.size)

    def frameHlp(self, size, frames):
        return [pygame.transform.scale(t, size) for t in frames]

    def load_images(self):
        tls = pygame.image.load(
            './resources/images/world_tileset.png'
        ).convert_alpha()
        tw, th = tls.get_size()
        for y in range(0, th, TPS):
            for x in range(0, tw, TPS):
                rect = pygame.Rect(x, y, TPS, TPS)
                ct = tls.subsurface(rect)
                self.frames.append(pygame.transform.scale(ct, self.size))

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.world_x
        self.tile.x -= self.world_x

        if abs(self.rect.y - self.pos[1]) // self.size[1] >= 1:
            self.d_y *= -1

        self.rect.y += self.d_y * self.v_y

    def draw(self, screen):
        screen.blit(self.spike, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.tile.x, self.tile.y))
