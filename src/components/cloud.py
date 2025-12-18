import pygame
from src.settings import SCREEN_SIZE


class Cloud:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

        self.v_x = 2
        
        self.rect = pygame.Rect(*self.pos, *self.size)

        img = pygame.image.load('./resources/images/cloud.png').convert_alpha()
        self.image = pygame.transform.scale(img, self.size)

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.v_x
        self.rect.x -= self.world_x // 2
        if self.rect.right <= 0:
            self.rect.left = SCREEN_SIZE[0]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
