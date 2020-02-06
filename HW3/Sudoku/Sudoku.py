from copy import deepcopy
from pprint import pprint
import sys
import getopt
import time


def judge_unique(lis):
    n = []
    for i in lis:
        if i!=0:
            n.append(i)
    if len(n) != len(set(n)):
        return False
    return True


def get_unit(x, y):
    return round((x - 1) / 3) + round((y - 1) / 3) * 3, x - round((x - 1) / 3) * 3 + 3 * y - 9 * round((y - 1) / 3)


# Normal Sudoku
class Sudoku:
    column = []
    line = []
    unit = []

    def __init__(self):
        self.column = [[0 for i in range(9)] for j in range(9)]
        self.line = [[0 for i in range(9)] for j in range(9)]
        self.unit = [[0 for i in range(9)] for j in range(9)]

    def init_state(self, state):
        for i in range(9):
            for j in range(9):
                self.set_value(j, i, state[i][j])
        return True

    def set_value(self, x, y, value):
        self.column[x][y] = value
        self.line[y][x] = value
        unit_x, unit_y = get_unit(x, y)
        self.unit[unit_x][unit_y] = value
        return True

    def judge_constraint(self):
        for jtype in [self.column, self.line, self.unit]:
            for i in jtype:
                if judge_unique(i) == False:
                    return False
        return True

    def judge_one(self, x, y):
        unit_x, unit_y = get_unit(x, y)
        for i in [self.column[x], self.line[y], self.unit[unit_x]]:
            if judge_unique(i) == False:
                return False
        return True

    def judge_done(self):
        for i in self.column:
            for j in i:
                if j == 0:
                    return False
        return True

    def print_state(self):
        for i in self.line:
            pprint(i)
        return True


# Using normal backtracking to solve sudoku
class CSP:
    step = 0
    queue = []
    answer = None
    finished = None

    def __init__(self, shudoku):
        self.queue = [[shudoku, 0]]
        self.finished = False

    def extend(self):
        i = self.queue.pop()
        # i[0].print_state()
        # print("-------------------")
        if i[0].judge_done():
            self.answer = i[0]
            self.finished = True
        for y in range(9):
            for x in range(9):
                if i[0].column[x][y] == 0:
                    for v in range(1, 10):
                        s = deepcopy(i[0])
                        s.set_value(x, y, v)
                        if s.judge_one(x, y):
                            self.queue.append([s, i[1] + 1])
                    return True
        return True

    def sort(self):
        for i in range(len(self.queue)):
            for j in range(i, len(self.queue)):
                if self.queue[i][1] > self.queue[j][1]:
                    temp = self.queue[i]
                    self.queue[i] = self.queue[j]
                    self.queue[j] = temp
        return True

    def run(self):
        self.step = 0
        while (self.finished == False):
            self.extend()
            # self.sort()
            self.step += 1
        print("The result is:")
        self.answer.print_state()
        print("Steps Count:", self.step)


# Sudoku that support backjumping solution
class BackJumpingSudoku:
    column = []
    line = []
    unit = []
    all_conflict_set = []
    last_set = []

    def __init__(self):
        self.column = [[0 for i in range(9)] for j in range(9)]
        self.line = [[0 for i in range(9)] for j in range(9)]
        self.unit = [[0 for i in range(9)] for j in range(9)]
        self.all_conflict_set = [[[] for i in range(9)] for j in range(9)]

    def init_state(self, state):
        for i in range(9):
            for j in range(9):
                self.set_value(i, j, state[i][j])
        return True

    def set_value(self, x, y, value):
        self.column[x][y] = value
        self.line[y][x] = value
        unit_x, unit_y = get_unit(x, y)
        self.unit[unit_x][unit_y] = value

        for i in range(9):
            for j in range(9):
                unit_i, unit_j = get_unit(i, j)
                if (i == x) | (j == y) | (unit_i == unit_x):
                    self.all_conflict_set[i][j].append([value, [x, y]])
        return True

    def judge_constraint(self):
        for jtype in [self.column, self.line, self.unit]:
            for i in jtype:
                if judge_unique(i) == False:
                    return False
        return True

    def judge_one(self, x, y):
        unit_x, unit_y = get_unit(x, y)
        for i in [self.column[x], self.line[y], self.unit[unit_x]]:
            if judge_unique(i) == False:
                return False
        return True

    def judge_one_conflict(self, x, y):
        choice = []
        for i in self.all_conflict_set[x][y]:
            if i[0] != 0:
                choice.append(i[0])
            if len(set(choice)) == 9:
                return i[1]
        else:
            return None

    def judge_done(self):
        for i in self.column:
            for j in i:
                if j == 0:
                    return False
        return True

    def print_state(self):
        for i in self.column:
            pprint(i)
        return True


