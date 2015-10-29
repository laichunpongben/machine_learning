# Pirate Game
# Each pirate finds the strategy to maximize his own long run payoff by unsupervised learning
# For the common game description: https://en.wikipedia.org/wiki/Pirate_game

# Not finished

from math import exp

class Pirate:
    def __init__(self, rank):
        self.life = True
        self.priority = rank
        self.payoff_threshold = [0 for x in range(5)] # need learning
        self.proposal = [0 for x in range(5)] # need learning
        
    def is_alive(self):
        return self.life
        
    def dead(self):
        self.life = False
        
    def propose_payoff(self):
        return self.proposal
        
    def vote_proposal(self, payoff, proposal_no):
        if (payoff >= self.payoff_threshold[proposal_no]): return 1
        else: return 0
        
    def adjust_payoff_threshold(self, short_run_avg_payoff, long_run_avg_payoff, magnitude):
        if (short_run_avg_payoff <= long_run_avg_payoff): 
            adjustment = [0 for x in range(5)]
            for x in range(5):
                if (self.payoff_threshold[x] > 33): adjustment[x] = magnitude * -1
                else: adjustment[x] = magnitude
            self.payoff_threshold = [sum(x) for x in zip(self.payoff_threshold, adjustment)]
        else:
            adjustment = [0 for x in range(5)]
            for x in range(5):
                if (self.payoff_threshold[x] > 33): adjustment[x] = magnitude * 3
                else: adjustment[x] = magnitude * -3
            self.payoff_threshold = [sum(x) for x in zip(self.payoff_threshold, adjustment)]
            
        threshold_lower_bounds = [0 for x in range(5)]
        threshold_upper_bounds = [gold for x in range(5)]
        self.payoff_threshold = [max(x) for x in zip(self.payoff_threshold, threshold_lower_bounds)]
        self.payoff_threshold = [min(x) for x in zip(self.payoff_threshold, threshold_upper_bounds)]
        
    def adjust_proposal(self, short_run_avg_payoff, long_run_avg_payoff, magnitude):
        initialize_proposals()
        
total_game_count = 0
pirates = [0 for x in range(5)]
gold = 100
total_payoffs = [0 for x in range(5)]

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
    pirates[0].payoff_threshold = [40, 0, 0, 0, 0]
    pirates[1].payoff_threshold = [40, 50, 0, 0, 0]
    pirates[2].payoff_threshold = [30, 40, 50, 0, 0]
    pirates[3].payoff_threshold = [15, 30, 40, 100, 0]
    pirates[4].payoff_threshold = [15, 15, 20, 1, 100]

def initialize_proposals():
    global pirates
    pirates[0].proposal = [pirates[0].payoff_threshold[0], 0, (gold - pirates[0].payoff_threshold[0]) / 2, 0, (gold - pirates[0].payoff_threshold[0]) / 2]
    pirates[1].proposal = [0, pirates[1].payoff_threshold[1], 0, 0, (gold - pirates[1].payoff_threshold[1])]
    pirates[2].proposal = [0, 0, pirates[2].payoff_threshold[2], 0, (gold - pirates[2].payoff_threshold[2])]
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
    global total_game_count
    global pirates
    
    total_game_count += 1
    print("Game " + str(total_game_count))
    
    reset_life()
    payoffs = [0 for x in range(len(pirates))]

    print("Thresholds")
    for x in range(len(pirates)):
        print(["%0.2f" % a for a in pirates[x].payoff_threshold])

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
    global total_payoffs
    game_set_payoffs = [0 for x in range(len(pirates))]
    for x in range(count):
        payoffs = play_game()
        total_payoffs = [sum(x) for x in zip(total_payoffs, payoffs)]
        game_set_payoffs = [sum(x) for x in zip(game_set_payoffs, payoffs)]
    avg_payoffs = [x / count for x in game_set_payoffs]
    return avg_payoffs

def adjust_strategies(short_run_avg_payoffs, long_run_avg_payoffs):
    global pirates
    adj_magnitude = exp(-0.0001 * total_game_count)
    for x in range(len(pirates)):
        pirates[x].adjust_payoff_threshold(short_run_avg_payoffs[x], long_run_avg_payoffs[x], adj_magnitude)
        pirates[x].adjust_proposal(short_run_avg_payoffs[x], long_run_avg_payoffs[x], adj_magnitude)
        
def learn():
    initialize()
    for x in range(5000):
        avg_payoffs = play_game_set(1)
        long_run_avg_payoffs = [x / total_game_count for x in total_payoffs]
        adjust_strategies(avg_payoffs, long_run_avg_payoffs)

def report():
    equilibrium_payoffs = [x / total_game_count for x in total_payoffs]
    print("Equilibrium Payoffs")
    print(["%0.2f" % x for x in equilibrium_payoffs])
    equilibrium_payoff_thresholds = [x.payoff_threshold for x in pirates]
    print("Equilibrium Payoff Thresholds")
    for x in range(len(pirates)):
        print(["%0.2f" % y for y in equilibrium_payoff_thresholds[x]])
    print("Equilibrium Proposals")
    equilibrium_proposals = [x.proposal for x in pirates]
    for x in range(len(pirates)):
        print(["%0.2f" % y for y in equilibrium_proposals[x]])

learn()
report()
