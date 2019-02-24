
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # print(self.currentState.state[0])
        # print(self.currentState.state[1])
        # print(self.currentState.state[2])
        # print('')

        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True

        moves = self.gm.getMovables()

        if moves:
            for move in moves:
                self.gm.makeMove(move)
                new_child = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                if new_child not in self.visited:
                    new_child.parent = self.currentState
                    self.currentState.children.append(new_child)
                self.gm.reverseMove(move)

        if self.currentState.children:
            self.visitNextChild()
        else:
            self.findNextChild()

    def findNextChild(self):

        while self.currentState.nextChildToVisit < len(self.currentState.children):
            child = self.currentState.children[self.currentState.nextChildToVisit]
            if child not in self.visited:
                self.visitNextChild()
                return

        self.unvisit()

    def unvisit(self):

        # return to parent if no unvisited moves in children
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        self.findNextChild()

    def visitNextChild(self):

        self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
        self.currentState.parent.nextChildToVisit += 1
        self.gm.makeMove(self.currentState.requiredMovable)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True

        if self.currentState.depth == 0:
            self.populate_children()
            self.visitNextChild()
        elif self.currentState.parent.nextChildToVisit < len(self.currentState.parent.children):
            # return to parent
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.visitNextChild()
        else:
            self.common_root()

    def populate_children(self):
        moves = self.gm.getMovables()
        if moves:
            for move in moves:
                self.gm.makeMove(move)
                new_child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                if new_child not in self.visited:
                    new_child.parent = self.currentState
                    self.currentState.children.append(new_child)
                self.gm.reverseMove(move)

    def common_root(self):
        while self.currentState.depth > 0:
            if self.currentState != self.currentState.parent.children[-1]:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                break
            self.currentState.nextChildToVisit = 0
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.currentState.nextChildToVisit = 0
        self.find_next_child()

    def find_next_child(self):
        while self.currentState.nextChildToVisit < len(self.currentState.children):
            self.visitNextChild()
            if not self.currentState.children:
                self.populate_children()
            if self.currentState.children:
                if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                    self.visitNextChild()
                    return
            else:
                self.unvisit()

    def unvisit(self):
        # return to parent
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        self.find_next_child()

    def visitNextChild(self):
        self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
        self.currentState.parent.nextChildToVisit += 1
        self.gm.makeMove(self.currentState.requiredMovable)
