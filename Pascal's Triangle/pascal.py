# Power and term indices are both 0 based 

from cgi import test
import math as m
import time
import matplotlib.pyplot as plt

# Method 1: Uses Recursive Function to generate the row and then indexes the row for the column
def getRowGenerationIndex(power, term):
    return getRow(power)[term]

def getRow(n, prev_row = [1]):
    if len(prev_row) == (n + 1):
        return prev_row
    else:
        new_row = [1]
        if len(prev_row) != 1:
            for i in range(len(prev_row) - 1):
                new_row.append(prev_row[i] + prev_row[i + 1])
        new_row.append(1)
        return getRow(n, new_row)

# Method 2: Uses Binomial Expansion Theorem (n choose k where n is power and k is the term); can implement either custom recursive factorial or use from math package
def getIndexBinomial(power, term): 
    return m.factorial(power) / (m.factorial(term) * m.factorial(power - term))

def customFactorial(n):
    if n == 0: 
        return 1
    return n * customFactorial(n-1)

# Method 3 Courtesty of Jake

def JakePascalIndex(power, term):
    if term == 0: 
        return 1
    if power == 0:
        return term
    return (power * JakePascalIndex(power - 1, term -1 )) / term

def testPascalFunction(num, func, printBool = False):
    num-=1
    startTime = time.time()
    for row in range(num):
        for elem in range(row + 1):
            val = int(func(row,elem))
            if printBool:
                print(val, end=" ")
        if printBool:
            print("\n")
    return (time.time() - startTime) * 1000

RowGenerationData = []
BinomialExpansionData = []
JakeAlgorithmData = []

xPoints = [y+1 for y in range(150)]
for x in xPoints: 
    print(x)
    RowGenerationData.append(testPascalFunction(x, getRowGenerationIndex))
    BinomialExpansionData.append(testPascalFunction(x, getIndexBinomial))
    JakeAlgorithmData.append(testPascalFunction(x, JakePascalIndex))

fig, ax = plt.subplots()
ax.plot(xPoints, RowGenerationData, label="Row Generation Algorithm")
ax.plot(xPoints, BinomialExpansionData, label="Binary Expansion Algoritm")
ax.plot(xPoints, JakeAlgorithmData, label="Jake's Algorithm")
ax.set_ylabel('Time (ms)')  
ax.set_xlabel('Number of Rows Generated')  
ax.set_title("Efficiency of Pascal's Triangle Indexing Algorithms")
ax.legend()
plt.savefig("pascal.png")