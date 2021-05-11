# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    pos = Stack()
    pos.push((problem.getStartState(), []))

    if problem.isGoalState(problem.getStartState()):
        return []
    while True:
        if pos.isEmpty():
            return []
        curPos, path = pos.pop()
        visited.append(curPos)
        if problem.isGoalState(curPos):
            return path
        newPos = problem.getSuccessors(curPos)
        if newPos:
            for alt in newPos:
                if alt[0] not in visited:
                    newPath = path + [alt[1]]
                    pos.push((alt[0], newPath))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    posQueue = Queue()
    posQueue.push((problem.getStartState(), []))

    if problem.isGoalState(problem.getStartState()):
        return []
    while True:
        if posQueue.isEmpty():
            return []
        curPos, path = posQueue.pop()
        visited.append(curPos)
        if problem.isGoalState(curPos):
            return path
        curPos = problem.getSuccessors(curPos)
        if curPos:
            for newPos in curPos:
                if newPos[0] not in visited and newPos[0] not in (state[0] for state in posQueue.list):
                    newPath = path + [newPos[1]]
                    posQueue.push((newPos[0], newPath))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    posQueue = PriorityQueue()
    posQueue.push((problem.getStartState(), []), 0)

    if problem.isGoalState(problem.getStartState()):
        return []
    while True:
        if posQueue.isEmpty():
            return []
        curPos, path = posQueue.pop()
        visited.append(curPos)
        if problem.isGoalState(curPos):
            return path
        curPos = problem.getSuccessors(curPos)
        if curPos:
            for newPos in curPos:
                if newPos[0] not in visited and (
                        newPos[0] not in (state[2][0] for state in posQueue.heap)):
                    newPath = path + [newPos[1]]
                    p = problem.getCostOfActions(newPath)
                    posQueue.push((newPos[0], newPath), p)
                elif newPos[0] not in visited and (
                        newPos[0] in (state[2][0] for state in posQueue.heap)):
                    for state in posQueue.heap:
                        if state[2][0] == newPos[0]:
                            oldP = problem.getCostOfActions(state[2][1])
                    newP = problem.getCostOfActions(path + [newPos[1]])
                    if oldP > newP:
                        newPath = path + [newPos[1]]
                        posQueue.update((newPos[0], newPath), newP)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


class priorityQueue(PriorityQueue):
    def __init__(self, problem, priority):
        self.problem = problem
        self.priority = priority
        PriorityQueue.__init__(self)

    def push(self, alt, heuristic):
        PriorityQueue.push(self, alt, self.priority(self.problem, alt, heuristic))


def f(problem, state, heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0], problem)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    pos = priorityQueue(problem, f)
    if problem.isGoalState(problem.getStartState()):
        return []
    pos.push((problem.getStartState(), []), heuristic)
    while True:
        if pos.isEmpty():
            return []
        curPos, path = pos.pop()
        if curPos in visited:
            continue
        visited.append(curPos)
        if problem.isGoalState(curPos):
            return path
        newPos = problem.getSuccessors(curPos)
        if newPos:
            for alt in newPos:
                if alt[0] not in visited:
                    newPath = path + [alt[1]]
                    pos.push((alt[0], newPath), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
