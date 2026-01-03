import pygame
from src.settings import (PLAYER_SIZE, PLAYER_POS,
                          V_X, V_Y, PLAYER_ANIMATION_SPEED, PTS, SCREEN_SIZE,
                          PLAYER_RBP, PLAYER_LBP)


class Player:
    def __init__(self, screen):
        # Init variables
        self.screen = screen
        self.size = PLAYER_SIZE
        self.start_pos = PLAYER_POS
        self.rect = pygame.Rect(*self.start_pos, *self.size)

        # Sounds
        self.jump_sound = pygame.mixer.Sound(
            './resources/sounds/jump.wav'
        )
        self.coin_sound = pygame.mixer.Sound(
            './resources/sounds/coin.wav'
        )
        self.enemy_sound = pygame.mixer.Sound(
            './resources/sounds/power_up.wav'
        )

        # Images
        self.tiles = []
        self.load_tiles()
        self.run_frames = self.runFramesHlp(self.tiles, self.size)
        self.run_frames = []
        for of in self.tiles[:2]:
            tr = of.get_bounding_rect()
            ti = of.subsurface(tr)
            si = pygame.transform.scale(ti, self.size)
            self.run_frames.append(si)

        # Game loop variables
        self.on_ground = True
        self.is_alive = True
        self.kills = 0
        self.coins = 0

        self.v_y = 0
        self.d_y = 1

        self.v_x = V_X

        self.distance_x = self.start_pos[0]
        self.position_x = self.start_pos[0]

        self.world_x = 0
        self.frame_index = 0
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.image = self.run_frames[0]
        self.facing_right = True

    def runFramesHlp(self, tiles, size):
        return [pygame.transform.scale(tiles[0], size),
                pygame.transform.scale(tiles[1], size)]

    def load_tiles(self):
        tileset = pygame.image.load('./resources/images/knight.png')
        tw, th = tileset.get_size()
        for y in range(0, th, PTS):
            for x in range(0, tw, PTS):
                rect = pygame.Rect(x, y, PTS, PTS)
                ct = tileset.subsurface(rect)
                self.tiles.append(ct)

    def update(self, keys, tiles, enemies, coins, spikes):
        # Movement
        prev = self.rect.x
        self.moving = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # Move right
            self.rect.x += self.v_x

            # Animation right
            self.facing_right = True
            self.moving = True
            self.frame_index += self.animation_speed
            if self.on_ground:
                self.image = self.run_frames[int(self.frame_index) % 2]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # Move left
            self.rect.x -= self.v_x

            # Animation left
            self.facing_right = False
            self.moving = True
            self.frame_index += self.animation_speed
            cf = self.run_frames[int(self.frame_index) % 2]
            if self.on_ground:
                self.image = pygame.transform.flip(cf, True, False)
        jmpks = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        if jmpks and self.on_ground:
            # Jump
            self.jump_sound.play()
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
        if self.rect.right > SCREEN_SIZE[0]:
            self.rect.x = SCREEN_SIZE[0] - self.size[0]
        if self.rect.left < 0:
            self.rect.x = 0

        # Tile collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if prev < self.rect.x:
                    self.rect.right = tile.rect.left
                    self.moving = False
                if prev > self.rect.x:
                    self.rect.left = tile.rect.right
                    self.moving = False

        for spike in spikes:
            if self.rect.colliderect(spike.tile):
                if prev < self.rect.x:
                    self.right = spike.tile.left
                    self.moving = False
                if prev > self.rect.x:
                    self.rect.left = spike.tile.right
                    self.moving = False

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and enemy.is_alive:
                if self.on_ground:
                    self.is_alive = False
                    self.rect.bottom = enemy.rect.bottom
                    enemy.image = enemy.player_frame

        for coin in coins:
            if self.rect.colliderect(coin.rect) and coin.is_alive:
                coin.on_death()
                self.coins += 1
                self.coin_sound.play()

        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.is_alive = False
                self.rect.bottom = spike.rect.top + 10

        if self.is_alive:
            self.jump(tiles, enemies, spikes)

        # Scroll
        if self.rect.x > PLAYER_RBP*SCREEN_SIZE[0]:  # 50% Screen Width
            self.world_x = self.rect.x - prev
            self.rect.x = prev
        elif self.rect.x < PLAYER_LBP*SCREEN_SIZE[0]:  # 10% Screen Width
            self.world_x = 0
            self.rect.x = prev
        else:
            self.world_x = 0

        self.position_x += self.rect.x - prev
        self.position_x += self.world_x
        self.distance_x = max(self.distance_x, self.position_x)

    def jump(self, tiles, enemies, spikes):
        prev = self.rect.y
        dg = False
        self.rect.y -= (1 / 2) * self.d_y * (self.v_y ** 2)  # <- F = (m*v^2)/2
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
        for spike in spikes:
            if self.rect.colliderect(spike.tile):
                if prev < self.rect.y:
                    self.rect.bottom = spike.tile.top
                    self.on_ground = True
                    dg = True
                    self.v_y = 0
                    self.d_y = 1
                if prev > self.rect.y and not self.on_ground:
                    self.rect.top = spike.tile.bottom
                    self.d_y = -1
                    self.v_y = 0
        for i, enemy in enumerate(enemies):
            if self.rect.colliderect(enemy.rect) and enemy.is_alive:
                if prev < self.rect.y:
                    self.rect.bottom = enemy.rect.top
                    self.on_ground = False
                    self.v_y = V_Y // 2
                    self.d_y = 1
                    enemy.on_death()
                    self.enemy_sound.play()
                    self.kills += 1
                if prev > self.rect.y:
                    self.is_alive = False
                    enemy.image = enemy.player_frame
                    self.rect.bottom = enemy.rect.bottom

        if self.v_y < 0:
            self.d_y = -1
        if self.rect.y > self.start_pos[1]*2:
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
        screen.blit(self.image, (self.rect.x, self.rect.y))
