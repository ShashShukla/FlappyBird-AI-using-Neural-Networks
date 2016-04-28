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

######################NEURAL NET CLASS######################
class NeuralNet():
    #Constructor for the class which initializes the parameters of the NeuralNet
    def __init__(self, weights1=None, weights2=None):
        #The number of input, hidden and output nodes is set
        self.inputnodes = 2
        self.hiddennodes = 2
        self.outputnodes = 1
	#If weights are provided in the constructor call, then set them as it is
        if weights1 and weights2:
	    #Weights1 is a set of 2 2-tuples which represents the weights rom the input layer to the hidden layer
            self.weights1 = weights1
	    #Weights2 is represents 2 weights which correspond to the edges from the 2 hidden nodes to the single output node
            self.weights2 = weights2
        else:
            #set the weights randomly around the base value
            self.random()

    #Getting output value for the NeuralNet from the input
    def forward(self, inputvalues):
        #First finding out the value of the hidden layer nodes using the weights from the input layer
        hiddenlayeroutput = self.sigmoid(np.dot(inputvalues, self.weights1))
        #Then finding the value of the output nodes using the weight and values of the hidden layer 
        output = self.sigmoid(np.dot(hiddenlayeroutput, self.weights2))
        return output
	
    #creating the weights of the NeuralNet if no parameters are given while forming the NeuralNet
    def random(self):
        weightslist = []
        for weight in base:
            #Perturbing the weight by an amount proportional to it and also taken from a random triangular distribution
            weightslist.append(weight + random.triangular(weight - .3, weight + .3))
            #Adding the weights to the NeuralNet by using the listtonet function
        self.listtonet(weightslist)

    #Converting the NeuralNet weights into a list
    def nettolist(self):
	#initializing the list to an empty one
	weightslist = []
	#First adding the weights from the input nodes to the hidden nodes
        for i in self.weights1:
            weightslist.extend(i)
        #Then adding the weights from the hidden nodes to the output nodes
	for i in self.weights2:
            weightslist.extend(i)
        return weightslist

    #converts a list of weights to the weight of a NeuralNet
    def listtonet(self, weightslist):
        weights1 = []
        weights2 = []
        count = 0
	#Initially parsing through the list for first filling the values of weights1
        for i in xrange(self.inputnodes):
            n = [] 
            for j in xrange(self.hiddennodes):
                n.append(weightslist[count])
                count += 1
            weights1.append(n)
	#Now parsing through the list for filling the values of weights2
        for i in xrange(self.hiddennodes):
            n = [] 
            for j in xrange(self.outputnodes):
                n.append(weightslist[count])
                count += 1
            weights2.append(n)
	#setting these weights to the NeuralNet
        self.weights1 = weights1
        self.weights2 = weights2

    #Sigmoid funtion returns the value of the sigmoid function the input provided
    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

######################GENETIC ALGORITHM######################

#returns the score (fitness parameter for the evolutionary selection)
#performance= score + distance to next pipe
def performance(n):
    #Parameter 'True' represents playing the game without displaying on screen
    return play(True,n)

#Initialising a list of 'netsize' number of NeuralNets
def oldnetlist():
    netlist=[]
    for i in range (0,netsize):
	#Creating a default NeuralNet with weights randomly distributed around the base value (triangular distribution)
        netelement = NeuralNet()
	#Adding this NeuralNet to the netlist
        netlist.append(netelement)
    return netlist

#Function to crossbreed and mutate the weights of 2 NeuralNets n1 and n2  (basically updating values of weights of n1 and n2)
def updateweights(n1, n2):
    #Initialising a random number and if that number exceeds the crossingover rate then proceeding ahead for crossing over
    #else returning the 2 NeuralNets as it is
    a= random.random()
    if a < crossingoverrate:
        #Creating a list of weights of both the NeuralNets for easy processing ahead
	weightslist1 = np.array(n1.nettolist())
	weightslist2 = np.array(n2.nettolist())
	#Main Crossing over step- We take an element-wise average of the weights of 
	#both the NeuralNets . This incorporates the weights of both the NeuralNets
	#in equal proportion. We make 2 such lists , this is the crossing over step 
	#since we are taking characters from both the NeuralNets that too equally.
	child1 = [i * 0.5 for i in np.add(weightslist1, weightslist2)]
	child2 = [i * 0.5 for i in np.add(weightslist1, weightslist2)]
	#Initialising a random number and if that number exceeds the mutation rate then proceeding ahead for mutation
	#else the child remains as it is
	b= random.random()
	c= random.random()
	if b < mutationrate:
            print "Hi"
            #Randomly picking any one index of the list to be mutated
	    index = random.randint(0, len(child1) - 1)
            #perturbing the value slightly by adding a small component proportional to the original value of the weight
	    #for that index (it is being multiplied by a random number generated from a triangular distribution)
	    #This step is similar to mutation in genetics, where the genome gets randomly perturbed by external mutagens.
	    child1[index] += random.triangular(-1, 1) * child1[index]
	if c < mutationrate:
            print "Hello"
	    index = random.randint(0, len(child2) - 1)
	    child2[index] += random.triangular(-1, 1) * child2[index]
        #After the crossing over and mutation (if any), the list of weights is converted back to weights for the NeuralNets.
	n1.listtonet(child1)
	n2.listtonet(child2)
    return (n1, n2)

#Function which gives a NeuralNet from the genome that has a higher performance associated with it
def survivaloffittest(genome):
    #Selecting 2 random NeuralNets from the genome
    first = genome[random.randint(0, len(genome) - 1)]
    second = genome[random.randint(0, len(genome) - 1)]
    #Returning the NeuralNet having higher performance parameter
    if performance(first) > performance(second):
        return first
    else:
        return second

#Function which updates the genome from every generation to the next 
def newnetlist(genome):
	#Initialising an empty list for the newgenome
	newnetlist = []
	#Sorting the genome (i.e the 'netlist' number of NeuralNets based on their 
	#performance values in descending order
	genome = sorted(genome, key=performance,reverse=True)
	#Selecting the top 1/4th NeuralNets performing the best as it is to the next generation 
	newnetlist.extend(genome[0:5])
	#Now for building the remaining NeuralNets of the newgenome 
	while len(newnetlist) < len(genome):
		#Till the newgenome doesn't have 'netlist' number of NeuralNets
		#Selecting 2 NeuralNets from the genome which have a good performance value by calling
		#the survival of the fittest function defined above
		first = survivaloffittest(genome)
		second = survivaloffittest(genome)
		#For these 2 NeuralNets, now updating their weights by calling the update weights function defined above
		first, second = updateweights(first, second)
                #Adding the updated weight NeuralNets to the newgenome
		newnetlist.append(first)
                newnetlist.append(second)
	return newnetlist


# Running of the main genetic algorithm
#Initialising the genome by calling the oldnetlist function
genome = oldnetlist()
#Iterating over all the generations
for i in range(0,generations):
    print 'GENERATION ' + str(i)
    genome = newnetlist(genome)
    #Playing the game after complete training in every generation
    #Here the play function is called with parameter False which indicates showing it on the screen
    play(False, genome[0])

