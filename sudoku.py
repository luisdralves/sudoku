import numpy
from termcolor import colored
import os


def importGrid(fname):
    grid = []
    f = open(fname, 'r')
    lines = f.readlines()
    for line in lines:
        if line[0] == '-':
            continue
        gridLine = []
        for char in line:
            if char == ' ':
                gridLine.append(0)
            elif char != '|' and char != '\n':
                gridLine.append(int(char))
        while len(gridLine) < 9:
            gridLine.append(0)
        grid.append(gridLine)
    return grid

def displayGrid(grid, fixed):
    print(colored("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗", 'green'))
    for y in range(len(grid)):
        line = grid[y]
        print(colored('║', 'green'), end='')
        for x in range(len(line)):
            number = line[x]
            if number == 0:
                print('   ', end='')
            elif fixed[y][x]:
                print(colored(' ' + str(number)[0] + ' ', 'yellow'), end='')
            else:
                print(colored(' ' + str(number)[0] + ' ', 'cyan'), end='')
            if (x+1) % 3 == 0:
                print(colored('║', 'green'), end='')
            else:
                print(colored('│', 'green'), end='')
        print()
        if y == len(grid) - 1:
            print(colored("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝", 'green'))
        elif (y+1) % 3 == 0:
            print(colored("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣", 'green'))
        else:
            print(colored("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢", 'green'))


def fixed(grid):
    fixed = []
    for line in grid:
        fixedLine = []
        for number in line:
            fixedLine.append(number > 0)
        fixed.append(fixedLine)
    return fixed


def cols(grid):
    return numpy.array(grid).T.tolist()


def subgrids(grid):
    subgrids = []
    for suby in range(3):
        for subx in range(3):
            subgrid = []
            for y in range(3):
                for x in range(3):
                    subgrid.append(grid[y+3*suby][x+3*subx])
            subgrids.append(subgrid)
    return subgrids


def valid(grid, number=None):
    if number is None:
        for number in range(1, 10):
            if not valid(grid, number):
                return False
        return True
    else:
        for line in grid:
            if line.count(number) > 1:
                return False
        for col in cols(grid):
            if col.count(number) > 1:
                return False
        for subgrid in subgrids(grid):
            if subgrid.count(number) > 1:
                return False
        return True


def availableSpots(grid, number):
    spots = []
    for y in range(len(grid)):
        spotsLine = []
        line = grid[y]
        for x in range(len(line)):
            col = cols(grid)[x]
            subgrid = subgrids(grid)[3*(y//3)+x//3]
            spotsLine.append(
                not(number in line or number in col or number in subgrid)
                and grid[y][x] == 0)
        spots.append(spotsLine)
    return spots


def solved(grid):
    for line in grid:
        for number in line:
            if number == 0:
                return False
    return valid(grid)


def fillMissing(toFill):
    for number in range(1, 10):
        if not number in toFill:
            toFill[toFill.index(0)] = number
            break


def solve(grid):
    while not solved(grid):
        if not valid(grid):
            print('something went wrong!')
            return False
        for number in range(1, 10):
            spots = availableSpots(grid, number)
            for y in range(len(spots)):
                line = spots[y]
                for x in range(len(line)):
                    if spots[y][x]:
                        col = cols(spots)[x]
                        subgrid = subgrids(spots)[3*(y//3)+x//3]
                        if line.count(True) == 1 or col.count(True) == 1 or subgrid.count(True) == 1:
                            grid[y][x] = number
        """
        #this part checks if theres only 1 empty spot and fills it, but its buggy maybe not needed
        for y in range(len(grid)):
            line = grid[y]
            if line.count(0) == 1:
                for number in range(1, 10):
                    if not number in line:
                        line[line.index(0)] = number
                        break
            for x in range(len(line)):
                col = cols(grid)[x]
                subgrid = subgrids(grid)[3*(y//3)+x//3]
                if col.count(0) == 1:
                    for number in range(1, 10):
                        if not number in col:
                            grid[y][x] = number
                            break
                if subgrid.count(0) == 1:
                    for number in range(1, 10):
                        if not number in subgrid:
                            grid[y][x] = number
                            break
        """
    displayGrid(grid, fixedNumbers)
    print('solved!')
    return True

grid = importGrid(os.sys.argv[1])
fixedNumbers = fixed(grid)
displayGrid(grid, fixedNumbers)
solve(grid)
