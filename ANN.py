import theano.tensor as T
from theano import function
import numpy as np
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x)) 

x = T.scalar()
y = T.scalar()
z = x * y
multi = function([x,y], z)
print multi(3,3)

x = T.matrix()
y = T.matrix()
z = x * y
multi = function([x,y], z)
print multi([[1,2],[3,4]],[[1,2],[3,4]])

a = T.vector()
b = T.vector()
quad = a**2 + 2*a*b + b**2
print quad.eval({a : [0,1,2], b : [0,1,2]})

class NeuralNet():

    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output

    def feed_forward(*inputs):
        assert len(inputs) == num_input


# if __name__ == "__main__":
#     print multi(3,3)