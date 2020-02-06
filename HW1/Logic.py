Env = {
    "BATTERY_LEVEL": 100,
    "SPOT": True,
    "GENERAL": True,
    "DUSTY_SPOT": True,
    "HOME_PATH": [],
}


class Node:
    SonNodes=[]
    TrueMessage = ""
    FalseMessage = ""

    def __init__(self,TrueMessage, FalseMessage):
        this.TrueMessage = TrueMessage
        this.FalseMessage = FalseMessage

    def run():
        status = True
        return status


class Composite(Node):
    SonNodes = []

    def __init__(self,TrueMessage, FalseMessage, SonNodes):
        this.TrueMessage = TrueMessage
        this.FalseMessage = FalseMessage
        this.SonNodes = SonNodes

    def run():
        status = True
        if(runComposite):
            return True

    def runComposite():
        return True


class Sequence(Composite):

class Priority(Composite):
    PriorityState={}
    def __init__(self,TrueMessage, FalseMessage, SonNodes, PriorityState):
        this.TrueMessage = TrueMessage
        this.FalseMessage = FalseMessage
        this.SonNodes = SonNodes
        this.PriorityState=PriorityState

class Selection(Composite):


class Task(Composite):


class Find_Home(Composite):


class Roomba:
    def Back_To_Dock():
        if Env["BATTERY_LEVEL"] < 30:
            try:
                Env["HOME_PATH"] = FIND_HOME()
                GO_HOME(Env["HOME_PATH"])
                DOCK()
                return True
            except:
                return False
        else return False

    def Cleaning_Spot():
        if Env["SPOT"] == True:
            Time = 0
            try:
                while (Time <= 20000):
                    CLEAN_SPOT()
                DONE_SPOT(Env["SPOT"])
                return True
            except:
                return False
        else return False

    def Dusty_Spot_Cleaning():
        if Env["DUSTY_SPOT"] == True:
            Time = 0
            try:
                while(Time < 35000):
                    CLEAN_SPOT()
                return True
            except:
                return False
        else return False

    def General_Cleaning():
        if Env["GENERAL"] == TRUE:
            flag = True
            try:
                while(flag):
                    if Env["BATTERY_LEVEL"] >= 30:
                        if self.Dusty_Spot_Cleaning() == False:
                            Flag == False
                    else:
                        Flag == False
                DONE_GENERAL(Env["GENERAL"])
                return True
            except:
                return False
        else:
            return False

    def Do_Cleaning():
        if Cleaning_Spot() == True:
            return True

        if General_Cleaning() == True:
            return True

        return False

    def Do_Nothing():
        try:
            DO_NOTHING()
            return True
        except:
            return False

    def run():
        while(True):

            if Back_To_Dock() == True:
                return True

            if Do_Cleaning() == True:
                return True

            if Do_Nothing() == True:
                return True

            return False

            sleep(1000)