# Using backjumping to solve sudoku
class BackJumpingCSP:
    queue = []
    step = 0
    answer = None
    finished = None
    conflict = None
    last = None

    def __init__(self, s):
        self.queue = [[s, [0, 0], 0]]
        self.finished = False

    def extend(self):
        i = self.queue.pop()
        self.last = i
        # i[0].print_state()
        # print("-------------------")
        if i[0].judge_done():
            self.answer = i[0]
            self.finished = True

        for y in range(9):
            for x in range(9):
                if i[0].column[x][y] == 0:
                    if len(i[0].all_conflict_set[x][y]) >= 9:
                        if i[0].judge_one_conflict(x, y) is not None:
                            self.conflict = i[0].judge_one_conflict(x, y)
                            return False
                    for v in range(1, 10):
                        s = deepcopy(i[0])
                        s.set_value(x, y, v)
                        if s.judge_one(x, y):
                            self.queue.append([s, [x, y], v])
                    return True
        return True

    def sort(self):
        for i in range(len(self.queue)):
            for j in range(i, len(self.queue)):
                if self.queue[i][1][1] > self.queue[j][1][1]:
                    temp = self.queue[i]
                    self.queue[i] = self.queue[j]
                    self.queue[j] = temp
                elif self.queue[i][1][1] == self.queue[j][1][1]:
                    if self.queue[i][1][0] > self.queue[j][1][0]:
                        temp = self.queue[i]
                        self.queue[i] = self.queue[j]
                        self.queue[j] = temp
        return True

    def backjumping(self):
        # print("-------------------")
        # print("backJumping To",self.conflict)
        # print("-------------------")
        queue = []
        for i in self.queue:
            if (i[1][1] < self.conflict[1]):
                queue.append(i)
            elif (i[1][1] == self.conflict[1]) & (i[1][0] <= self.conflict[0]):
                queue.append(i)
        self.queue = queue
        self.conflict = None
        return True

    def run(self):
        self.step = 0
        while (self.finished == False):
            # print(self.queue)
            extend = self.extend()
            if extend == False:
                self.backjumping()
            #self.sort()
            self.step += 1
        print("The result is:")
        self.answer.print_state()
        print("Steps Count:", self.step)



# Read the command line options.
def read_arg(argv):
    input_state = ''
    algo = ''

    try:
        opts, args = getopt.getopt(argv, "hi:a:", ["input_state=", "algorithm="])
    except getopt.GetoptError:
        print("Sudoku.py -i <input_state>(easy or evil) -a <algorithm>(backtracking or backjumping)")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Sudoku.py -i <input_state>(easy or evil) -a <algorithm>(backtracking or backjumping)")
            sys.exit()
        elif opt in ["-i", "--input_state"]:
            input_state = arg
        elif opt in ["-a", "--algorithm"]:
            algo = arg
    if (input_state not in ["easy", "evil"]) | (algo not in ["backjumping", "backtracking"]):
        print("Sudoku.py -i <input_state>(easy or evil) -a <algorithm>(backtracking or backjumping)")
        sys.exit(2)
    return input_state, algo


# Please run this program through Terminal!
if __name__ == "__main__":
    time0 = time.time()
    input_state, algo = read_arg(sys.argv[1:])
    #print(input_state, algo)
    if input_state == "easy":
        lines = [[int(i) for i in line.rstrip('\n').strip(" ").split(",")] for line in open('easy.txt')]
    else:
        lines = [[int(i) for i in line.rstrip('\n').strip(" ").split(",")] for line in open('evil.txt')]

    if algo == "backtracking":
        print("Using normal backtraking to solve the soduku problem...")
        s = Sudoku()
        s.init_state(lines)
        p = CSP(s)
    else:
        print("Using backjumping to solve the soduku problem...")
        s = BackJumpingSudoku()
        s.init_state(lines)
        p = BackJumpingCSP(s)
    p.run()

    print(round(time.time() - time0, 2), "Seconds Used")
