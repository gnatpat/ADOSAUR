import numpy as np


# vanilla sigmoid function
def sigmoid(x, derivative=False):
    if derivative:
        return sigmoid(x) * (1 - sigmoid(x))
    return 1 / (1 + np.exp(-x))


class ANN(object):

    def __init__(self, num_hidden, num_inputs=2267, num_outputs=46, eta=0.1, cycles=100):
        # user determined
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.eta = eta
        self.cycles = cycles

        # common to all
        self.syn0 = 2 * np.random.rand(num_inputs, num_hidden) - 1  # input - hidden weights
        self.syn1 = 2 * np.random.rand(num_hidden, num_outputs) - 1  # hidden - output weights

    def learn_from(self, input, expected_output):
        # takes input vector x and adjusts weights according to y

        for iteration in range(self.cycles):

            # forward propagation
            l0 = input  # input layer
            l1 = sigmoid(np.dot(input, self.syn0))  # hidden layer
            l2 = sigmoid(np.dot(l1, self.syn1))  # output layer

            # compute error
            l2_error = expected_output - l2

            # weight change vector by certainty
            l2_delta = l2_error * sigmoid(l2, True)

            # calculate contribution of error for each hidden node
            l1_error = l2_delta.dot(self.syn1.T)

            # weight error contribution by certainty
            l1_delta = l1_error * sigmoid(l1, True)

            # update weights
            self.syn1 += self.eta * np.dot(l1.T, l2_delta)
            self.syn0 += self.eta * np.dot(l0.T, l1_delta)

            # if iteration % 10 == 0:
            #     print "Training Error:\t", np.mean(np.abs(l2_error))

        return l2, l2_error  # output layer

    def run(self, input, expected_output):
        output = sigmoid(np.dot(sigmoid(np.dot(input, self.syn0)),self.syn1))
        error = expected_output - output
        return output, np.mean(np.abs(error))

# # input
# X = np.array([ [0,0,1],
#                [0,1,1],
#                [1,0,1],
#                [1,1,1] ])

# # output
# y = np.array([[0,0,0,1],[0,1,1,0]]).T

# # create net and test output
# net = ANN(5, num_inputs=3,num_outputs=2)
# net.learn_from(X,y)

# # print net.run(np.array([[0,1,1]]))
