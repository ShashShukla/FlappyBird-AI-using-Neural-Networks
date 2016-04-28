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

#values of the weights after successive epochs of running our code (evolving as our program learns)

#base=[0,0,0,0,0,0]
#base = [0.042519551127491853, 0.026843709686133501, -0.050357254741919544, 0.085670010174344974, 0.031663501503816416, -0.084773869448002651]
#base = [0.09020933928636754, 0.069721555189387621, -0.10456483366263267, 0.15611939309709491, 0.080371307962302158, -0.2799036720745971]
#base = [-0.008519243330074033, -0.0061281699701674075, -0.06360857528267838, -0.14224203608252706, -0.033626132263882225, 0.1706027141463319]
#base = [-0.012027221898312094, - 0.024197030996745333, -0.12981616350320127, -0.27641178170974701, -0.11187500423124713, 0.41251407008711333]
#base = [-0.030158449535774418, -0.032174969583628574, -0.15561397810608851, -0.38055329130672638, -0.1117135741338017, 0.30910123984699178]
#base = [-0.062956262823249745, -0.078620521049947351, -0.27685694817610196, -0.462434926480641, -0.2649282884709499, 0.86250537688691487]
#base = [-0.16010507135041691, -0.19879276762554632, -0.59915824916006111, -0.90233439238094926, -0.47931038337885729, 1.3849529127423363]
#base = [-0.16353824353755686, -0.19902444703743297, -0.59780310751603061, -0.90283398035452056, -0.47816876960445698, 1.5235055372868147]
#base = [-0.16294809831258883, -0.19673017717133578, -0.59951544785675681, -0.90224368793338749, -0.4207764859184282, 1.5573747364812216]
#base = [-0.15278282428585885, -0.1445825428587585, -0.7958565265629295, -0.95132684265462359, -0.4365654855556155, 1.5565526878854845]
#base = [-0.14013550672510061, -0.12384403428728191, -0.90842888066666294, -0.88967397387175162, -0.48273240811114315, 1.7779624257556761]
#base = [-0.3652656255626326, -0.20545548151554558, -1.0545625822552526, -0.65515255628585, -.65565548158415, 2.35451595418541]
#base = [-0.2165727712549437, -0.24815280677719667, -1.8868971962376511, -1.8893558662194452, -1.0300733228720917, 3.5832501918137543]
base = [-0.252165132632152, -0.125465654654654165, -0.62625521521526,-0.365545284852,-0.4054554656265656,1.982126516512]
#base = [-.5492326596523, -0.2495625644, -1.272124584125, -0.7305451455, -0.809896551525, 3.9812152125252]


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


n = NeuralNet()
good = [-.5492326596523, -0.2495625644, -1.272124584125, -0.7305451455, -0.809896551525, 3.9812152125252]
n.listtonet(good)
play(False, n)

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

