# Pirate Game
# Each pirate finds the strategy to maximize his own long run payoff by unsupervised learning
# For the common game description: https://en.wikipedia.org/wiki/Pirate_game

from math import exp

class Pirate:
    def __init__(self, rank):
        self.life = True
        self.priority = rank
        self.payoffThreshold = [0 for x in range(5)] # need learning
        self.proposal = [0 for x in range(5)] # need learning
        
    def is_alive(self):
        return self.life
        
    def dead(self):
        self.life = False
        
    def propose_payoff(self):
        return self.proposal
        
    def vote_proposal(self, payoff, proposalNo):
        if (payoff >= self.payoffThreshold[proposalNo]): return 1
        else: return 0
        
    def adjust_payoff_threshold(self, shortRunAvgPayoff, longRunAvgPayoff, magnitude):
        if (shortRunAvgPayoff <= longRunAvgPayoff): 
            adjustment = [0 for x in range(5)]
            for x in range(5):
                if (self.payoffThreshold[x] > 33): adjustment[x] = magnitude * -1
                else: adjustment[x] = magnitude
            self.payoffThreshold = [sum(x) for x in zip(self.payoffThreshold, adjustment)]
        else:
            adjustment = [0 for x in range(5)]
            for x in range(5):
                if (self.payoffThreshold[x] > 33): adjustment[x] = magnitude * 3
                else: adjustment[x] = magnitude * -3
            self.payoffThreshold = [sum(x) for x in zip(self.payoffThreshold, adjustment)]
            
        thresholdLowerBounds = [0 for x in range(5)]
        thresholdUpperBounds = [gold for x in range(5)]
        self.payoffThreshold = [max(x) for x in zip(self.payoffThreshold, thresholdLowerBounds)]
        self.payoffThreshold = [min(x) for x in zip(self.payoffThreshold, thresholdUpperBounds)]
        
    def adjust_proposal(self, shortRunAvgPayoff, longRunAvgPayoff, magnitude):
        initialize_proposals()
        
totalGameCount = 0
pirates = [0 for x in range(5)]
gold = 100
totalPayoffs = [0 for x in range(5)]

def initialize():
    initialize_pirates()
    initialize_payoff_thresholds()
    initialize_proposals()

def initialize_pirates():
    global pirates
    for x in range(5):
        pirates[x] = Pirate(5 - x)

def initialize_payoff_thresholds():
    global pirates
    pirates[0].payoffThreshold = [40, 0, 0, 0, 0]
    pirates[1].payoffThreshold = [40, 50, 0, 0, 0]
    pirates[2].payoffThreshold = [30, 40, 50, 0, 0]
    pirates[3].payoffThreshold = [15, 30, 40, 100, 0]
    pirates[4].payoffThreshold = [15, 15, 20, 1, 100]

def initialize_proposals():
    global pirates
    pirates[0].proposal = [pirates[0].payoffThreshold[0], 0, (gold - pirates[0].payoffThreshold[0]) / 2, 0, (gold - pirates[0].payoffThreshold[0]) / 2]
    pirates[1].proposal = [0, pirates[1].payoffThreshold[1], 0, 0, (gold - pirates[1].payoffThreshold[1])]
    pirates[2].proposal = [0, 0, pirates[2].payoffThreshold[2], 0, (gold - pirates[2].payoffThreshold[2])]
    pirates[3].proposal = [0 for x in range(3)] + [gold, 0]
    pirates[4].proposal = [0 for x in range(4)] + [gold]
    
def reset_life():
    global pirates
    for x in range(len(pirates)):
        pirates[x].life = True
    
def count_alive_pirates():
    count = 0
    for x in range(len(pirates)):
        if (pirates[x].is_alive()): count += 1
    return count
    
def play_game():
    global totalGameCount
    global pirates
    
    totalGameCount += 1
    print("Game " + str(totalGameCount))
    
    reset_life()
    payoffs = [0 for x in range(len(pirates))]

    print("Thresholds")
    for x in range(len(pirates)):
        print(["%0.2f" % a for a in pirates[x].payoffThreshold])

    for x in range(len(pirates)):
        proposal = pirates[x].propose_payoff()
        print("Proposal " + str(x))
        print(["%0.2f" % a for a in proposal])
        vote = 0
        votes = [0 for x in range(len(pirates))]
        for y in range(len(pirates)):
            if (pirates[y].is_alive):
                votes[y] = pirates[y].vote_proposal(proposal[y], x) 
                vote += pirates[y].vote_proposal(proposal[y], x)
        print("Votes = " + str(votes))
        if (vote >= count_alive_pirates() / 2):
            payoffs = proposal
            break
        else: pirates[x].dead()
    print("Choice = " + str(x))
    print(' ')
    return payoffs
        
def play_game_set(count):
    global totalPayoffs
    gameSetPayoffs = [0 for x in range(len(pirates))]
    for x in range(count):
        payoffs = play_game()
        totalPayoffs = [sum(x) for x in zip(totalPayoffs, payoffs)]
        gameSetPayoffs = [sum(x) for x in zip(gameSetPayoffs, payoffs)]
    avgPayoffs = [x / count for x in gameSetPayoffs]
    return avgPayoffs

def adjust_strategies(shortRunAvgPayoffs, longRunAvgPayoffs):
    global pirates
    adjMagnitude = exp(-0.0001 * totalGameCount)
    for x in range(len(pirates)):
        pirates[x].adjust_payoff_threshold(shortRunAvgPayoffs[x], longRunAvgPayoffs[x], adjMagnitude)
        pirates[x].adjust_proposal(shortRunAvgPayoffs[x], longRunAvgPayoffs[x], adjMagnitude)
        
def learn():
    initialize()
    for x in range(5000):
        avgPayoffs = play_game_set(1)
        longRunAvgPayoffs = [x / totalGameCount for x in totalPayoffs]
        adjust_strategies(avgPayoffs, longRunAvgPayoffs)

def report():
    equilibriumPayoffs = [x / totalGameCount for x in totalPayoffs]
    print("Equilibrium Payoffs")
    print(["%0.2f" % x for x in equilibriumPayoffs])
    equilibriumPayoffThresholds = [x.payoffThreshold for x in pirates]
    print("Equilibrium Payoff Thresholds")
    for x in range(len(pirates)):
        print(["%0.2f" % y for y in equilibriumPayoffThresholds[x]])
    print("Equilibrium Proposals")
    equilibriumProposals = [x.proposal for x in pirates]
    for x in range(len(pirates)):
        print(["%0.2f" % y for y in equilibriumProposals[x]])

learn()
report()
