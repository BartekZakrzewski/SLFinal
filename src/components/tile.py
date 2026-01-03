import pygame
from src.settings import TPS


class Tile:
    def __init__(self, size, pos, id):
        self.size = size
        self.pos = pos
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.id = id

        self.tiles = []
        self.load_images()
        self.tiles = [pygame.transform.scale(t, self.size) for t in self.tiles]
        self.image = self.tiles[self.tileHlp(self.id)]

    def tileHlp(self, id):
        if id == 'grass':
            return 0
        if id == 'platform':
            return 1
        return 24

    def load_images(self):
        tls = pygame.image.load(
            './resources/images/world_tileset.png'
        ).convert_alpha()
        tw, th = tls.get_size()
        for y in range(0, th, TPS):
            for x in range(0, tw, TPS):
                rect = pygame.Rect(x, y, TPS, TPS)
                ct = tls.subsurface(rect)
                self.tiles.append(ct)

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.world_x

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        """
        # DEBUG set corners variables
        bpx = self.rect.x
        bpy = self.rect.y
        bs = 8
        w = self.size[0]
        h = self.size[1]
        # DEBUG Draw corners
        ctl = pygame.Rect(bpx, bpy, bs, bs)
        ctr = pygame.Rect(bpx + w - bs, bpy, bs, bs)
        cbl = pygame.Rect(bpx, bpy + h - bs, bs, bs)
        cbr = pygame.Rect(bpx + w - bs, bpy + h - bs, bs, bs)
        pygame.draw.rect(screen, 'black', ctl)
        pygame.draw.rect(screen, 'black', ctr)
        pygame.draw.rect(screen, 'black', cbl)
        pygame.draw.rect(screen, 'black', cbr)
        """
