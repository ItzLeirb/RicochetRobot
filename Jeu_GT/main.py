from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from settings import *
from sprites import *

class Game:
    def __init__(self, robots:list, cross_pos:tuple, use_file:bool=False) -> None:
        colorama_init()
        self.running = True
        self.grid = self.create_grid()
        self.cross = Cross(cross_pos)
        self.robots:list[Robot] = []
        self.active_robot = -1
        for i, robot in enumerate(robots):
            self.robots.append(Robot(robot[0], robot[1], self.grid, self.cross))
            if robot[1]:
                self.robots[-1].setActive()
                self.active_robot = i
        for robot in self.robots:
            robot.provideRobots(self.robots)
        self.moves = 0
        self.use_file = use_file
        if self.use_file:
            self.file = ANSWER_FILE
            self.instructions = []
            self.current_instruction = 0
            file = open(self.file, 'r')
            for line in file:
                self.instructions.append(line.split('\n')[0])
            self.instructions.append((""))
            file.close()
             
    def create_grid(self) -> list:
        grid:list[list] = []
        for y, row in enumerate(GRID):
            grid.append([])
            for x, column in enumerate(row):
                if column == 1:
                    grid[y].append(Wall((x, y)))
                else:
                    grid[y].append(Floor((x, y)))
        return grid
    
    def letterToCoordinate(self, letter) -> int:
        for i, l in enumerate(ALPHABET):
            if l == letter:
                return i
        return -1
    
    def update(self) -> None:       
        if self.use_file:
            action = self.instructions[self.current_instruction]
            print('')
            print(f'Instruction : {Fore.RED}{action}{Style.RESET_ALL}')
            self.current_instruction += 1
        else:
            print(f'{Style.RESET_ALL}You can move the selected robot (◉), switch to another robot (◯) or quit.')
            print(f'Enter coordinates to move (e.g.: 6b) ; Enter "switch" or "s" to switch robots ; Enter "quit" or "" to quit.')
            action = input("").lower()
        if "quit" in action or action == "":
            self.running = False
            return
        elif "switch" in action or action == "s":
            self.switchRobot()
            self.moves += 1
        else:
            try:
                coordinates = (self.letterToCoordinate(action[-1]), int(action[:-1])-1)
                if not self.robots[self.active_robot].move(coordinates):
                    print("This move is illegal.")
                else:
                    self.moves += 1
            except:
                print("Bad input, try again.")
        self.draw()
        if self.robots[self.active_robot].is_main and self.robots[self.active_robot].pos == self.cross.pos:
            self.running = False
            print(f'{Fore.RED}Y{Fore.YELLOW}o{Fore.GREEN}u {Fore.GREEN}W{Fore.CYAN}i{Fore.BLUE}n {Fore.MAGENTA}! {Style.RESET_ALL}')
            print(f'Number of moves : {self.moves}')
    
    def draw(self) -> None:
        firstLine = '     '
        for l in ALPHABET[:len(self.grid[0])]:
            firstLine = firstLine + l + '  '
        secondLine = '   ——'
        for i in range(len(self.grid[0])):
            secondLine = secondLine + '———'
        print(firstLine)
        print(secondLine)
        
        for row, elements in enumerate(self.grid):
            self.drawRow(row)
    
    def drawRow(self, row:int) -> print:
        rowString = f'{row+1}'
        if row < 9: rowString = rowString + ' '
        rowString = rowString + '|  '
        
        for column, tile in enumerate(self.grid[row]):
            char = ''
            for robot in self.robots:
                if (column, row) == robot.pos:
                    char = robot.sprite[1] + robot.sprite[0] + '  ' # color + text
            if (column, row) == self.cross.pos and char == '':
                char = self.cross.sprite[1] + self.cross.sprite[0] + '  '
            elif char == '':
                char = tile.sprite[1] + tile.sprite[0] + '  '
            rowString = rowString + char
            
        return print(rowString + Style.RESET_ALL)

    def switchRobot(self) -> None:
        self.robots[self.active_robot].setNonActive()
        self.active_robot = self.active_robot + 1
        while not self.active_robot < len(self.robots):
            self.active_robot -= len(self.robots)
        self.robots[self.active_robot].setActive()
        


game = Game(ROBOT_POS, CROSS_POS, use_file=True)
game.draw()
while game.running:
    game.update()