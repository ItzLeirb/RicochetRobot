from settings import *
from sprites import *
from time import time

class Game():
    def __init__(self, cross_pos:tuple, robots:list[tuple]) -> None:
        self.win = False
        self.grid:list[list[Floor | Wall]] = self.create_grid()
        self.cross = Cross(cross_pos)
        self.robots:list[tuple] = []
        self.active_robot = -1
        for i, robot in enumerate(robots):
            self.robots.append(robot[0])
            if robot[1]:
                self.active_robot = i
        self.possibles = ['u', 'd', 'l', 'r', 's']
        self.moves = []
        self.max_generation = 0
        self.Tree = Node([self.robots, self.active_robot, self.cross, self.grid], ['Optimal Path:'], self, 0)
             
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
      
    def switchRobot(self) -> None:
        self.active_robot = (self.active_robot + 1) % len(self.robots)

    def directionToCoords(self, direction:str) -> str:
        pos = self.robots[self.active_robot]
        on_robot = False
        if direction == "u":
            while not self.grid[pos[1]][pos[0]].is_wall and not on_robot:
                pos = (pos[0], pos[1] - 1)
                for robot in self.robots:
                    if pos == robot:
                        on_robot = True
            return (pos[0], pos[1]+1)
        elif direction == "d":
            while not self.grid[pos[1]][pos[0]].is_wall and not on_robot:
                pos = (pos[0], pos[1] + 1)
                for robot in self.robots:
                    if pos == robot:
                        on_robot = True
            return (pos[0], pos[1]-1)
        elif direction == "l":
            while not self.grid[pos[1]][pos[0]].is_wall and not on_robot:
                pos = (pos[0] - 1, pos[1])
                for robot in self.robots:
                    if pos == robot:
                        on_robot = True
            return (pos[0]+1, pos[1])
        elif direction == "r":
            while not self.grid[pos[1]][pos[0]].is_wall and not on_robot:
                pos = (pos[0] + 1, pos[1])
                for robot in self.robots:
                    if pos == robot:
                        on_robot = True
            return (pos[0]-1, pos[1])
    
    def coordsToLetter(self, coords:tuple[int]) -> str:
        return f'{ALPHABET[coords[0]]}{coords[1]+1}'

    def quit(self, path:list[str]):
        optimal_path = []
        for action in path:
            if ',' in action: # is a coordinate
                _action = action.split(',')
                coords = (int(_action[0]), int(_action[1]))
                optimal_path.append(self.coordsToLetter(coords))
            else:
                optimal_path.append(action)
            print(optimal_path[-1])
        
        print(f'Optimal solution found in {len(path)-1} moves')
        
        self.win = True
                
    def updateTree(self) -> list:
        list_index = 0
        allChildren:list[list[Node]] = [[self.Tree], []]
        for generation in range(self.max_generation):
            list_index = (list_index + 1) % 2 # switches between 0 & 1
            allChildren[list_index] = []
            for parent in allChildren[(list_index+1)%2]:
                for child in parent.children:
                    allChildren[list_index].append(child)
        for node in allChildren[list_index]:
            node.generateChildren()

class Node(Game):
    def __init__(self, state:list, path:list, main_game:Game, generation:int) -> None:
        self.state = state
        self.moves:list = path
        self.children:list = []
        self.main_game = main_game
        
        self.robots:list[Robot] = state[0]
        self.cross:Cross = state[2]

        self.grid:list[list[Floor | Wall]] = self.state[3]
        self.active_robot = self.state[1]
        self.generation = generation
        if self.main_game.max_generation < self.generation:
            self.main_game.max_generation = self.generation
        self.possibles = POSSIBLES
        
    def checkVictory(self) -> None:
        if self.active_robot == 0 and self.robots[self.active_robot] == self.cross.pos:
            self.win = True
            self.main_game.quit(self.moves)
       
    def generateChild(self, action) -> Game:
        state  = [[], self.active_robot, self.cross, self.grid]
        moves = []
        main_game = self.main_game
        gen = self.generation + 1
        
        for robot in self.robots:
            state[0].append(robot)
        
        for move in self.moves:
            moves.append(move)
        
        node = self.returnChild(state, moves, main_game, gen)
        node.update(action)
        
        return node
    
    def returnChild(self, state, moves, main_game, gen):
        return Node(state, moves, main_game, gen)
    
    def generateChildren(self):
        for action in self.possibles:
            direction_useful = True
            active_robot_pos = self.robots[self.active_robot]
            if action == 'u' and self.grid[active_robot_pos[1]-1][active_robot_pos[0]].is_wall:
                direction_useful = False
            if action == 'd' and self.grid[active_robot_pos[1]+1][active_robot_pos[0]].is_wall:
                direction_useful = False
            if action == 'l' and self.grid[active_robot_pos[1]][active_robot_pos[0]-1].is_wall:
                direction_useful = False
            if action == 'r' and self.grid[active_robot_pos[1]][active_robot_pos[0]+1].is_wall:
                direction_useful = False
                
            if action in 'udlr':
                coords = self.directionToCoords(action)
                action = f'{coords[0]},{coords[1]}'
                
            for index in range(2, min(len(self.moves)+1, 7), 2):
                if self.moves[-index] == action:
                    direction_useful = False
            
            if action != self.moves[-1] and direction_useful:
                self.children.append(self.generateChild(action))
    
    def update(self, action:str) -> None:
        if action == "s": 
            action = "switch"
        if "switch" in action:
            self.switchRobot()
            if len(self.moves) <= self.generation:
                self.moves.append(action)
        else:
            coordinates:tuple = (int(action.split(',')[0]), int(action.split(',')[1]))
            self.robots[self.active_robot] = coordinates
            if len(self.moves) <= self.generation:
                self.moves.append(action)
        self.checkVictory()
    

if __name__ == '__main__':
    start_time = time()
    loop_time = start_time
    game = Game(CROSS_POS, ROBOT_POS)
    for i in range(MAX_ITERATIONS):
        print(f'Current level: {game.max_generation+1}')
        print(f'Total elapsed Time: {time()-start_time}s')
        print(f'Elapsed time this level: {time()-loop_time}s')
        loop_time = time()
        game.updateTree()
        if game.win: break
