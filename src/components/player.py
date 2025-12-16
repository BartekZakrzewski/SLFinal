import pygame
from src.settings import PLAYER_SIZE, PLAYER_POS, V_X, V_Y, PLAYER_ANIMATION_SPEED, PTS, SCREEN_SIZE, PLAYER_RBP, PLAYER_LBP, PLAYER_JUMP_OFFSET

# TODO Create settings with screen size
class Player:
    def __init__(self, screen):
        self.screen = screen
        self.size = PLAYER_SIZE
        self.start_pos = PLAYER_POS
        self.rect = pygame.Rect(*self.start_pos, *self.size)

        self.surface = pygame.Surface(self.size)
        self.image = pygame.image.load('./resources/images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.tiles = []
        self.load_tiles()
        self.run_frames = [pygame.transform.scale(self.tiles[0], self.size), pygame.transform.scale(self.tiles[1], self.size)]
        self.run_frames = []
        for of in self.tiles[:2]:
            tr = of.get_bounding_rect()
            ti = of.subsurface(tr)
            si = pygame.transform.scale(ti, self.size)
            self.run_frames.append(si)

        self.on_ground = True

        self.v_y = 0
        self.d_y = 1

        self.v_x = V_X
        print(self.v_x, V_X)

        self.world_x = 0
        self.frame_index = 0
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.image = self.run_frames[0] 
        self.facing_right = True

    def load_tiles(self):
        tileset = pygame.image.load('./resources/images/knight.png')
        tw, th = tileset.get_size()
        for y in range(0, th, PTS):
            for x in range(0, tw, PTS):
                rect = pygame.Rect(x, y, PTS, PTS)
                ct = tileset.subsurface(rect)
                self.tiles.append(ct)

    def update(self, keys, tiles):
        # Movement
        prev = self.rect.x
        moving = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            # Move right
            self.rect.x += self.v_x

            # Animation right
            self.facing_right = True
            moving = True
            self.frame_index += self.animation_speed
            if self.on_ground:
                self.image = self.run_frames[int(self.frame_index) % 2]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            # Move left
            self.rect.x -= self.v_x

            # Animation left
            self.facing_right = False
            moving = True
            self.frame_index += self.animation_speed
            cf = self.run_frames[int(self.frame_index) % 2]
            if self.on_ground:
                self.image = pygame.transform.flip(cf, True, False)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            # Jump
            self.on_ground = False
            self.v_y = V_Y

            # Animation jump
            tr = self.tiles[22].get_bounding_rect()
            ti = self.tiles[22].subsurface(tr)
            jimg = pygame.transform.scale(ti, self.size)
            if not self.facing_right:
                jimg = pygame.transform.flip(jimg, True, False)
            self.image = jimg

        # Borders
        if self.rect.right > SCREEN_SIZE[0]: # SCREEN WIDTH
            self.rect.x = SCREEN_SIZE[0] - self.size[0]
        if self.rect.left < 0:
            self.rect.x = 0

        # Tile collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if prev < self.rect.x:
                    self.rect.right = tile.rect.left
                if prev > self.rect.x:
                    self.rect.left = tile.rect.right
                

        self.jump(tiles)
        # Scroll
        if self.rect.x > PLAYER_RBP*SCREEN_SIZE[0]: # 50% Screen Width
            self.world_x = self.rect.x - prev
            self.rect.x = prev
        elif self.rect.x < PLAYER_LBP*SCREEN_SIZE[0]: # 10% Screen Width
            self.world_x = 0
            self.rect.x = prev
        else:
            self.world_x = 0

        

    def jump(self, tiles):
        prev = self.rect.y
        dg = False
        self.rect.y -= (1 / 2) * self.d_y * (self.v_y ** 2) # <- F = (m*v^2)/2
        self.v_y -= 1 if not self.on_ground else 0
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if prev < self.rect.y:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    dg = True
                    self.v_y = 0
                    self.d_y = 1
                if prev > self.rect.y and not self.on_ground:
                    self.rect.top = tile.rect.bottom
                    self.d_y = -1
                    self.v_y = 0
        if self.v_y < 0:
            self.d_y = -1
        if self.rect.y > self.start_pos[1] + PLAYER_JUMP_OFFSET:
            self.rect.y = PLAYER_POS[1]
            self.v_y = 0
            self.on_ground = True
            dg = True
            self.d_y = 1
        if not dg:
            self.d_v = -1
            self.on_ground = False
        if dg and self.on_ground:
            self.image = self.run_frames[int(self.frame_index) % 2]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)


    def draw(self, screen):
        # pygame.draw.rect(screen, 'white', self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        """fb_sf = pygame.Surface(self.size)
        fb_sf = fb_sf.convert()
        fb_sf.fill('red')
        fb_rc = pygame.Rect(*self.size, self.rect.x, self.rect.y)
        # fb_img = pygame.image.load('/Users/7artek/Documents/Politechnika Łódzka/SLFinal/resources/images/player.png')
        # os.path.abspath('../../resources/images/player.png')
        fb_img = pygame.image.load('./resources/images/player.png')
        fb_img = pygame.transform.scale(fb_img, fb_rc.size)
        fb_img = fb_img.convert_alpha()
        fb_sf.blit(fb_img, fb_rc)
        screen.blit(fb_sf, (self.rect.x, self.rect.y))"""

