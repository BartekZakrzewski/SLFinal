"""
Main game module.

This module contains the Game class which manages the main game loop,
rendering, physics, and entity management.
"""

import pygame
import random as ran
from src.components.player import Player
from src.components.tile import Tile
from src.components.enemy import Enemy
from src.components.cloud import Cloud
from src.components.coin import Coin
from src.components.spikes import Spike
from resources.chunks import chunks
from src.settings import SCREEN_SIZE, TILE_SIZE, TICK


class Game:
    """
    The main Game class.

    Manages the game state, level generation, and main loop.
    """

    def __init__(self, username):
        """
        Initialize the game.

        Args:
            username (str): The name of the player.
        """
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption(f"Super Python Bros - {username}")

        self.death_s = pygame.mixer.Sound("./resources/sounds/explosion.wav")
        self.bgmusic = pygame.mixer.Sound("./resources/music/bgmusic.mp3")

        self.username = username
        self.screen_size = SCREEN_SIZE
        self.screen = pygame.display.set_mode(self.screen_size)
        self.running = False
        self.clock = pygame.time.Clock()
        self.w_offset_x = 0
        self.enemies = []
        self.clouds = []
        self.coins = []
        self.spikes = []
        self.init_player()
        self.init_level()
        self.world_x = 0
        self.isFirstRun = True
        self.score = 0
        self.kills = 0
        self.earned = 0

    def init_player(self):
        """Initialize the player entity."""
        self.player = Player(self.screen)

    def generate_chunk(self, seed):
        """
        Generate a level chunk based on a seed index.

        Args:
            seed (int): The index of the chunk definition in chunks list.
        """
        offset_w = 0
        if len(self.tiles) > 0:
            for tile in self.tiles:
                offset_w = max(offset_w, tile.rect.right)
        self.w_offset_x = offset_w - 80

        for y, row in enumerate(chunks[seed][::-1]):
            y = y + 1
            for x, t in enumerate(row):
                x = x + 1
                if t == "H":
                    self.tiles.append(
                        Tile(
                            (TILE_SIZE, TILE_SIZE),
                            (
                                (TILE_SIZE * x + self.w_offset_x),
                                (SCREEN_SIZE[1] - TILE_SIZE * y),
                            ),
                            "grass",
                        )
                    )
                elif t == "X":
                    self.tiles.append(
                        Tile(
                            (TILE_SIZE, TILE_SIZE),
                            (
                                (TILE_SIZE * x + self.w_offset_x),
                                (SCREEN_SIZE[1] - TILE_SIZE * y),
                            ),
                            "platform",
                        )
                    )
                elif t == "E":
                    self.enemies.append(
                        Enemy(
                            (TILE_SIZE, TILE_SIZE),
                            (
                                (TILE_SIZE * x + self.w_offset_x),
                                (SCREEN_SIZE[1] - TILE_SIZE * y),
                            ),
                        )
                    )
                elif t == "C":
                    self.coins.append(
                        Coin(
                            (TILE_SIZE, TILE_SIZE),
                            (
                                (TILE_SIZE * x + self.w_offset_x),
                                (SCREEN_SIZE[1] - TILE_SIZE * y),
                            ),
                        )
                    )
                elif t == "S":
                    self.spikes.append(
                        Spike(
                            (TILE_SIZE, TILE_SIZE),
                            (
                                (TILE_SIZE * x + self.w_offset_x),
                                (SCREEN_SIZE[1] - TILE_SIZE * y),
                            ),
                        )
                    )
                if t == "H" or t == "X":
                    offset_w = max(offset_w, self.tiles[-1].rect.right)

    def init_level(self):
        """Initialize the starting level state."""
        self.tiles = []
        cloud1 = Cloud(
            (3 * TILE_SIZE, 2 * TILE_SIZE),
            ((SCREEN_SIZE[0] - TILE_SIZE) // 2, (SCREEN_SIZE[1] - TILE_SIZE) // 2),
            1,
        )
        cloud2 = Cloud(
            (3 * TILE_SIZE, 2 * TILE_SIZE),
            (
                (SCREEN_SIZE[0] - TILE_SIZE * (12)) // 2,
                (SCREEN_SIZE[1] - TILE_SIZE * (3)) // 2,
            ),
            60,
        )
        self.clouds = [cloud1, cloud2]
        self.generate_chunk(0)
        self.generate_chunk(4)
        self.generate_chunk(5)

    def update_chunks(self):
        """
        Check if new chunks need to be generated
        based on player position.
        """
        if self.tiles[-1].rect.right < self.player.distance_x * 0.5:
            self.generate_chunk(ran.randint(0, len(chunks) - 1))

    def update_score(self):
        """Calculate and update the player's score."""
        self.score = (
            self.player.distance_x / 100
            + (self.player.kills + self.player.coins) * self.player.v_x
        )
        for i, tile in enumerate(self.tiles):
            if tile.rect.x + TILE_SIZE < 0:
                del self.tiles[i]

    def draw_score(self):
        """Draw the score on the screen."""
        score = self.game_font.render(
            f"Score: {max(0, int(self.score))}", False, "black"
        )
        self.screen.blit(score, (0, 0))

    def animate_dead(self, ani, ans, scaled_frames):
        """
        Animate the player's death sequence.

        Args:
            ani (float): Animation index.
            ans (float): Animation speed.
            scaled_frames (list): List of scaled image frames for animation.

        Returns:
            tuple: (ans, ani) updated animation state.
        """
        # End text
        death_text = self.dripping_font.render("YOU DIED!", True, "red")
        dtw, dth = death_text.get_size()
        self.screen.blit(
            death_text, ((SCREEN_SIZE[0] - dtw) // 2, (SCREEN_SIZE[1] - dth * 2) // 2)
        )

        quit_text = self.game_font.render("Press [q] to quit", False, "black")
        qtw, qth = quit_text.get_size()
        self.screen.blit(
            quit_text, ((SCREEN_SIZE[0] - qtw) // 2, (SCREEN_SIZE[1] - qth) // 2)
        )

        score_text = self.game_font.render(
            f"Your score: {int(self.score)}", False, "darkgray"
        )
        stw, sth = score_text.get_size()
        self.screen.blit(
            score_text, ((SCREEN_SIZE[0] - stw) // 2, (SCREEN_SIZE[1] - sth) // 2 + qth)
        )

        # Death sound
        if ani == 0:
            self.death_s.play()

        # Animate
        ani += ans
        self.player.image = scaled_frames[min(int(ani), len(scaled_frames) - 1)]
        return ans, ani

    def update(self):
        """Update game entities and handle logic for one frame."""
        keys = pygame.key.get_pressed()

        for cloud in self.clouds:
            cloud.update(self.world_x)
            cloud.draw(self.screen)

        self.player.update(keys, self.tiles, self.enemies, self.coins, self.spikes)
        self.player.draw(self.screen)

        self.world_x = self.player.world_x

        self.update_chunks()
        for tile in self.tiles:
            tile.update(self.world_x)
            tile.draw(self.screen)

        for i, enemy in enumerate(self.enemies):
            enemy.update(self.world_x, self.tiles)
            enemy.draw(self.screen, self.game_font)
            if not enemy.is_alive and enemy.frame_index >= len(enemy.frames) - 1:
                del self.enemies[i]

        for i, coin in enumerate(self.coins):
            coin.update(self.world_x)
            coin.draw(self.screen, self.game_font)
            if not coin.is_alive and coin.frame_index >= len(coin.frames) - 1:
                del self.coins[i]

        for spike in self.spikes:
            spike.update(self.world_x)
            spike.draw(self.screen)

        self.update_score()
        self.draw_score()

    def run(self):
        """
        Run the main game loop.

        Returns:
            int: Final score of the game session.
        """
        self.running = True
        self.font = pygame.sysfont.SysFont("Arial", 30)
        self.dripping_font = pygame.font.Font(
            "./resources/fonts/Butcherman/Butcherman-Regular.ttf", 90
        )
        self.game_font = pygame.font.Font(
            "./resources/fonts/Silkscreen/Silkscreen-Bold.ttf", 35
        )

        death_frames = [
            self.player.tiles[50],
            self.player.tiles[58],
            self.player.tiles[59],
        ]
        scaled_frames = []
        for death in death_frames:
            tr = death.get_bounding_rect()
            ti = death.subsurface(tr)
            si = pygame.transform.scale(ti, self.player.size)
            scaled_frames.append(si)
        ans = 0.075
        ani = 0

        while self.running:
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_q
                ):
                    self.running = False

            if not pygame.mixer.get_busy():
                self.bgmusic.play()

            # Game loop

            self.screen.fill("lightblue")

            if self.player.is_alive:
                self.update()
            else:
                for enemy in self.enemies:
                    enemy.draw(self.screen, self.game_font)
                for spike in self.spikes:
                    spike.draw(self.screen)
                ans, ani = self.animate_dead(ani, ans, scaled_frames)
                self.player.draw(self.screen)

            if not self.isFirstRun and self.player.rect.bottom > SCREEN_SIZE[1]:
                self.player.is_alive = False
                self.player.rect.bottom = SCREEN_SIZE[1]
            self.isFirstRun = False
            pygame.display.flip()
            self.clock.tick(TICK)

        pygame.quit()
        return int(self.score)
