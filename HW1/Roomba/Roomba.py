import time
import random
from pprint import pprint

global env
env= {
    "BATTERY_LEVEL": 100,
    "SPOT": False,
    "SPOT_LOCATION": (3.0, 7.0),
    "GENERAL": False,
    "DUSTY_SPOT": False,
    "DUSTY_SPOT_LOCATION": (0.0, -4.0),
    "HOME_PATH": [],
    "LOCATION": (-3.0, 5.0),
    "FACING": (0, 1)
}

NODE_INITIALIZED = -1
NODE_SUCCEED = 0
NODE_RUNNING = 1
NODE_FAILED = 2

def Update_Battery(conditions, precent):
    battery = conditions["BATTERY_LEVEL"]
    battery += precent
    if battery >= 100:
        battery = 100
    elif battery <= 0:
        battery = 0
    conditions.update({"BATTERY_LEVEL": battery})
    return True

def RandomChangeLocation(env, degree_x, degree_y):
    random_x = round(random.random()-0.5, 1)*degree_x
    random_y = round(random.random()-0.5, 1)*degree_y
    location = (round(env["LOCATION"][0]+random_x, 1),
                round(env["LOCATION"][1]+random_y, 1))
    env.update({"LOCATION": location})

def FindCompletePath(env, path):
    pathi = path[0]
    pathj = path[1]
    faci = env["FACING"][0]
    facj = env["FACING"][1]
    return_path = []
    if pathi != 0:
        if faci*pathi > 0:
            return_path.append([0, pathi/faci])
            env.update({"FACING": (faci, facj)})
            faci = faci
            facj = facj
        elif faci*pathi < 0:
            return_path.append([180, -pathi/faci])
            env.update({"FACING": (-faci, facj)})
            faci = -faci
            facj = facj

        elif faci == 0:
            if (pathi > 0) & (facj > 0):
                return_path.append([90, pathi])
                env.update({"FACING": (1, 0)})
                faci = 1
                facj = 0
            if (pathi > 0) & (facj < 0):
                return_path.append([-90, pathi])
                env.update({"FACING": (1, 0)})
                faci = 1
                facj = 0
            if (pathi < 0) & (facj > 0):
                return_path.append([-90, -pathi])
                env.update({"FACING": (-1, 0)})
                faci = -1
                facj = 0
            if (pathi < 0) & (facj < 0):
                return_path.append([90, -pathi])
                env.update({"FACING": (-1, 0)})
                faci = -1
                facj = 0

    if pathj != 0:
        if facj*pathj > 0:
            return_path.append([0, pathj/facj])
            env.update({"FACING": (faci, facj)})
            faci = faci
            facj = facj
        elif facj*pathj < 0:
            return_path.append([180, -pathj/facj])
            env.update({"FACING": (faci, -facj)})
            faci = faci
            facj = -facj
        elif facj == 0:
            if (pathj > 0) & (faci > 0):
                return_path.append([-90, pathj])
                env.update({"FACING": (0, 1)})
                faci = 0
                facj = 1
            if (pathj > 0) & (faci < 0):
                return_path.append([90, pathj])
                env.update({"FACING": (0, 1)})
                faci = 0
                facj = 1
            if (pathj < 0) & (faci > 0):
                return_path.append([90, -pathj])
                env.update({"FACING": (0, -1)})
                faci = 0
                facj = -1
            if (pathj < 0) & (faci < 0):
                return_path.append([-90, -pathj])
                env.update({"FACING": (0, -1)})
                faci = 0
                facj = -1
    env.update({"FACING": (faci, facj)})
    return return_path


class Node:
    ParentNode = None
    TrueMessage = ""
    FalseMessage = ""

    NodeStatus = NODE_INITIALIZED

    def __init__(self, TrueMessage, FalseMessage, ParentNode):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.NodeStatus = NODE_INITIALIZED

    def SetParent(self, ParentNode):
        self.ParentNode = ParentNode

    def run(self, conditions):
        pass

    def evaluate_state(self):
        return self.NodeStatus


class Decorator(Node):
    ChildNode = None

    def __init__(self, TrueMessage, FalseMessage, ParentNode, ChildNode):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.ChildNode = ChildNode
        self.NodeStatus = NODE_INITIALIZED

    def set_child_node(self, NewNode):
        self.ChildNode = NewNode


