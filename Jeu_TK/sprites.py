from settings import *
        
class Cross():
    def __init__(self, pos:tuple) -> None:
        self.pos = pos
        self.sprite = SPRITES['cross']
        

class Robot():
    def __init__(self, pos: tuple, main: bool, grid:list, cross:Cross) -> None:
        self.pos = pos
        self.is_main = main
        self.grid = grid
        self.cross = cross
        self.win = False
        self.active = False
        self.setNonActive()
        self.robots:list[Robot] = []
    
    def provideRobots(self, robots:list) -> None:
        self.robots = robots
        
    def checkPath(self, path_start:tuple, path_end:tuple) -> bool:
        for robot in self.robots:
            if robot.pos == path_end:
                return False        
        
        if path_end[0] == path_start[0]:
            if path_start[1] < path_end[1]:
                for i in range(path_start[1]+1, path_end[1]+1):
                    if self.grid[i][path_start[0]].is_wall:
                        return False
                robot_block = False
                for robot in self.robots:
                    if robot.pos == (path_end[0], path_end[1]+1):
                        robot_block = True
                        break
                if not (self.grid[path_end[1]+1][path_start[0]].is_wall or robot_block):
                    return False
            else:
                for i in range(path_end[1], path_start[1]):
                    if self.grid[i][path_start[0]].is_wall:
                        return False
                robot_block = False
                for robot in self.robots:
                    if robot.pos == (path_end[0], path_end[1]-1):
                        robot_block = True
                        break
                if not (self.grid[path_end[1]-1][path_start[0]].is_wall or robot_block):
                    return False
            
        elif path_end[1] == path_start[1]:
            if path_start[0] < path_end[0]:
                for i in range(path_start[0]+1, path_end[0]+1):
                    if self.grid[path_start[1]][i].is_wall:
                        return False
                robot_block = False
                for robot in self.robots:
                    if robot.pos == (path_end[0]+1, path_end[1]):
                        robot_block = True
                        break
                if not (self.grid[path_start[1]][path_end[0]+1].is_wall or robot_block):
                    return False
            else:
                for i in range(path_end[0], path_start[0]):
                    if self.grid[path_start[1]][i].is_wall:
                        return False
                robot_block = False
                for robot in self.robots:
                    if robot.pos == (path_end[0]-1, path_end[1]):
                        robot_block = True
                        break
                if not (self.grid[path_start[1]][path_end[0]-1].is_wall or robot_block):
                    return False
                        
        else:
            return False
        
        return True
    
            
    def move(self, destination_pos) -> bool: # success
        path_is_valid = self.checkPath(self.pos, destination_pos)
        if not path_is_valid:
            return False
        self.pos = destination_pos
        return True
        
    
    def update(self) -> None:
        if self.active:
            pass

    
    def setActive(self) -> None:
        self.active = True
        if self.is_main:
            self.sprite = SPRITES['robot_main_chosen']
        else:
            self.sprite = SPRITES['robot_chosen']
    
    
    def setNonActive(self) -> None:
        self.active = False
        if self.is_main:
            self.sprite = SPRITES['robot_main']
        else:
            self.sprite = SPRITES['robot']
            
    
class Wall(): 
    def __init__(self, pos: tuple) -> None:
        self.pos = pos
        self.sprite = SPRITES['wall']
        self.is_wall = True


class Floor():
    def __init__(self, pos: tuple) -> None:
        self.pos = pos
        self.sprite = SPRITES['floor']
        self.is_wall = False
