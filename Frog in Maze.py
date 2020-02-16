# -*- coding: utf-8 -*-
"""
Created on January 2017

@author: Salman
"""

import numpy as np

def from_1d_to_2d(number):
    return ((number // m, number % m))

def from_2d_to_1d(i, j):
    return (i * m + j)

def transition_prob(a, b):
    return(probabilities[from_2d_to_1d(a[0], a[1]), from_2d_to_1d(b[0], b[1])])

def get_probability_1d(i, j):
    return absorption_prob[index[i], index[j]]

def get_probability_2d(a, b):
    i = from_2d_to_1d(a[0], a[1])
    j = from_2d_to_1d(b[0], b[1])
    return get_probability_1d(i, j)

n, m, k = [3, 6, 1]
maze = [["#", "#", "#", "*", "O", "O"], 
        ["O", "#", "O", "A", "%", "O"], 
        ["#", "#", "#", "*", "O", "O"]]
tunnels = [[(2,3), (2,1)]]

# change to np format
maze = np.array(maze)
tunnels = np.array(tunnels)

# size of markov chain is the number of elements
size = n * m
probabilities = np.zeros(shape=(size,size), dtype=float)

# set up tunnels dictionary
tunnel_dict = {}
for tunnel in tunnels:
    # change to zero indexing
    tunnel[0] = np.subtract(tunnel[0], (1,1))
    tunnel[1] = np.subtract(tunnel[1], (1,1))
    # add to dict
    tunnel_dict[tuple(tunnel[0])] = tuple(tunnel[1])
    tunnel_dict[tuple(tunnel[1])] = tuple(tunnel[0])
    # mark on map
    maze[tuple(tunnel[0])] = "T"
    maze[tuple(tunnel[1])] = "T"

# 1. encode exit states and death state as absorbing
# 2. compute probabilities for each element

for i in range(n):
    for j in range(m):
        # (i,j) is row, column
        moves = np.array([np.add((i,j), (-1, 0)), np.add((i,j), (1, 0)), 
                 np.add((i,j), (0, -1)), np.add((i,j), (0, 1))])
        # udlr keeps track of illegal moves. updating:
        # which of up down left right are on the board?
        udlr = np.array([i-1 >= 0, i+1 < n, j-1 >= 0, j+1 < m])
        # examine each of the possible moves for brick walls and tunnels
        for k in range(4):
            if udlr[k]:
                # brick wall? illegal move
                if maze[tuple(moves[k])] == "#":
                    udlr[k] = False
                # which moves are a tunnel? update move coords
                elif maze[tuple(moves[k])] == "T":
                    moves[k] = np.array(tunnel_dict[tuple(moves[k])])
        # delete illegal moves
        moves = moves[udlr]
        """
        Calculating transition probability (self, moves)
        1. Absorb if current space is a bomb (*), exit (%) or no legal moves
        2. Else transition from current to move with probability 1/len(moves)
        """
        current = maze[(i,j)]
        state_i = from_2d_to_1d(i, j)
        if current == "*" or current == "%" or len(moves) == 0:
            probabilities[state_i, state_i] = 1
        else:
            pij = 1/len(moves)
            for move in moves:
                state_j = from_2d_to_1d(move[0], move[1])
                probabilities[state_i, state_j] = pij

# convert the probability matrix to canonical form
absorbing_states = np.diag(probabilities) == 1
no_transient = np.sum(np.logical_not(absorbing_states))

canonical_Q = probabilities[:, np.logical_not(absorbing_states)]
canonical_Q = canonical_Q[np.logical_not(absorbing_states), :]
canonical_R = probabilities[:, absorbing_states]
canonical_R = canonical_R[np.logical_not(absorbing_states), :]

fundamental_N = np.linalg.inv(np.identity(no_transient) - canonical_Q)

absorption_prob = np.matmul(fundamental_N, canonical_R)

transient_id = np.arange(size)[np.logical_not(absorbing_states)]
absorbing_id = np.arange(size)[absorbing_states]

transient = 0
absorbing = 0
index = []
for i in range(size):
    if absorbing_states[i]:
        index.append(absorbing)
        absorbing += 1
    else:
        index.append(transient)
        transient += 1

exits = []
for i in range(size):
    current = maze[from_1d_to_2d(i)]
    if current == "%":
        exits.append(i)
    elif current == "A":
        alef = i

output = 0
for element in exits:
    output += get_probability_1d(alef, element)
print(output)