Assignment III - Using CSP (Backtracking and Backjumping) to solve Sudoku Problem

Group Member : Yuchen Yang (yyang17@tufts.edu)

Environment : Python 3.7

Usage :
    (Please run this program through terminal!)
    1. Download "easy.txt", "evil.txt", "Sudoku.py" to the same dictionary.

    2. Input "Sudoku.py -i <input_state> -a <algorithm>" in terminal to run the algorithm and see the result.
        - <input_state> (easy or evil) these are two puzzles that already saved in the form of txt.
        - <algorithm> (backtracking or backjumping) is what algorithm we are going to use to solve the problem.

    3. The program will calculate the solution if possible, it will then print the detailed steps of solution. The backtracking use about 9000 steps to solve evil puzzle, while backjumping use about 2000 steps.

Usage Example:
    "python sudoku.py -i easy -a backjumping"

    "python sudoku.py -i evil -a backtracking"

Description :
    This project is a homework for Artificial Intelligence assignment III. It use both Backtracking and Backjumping to solve the Sudoku problem.

    - Our Approach to the problem :
        - 1. Backtracking :
            - Organization of The Solution:
                State of Sudoku:
                    1. We use three lists of lists of number to save every number in the 9x9 space, which represent the 9 lines, 9 columns and 9 units of the Sudoku Problem.
                    2. When a empty block is assigned a value, we update all of its existence in line, column and unit.
                    3. This help us to judge whether a new value satisfied the constraints or not.
                    4. When all the blocks in Sudoku are not empty, and all constraints are satisfied, the Sudoku problem is solved.
                Queue of possible extensions:
                    1. We use a queue to hold the possible new state of the problem, each object inside is [a state of Sudoku, how many blocks filled]
                    2. Each time we pop out the state that has the fewest empty blocks, and put all possible new states in the queue.

            - Steps : (Use DFS to solve the problem)
                Add initial state into the Queue as the root node
                While (solution not found):
                    If priority queue empty:
                        Return Failure
                    Pop out the state with most block filled.
                    Extend the state: Pick the next empty block and add all its possible children which satisfied the constraints into the state queue.
                Print the solution

        - 2. Backjumping :
            - Organization of The Solution:
                State of Sudoku:
                    1. We use three lists of lists of number to save every number in the 9x9 space, which represent the 9 lines, 9 columns and 9 units of the Sudoku Problem.
                    2. When a empty block is assigned a value, we update all of its existence in line, column and unit.
                    3. This help us to judge whether a new value satisfied the constraints or not.
                    4. When all the blocks in Sudoku are not empty, and all constraints are satisfied, the Sudoku problem is solved.
                    5. Besides, we use a list of list of list to save the conflict sets of every block. The list contains [the value assigned in related block, the position of related block]
                Queue of possible extensions:
                    1. We use a queue to hold the possible new state of the problem, each object inside is [a state of Sudoku, last block assigned]
                    2. Each time we pop out the state that has the fewest empty blocks, and put all possible new states in the queue.
                    3. When the state we pop out has no possible value, we jumped back to state before the last valid value assigned the affected the conflict set.

            - Steps : (Use DFS with backjumping to solve the problem)
                Add initial state into the Queue as the root node
                While (solution not found):
                    If priority queue empty:
                        Return Failure
                    Pop out the state with most block filled.
                    If no possible value remained, we jumped back to state before the last valid value assigned the affected the conflict set. Remove all state after that.
                    Extend the state: Pick the next empty block and add all its possible children which satisfied the constraints into the state queue.
                Print the solution