class Negation(Decorator):
    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        self.ChildNode.run(conditions)
        i_status = 2 - self.ChildNode.NodeStatus
        self.NodeStatus = i_status
        return True


class Until(Decorator):
    UntilSuccess = False
    UntilFail = False

    def __init__(self, TrueMessage, FalseMessage, ParentNode, ChildNode, UntilFail):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.ChildNode = ChildNode
        self.NodeStatus = NODE_INITIALIZED

        if (UntilFail == True):
            self.UntilFail = True
            self.UntilSuccess = False

        elif (UntilFail == False):
            self.UntilFail = False
            self.UntilSuccess = True

    def run(self, conditions):
        if (self.UntilSuccess):
            self.NodeStatus = NODE_RUNNING
            while (True):
                self.ChildNode.run(conditions)
                i_status = self.ChildNode.evaluate_state()
                if i_status == NODE_SUCCEED:
                    break
            self.NodeStatus = NODE_SUCCEED
            return True
        elif (self.UntilFail):
            self.NodeStatus = NODE_RUNNING
            while (True):
                self.ChildNode.run(conditions)
                i_status = self.ChildNode.evaluate_state()
                if i_status == NODE_FAILED:
                    break
            self.NodeStatus = NODE_SUCCEED
            return True


class Timer(Decorator):
    Interval = 0

    def __init__(self, TrueMessage, FalseMessage, ParentNode, ChildNode, Interval):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.ChildNode = ChildNode
        self.NodeStatus = NODE_INITIALIZED
        self.Interval = Interval

    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        i_status = 2 - self.ChildNode.run(conditions, self.Interval)
        self.NodeStatus = i_status
        return True


class Composite(Node):
    ChildNodes = []

    def __init__(self, TrueMessage, FalseMessage, ParentNode, ChildNodes):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.ChildNodes = ChildNodes
        self.NodeStatus = NODE_INITIALIZED

    def add_child_node(self, NewNode):
        self.ChildNodes.append(NewNode)

    def set_child_nodes(self, NewNodes):
        self.ChildNodes = []
        for i in NewNodes:
            self.ChildNodes.append(i)


class Sequence(Composite):
    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        for i in self.ChildNodes:
            i.run(conditions)
            i_status = i.evaluate_state()
            if i_status == NODE_FAILED:
                self.NodeStatus = NODE_FAILED
                break
        if self.NodeStatus != NODE_FAILED:
            self.NodeStatus = NODE_SUCCEED
        return True


class Selection(Composite):
    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        for i in self.ChildNodes:
            i.run(conditions)
            i_status = i.evaluate_state()
            if i_status == NODE_SUCCEED:
                self.NodeStatus = NODE_SUCCEED
                break
        if self.NodeStatus != NODE_SUCCEED:
            self.NodeStatus = NODE_FAILED
        return True


class Priority(Composite):
    PriorityMap = {}

    def __init__(self, TrueMessage, FalseMessage, ParentNode, ChildNodes, PriorityMap):
        self.TrueMessage = TrueMessage
        self.FalseMessage = FalseMessage
        self.ParentNode = ParentNode
        self.ChildNodes = ChildNodes
        self.NodeStatus = NODE_INITIALIZED
        self.PriorityMap = PriorityMap

    def view_priority_map(self):
        pprint(self.PriorityMap)

    def add_child_node(self, NewNode, Priority):
        for i in range(len(self.PriorityMap) + 1, Priority, -1):
            self.PriorityMap.update({i: self.PriorityMap[i - 1]})
        self.PriorityMap.update({Priority: NewNode})
        self.ChildNodes.append(NewNode)

    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        for i in range(1, len(self.PriorityMap)+1):
            node = self.PriorityMap[i]
            node.run(conditions)
            i_status = node.evaluate_state()
            if i_status == NODE_SUCCEED:
                self.NodeStatus = NODE_SUCCEED
                break
        if self.NodeStatus != NODE_SUCCEED:
            self.NodeStatus = NODE_FAILED
        return True


class Condition(Node):
    def judge(self, conditions):
        return True

    def run(self, conditions):
        if self.judge(conditions) == True:
            self.NodeStatus = NODE_SUCCEED
        else:
            self.NodeStatus = NODE_FAILED
        return True


class Judge_Battery(Condition):
    def judge(self, conditions):
        if conditions["BATTERY_LEVEL"] <= 30:
            print("Battery lower than 30%!")
            return True
        else:
            return False


