import numpy as np


# vanilla sigmoid function
def sigmoid(x, derivative=False):
    if derivative:
        return sigmoid(x) * (1 - sigmoid(x))
    return 1 / (1 + np.exp(-x))


class NeuralNet():

    def __init__(self, num_inputs, num_outputs, eta=0.1):
        # user determined
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.eta = eta

        # common to all
        self.weights = 2 * np.random.rand(num_inputs, num_outputs) - 1
        self.UPDATE_CYCLES = 200

    def learn_from(self, input, expected_output):
        # takes input vector x and adjusts weights according to y

        for iteration in range(self.UPDATE_CYCLES):

            # forward propagation
            actual_output = sigmoid(np.dot(input, self.weights))

            # compute error
            error = expected_output - actual_output

            # weight change vector by certainty
            delta = error * sigmoid(actual_output, True)

            # update weights
            self.weights += self.eta * np.dot(input.T, delta)

            if iteration % 50 == 0:
                print "Iteration:", iteration
                print np.around(actual_output)
                print  # new line

        return actual_output

# input
X = np.array([ [0,0,1],
               [0,1,1],
               [1,0,1],
               [1,1,1] ])

# output
y = np.array([[0,0,1,1], [0,0,0,1], [1,1,1,0]]).T

# create net and test output
net = NeuralNet(3,3)
net.learn_from(X,y)
