import heapq
import copy
from flappygame import play
import numpy as np
import math
import random

#Setting parameters initially
crossingoverrate = .9
mutationrate = .05
#Number of generations for which the program is being trained
generations = 50
#Number of NeuralNets being created in each generation
netsize = 20

#values of the weights after successive epochs of running our code
base= [0,0,0,0,0,0]

