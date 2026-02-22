# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    # -distFantoma + distantaMancare
    # in jurul fontomei sa fie toate -inf si in jurul pacman sa fie +inf unde este mancare
    # adica mereu trb sa aiba cel putin un patrat distanta pacman fata de fantoma
    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # Initialize the score
        score = successorGameState.getScore()

        # Check distance to ghosts
        for ghostState in newGhostStates:
            dist = util.manhattanDistance(newPos, ghostState.getPosition())
            # ghost este prea aproape si NU este scared => scaredTimer > 0 si il poti manca
            if dist < 2 and ghostState.scaredTimer == 0:
                return -float('inf')

        # Calculate distance to the nearest food
        foodList = newFood.asList()
        if foodList:
            min_food_dist = min([util.manhattanDistance(newPos, food) for food in foodList])
            # Adaug min_food_dist + 1 ca sa evit impartirea la 0 cand este min_food_dist == 0
            # Daca dist = 1 => score = 10/2 = 5 ....sau.... dist = 4 => score = 10/5 = 2
            # Deci logic ca va merge spre score-ul mai mare, adica spre distanta mai mica
            score += 10.0 / (min_food_dist + 1)

        # penalizam daca vrea sa stea pe loc
        if action == Directions.STOP:
            score -= 10

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    # min function si max function pt a calcula pt fiecare miscare min si max
    # se evalueaza de jos, si merge in sus cu.. luam MIN dupa luam MAX
    # max(min(a,b), min(c,d))
    # agentIndex = 0 si ghostIndex >= 1
    # fiecare node e un alt game state 
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # functia care se ajuta sa returneze min/max
        def minimax_value(state, agentIndex, currentDepth):
            # conditii de oprire
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)

            # daca e randul lui Pacman (Agent 0) -> MAXIMIZAM
            if agentIndex == 0:
                bestScore = -float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    # urm este prima fantoma (Agent 1), adancimea ramane la fel
                    score = minimax_value(successor, 1, currentDepth)
                    bestScore = max(bestScore, score)
                return bestScore

            # daca e randul Fantomei (Agent >= 1) -> MINIMIZAM
            else:
                bestScore = float('inf')
                numAgents = state.getNumAgents()
                nextAgent = agentIndex + 1
                nextDepth = currentDepth

                # daca am terminat cu ultima fantoma, revenim la Pacman si crestem adancimea
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth += 1

                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax_value(successor, nextAgent, nextDepth)
                    bestScore = min(bestScore, score)
                return bestScore

        # de aici incepe functia propriu zisa

        bestAction = Directions.STOP
        maxScore = -float('inf')

        # iteram prin actiunile posibile a lui Pacman
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = minimax_value(successor, 1, 0)

            if score > maxScore:
                maxScore = score
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # functia ajutatoare cu alfa si beta
        def alpha_beta(state, agentIndex, currentDepth, alpha, beta):

            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)

            # MAXIMIZARE (Pacman -> Agent 0)
            if agentIndex == 0:
                v = -float('inf')
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    # next e prima fantoma (agent1) cu depth la fel
                    v = max(v, alpha_beta(successor, 1, currentDepth, alpha, beta))

                    # PRUNING: daca valoarea e mai mare decat beta, MINIMIZER nu va merge pe calea asta
                    if v > beta:
                        return v

                    alpha = max(alpha, v)
                return v

            # MINIMIZER (Fantome -> Agent >= 1)
            else:
                v = float('inf')
                numAgents = state.getNumAgents()
                nextAgent = agentIndex + 1
                nextDepth = currentDepth

                # daca nu mai is fantome, urmeaza Pacman din nou si crestem adancimea
                if nextAgent == numAgents:
                    nextAgent = 0
                    nextDepth += 1

                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    v = min(v, alpha_beta(successor, nextAgent, nextDepth, alpha, beta))

                    # PRUNING: daca valoarea e mai mica decat alfa, MAXIMIZER nu va merge pe calea asta
                    if v < alpha:
                        return v

                    beta = min(beta, v)
                return v

        # de aici incepe functia propiu zisa

        alpha = -float('inf')
        beta = float('inf')
        bestScore = -float('inf')
        bestAction = Directions.STOP

        # iteram prin actiunile posibile ale lui Pacan
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = alpha_beta(successor, 1, 0, alpha, beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            if bestScore > alpha:
                alpha = bestScore

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
