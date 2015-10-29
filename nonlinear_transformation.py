import numpy as np
import random

class TestCase:
    def __init__(self):
        self.n = 1000
        self.d = 2
        self.p0 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.p1 = [1] + [random.uniform(-1,1) for x in range(2)]
        self.w = [0 for x in range(self.d+1)]
        self.X = np.array([[1] + [random.uniform(-1,1) for x in range(self.d)] for x in range(self.n)])
        self.y = np.array([self.target_function(x) for x in self.X])
        self.learning_rate = 0.1
        self.p_noise = 0.1
        
        noise = np.array([-1 if random.uniform(0,1) < self.p_noise else 1])
        self.y = self.y * noise 
        
    def target_function(self, x):
        return np.sign(x[1]**2+x[2]**2-0.6)
        
    def hypothesis_function(self, x):
        return np.sign(np.dot(x, self.w))
        
    def train(self):
        x_pinv = np.linalg.pinv(self.X)
        self.w = np.dot(x_pinv, self.y)
        
    def estimate_p_training_error(self):
        hx = [self.hypothesis_function(x) for x in self.X]
        error = [a - b for a,b in zip(hx, self.y)]
        return sum(1 for d in error if d != 0) / self.n
        
    def estimate_p_test_error(self, count):
        error_count = 0
        for x in range(count):
            x1 = random.uniform(-1,1)
            x2 = random.uniform(-1,1)
            x = tuple([1] + [x1, x2, x1*x2, x1**2, x2**2])
            y = self.target_function(x)
            hx = self.hypothesis_function(x)
            if hx != y: error_count += 1
        return (error_count / count)
        
    def transform_x(self):
        x1x2 = np.array([x[1]*x[2] for x in self.X])
        x1x1 = np.array([x[1]*x[1] for x in self.X])
        x2x2 = np.array([x[2]*x[2] for x in self.X])
        self.X = np.column_stack([self.X, x1x2, x1x1, x2x2])
        
        self.w = self.w + [0 for x in range(3)]
        
def learn_repeatedly(test_case_count):
    p_training_error = 0
    p_test_error = 0
    for x in range(test_case_count):
        test_case = TestCase()
        test_case.transform_x()
        test_case.train()
        p_training_error += test_case.estimate_p_training_error()
        p_test_error += test_case.estimate_p_test_error(1000)

    print('P training error: ' + str(p_training_error / test_case_count))
    print('P test error: ' + str(p_test_error / test_case_count))
    print(test_case.w)
        
learn_repeatedly(1000)
