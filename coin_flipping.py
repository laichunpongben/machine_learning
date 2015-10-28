import numpy as np
import random
from operator import attrgetter
from math import exp

class Coin:
    def __init__(self, p, flip_count):
        self.p_head = p
        self.p_head_estimate = self.flip_repeatedly(flip_count)
        
    def flip(self):
        if random.uniform(0,1) < self.p_head: return 1
        else: return 0
    
    def flip_repeatedly(self, count):
        head_count = 0
        for x in range(count):
            head_count += self.flip()
        return head_count / count
        
class TestCase:
    def __init__(self, p, coin_count):
        coins = [Coin(p, 10) for x in range(coin_count)]
        self.c1 = coins[0]
        self.c_rand = random.choice(coins)
        self.c_min = min(coins, key=attrgetter('p_head_estimate'))
        self.nu1 = self.c1.p_head_estimate
        self.nu_rand = self.c_rand.p_head_estimate
        self.nu_min = self.c_min.p_head_estimate

def run_test(run_count, coin_count, threshold):
    p_head = 0.5
    test_cases = [TestCase(p_head, coin_count) for x in range(run_count)]
    nu1s = []
    nu_rands = []
    nu_mins = []
    hoeffding_upper_bound = 2*exp(-2*coin_count*threshold**2)
    print(hoeffding_upper_bound)
    bad_c1_count = 0
    bad_c_rand_count = 0
    bad_c_min_count = 0
    
    for x in range(run_count):
        nu1s.append(test_cases[x].nu1)
        if abs(nu1s[x]-p_head)>threshold: bad_c1_count += 1
        
        nu_rands.append(test_cases[x].nu_rand)
        if abs(nu_rands[x]-p_head)>threshold: bad_c_rand_count += 1
        
        nu_mins.append(test_cases[x].nu_min)
        if abs(nu_mins[x]-p_head)>threshold: bad_c_min_count += 1
        
    avg_nu1 = np.mean(nu1s)
    avg_nu_rand = np.mean(nu_rands)
    avg_nu_min = np.mean(nu_mins)
    
    print(avg_nu1)
    print(avg_nu_rand)
    print(avg_nu_min)

    p_bad_c1 = bad_c1_count / run_count
    print('c1: ' + str(p_bad_c1) + ',' + str(p_bad_c1 <= hoeffding_upper_bound))
    
    p_bad_c_rand = bad_c_rand_count / run_count
    print('c_rand: ' + str(p_bad_c_rand) + ',' + str(p_bad_c_rand <= hoeffding_upper_bound))
    
    p_bad_c_min = bad_c_min_count / run_count
    print('c_min: ' + str(p_bad_c_min) + ',' + str(p_bad_c_min <= hoeffding_upper_bound))
    
run_test(1000, 1000, 0.02)