class Judge_Spot(Condition):
    def judge(self, conditions):
        if conditions["SPOT"] == True:
            print("Need Spot Cleaning!")
            return True
        else:
            return False


class Judge_General(Condition):
    def judge(self, conditions):
        if conditions["GENERAL"] == True:
            print("Need General Cleaning!")
            return True
        else:
            return False


class Judge_Dusty_Spot(Condition):
    def judge(self, conditions):
        if conditions["DUSTY_SPOT"] == True:
            print("Found Dusty Spot!")
            return True
        else:
            return False


class Task(Node):
    def job(self, conditions):
        return True

    def run(self, conditions):
        self.NodeStatus = NODE_RUNNING
        job_status = self.job(conditions)
        if (job_status):
            self.NodeStatus = NODE_SUCCEED
        elif job_status == False:
            self.NodeStatus = NODE_FAILED
        return True


class Find_Home(Task):
    def job(self, conditions):
        conditions.update({"HOME_PATH": FindCompletePath(conditions, conditions["LOCATION"])})
        time.sleep(2)
        print("Finding Home!")
        return True


class Go_Home(Task):
    def job(self, conditions):
        print("Going Home!")
        for i in conditions["HOME_PATH"]:
            print("Turn {} degree clockwise...".format(i[0]))
            time.sleep(1)
            print("Go {} metres ahead...".format(i[1]))
            time.sleep(2)
        conditions.update({"HOME_PATH": []})
        conditions.update({"LOCATION": (0, 0)})
        print("Back To Home!")
        return True


class Dock(Task):
    def job(self, conditions):
        print("Docked!")
        Update_Battery(conditions, 100)
        time.sleep(4)
        print("Charge Finished!")
        time.sleep(1)
        return True


class Clean_Spot(Task):
    def job(self, conditions, interval):
        # TODO!!!!!!!!!!!!!!!!!!!
        print("Spot detected at {}".format(conditions["SPOT_LOCATION"]))
        path_x = conditions["SPOT_LOCATION"][0] - conditions["LOCATION"][0]
        path_y = conditions["SPOT_LOCATION"][1] - conditions["LOCATION"][1]
        to_spot_path = FindCompletePath(conditions, (path_x, path_y))
        time.sleep(1)
        for i in to_spot_path:
            print("Turn {} degree clockwise...".format(i[0]))
            time.sleep(1)
            print("Go {} metres ahead...".format(i[1]))
            time.sleep(2)

        time0 = time.time()
        while (time.time() <= time0 + interval):
            print("Cleaning Spot")
            time.sleep(1)
            RandomChangeLocation(conditions, 1, 1)
            Update_Battery(conditions, -1)
        return True

    def run(self, conditions, interval):
        self.NodeStatus = NODE_RUNNING
        job_status = self.job(conditions, interval)
        if (job_status):
            self.NodeStatus = NODE_SUCCEED
        elif job_status == False:
            self.NodeStatus = NODE_FAILED
        return True


class Clean_Dusty_Spot(Clean_Spot):
    def job(self, conditions, interval):
        # TODO!!!!!!!!!!!!!!!!!!!
        print("Spot detected at {}".format(conditions["DUSTY_SPOT_LOCATION"]))
        path_x = conditions["DUSTY_SPOT_LOCATION"][0] - conditions["LOCATION"][0]
        path_y = conditions["DUSTY_SPOT_LOCATION"][1] - conditions["LOCATION"][1]
        to_spot_path = FindCompletePath(conditions, (path_x, path_y))
        time.sleep(1)
        for i in to_spot_path:
            print("Turn {} degree clockwise...".format(i[0]))
            time.sleep(1)
            print("Go {} metres ahead...".format(i[1]))
            time.sleep(2)

        time0 = time.time()
        while (time.time() <= time0 + interval):
            print("Cleaning Dusty Spot")
            time.sleep(1)
            RandomChangeLocation(conditions, 1, 1)
            Update_Battery(conditions, -1)
        return True


class Done_Spot(Task):
    def job(self, conditions):
        print("Done Spot!")
        conditions.update({"SPOT": False})
        conditions.update({"SPOT_LOCATION": (0, 0)})
        time.sleep(1)
        return True


