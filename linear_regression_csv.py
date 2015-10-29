import csv
import numpy as np

class TestCase:
    def __init__(self):
        dataset_file = "dataset.csv"
        self.col_count = 47
        self.training_data_count = 10000
        self.training_set = np.loadtxt(open(dataset_file,"rb"),delimiter=",",skiprows=1)
        self.test_set = np.loadtxt(open(dataset_file,"rb"),delimiter=",",skiprows=self.training_data_count+1)
        self.X = self.training_set[:self.training_data_count,1:self.col_count-1]
        self.y = self.training_set[:self.training_data_count,self.col_count-1]
        self.X_pinv = np.linalg.pinv(self.X)
        self.w = np.dot(self.X_pinv, self.y)
        self.header = next(csv.reader(open(dataset_file)))[1:self.col_count-1]

    def g(self, x):
        return np.dot(x, self.w)
        
    def estimate_training_error(self):
        error = 0
        for i in range(len(self.y)):
            error += (self.y[i] - self.g(self.X[i]))**2
        return (error / len(self.y))**0.5
        
    def estimate_test_error(self):
        error = 0
        X = self.test_set[:,1:self.col_count-1]
        y = self.test_set[:,self.col_count-1]
        for i in range(len(y)):
            error += (y[i] - self.g(X[i]))**2
        return (error / len(y))**0.5

test_case = TestCase()
result = [h + ': ' + '%.4f' % w for h,w in zip(test_case.header, test_case.w)]

print('Result hypothesis weights:')
for x in result: print(x)

print('-'*60)
print('Training error: ' + '%.4f' % test_case.estimate_training_error())
print('Test error: ' + '%.4f' % test_case.estimate_test_error())
