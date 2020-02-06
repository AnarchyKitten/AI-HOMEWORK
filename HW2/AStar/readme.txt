Assignment II - A star Algorithm and UCS Bonus

Group Member : Yuchen Yang (yyang17@tufts.edu)

Environment : Python 3.7

Usage :
    (Please run this program through terminal!)

    Input "python Astar.py -i <input_state> -a <algorithm>" in terminal to run the algorithm and see the steps.
    - <input_state> is a list of digits separated by commas that used to describe the initial order of pancakes. Start from the top and End with the bottom.
    - <algorithm> is what algorithm we are going to use to solve the problem.

    The program will calculate the solution if possible, it will then print the detailed steps of solution.

Usage Example:
    "python Astar.py -i 3,1,4,5,2 -a astar"

    "python Astar.py -i 2,1,5,4,3 -a ucs"

Description :
    This project is a homework for Artificial Intelligence assignment II. It use both AStar and UCS algorithm to solve the pancake sorting problem.

    - Our Approach to the problem :
        - AStar Algorithm :
            - Heuristic Function : The number of stack positions for which the pancake at that position is not of adjacent size to the pancake below.
            - Cost Function : Number of flips to reach that node from initial state.
            - Steps :
                Add initial state into a Priority Queue as the root node
                While (solution not found):
                    If priority queue empty:
                        Return Failure
                    Pop out the node with smallest F(n) = g(n) + h(n)
                    Extend the node and add all its children into the priority queue
                    sort the priority queue based on F(n)
                Print the solution

        - UCS Algorithm :
            - Steps :
                - Cost of Node : Number of flips to reach that node from initial state.
                    Add initial state into a Priority Queue as the root node
                    While (solution not found):
                        If priority queue empty:
                            Return Failure
                        Pop out the node with smallest cost
                        Extend the node and add all its children into the priority queue
                        sort the priority queue based on the cost of node
                    Print the solution