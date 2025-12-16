"""
Global settings

Include constants for different components
to avoid repetition
"""

"""SCREEN"""
SCREEN_SIZE = (1200, 800)
TICK = 60

"""CHUNK & LEVEL"""
CHUNK_BRAKEPOINT = 0.9
STEP_X = 10

"""SCORE"""
SCORE_OFFSET_X = 11

"""PLAYER"""
PLAYER_SIZE = (62, 80)
PLAYER_POS = (160, SCREEN_SIZE[1] - PLAYER_SIZE[1]*2)
V_Y = 10
V_X = 10
PLAYER_ANIMATION_SPEED = 0.15
PTS = 32
PLAYER_RBP = 0.5
PLAYER_LBP = 0.1
PLAYER_JUMP_OFFSET = 41

"""TILE"""
TPS = 16
TILE_SIZE = 80
