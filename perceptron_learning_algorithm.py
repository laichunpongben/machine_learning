import numpy as np
import random

class TestCase:
    def __init__(self):
        self.n = 10
        self.d = 2
        self.p0 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.p1 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.weights = [0 for x in range(self.d+1)]
        self.training_set = [0 for x in range(self.n)]
        self.threshold = 0
        self.learning_rate = 1

    def target_function(self, point):
        v1 = (self.p1[1] - self.p0[1], self.p1[2] - self.p0[2])
        v2 = (self.p1[1] - point[1], self.p1[2] - point[2])
        xp = v1[0]*v2[1]-v1[1]*v2[0]
        return np.sign(xp)

    def initialize_training_set(self):
        for i in range(self.n):
            x = tuple([1] + [random.uniform(-1,1) for x in range(self.d)])
            y = self.target_function(x)
            self.training_set[i] = (x, y)

    def learn(self):
        iteration = 0
        while iteration < 1000:
            iteration += 1
            error_count = 0
            misclassified_x = {}
            for x, y in self.training_set:
                hx = np.sign(np.dot(x, self.weights))
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

def learn_repeatedly(count):
    total_iteration = 0
    test_case_count = 0
    for x in range(count):
        test_case_count += 1
        test_case = TestCase()
        test_case.initialize_training_set()
        iteration = test_case.learn()
        total_iteration += iteration
    print(total_iteration / test_case_count)
    
learn_repeatedly(50000)
