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

        pframe = self.tiles[8]
        ptr = pframe.get_bounding_rect()
        pti = pframe.subsurface(ptr)
        self.player_frame = pygame.transform.scale(pti, self.size)

        self.kill_frames = []
        __t = self.tiles[:5]
        _temp = [self.tiles[10] for _ in range(2)] + __t[::-1] + [self.tiles[0] for _ in range(5)] # self.tiles[8:12]
        for f in _temp:
            # tr = f.get_bounding_rect()
            # ti = f.subsurface(tr)
            # si = pygame.transform.scale(ti, self.size)
            #
            # si = pygame.transform.scale(f, self.size)
            #
            si = pygame.transform.scale(f, (2*self.size[0], 2*self.size[1]))
            self.kill_frames.append(si)

        self.v_x = 5 # Move to settings
        self.d_x = -1
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]
        self.fracing_right = False

        self.kfi = 0
        self.kas = 0.15
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

    def update(self, world_x, tiles):
        pff = self.image == self.player_frame
        cf = False # Collide flag
        self.world_x = world_x


        self.rect.x -= world_x
        self.pos[0] -= world_x

        prev = self.rect.x
        if self.is_alive:
            self.rect.x += self.d_x*self.v_x

        for tile in tiles:
            if self.rect.colliderect(tile):
                cf = True
                if prev > self.rect.x:
                    self.rect.left = tile.rect.right
                elif prev < self.rect.x:
                    self.rect.right = tile.rect.left 

        # Check if walking on air
        af = False
        self.rect.y += 40
        self.rect.x = self.rect.x + self.d_x*80
        for tile in tiles:
            if self.rect.colliderect(tile):
                af = True
        self.rect.x = self.rect.x - self.d_x*80
        self.rect.y -= 40


        # if abs(self.rect.x - self.pos[0]) // self.size[0] > 2 or 
        if cf or not af:
            self.d_x *= -1
        
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

        if pff:
            self.image = self.player_frame
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

    def draw(self, screen, font):
        if not self.is_alive:
            plus_text = font.render("+10", False, 'black')
            screen.blit(plus_text, (self.rect.x, self.rect.y - 40 - int(self.frame_index)*5))
            screen.blit(self.image, (self.rect.x - self.size[0]//2, self.rect.y - self.size[1]))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))



