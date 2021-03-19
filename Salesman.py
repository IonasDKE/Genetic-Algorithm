import random as rand
import itertools
import math
import matplotlib.pyplot as plt


def getPop(popSize, maxCoord, cities):
    pop = []
    for i in range(popSize):
        cititesInd = [i for i in range(len(cities))]
        individual = []
        for j in range(len(cities)):
            index = rand.randrange(len(cititesInd))
            individual.append(cititesInd[index])
            cititesInd.pop(index)

        pop.append([individual, fitness(cities, individual)])

    return pop

def fitness(cities, ind):
    totalDist = 0
    for i in range(len(ind)):

        if i+1 < len(ind):
            cityA = ind[i]
            cityB = ind[i+1]
            totalDist += getDistance(cities[cityA], cities[cityB])
        else:
            cityA = ind[i]
            cityB = ind[0]
            totalDist += getDistance(cities[cityA], cities[cityB])

    return totalDist

def getDistance(pointA, pointB):
    return math.sqrt((pointB[0]-pointA[0])**2+(pointB[1]+pointA[1])**2)

def GA(cities, pop, maxIter):
    iteration = 0
    sortedPop = sorted(pop, key=lambda ind: ind[1])
    scores = []

    while iteration < maxIter:
        iteration+=1

        #print('--- iteration ' + str(iteration) + '---')
        #print(sortedPop)
        #print()

        parents = sortedPop[:int(len(sortedPop)/4)] # take PopSize/4 parents

        newPop = []
        while len(newPop) < len(pop):

            # Pick the parents:
            parentA = parents[rand.randrange(len(parents))]
            parents.remove(parentA) # remove it to prevent taking the same parent 
            parentB = parents[rand.randrange(len(parents))]
            parents.remove(parentB)

            parents.append(parentA)
            parents.append(parentB)

            parentA = parentA[0] # Only take the solution and not the score 
            parentB = parentB[0]

            children = []

            # Order Crossover Operator:
            cut1 = int(len(parentA)/3)
            cut2 = math.ceil(2*len(parentB)/3)

            newInd1 = parentA[cut1:cut2]
            newInd2 = parentB[cut1:cut2]

            tmp1 = parentB[:] 
            tmp2 = parentA[:]

            for i in range(len(newInd1)):
                tmp1.remove(newInd1[i])
                tmp2.remove(newInd2[i])

            len1 = len(parentA[cut2:])

            newInd1.extend(tmp1[:len1])
            newInd1[1:1] = tmp1[len1:]

            newInd2.extend(tmp2[:len1])
            newInd2[1:1] = tmp2[len1:]

            children = [newInd1, newInd2]


            # Mutation:
            for child in children:
                if rand.random() <= 0.1:
                    pos1 = rand.randrange(len(child))
                    pos2 = rand.randrange(len(child))

                    while pos1 == pos2:
                        pos2 = rand.randrange(len(child))
                    
                    tmp = child[pos1]
                    child[pos1] = child[pos2]
                    child[pos2] = tmp


            '''
            print('parents:')
            print(parentA)
            print(parentB)
            print('children: ')
            print(newInd1)
            print(newInd2)
            print()
            '''
            for child in children:
                newPop.append([newInd1, fitness(cities, child)])

        #print(len(newPop))
        #print(newPop)

        pop = newPop

        sortedPop = sorted(pop, key=lambda ind: ind[1])
        scores.append(sortedPop[0][1])

    return sortedPop[0][0], sortedPop[0][1], scores


def main():
    maxCoord = 100 # Maximum value on the x and y axis, min is 0
    popSize = 100
    numOfCities = 10

    rand.seed(2)

    cities = []
    for i in range(numOfCities):
        newX = rand.randrange(maxCoord)
        newY = rand.randrange(maxCoord)
        cities.append([newX, newY])

    pop = getPop(popSize, maxCoord, cities)
    bestSolution, score, scores  = GA(cities, pop, maxIter=1000000)
    
    # Extract the x and y coordinate to plot the cities:
    x = [xpos[0] for xpos in cities]
    y = [ypos[1] for ypos in cities]

    # Generate lines too see the solution: 
    xcoord = []
    ycoord = []
    for i in range(len(bestSolution)):
        if i+1 < len(bestSolution):
            i1 = bestSolution[i]
            i2 = bestSolution[i+1]

            point1 = cities[i1]
            point2 = cities[i2]

            xcoord.append([point1[0], point2[0]])
            ycoord.append([point1[1], point2[1]])
        else:
            i1 = bestSolution[i]
            i2 = bestSolution[0]

            point1 = cities[i1]
            point2 = cities[i2]
            
            xcoord.append([point1[0], point2[0]])
            ycoord.append([point1[1], point2[1]])

    plt.scatter(x=x, y=y)
    plt.plot(xcoord, ycoord)
    plt.title('1 000 000 iterations ')
    plt.show()

    scores = scores[::10000]
    x = [i*10000 for i in range(len(scores))]
    plt.plot(x, scores)
    plt.title('Performance for 1 000 000 iterations')
    plt.xlabel('iterations')
    plt.ylabel('distance')
    plt.show()

if __name__ == '__main__':
    main()
