CS 403 : Project : FLAPPY BIRD AI USING NEURAL NETWORKS 
==============================================================
Team Members :
Saurabh Garg, 140070003
Aviral Kumar, 140070031
Siddhant Garg, 14D070027
Ritwick Chaudhury, 14D070063
===============================================================

Instructions for running the code :

Code Dependancies : pygame
To install : sudo apt-get python-pygame

1. Untar the entire directory into ~/dir
2. cd ~/dir
3. Run the file newgen.py : python newgen.py

=================================================================

Brief description of the code : (Explained in more detail in the report) :

1. We have used pygame, numpy, math and random libraries of python for implementing ths stuff. 
2. The code is organised into 2 files :- newgen.py (creates NN and applies Genetic Algo), flappyGame.py (Implements the simple game UI)
3. The file newgen.py has 4 main functions : performance(), updateweights(), survivaloffittest() and newnetlist() and a class that 
   implements a Neural Network.
4. The NN is straightforward, it has functions to feed forward inputs and functions to convert the NN to a list and backwards.
5. The performance() function returns an instance of the game where the bird actually plays the game.
6. The survivalofthefittest() function considers the two topmost entries of the genome and then returns the one the maximum fitness level. 
7. The updateweights() function combines them all into one function. Children are formed from the current generation by crossing over the 
   two parents. Along with this, some of these children suffer random mutations (only some of these, as the condition of the if statement 
   corresponds to an inequality with the mutationrate,which might not be satisfied always), and then they get passed on as the 
   individuals of the next generation
8. The function newnetlist() takes in the genome of generation i and then takes two individuals in pairs from the sorted genome in decreasing
   order of fitness, breeds them and returns the result as the individuals of generation (i+1)
9. The file newgen.py also corresponds to the implementation of the underlying Neural Net class on which the entire computation is being done. It has two new functions apart from the common neural net, which are : nettolist() and listtonet(). These are used to convert the weight vector back to and convert to weight vector back from, the string representing the weight array (individuals).

===================================================================
