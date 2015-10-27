import numpy as np
import random

class TestCase:
    def __init__(self):
        self.n = 10
        self.d = 2
        self.p0 = [random.uniform(-1,1) for x in range(2)]
        self.p1 = [random.uniform(-1,1) for x in range(2)]
        self.weights = [0 for x in range(self.d)]
        self.training_set = [0 for x in range(self.n)]
        self.threshold = 0
        self.learning_rate = 1

    def target_function(self, point):
        v1 = (self.p1[0] - self.p0[0], self.p1[1] - self.p0[1])
        v2 = (self.p1[0] - point[0], self.p1[1] - point[1])
        xp = v1[0]*v2[1]-v1[1]*v2[0]
        return np.sign(xp)

    def initialize_training_set(self):
        for i in range(self.n):
            x = tuple(random.uniform(-1,1) for x in range(self.d))
            y = self.target_function(x)
            self.training_set[i] = (x, y)

    def learn(self):
        print(self.training_set)
        iteration = 0
        while iteration < 100:
            iteration += 1
            #print('-' * 50)
            #print(iteration)
            error_count = 0
            error_input_vectors = []
            print(self.weights)
            for input_vector, desired_output in self.training_set:
                #print(['%.2f' % x for x in self.weights])
                #print(input_vector)
                result = np.sign(np.dot(input_vector, self.weights) - self.threshold)
                #print('result: '+ str(result))
                error = desired_output - result
                #print('error: ' + str(error))
                if error != 0:
                    error_count += 1
                    error_input_vectors.append(input_vector)
            if error_count > 0:
                print('error count: ' + str(error_count))
                update_vector = random.choice(error_input_vectors)
                #print(update_vector)
                y = self.target_function(update_vector)
                self.weights = [w + self.learning_rate * y * x for w, x in zip(self.weights, update_vector)]
                #print(error, error_count)
            else:
                break
        #print('Iteration: ' + str(iteration))
        return iteration

total_iteration = 0
test_case_count = 0
for x in range(1):
    test_case_count += 1
    test_case = TestCase()
    test_case.initialize_training_set()
    iteration = test_case.learn()
    total_iteration += iteration
    print(test_case.weights)
    print(iteration)
print(total_iteration / test_case_count)
