from colorama import init as colorama_init
from colorama import Fore
from os import path

MOVE_SPEED = 5
FPS = 60

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
] # 0 = floor ; 1 = wall

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

ROBOT_POS = [((5, 3), True), ((7, 9), False), ((2, 6), False)]
CROSS_POS = (2,8)

MAIN_DIR = path.dirname(__file__)
IMG_DIR = path.join(MAIN_DIR, "img")
ANSWER_FILE = path.join(MAIN_DIR, "answer.txt")
SPRITES = {
    'wall': ('■', Fore.GREEN),
    'floor': ('□', Fore.GREEN),
    'cross': ('✕', Fore.RED),
    'robot': ('○', Fore.YELLOW),
    'robot_main': ('◯', Fore.RED),
    'robot_chosen': ('◉', Fore.YELLOW),
    'robot_main_chosen': ('◉', Fore.RED)
}