import pygame
from src.settings import SCREEN_SIZE


class Cloud:
    def __init__(self, size, pos, delay):
        self.size = size
        self.pos = pos

        self.v_x = 2

        self.v_y = 1
        self.d_y = 1
        self.delay = delay
        self.delayed_frame = 0
        print(delay)
        
        self.rect = pygame.Rect(*self.pos, *self.size)

        img = pygame.image.load('./resources/images/cloud.png').convert_alpha()
        self.image = pygame.transform.scale(img, self.size)

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.v_x
        self.rect.x -= self.world_x // 2

        if self.delayed_frame % 3:
            self.rect.y += self.d_y * self.v_y
        self.delayed_frame += 1

        if self.delayed_frame % self.delay == 0 and abs(self.rect.y - self.pos[1]) // (self.size[1]//16) > 1:
            self.d_y *= -1

        if self.rect.right <= 0:
            self.rect.left = SCREEN_SIZE[0]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
