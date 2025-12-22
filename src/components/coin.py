import pygame


class Coin:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

        self.rect = pygame.Rect(*self.pos, *self.size)

        self.frames = []
        self.load_images()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]

        self.scale_speed = 0.0375
        self.scale = 1
        self.v_y = 2
        self.is_alive = True

    def load_images(self):
        tls = pygame.image.load('./resources/images/coin.png').convert_alpha()
        tw, th = tls.get_size()
        for y in range(0, th, 16):
            for x in range(0, tw, 16):
                rect = pygame.Rect(x, y, 16, 16)
                ct = tls.subsurface(rect)
                self.frames.append(pygame.transform.scale(ct, self.size))

    def on_death(self):
        self.is_alive = False
        _frames = []
        for f in self.frames:
            df = pygame.transform.scale(f, (self.size[0]*self.scale, self.size[1]*self.scale))
            self.scale += self.scale_speed
            _frames.append(df)
        self.frames = _frames
        self.frame_index = 0
        self.animation_speed = 0.25

    def update(self, world_x):
        self.world_x = world_x
        self.rect.x -= self.world_x
        
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index) % 12]

        if not self.is_alive:
            self.rect.y -= self.v_y

    def draw(self, screen, font):
        imgw = 0
        if not self.is_alive:
            imgw, _ = self.image.get_size()
            plus_text = font.render("+10", False, 'black')
            screen.blit(plus_text, (self.rect.x, self.rect.y - 40 - int(self.frame_index) * 5))
        screen.blit(self.image, (self.rect.x - imgw // 8, self.rect.y))
