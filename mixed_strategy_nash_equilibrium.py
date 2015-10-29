# Payout: 
# 0,0 => A+1
# 1,1 => A+3
# 0,1 or 1,0 => B+2
# Find the mixed strategy Nash equilibrium by reinforcement learning

# Unsolved

import random
from math import exp

strategy_a = 0.5
strategy_b = 0.5
games_payout_a = 0
games_payout_b = 0
games_cards_a = [0, 0]
games_cards_b = [0, 0]
total_game_count = 0
total_game_payout_a = 0
total_game_payout_b = 0

def sample_uniform(p):
    u = random.uniform(0, 1)
    if (u < p): return 0 # card 0
    else: return 1 # card 1

def do_payout(a, b):
    x = a + b
    return {
        0: [1, 0],
        1: [0, 2],
        2: [3, 0],
    }[x]

def play_game(p_a, p_b):
    global games_payout_a
    global games_payout_b
    global games_cards_a
    global games_cards_b
    
    a = sample_uniform(p_a)
    b = sample_uniform(p_b)
    
    if (a == 0): games_cards_a[0] += 1
    else: games_cards_a[1] += 1
    
    if (b == 0): games_cards_b[0] += 1
    else: games_cards_b[1] += 1
    
    payout = do_payout(a, b)
    games_payout_a += payout[0]
    games_payout_b += payout[1]
    
def play_game_set(game_count_in_set):
    for x in range(game_count_in_set):
        play_game(strategy_a, strategy_b)
    p_a = estimate_rival_strategy(games_cards_a, game_count_in_set)
    p_b = estimate_rival_strategy(games_cards_b, game_count_in_set)
    avg_payout_a = games_payout_a / game_count_in_set
    avg_payout_b = games_payout_b / game_count_in_set
    update_strategy_a(avg_payout_a, p_b)
    update_strategy_b(avg_payout_b, p_a)
    update_total_game_count(game_count_in_set)
    update_total_game_payout_a(games_payout_a)
    update_total_game_payout_b(games_payout_b)
    reset_game_set()
    
def estimate_rival_strategy(games_cards, game_count):
    return games_cards[0] / game_count
        
def update_strategy_a(avg_payout_a, p_b):
    global strategy_a
    d = exp(- 0.00001 * total_game_count)
    new_strategy_a = 0
    payout_history_a = 0
    if (total_game_count > 0): total_game_payout_a / total_game_count
    
    if (avg_payout_a > payout_history_a and p_b < 0.5): new_strategy_a = strategy_a * 0.1
    elif (avg_payout_a > payout_history_a and p_b > 0.5): new_strategy_a = strategy_a * 0.1 + 0.9
    elif (avg_payout_a < payout_history_a and p_b < 0.5): new_strategy_a = strategy_a * 0.8 + 0.1
    elif (avg_payout_a < payout_history_a and p_b > 0.5): new_strategy_a = strategy_a * 0.8 + 0.1
    
    strategy_a = (1 - d) * strategy_a + d * new_strategy_a
    if (strategy_a < 0): strategy_a = 0
    if (strategy_a > 1): strategy_a = 1
    
def update_strategy_b(avg_payout_b, p_a):
    global strategy_b
    d = exp(- 0.00001 * total_game_count)
    new_strategy_b = 0
    payout_history_b = 0
    if (total_game_count > 0): payout_history_b = total_game_payout_b / total_game_count
    
    if (avg_payout_b > payout_history_b and p_a < 0.5): new_strategy_b = strategy_b * 0.1 + 0.9
    elif (avg_payout_b > payout_history_b and p_a > 0.5): new_strategy_b = strategy_b * 0.1
    elif (avg_payout_b < payout_history_b and p_a < 0.5): new_strategy_b = strategy_b * 0.8 + 0.1
    elif (avg_payout_b < payout_history_b and p_a > 0.5): new_strategy_b = strategy_b * 0.8 + 0.1
    
    strategy_b = (1 - d) * strategy_b + d * new_strategy_b
    if (strategy_b < 0): strategy_b = 0
    if (strategy_b > 1): strategy_b = 1
    
def update_total_game_count(count):
    global total_game_count
    total_game_count += count
    
def update_total_game_payout_a(payout):
    global total_game_payout_a
    total_game_payout_a += payout
    
def update_total_game_payout_b(payout):
    global total_game_payout_b
    total_game_payout_b += payout
    
def reset_game_set():
    global games_payout_a
    global games_payout_b
    global games_cards_a
    global games_cards_b
    
    games_payout_a = 0
    games_payout_b = 0
    games_cards_a = [0, 0]
    games_cards_b = [0, 0]
            
def learn():
    global strategy_a
    global strategy_b
    strategy_a = random.uniform(0, 1)
    strategy_b = random.uniform(0, 1)
    
    for x in range(500):
        play_game_set(100)    

def report():
    print('% 1.0f' % total_game_count)
    print('% 1.6f' % strategy_a)
    print('% 1.6f' % strategy_b)
    print('% 1.0f' % total_game_payout_a)
    print('% 1.0f' % total_game_payout_b)
    avg_payout_a = total_game_payout_a / total_game_count
    avg_payout_b = total_game_payout_b / total_game_count
    avg_payout = (total_game_payout_a + total_game_payout_b) / total_game_count
    print('% 1.6f' % avg_payout_a)
    print('% 1.6f' % avg_payout_b)
    print('% 1.6f' % avg_payout)

learn()
report()
