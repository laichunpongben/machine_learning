import numpy as np
import random

class TestCase:
    def __init__(self):
        self.n = 100
        self.d = 2
        self.p0 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.p1 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.weights = [0 for x in range(self.d+1)]
        self.training_set = [0 for x in range(self.n)]
        self.threshold = 0
        self.learning_rate = 1
        
        for i in range(self.n):
            x = tuple([1] + [random.uniform(-1,1) for x in range(self.d)])
            y = self.target_function(x)
            self.training_set[i] = (x, y)

    def target_function(self, x):
        v1 = (self.p1[1] - self.p0[1], self.p1[2] - self.p0[2])
        v2 = (self.p1[1] - x[1], self.p1[2] - x[2])
        xp = v1[0]*v2[1]-v1[1]*v2[0]
        return np.sign(xp)
        
    def hypothesis_function(self, x):
        return np.sign(np.dot(x, self.weights))       

    def train(self):
        iteration = 0
        while iteration < 1000:
            iteration += 1
            error_count = 0
            misclassified_x = {}
            for x, y in self.training_set:
                hx = self.hypothesis_function(x)
                error = y - hx
                if error != 0:
                    error_count += 1
                    misclassified_x[x] = error
            if error_count > 0:
                update_x = random.choice(list(misclassified_x.keys()))
                epsilon = misclassified_x[update_x]
                self.weights = [w + self.learning_rate * epsilon * x for w, x in zip(self.weights, update_x)]
            else:
                break
        return iteration
        
    def estimate_p_learning_error(self, count):
        error_count = 0
        for x in range(count):
            x = tuple([1] + [random.uniform(-1,1) for x in range(self.d)])
            y = self.target_function(x)
            hx = self.hypothesis_function(x)
            if hx != y: error_count += 1
        return (error_count / count)

def learn_repeatedly(test_case_count, p_test_count):
    total_iteration = 0
    total_error_count = 0
    for x in range(test_case_count):
        test_case = TestCase()
        iteration = test_case.train()
        total_iteration += iteration
        
        error_count = test_case.estimate_p_learning_error(p_test_count)*p_test_count
        total_error_count += error_count
        
    print(total_iteration / test_case_count)
    print(total_error_count / test_case_count / p_test_count)
    
learn_repeatedly(1000, 1000)
