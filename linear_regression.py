import numpy as np
import random

class TestCase:
    def __init__(self):
        self.n = 10
        self.d = 2
        self.p0 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.p1 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.w = [0 for x in range(self.d+1)]
        self.X = np.array([[1] + [random.uniform(-1,1) for x in range(self.d)] for x in range(self.n)])
        self.y = [self.target_function(x) for x in self.X]
        self.learning_rate = 0.1

    def target_function(self, x):
        v1 = (self.p1[1] - self.p0[1], self.p1[2] - self.p0[2])
        v2 = (self.p1[1] - x[1], self.p1[2] - x[2])
        xp = v1[0]*v2[1]-v1[1]*v2[0]
        return np.sign(xp)
        
    def hypothesis_function(self, x):
        return np.sign(np.dot(x, self.w))       

    def train(self):
        x_pinv = np.linalg.pinv(self.X)
        self.w = np.dot(x_pinv, self.y)
        
    def estimate_p_training_error(self):
        hx = [self.hypothesis_function(x) for x in self.X]
        error = [a - b for a,b in zip(hx, self.y)]
        return sum(1 for d in error if d != 0) / self.n
        
    def estimate_p_learning_error(self, count):
        error_count = 0
        for x in range(count):
            x = tuple([1] + [random.uniform(-1,1) for x in range(self.d)])
            y = self.target_function(x)
            hx = self.hypothesis_function(x)
            if hx != y: error_count += 1
        return (error_count / count)
        
    def train_pla(self):
        iteration = 0
        while iteration < 500:
            iteration += 1
            error_count = 0
            misclassified_x = {}
            for i in range(len(self.X)):
                hx = self.hypothesis_function(self.X[i])
                y = self.y[i]
                error = y - hx
                if error != 0:
                    error_count += 1
                    misclassified_x[i] = error
            if error_count > 0:
                update_index = random.choice(list(misclassified_x.keys()))
                epsilon = misclassified_x[update_index]
                self.w = [w + self.learning_rate * epsilon * x for w, x in zip(self.w, self.X[update_index])]
                #print(self.w)
            else:
                break
        return iteration

def learn_repeatedly(test_case_count):
    p_training_error = 0
    p_learning_error = 0
    total_iteration_pla = 0
    for x in range(test_case_count):
        test_case = TestCase()
        test_case.train()
        p_training_error += test_case.estimate_p_training_error()
        p_learning_error += test_case.estimate_p_learning_error(100)
        
        iteration = test_case.train_pla()
        total_iteration_pla += iteration
        
    print('P training error: ' + str(p_training_error / test_case_count))
    print('P learning error: ' + str(p_learning_error / test_case_count))
    print('Iteration: ' + str(total_iteration_pla / test_case_count))
        
learn_repeatedly(1000)
