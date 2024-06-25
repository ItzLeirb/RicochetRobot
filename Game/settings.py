from os import path

MOVE_SPEED = 5
FPS = 60

GRID = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
] # 0 = floor ; 1 = wall

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

ROBOT_POS = [((7, 9), True), ((1, 6), False)]
CROSS_POS = (4,6)

POSSIBLES = ['s', 'u', 'd', 'l', 'r']

COLORS = {
    'green': "GREEN",
    'lightgreen': "LIGHTGREEN",
    'darkgreen': "DARKGREEN",
    'purple': "MAGENTA",
    'black': "BLACK",
    'white': "WHITE",
    'lightyellow': "LIGHTYELLOW"
}

MAIN_DIR = path.dirname(__file__)
ANSWER_FILE = path.join(MAIN_DIR, 'answer.txt')
SPRITES = {
    'wall': [COLORS['lightgreen']],
    'floor': (COLORS['darkgreen'], COLORS['green']),
    'cross': ('✕', COLORS['red']),
    'robot': ('△', COLORS['yellow']),
    'robot_main': ('△', COLORS['purple']),
    'robot_chosen': ('▲', COLORS['yellow']),
    'robot_main_chosen': ('▲', COLORS['purple'])
}

FONT = 'Segoe UI Black bold'

MAX_ITERATIONS = 30