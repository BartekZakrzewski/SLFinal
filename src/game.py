import pygame
import sys
import subprocess
import random as ran
from src.components.player import Player
from src.components.tile import Tile
from resources.chunks import chunks
from src.settings import SCREEN_SIZE, TILE_SIZE, CHUNK_BRAKEPOINT, SCORE_OFFSET_X, STEP_X, TICK

class Game:
    def __init__(self):
        self.screen_size = SCREEN_SIZE
        self.screen = pygame.display.set_mode(self.screen_size)
        self.running = False
        self.clock = pygame.time.Clock()
        self.w_offset_x = 0
        self.init_player()
        self.init_level()
        self.world_x = 0
        self.isFirstRun = True
        self.score = 0

    def init_player(self):
        self.player = Player(self.screen)

    def generate_chunk(self, seed):
        chunk_tiles = []
        n_tiles = self.screen_size[0] // TILE_SIZE # Tile size
        
        # Generate ground level
        for i in range(n_tiles):
            chunk_tiles.append(Tile((TILE_SIZE, TILE_SIZE), ((TILE_SIZE * i + self.w_offset_x), SCREEN_SIZE[1] - TILE_SIZE), 'grass'))

        for y, row in enumerate(chunks[seed][::-1]):
            for x, t in enumerate(row):
                if t == 'H':
                    for i, c in enumerate(chunk_tiles):
                        if c.rect.x == TILE_SIZE * x + self.w_offset_x:
                            del chunk_tiles[i]
                            break
                elif t == 'X':
                    chunk_tiles.append(Tile((TILE_SIZE, TILE_SIZE), ((TILE_SIZE * x + self.w_offset_x), (SCREEN_SIZE[1] - TILE_SIZE * y)), 'platform'))

        # TODO Enemies

        self.w_offset_x += self.screen_size[0]
        return chunk_tiles

    def init_level(self):
        self.tiles = []
        for chunk in self.generate_chunk(0):
            self.tiles.append(chunk)

    def update_chunks(self):
        if self.tiles[-1].rect.x <= (self.screen_size[0] + self.w_offset_x)*CHUNK_BRAKEPOINT: # Before player break point
            next_chunk = self.generate_chunk(ran.randint(0, len(chunks) - 1))
            for tile in next_chunk:
                self.tiles.append(tile)

    def update_score(self):
        """
        The score is updated based on the offset of the next generated chunk
        Minus the initial offset so it starts at 0
        This basically rewards the player with 1 - 2 points per chunk
        Which I think is sufficient
        """
        self.score = (self.w_offset_x - self.screen_size[0] * SCORE_OFFSET_X)//self.screen_size[0]

    def draw_score(self):
        # max(0, score) is a fallback in case my scoring system fails
        score = self.font.render(f"Score: {max(0, self.score)}", True, 'black') 
        self.screen.blit(score, (0, 0))

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys, self.tiles)
        self.player.draw(self.screen)

        self.w_offset_x += self.player.world_x//STEP_X
        self.world_x = self.player.world_x

        # DEBUG bottom_level = pygame.Rect(self.w_offset_x, 0, self.screen_size[0], 80)
        # DEBUG pygame.draw.rect(self.screen, 'red', bottom_level)
        self.update_chunks()
        for tile in self.tiles:
            tile.update(self.world_x)
            tile.draw(self.screen)

        self.update_score()
        self.draw_score()
        

    def run(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Super Python Brothers")

        self.running = True
        self.font = pygame.sysfont.SysFont('Arial', 30)

        try:
            subprocess.call(["wmctrl", "-r", "Super Python Brothers", "-b", "add,above"])
        except FileNotFoundError:
            print("wmctrl not installed. Run: sudo apt-get install wmctrl")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False

            # Game loop

            self.screen.fill('lightblue')

            self.update()

            if not self.isFirstRun and self.player.rect.bottom > SCREEN_SIZE[1]: # Screen height
                print("Game Over")
                self.running = False
            self.isFirstRun = False
            pygame.display.flip()
            self.clock.tick(TICK)

        pygame.quit()
        sys.exit()
