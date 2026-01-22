"""
Tile component.

This module provides the Tile class, representing static environmental blocks
like ground and platforms.
"""
import pygame
from src.settings import TPS


class Tile:
    """
    World tile entity.

    Used for constructing the level geometry.
    """

    def __init__(self, size, pos, id):
        """
        Initialize the tile.

        Args:
            size (tuple): Size of the tile.
            pos (tuple): Position of the tile.
            id (str): Type identifier ('grass' or 'platform').
        """
        self.size = size
        self.pos = pos
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.id = id

        self.tiles = []
        self.load_images()
        self.tiles = [pygame.transform.scale(t, self.size) for t in self.tiles]
        self.image = self.tiles[self.tileHlp(self.id)]

    def tileHlp(self, id):
        """
        Helper to map tile ID to sprite index.

        Args:
            id (str): Tile type identifier.

        Returns:
            int: Index in the tiles list.
        """
        if id == 'grass':
            return 0
        if id == 'platform':
            return 1
        return 24

    def load_images(self):
        """Load the world tileset."""
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
        """
        Update tile position based on world scroll.

        Args:
            world_x (int): World scroll offset.
        """
        self.world_x = world_x
        self.rect.x -= self.world_x

    def draw(self, screen):
        """
        Draw the tile on the screen.

        Args:
            screen (pygame.Surface): Screen to draw on.
        """
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
