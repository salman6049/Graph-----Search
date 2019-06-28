# -*- coding: utf-8 -*-
"""
Created on Fri May 10 18:26:03 2019

@author: Salman
"""

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        solution = [[1]*m]*n
        for y in range(1, n):
            for x in range(1, m):
                solution[y][x] = solution[y][x-1] + solution[y-1][x]
        return solution[n-1][m-1]

"""
Approach:
- Create a 2D matrix of same size of the given matrix to store the results.
- Traverse through the created array row wise and start filling the values in it.
- If an obstacle is found, set the value to 0.
- For the first row and column, set the value to 1 if obstacle is not found.
- Set the sum of the right and the upper values if obstacle is not present at that corresponding position in the given matirx
- Return the last value of the created 2d matrix

"""


def uniquePaths(m,n):
    solution = [[1]*m]*n
    for y in range(1, n):
        for x in range(1, m):
            solution[y][x] = solution[y][x-1] + solution[y-1][x]
    return solution[n-1][m-1]        

uniquePaths(8,8)



# Python code to find number of unique paths in a  
# matrix with obstacles. 
  
def uniquePathsWithObstacles(A): 
    
    # create a 2D-matrix and initializing with value 0 
    paths = [[0]*len(A[0]) for i in A] 
      
    # initializing the left corner if no obstacle there 
    if A[0][0] == 0: 
        paths[0][0] = 1
      
    # initializing first column of the 2D matrix 
    for i in range(1, len(A)): 
        if A[i][0] == 0:  // If not obstacle 
            paths[i][0] = paths[i-1][0] 
              
    # initializing first row of the 2D matrix 
    for j in range(1, len(A[0])): 
        if A[0][j] == 0:  // If not obstacle 
            paths[0][j] = paths[0][j-1] 
              
    for i in range(1, len(A)): 
      for j in range(1, len(A[0])): 
  
        # If current cell is not obstacle 
        if A[i][j] == 0: 
          paths[i][j] = paths[i-1][j] + paths[i][j-1] 
    
    # returning the corner value of the matrix 
    return paths[-1][-1] 
  
  
# Driver Code 
A = [[0, 0, 0], [0, 1, 0], [0, 0, 0]] 
print(uniquePathsWithObstacles(A)) 
