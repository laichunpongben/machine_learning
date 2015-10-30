# A deck with 26 red and 26 black.
# Payoff: Red = +1, Black = -1
# Can stop any time. 
# Find the best strategy

# Stop when payoff reach k and remaining cards only x left

import random

class Deck:
    def __init__(self, plus, minus):
        self.plus_cards = plus
        self.minus_cards = minus

    def draw(self):
        deck_count = self.plus_cards + self.minus_cards
        if deck_count > 0:
            p_plus = self.plus_cards / deck_count
            if random.uniform(0,1) < p_plus: 
                self.plus_cards += -1
                return 1
            else:
                self.minus_cards += -1
                return -1
        else:
            return 0
            
def terminate_condition(deck, payoff):
    deck_count = deck.plus_cards + deck.minus_cards
    if deck_count == 0: return True
    elif payoff > 3: return True
    else: False
            
def play_game(terminate_condition_method, *args):
    payoff = 0
    deck = Deck(26,26)
    while not(terminate_condition_method(*args)):
        payoff += deck.draw()
    return payoff

def play_many_games(count):
    total_payoff = 0
    for x in range(count):
        total_payoff += play_game(terminate_condition(deck, payoff))
    return total_payoff / count

print(play_many_games(10000))