class Done_Dusty_Spot(Task):
    def job(self, conditions):
        print("Done Spot!")
        conditions.update({"DUSTY_SPOT": False})
        conditions.update({"DUSTY_SPOT_LOCATION": (0, 0)})
        time.sleep(1)
        return True


class Clean(Task):
    def job(self, conditions):
        time.sleep(1)
        RandomChangeLocation(conditions, 2, 2)
        Update_Battery(conditions, -10)
        print("Cleaning!")
        return True


class Done_General(Task):
    def job(self, conditions):
        print("Done General!")
        conditions.update({"GENERAL": False})
        time.sleep(1)
        return True


#class FailedTest(Task):
#    def job(self, conditions):
#        time.sleep(0)
#        print("Failed")
#        return False


class Do_Nothing(Task):
    def job(self, conditions):
        time.sleep(5)
        Update_Battery(conditions, -5)
        print("Doing Nothing...")
        return True

class Roomba:
    p1 = Priority("", "", None, [], {})

    s1 = Sequence("", "", p1, [])
    j1 = Judge_Battery("", "", s1)
    t1 = Find_Home("", "", s1)
    t2 = Go_Home("", "", s1)
    t3 = Dock("", "", s1)

    s2 = Selection("", "", p1, [])

    s2_1 = Sequence("", "", s2, [])
    j2 = Judge_Spot("", "", s2_1)
    timer_1 = Timer("", "", s2_1, None, 20)
    t4 = Clean_Spot("", "", timer_1)
    t5 = Done_Spot("", "", s2_1)

    s2_2 = Sequence("", "", s2, [])
    j3 = Judge_General("", "", s2_2)

    s2_2_1 = Sequence("", "", s2_2, [])
    uf1 = Until("", "", s2_2_1, [], UntilFail=True)

    s2_2_1_1 = Sequence("", "", s2_2_1, [])
    n1 = Negation("", "", s2_2_1_1, [])
    j4 = Judge_Battery("", "", n1)

    s2_2_1_1_1 = Selection("", "", s2_2_1_1, [])

    s2_2_1_1_1_1 = Sequence("", "", s2_2_1_1_1, [])
    j5 = Judge_Dusty_Spot("", "", s2_2_1_1_1_1)
    timer_2 = Timer("", "", s2_2_1_1_1_1, None, 35)
    t6 = Clean_Dusty_Spot("", "", timer_2)
    t10 = Done_Dusty_Spot("", "", timer_2)

    t7 = Clean("", "", s2_2_1_1_1)

    t8 = Done_General("", "", s2_2_1)

    t9 = Do_Nothing("", "", p1)

    p1.add_child_node(s1, 1)
    p1.add_child_node(s2, 2)
    p1.add_child_node(t9, 3)

    s1.set_child_nodes([j1, t1, t2, t3])

    s2.set_child_nodes([s2_1, s2_2])

    s2_1.set_child_nodes([j2, timer_1, t5])
    timer_1.set_child_node(t4)

    s2_2.set_child_nodes([j3, s2_2_1])

    s2_2_1.set_child_nodes([uf1, t8])
    uf1.set_child_node(s2_2_1_1)

    s2_2_1_1.set_child_nodes([n1, s2_2_1_1_1])
    n1.set_child_node(j4)

    s2_2_1_1_1.set_child_nodes([s2_2_1_1_1_1, t7])

    s2_2_1_1_1_1.set_child_nodes([j5, timer_2, t10])
    timer_2.set_child_node(t6)

    def run(self,env):
        while (True):
            rand = random.random()
            if rand > 0.6:
                env.update({"SPOT": True})
                env.update({"SPOT_LOCATION": (round(random.random() * 10 - 5, 1), round(random.random() * 10 - 5, 1))})
                env.update({"GENERAL": False})
            elif rand >0.2:
                env.update({"SPOT": False})
                env.update({"GENERAL": True})
                if rand > 0.4:
                    env.update({"DUSTY_SPOT": True})
                    env.update({"DUSTY_SPOT_LOCATION": (
                    round(random.random() * 10 - 5, 1), round(random.random() * 10 - 5, 1))})
                else:
                    env.update({"DUSTY_SPOT": False})
            else:
                env.update({"SPOT":False})
                env.update({"GENERAL":False})
            print("--------------------")
            pprint(env)
            print("--------------------")
            self.p1.run(env)

if __name__=="__main__":
    roomba=Roomba()
    roomba.run(env)
