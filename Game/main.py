import tkinter as tk

from settings import *
from sprites import *

# To input instruction, insert them in "answer.txt"

class Game(tk.Tk):
    def __init__(self, cross_pos:tuple, robots:list[tuple], use_file:bool=True) -> None:
        super().__init__(screenName='Ricochet Robot')
        self.title = 'Ricochet Robot'
        self.win = False
        self.grid:list[list[Floor | Wall]] = self.create_grid()
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
        self.initGrid()
        self.drawGrid()
        self.bind('<space>', lambda event: self.update())
             
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
    
    def getAction(self) -> str:
        return self.instructions[self.current_instruction]
    
    def update(self) -> None:       
        action = self.getAction()
        if "quit" in action or action == "":
            self.quit()
            return
        else:
            if action == "s": action = "switch"
            print('')
            print(f'Instruction: {action}')
            self.current_instruction += 1
        if "switch" in action:
            self.switchRobot()
            self.moves += 1
        else:
            try:
                coordinates = (self.letterToCoordinate(action[0]), int(action[1:])-1)
                if not self.robots[self.active_robot].move(coordinates):
                    print("This move is illegal.")
                else:
                    self.moves += 1
            except:
                print("Bad input, try again.")
        self.drawGrid()
        if self.robots[self.active_robot].is_main and self.robots[self.active_robot].pos == self.cross.pos:
            self.win = True
            print(f'You won in {self.moves} moves.')
      
    def switchRobot(self) -> None:
        self.robots[self.active_robot].setNonActive()
        self.active_robot = self.active_robot + 1
        while not self.active_robot < len(self.robots):
            self.active_robot -= len(self.robots)
        self.robots[self.active_robot].setActive()
        
    def initGrid(self):
        self.label_grid:list[list[tk.Label]] = []
        for n_row, row in enumerate(self.grid):
            self.label_grid.append([])
            for n_column, element in enumerate(row):
                reference = self.grid[n_row][n_column]
                if len(reference.sprite) > 1:
                    index_color = (n_column + n_row) % len(reference.sprite)
                else: index_color = 0
                self.label_grid[n_row].append(tk.Label(self, background=reference.sprite[index_color], font=(FONT, 30)))
                self.label_grid[n_row][n_column].grid(column=n_column+1, row=n_row+1, sticky='nsew')
        tk.Label(self, background=COLORS['black']).grid(column=0, row=0, sticky='nsew')
        for row in range(len(self.grid)):
            tk.Label(self, background=COLORS['black'], foreground=COLORS['white'], font=(FONT, 22), text=str(row+1)).grid(column=0, row=row+1, sticky='nsew', ipadx=8)
        for col in range(len(self.grid[0])):
            tk.Label(self, background=COLORS['black'], foreground=COLORS['white'], font=(FONT, 22), text=ALPHABET[col].upper()).grid(column=col+1, row=0, sticky='nsew', ipady=8)
        
        self.drawGrid()
                
    def drawGrid(self) -> None:
        for n_row, row in enumerate(self.label_grid):
            for n_column, element in enumerate(row):
                label = ''
                for robot in self.robots:
                    if robot.pos == (n_column, n_row):
                        label = robot.sprite[0]
                        label_color = robot.sprite[1]
                if label == '':
                    if self.cross.pos == (n_column, n_row):
                        label = self.cross.sprite[0]
                        label_color = self.cross.sprite[1]
                if label != '':
                    element.config(text=f'{label}', foreground=label_color)
                else:
                    element.config(text=f'    ')
                    
                element.grid_configure(column=n_column+1, row=n_row+1, sticky='nsew')
                
                
if __name__ == "__main__":
    game = Game(CROSS_POS, ROBOT_POS)
    game.mainloop() 