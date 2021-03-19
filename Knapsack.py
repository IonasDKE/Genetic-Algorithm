import random as rand
import math
import matplotlib.pyplot as plt

 
def setFitness(ind, items):
    weightSum = 0
    valueSum = 0
    for i in range(len(ind)):
        if ind[i] == 1:
            try :
                weightSum += items[i][0]
                valueSum += items[i][1]
            except IndexError:
                print('--- ERROR ---')
                print(i)
                print(len(items))

    ind.append(weightSum)
    ind.append(valueSum)

    return ind

def getItems(numItems):
    #Generate the items:
    items = []
    for i in range (0, numItems):
        weight = rand.randrange(1, 10)
        value = rand.randrange(1, 10)

        item = [weight, value]
        items.append(item)
    return items

def getInitialPop(items, popSize):
    # Generate the population:
    population = []
    for i in range(popSize):
        individual = []
        for i in items:
            if rand.random() > 0.5:
                individual.append(1)
            else:
                individual.append(0)

        population.append(setFitness(individual, items))
        #print(individual)

    #print()
    return population

def GA(items, population, crossoverMethod, maxWeight, maxIteration):
    popSize = len(population)
    itemsSize = len(items)
    population = [ind for ind in population if ind[-2] <= maxWeight] # remove the individuals that have where the sum of the wieghts is larger than the maximum capacity of our backpack
    population = sorted(population, key=lambda ind: ind[-1], reverse=True) # Sort our population by biggest value 
    #print(population)
    scores = []
    mutationProb = 0.1
    numberOfParents = int(popSize/4)

    last = 0
    new = 1
    iteration = 0

    while iteration < maxIteration:
        iteration += 1
        # Select the best induvidual
        last = population[0][-1] # Best score of last iteration
        parents = population[:numberOfParents] # Take the top x parents 
        #print(parents)

        newPop = []
        while len(newPop) < popSize:
            newPop.clear
            # Select random parent for reproduction
            p1 = population[rand.randrange(numberOfParents)]
            population.remove(p1)
            p2 = population[rand.randrange(numberOfParents-1)]
            population.append(p1)

            newInd = []

            p1 = p1[:-2]
            p2 = p2[:-2]

            # Uniform Crossover:
            if crossoverMethod == "uniform":
                newInd = p1[:]

                for i in range(len(p1)-2):
                    if rand.random() < 0.5:
                        newInd[i] = p2[i]

            # One point Crossover 
            if crossoverMethod == "one point":
                crossPoint = rand.randrange(len(p1))
                newInd = p1[:crossPoint]
                newInd.extend(p2[crossPoint:])
                if len(newInd) > itemsSize:
                    raise Exception("out of range: "+ str(len(newInd)))

            # Multiple point Crossover
            if crossoverMethod == "multi point":
                indexes = [round(len(p1)/4), round(len(p1)/2), round(3*len(p1)/4)]

                newInd = p1[:indexes[0]]
                newInd.extend(p2[indexes[0]:indexes[1]])
                newInd.extend(p1[indexes[1]:indexes[2]])
                newInd.extend(p2[indexes[2]:])

            # Mutation
            if rand.random() < mutationProb:
                mutInd = rand.randrange(len(newInd))
                if newInd[mutInd] == 0:
                    newInd[mutInd] = 1
                else:
                    newInd[mutInd] = 0

            newPop.append(setFitness(newInd, items))

        newPop = [ind for ind in newPop if ind[-2] <= maxWeight]
        newPop = sorted(newPop, key=lambda ind: ind[-1], reverse=True)

        new = newPop[0][-1] # new best score
        
        print('iteration:' + str(iteration))
        print("--- new ---")
        print(last)
        print(new)
        print()
        #print("--- NEW POPULATION ---")
        #print(newPop)

        population = newPop
        scores.append(last)

    return new, scores

def main():
    maxWeight = 100
    popSize = 1000
    itemsSize = 20

    rand.seed(1)
    items = getItems(itemsSize)
    population = getInitialPop(items, popSize)
    methods = ["uniform", "one point", "multi point"]
    bestScore, scores = GA(items, population, methods[0], maxWeight, maxIteration=100)

    # Plotting
    x = [i for i in range(len(scores))]
    plt.plot(x, scores)
    plt.title("Uniform crossover")
    plt.xlabel("iterations")
    plt.ylabel("scores")
    plt.show()

if __name__ == '__main__':
    main()
