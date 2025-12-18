import pygame

class Enemy:
    def __init__(self, size, pos):
        self.pos = [*pos]
        self.size = size
        self.rect = pygame.Rect(*self.pos, *self.size)

        self.tiles = []
        self.load_tiles()
        self.frames = []
        for f in self.tiles[4:8]:
            tr = f.get_bounding_rect()
            ti = f.subsurface(tr)
            si = pygame.transform.scale(ti, self.size)
            self.frames.append(si)

        self.kill_frames = []
        for f in self.tiles[8:12]:
            tr = f.get_bounding_rect()
            ti = f.subsurface(tr)
            si = pygame.transform.scale(ti, self.size)
            self.kill_frames.append(si)

        self.v_x = 5 # Move to settings
        self.d_x = -1
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.fracing_right = False

        self.kfi = 0
        self.kas = 0.075
        self.is_alive = True


    def load_tiles(self):
        tls = pygame.image.load('./resources/images/slime_purple.png')
        tw, th = tls.get_size()
        for y in range(0, th, 24):
            for x in range(0, tw, 24):
                rect = pygame.Rect(x, y, 24, 24)
                ct = tls.subsurface(rect)
                self.tiles.append(ct)

    def on_death(self):
        self.is_alive = False
        self.frames = self.kill_frames
        self.frame_index = self.kfi
        self.animation_speed = self.kas

    def update(self, world_x):
        self.world_x = world_x

        self.rect.x -= world_x
        self.pos[0] -= world_x

        if self.is_alive:
            self.rect.x += self.d_x*self.v_x

        if abs(self.rect.x - self.pos[0]) // self.size[0] > 2:
            self.d_x *= -1
        
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if self.d_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        """prev = self.rect.x
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
        print(self.rect.x)"""

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))



