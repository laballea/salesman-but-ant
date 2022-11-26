import random
import numpy as np

class Net:
    def __init__(self, ant_num):
        self.num_nodes = 0  # number of nodes inside net
        self.nodes = []  # 1d array of nodes (posx, posy)
        self.distances = None  # 2d array of disctances btw each node
        self.weights = None  # 2d array of weights btw each node, that will influe the "choice" of the ant
        self.ant_num = ant_num  # ant number
        self.alpha = 2.0  # impact of the weights
        self.beta = 2.0 # impact of the disctances
        self.best_path = None # store the best path seen
        self.best_len = np.inf  # init best len

    #reset net
    def reset_net(self):
        self.distances = None
        self.weights = None
        self.num_nodes = 0
        self.nodes = []
        self.best_len = np.inf  # init best len
        self.best_path = None # store the best path seen

    def set_net(self):
        self.distances = np.zeros((self.num_nodes, self.num_nodes)) # create 2d arrays of size (num_nodes, num_nodes) fill of zeros
        self.weights = np.zeros((self.num_nodes, self.num_nodes)) # create 2d arrays of size (num_nodes, num_nodes) fill of zeros
        #  iterate over them
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                # same node
                if i == j:
                    self.weights[i][j] = 0.0
                    self.distances[i][j] = 0.0
                    continue
                elif j < i: # connection already seen (6th to 7th is the same as 7th to 6th)
                    self.weights[i][j] = 1.0 # init weights
                    self.distances[i][j] = self.distances[j][i] # get previously calculated distances
                    continue
                self.weights[i][j] = 1.0 # init weights
                self.distances[i][j] = self.calc_distance(self.nodes[i], self.nodes[j])  # calculate disctance between this two points

    # this function will be run multiple time over time
    def compute_net(self):
        self.weights *= 0.999 # decrease all of the weights

        for _i in range(self.ant_num): # one loopIn for each ant
            # each ant will start from random point and wil be assign a path to follow
            ret = self.get_random_path_from(random.randint(0, self.num_nodes - 1))
            path = ret[0] # store the path
            l = ret[1] # store the lenght of it
            
            # is the best path
            if l < self.best_len:
                self.best_len = l
                self.best_path = path

            # iterate over the path
            for i in range(0, self.num_nodes + 1):
                curr_node = path[i % self.num_nodes] # current node
                next_node = path[(i + 1) % self.num_nodes] # next node
                # update weight of the connection
                self.weights[curr_node][next_node] += 0.01
                self.weights[next_node][curr_node] += 0.01

    def get_random_path_from(self, idx):
        # init path, dist
        path = []
        dist = 0.0
        path.append(idx)
        curr_node = idx

        # while our path is not complete
        while len(path) < self.num_nodes:
            possible_next = [] # store possible node to go
            possible_next_weight = [] # store it corresponding probability
            for node in range(self.num_nodes):
                if node in path: # already visited
                    continue
                possible_next_weight.append(self.get_transition_probability(curr_node, node)) # add prob. to list
                possible_next.append(node) #add node to list

            chosen_node_idx = random.choices(possible_next, possible_next_weight)[0] # choose node depending on the probability array
            dist += self.distances[curr_node][chosen_node_idx] #update distance
            curr_node = chosen_node_idx # update node
            path.append(chosen_node_idx) # update path
            
        dist += self.distances[curr_node][idx] # add final distance to the total
        return [path, dist]

    def add_nodes(self, pos):
        self.nodes.append(pos)
        self.num_nodes += 1

    # calculate probability to choose certain node to go depending on the weight and the distance
    # when an ant move, it drop pheromones our "weight" here, and depending on the distance concentration will decrease or increase
    # this function mimic that and we can influence impact of either the weight or distances by changing beta and alpha
    def get_transition_probability(self, idx1, idx2):
        return pow(self.weights[idx1][idx2], self.alpha) * pow(self.distances[idx1][idx2], -self.beta)

    def calc_distance(self, pos0, pos1):
        return (pos1[0] - pos0[0])**2 + (pos1[1] - pos0[1])**2
