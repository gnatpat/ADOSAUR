import numpy as np


def sigmoid(x, derivative=False):
    if derivative:
        return 
    return 1 / (1 + math.exp(-x)) 


class NeuralNet():

    self.UPDATE_CYCLES = 10000

    def run(*X, *Y):
    
        # no hidden layers
        num_inputs = len(X)
        num_outputs = len(Y)

        # weights from layer 0 to layer 1
        syn0 = 2*np.random.random((num_inputs, num_outputs))-1

        for _ in xrange(self.UPDATE_CYCLES):

            l0 = X
            l1 = np.dot(l0, syn0)













