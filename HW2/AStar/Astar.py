import copy
import sys
import getopt


# Heuristic function based on Landmark Heuristics For The Pancake Problem
def heuristic(state):
    h = 0
    for i in range(len(state) - 1):
        if abs(state[i] - state[i + 1]) > 1:
            h += 1
    if state[len(state) - 1] != len(state):
        h += 1
    return h


# Function that calculate the state after one flip
def swap(state, i):
    new_state = copy.deepcopy(state)
    for j in range(round(i / 2 + 0.1)):
        temp = new_state[j]
        new_state[j] = new_state[i - j]
        new_state[i - j] = temp
    return new_state


# AStar approach to the problem
class AstarPancake:
    init = []
    size = None
    # The structure of one node in priority queue is [[Flips to reach the state], state of node, backward cost,
    # heuristic cost, total cost]
    queue = []
    visited = []
    goal = None

    def __init__(self, state):
        self.init = state
        self.size = len(state)
        self.queue = [[[], state, 0, heuristic(state), heuristic(state)]]
        self.visited = [state]

    # Sort the priority queue based on F(n) = g(n) + h(n)
    def sort(self):
        for i in range(len(self.queue)):
            for j in range(i, len(self.queue)):
                if self.queue[i][4] < self.queue[j][4]:
                    temp = self.queue[i]
                    self.queue[i] = self.queue[j]
                    self.queue[j] = temp
                # elif self.queue[i][4]==self.queue[j][4]:
                # if self.queue[i][3]<self.queue[j][3]:
                # temp = self.queue[i]
                # self.queue[i] = self.queue[j]
                # self.queue[j] = temp
        return True

    # Extend one node and add its children to the priority queue.
    def extend(self):
        extendstate = self.queue.pop()
        for i in range(1, self.size):
            new_step = copy.deepcopy(extendstate[0])
            new_step.append(i)
            new_state = copy.deepcopy(extendstate[1])
            new_state = swap(new_state, i)
            new_bcost = extendstate[2] + 1
            new_fcost = heuristic(new_state)
            new_total = new_fcost + new_bcost
            if new_state not in self.visited:
                self.queue.insert(0, [new_step, new_state, new_bcost, new_fcost, new_total])
                self.visited.append(new_state)
        self.sort()
        return True

    # Check whether the solution is found.
    def goaltest(self):
        if len(self.queue) == 0:
            self.goal = False
            return True

        for i in self.queue:
            if i[1] == list(range(1, self.size + 1)):
                self.goal = i
                return True

        return False

    # Build up the whole process.
    def run(self):
        while not self.goaltest():
            self.extend()
        return self.goal

    # Print the detailed steps of the solution.
    def print_step(self):
        if self.goal is not None:
            if self.goal == False:
                print("Cannot Find A Solution.")
                return True
            print("Steps As Below:")
            print("The inital state is {}".format(str(self.init)))
            step = copy.deepcopy(self.init)
            count = 0
            for i in self.goal[0]:
                count += 1
                i = copy.deepcopy(i)
                step = swap(step, i)
                print("Step {} : Flip the Pancake No.{} and all pancakes above".format(count, i + 1))
                print("The new state is {}".format(str(step)))
            return True
        return False


# UCS approach to the problem
class UCSPancake:
    init = []
    size = None
    visited = []
    # The structure of one node in priority queue is [[Flips to reach the state], state of node, backward cost]
    queue = []
    goal = None

    def __init__(self, state):
        self.init = state
        self.size = len(state)
        self.queue = [[[], state, 0]]
        self.visited = [state]

    # Sort the priority queue based on g(n)
    def sort(self):
        for i in range(len(self.queue)):
            for j in range(i, len(self.queue)):
                if self.queue[i][2] < self.queue[j][2]:
                    temp = self.queue[i]
                    self.queue[i] = self.queue[j]
                    self.queue[j] = temp
        return True

    # Extend one node and add its children to the priority queue.
    def extend(self):
        extendstate = self.queue.pop()
        for i in range(1, self.size):
            new_step = copy.deepcopy(extendstate[0])
            new_step.append(i)
            new_state = copy.deepcopy(extendstate[1])

            new_state = swap(new_state, i)
            new_bcost = extendstate[2] + 1

            if new_state not in self.visited:
                self.queue.insert(0, [new_step, new_state, new_bcost])
                self.visited.append(new_state)

        self.sort()
        return True

    # Check whether the solution is found.
    def goaltest(self):
        if len(self.queue) == 0:
            self.goal = False
            return True

        for i in self.queue:
            if i[1] == list(range(1, self.size + 1)):
                self.goal = i
                return True

        return False

    # Build up the whole process.
    def run(self):
        while not self.goaltest():
            self.extend()
        return self.goal

    # Print the detailed steps of the solution.
    def print_step(self):
        if self.goal is not None:
            if self.goal == False:
                print("Cannot Find A Solution.")
                return True
            print("Steps As Below:")
            print("The inital state is {}".format(str(self.init)))
            step = copy.deepcopy(self.init)
            count = 0
            for i in self.goal[0]:
                count += 1
                i = copy.deepcopy(i)
                step = swap(step, i)
                print("Step {} : Flip the Pancake No.{} and all pancakes above".format(count, i + 1))
                print("The new state is {}".format(str(step)))
            return True
        return False


# Read the command line options.
def read_arg(argv):
    input_state = ''
    algo = ''

    try:
        opts, args = getopt.getopt(argv, "hi:a:", ["input_state=", "algorithm="])
    except getopt.GetoptError:
        print("Astar.py -i <input_state>(digits separated by,) -a <algorithm>(astar or ucs)")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Astar.py -i <input_state>(digits separated by,) -a <algorithm>(astar or ucs)")
            sys.exit()
        elif opt in ["-i", "--input_state"]:
            input_state = arg
            input_state = [int(num) for num in input_state.split(",")]
        elif opt in ["-a", "--algorithm"]:
            algo = arg
    return input_state, algo

# Please run this program through Terminal!
if __name__ == "__main__":
    input_state, algo = read_arg(sys.argv[1:])
    if algo == "astar":
        p = AstarPancake(input_state)
        print("Using AStar to solve problem state {} ...".format(str(input_state)))
    elif algo == "ucs":
        p = UCSPancake(input_state)
        print("Using UCS to solve problem state {} ...".format(str(input_state)))
    p.run()
    p.print_step()
