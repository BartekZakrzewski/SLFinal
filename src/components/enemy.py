import pygame

class Enemy:
    def __init__(self, size, pos):
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(*self.pos, *self.size)

        self.tiles = []
        self.load_tiles()
        self.frames = []
        self.kill_frame = []
        for f in self.tiles[:10]:
            tr = f.get_bounding_rect()
            ti = f.subsurface(tr)
            si = pygame.transform.scale(ti, self.size)
            self.frames.append(si)

        self.v_x = 10 # Move to settings
        self.d_x = 1
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.fracing_right = False


    def load_tiles(self):
        tls = pygame.image.load('./resources/images/slime_purple.png')
        tw, th = tls.get_size()
        for y in range(0, th, 24):
            for x in range(0, tw, 24):
                rect = pygame.Rect(x, y, 24, 24)
                ct = tls.subsurface(rect)
                self.tiles.append(ct)


    def update(self, world_x, tiles):
        self.rect.x -= world_x
        
        prev = self.rect.x
        self.rect.x += self.d_x * self.v_x
        print(self.rect.x)

        ff = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                ff = True
                if prev < self.rect.x:
                    self.rect.right = tile.rect.left
                if prev > self.rect.x:
                    self.rect.left = tile.rect.right

        if not ff:
            self.rect.x = prev
            self.d_x *= -1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))



