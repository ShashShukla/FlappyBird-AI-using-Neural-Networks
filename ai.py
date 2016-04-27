import numpy as np
import random

# values population is centered around
# old
base = [-.31342821235, -0.1139874, -0.59353849, -0.4720327, -.398302309, 2.0122036125]
#base = [-1.0554067493208676, 0.77013012508916701, -0.06705356825141548, 0.89721645929467075, 0.35432919902034599, -0.52726160234006003]
# goood
#base=[-0.29177897182904566, -0.02079601764656655, 0.050318894091150201, -0.31834221642285804, -0.080554413341745179, 0.29947136257458251]
#base=[-0.74453823061391411, -0.23431895690844284, 0.042310504279929273, -0.74926701195829093, -0.22131318363892011, 0.63796397875889266]
#base=[-1.7285691649175292, -0.61335489660695819, -0.011456718761088114, -1.4139638018522294, -0.40226843736628759, 1.2126820644738272]
#base = [-3.3816611191144652, -1.0835123452139612, -0.082575882826284891, -2.9941685247498007, -0.97572381473026326, 2.2776198385228601]


#base = [-0.36350832388949617, -0.21213182006279963, 0.34647927718174532, -0.54633886573716672, -0.1508851782072127, 0.48001593266439863]


#Application ID AA005VCQSU

#################################uski values####################################################
#base = [-.5524816518, -0.251785039, -1.2697808633, -0.72796955875826, -0.81684247849, 3.97877468847]
#base = [-0.592793429, -0.3034340092, -1.16798685, -0.911873095, -.823201093414, 4.02614127]
#base = [-1.3250002, -0.7360805918, -2.405525383, -1.5978525241, -1.887704711098, 8.09533357862]
#base = [-.61469627, -0.2552426139, -1.1648285816, -0.92243556333, -0.71739226198, 3.9997260310595]
class Net():
    def __init__(self, w1=None, w2=None):
        self.insize = 2
        self.hidsize = 2
        self.outsize = 1
        self.w1 = w1
        self.w2 = w2
        if not w1:
            self.random()
 #AA005VCBZ2
    # produce output given input values
    def forward(self, X):
        # inputs to hidden layer
        hout = self.sigmoid(np.dot(X, self.w1))
        # final output
        fout = self.sigmoid(np.dot(hout, self.w2))
        return fout

    # generate random weights around base value
    def random(self):
        gene = []
        for weight in base:
            gene.append(weight + random.triangular(weight - .3, weight + .3))

        self.decode(gene)

    # create gene from weights
    def encode(self):
        gene = []
        for i in self.w1:
            gene.extend(i)
        for i in self.w2:
            gene.extend(i)

        return gene

    # set weights given gene
    def decode(self, gene):
        w1 = []
        count = 0
        for i in xrange(self.insize):
            n = [] 
            for j in xrange(self.hidsize):
                n.append(gene[count])
                count += 1
            w1.append(n)
        self.w1 = w1

        w2 = []
        for i in xrange(self.hidsize):
            n = [] 
            for j in xrange(self.outsize):
                n.append(gene[count])
                count += 1
            w2.append(n)

        self.w2 = w2

    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

    def __repr__(self):
        return str(self.encode())

    def __str__(self):
        return str(self.encode())

