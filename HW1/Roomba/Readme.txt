Assignment I - Behavior Tree

Group Member : Yuchen Yang (yyang17@tufts.edu)

Environment : Python 3.7

Usage : Input "python Roomba.py" in terminal or run the Roomba.py in any kind of python IDE.

Description : This project is a homework for Artificial Intelligence assignment I. It use a hierarchy of Nodes to implement different kinds of tasks and judgements which Roomba is going to face when doing cleaning. And those tasks nodes and judgements node were used to build the overall behavior tree.

    - What We assume:
        - Roomba only stop docking when it reached 100% battery level.
        - Roomba doesn't know the path to home or dusty spot, the path is calculated based on its location.
        - Roomba is cleaning in an open space, a random displacement will cause when Roomba is doing cleaning, and Roomba always knows the exact position of itself, base and dusty spots.
        - Roomba lose battery level when doing cleaning, and it lose lesser battery level when doing nothing.
        - Roomba can only either move forward or turn left/right.

    - What We have done:
        - Build a hierarchy of Node Types, implements task and judgements with these node types:
                Node -|--Composite ---- Selection, Sequence, Priority
                      |--Decorator ---- Until, Negation, Timer
                      |--Condition ---- Judge_Battery, Judge_Spot, Judge_General...
                      |--Task      ---- Find_Home, Go_Home, Dock, Clean_Spot....
          Here we used a Node.run() function to run the logic of the node and its childnodes. We also used a Node.NodeStatus Variable to record whether the node is failed, succeed or still running. And judgements of Composite Nodes are made upon these status.

        - Build the whole behavior tree of Roomba using these nodes, the behavior tree will take the global variable env as a blackboard and run its logic.
        - Build algorithms to update the location, battery level of Roomba, and find path according to the location and where Roomba is facing.
        - Build an automatic random environment generating algorithm to simulate real time environment and user input.

    - What the program will do:
        - The program will always running turn after turn.
        - At the beginning of each turn, the algorithm will generate a random blackboard, the blackboard will decide whether the Roomba is going to do a spot cleaning or general cleaning. And it will generate a location (x,y) as the location of the dusty spot. But location and battery level of Roomba in the blackboard will not change.
        - Then the behavior tree will run from the top priority node. It will make judgements, do the tasks and change the conditions based on the blackboard.
        - In the terminal, the program will pprint the blackboard at the start of the behavior tree. It will also print some sentences when doing cleaning and finding paths.

