import random
#import numpy
from deap import creator, base, tools, algorithms
from cannon import Cannon
from math import cos
from math import sqrt
from math import sin
from math import pi
from src.gravity import Gravity
from math import isnan
#import sys

# Fitness algorithm
# def evaluate(individual):
#    return sum(individual), sum(individual)

MAX_boreWidth = 0.3048
MAX_boreLength = 1.524
MAX_launchAngle = 90
MAX_platformHeight = 3.048
MAX_gunPowderMass = 1.36078

MIN_boreWidth = 0
MIN_boreLength = 0
MIN_launchAngle = 45
MIN_platformHeight = 0
MIN_gunPowderMass = 0

SUN = 274.0
JUPITER = 24.92
NEPTUNE = 11.15
SATURN = 10.44
EARTH = 9.807
URUNUS = 8.87
VENUS = 8.87
MARS = 3.71
MERCURY = 3.7
MOON = 1.62
PLUTO = 0.58

targetDistance = 200 # Meters
gravity = EARTH

def getDistanceShot(cannon):
    # TODO: add wind resistance to calculations
    muzzleVelocity = cannon.muzzleVelocity
    angleRadians = cannon.launchAngle * pi / 180
    startHeight = cannon.startHeight
    distance = ((muzzleVelocity * cos(angleRadians)) / gravity) * (muzzleVelocity * sin(angleRadians) + sqrt((muzzleVelocity * sin(angleRadians)) + 2 * gravity * startHeight))
    return distance

def getDistanceToTarget(cannon):
    return abs(targetDistance - getDistanceShot(cannon))

def getFlightTime(cannon):
    muzzleVelocity = cannon.muzzleVelocity
    angleRadians = cannon.launchAngle * pi / 180
    #print(getDistanceShot(cannon))
    #print(muzzleVelocity)
    #print(cos(angleRadians))
    flightTime = None
    den = muzzleVelocity * cos(angleRadians)

    if (den == 0):
        flightTime = 0
    else:
        flightTime = getDistanceShot(cannon) / den
    if isnan(flightTime):
        flightTime = 0
    return flightTime


#boreWidth, boreLength, launchAngle, platformHeight, gunPowderMass
# Fitness algorithm
def evaluate(individual):

    cannon = Cannon(*individual)
    #print("chargeLength" + str(cannon.chargeLength))
    #print("velocity" + str(cannon.muzzleVelocity))
    #print("ball mass" + str(cannon.ballMass))
    #print("startHeight" + str(cannon.startHeight))
    print(individual)

    if (individual[0] > MAX_boreWidth) | (individual[1] > MAX_boreLength) | (individual[2] > MAX_launchAngle) | (individual[3] > MAX_platformHeight) | (individual[4] > MAX_gunPowderMass):
        return (float("inf"),)
    if (individual[0] < MIN_boreWidth) | (individual[1] < MIN_boreLength) | (individual[2] < MIN_launchAngle) | (individual[3] < MIN_platformHeight) | (individual[4] < MIN_gunPowderMass):
        return (float("inf"),)



    fitness = None

    distanceToTarget = getDistanceToTarget(cannon)
    flightTime = getFlightTime(cannon)
    if (flightTime != 0) & (distanceToTarget != targetDistance):
        fitness = distanceToTarget + flightTime * 70
    else:
        fitness = float("inf")

    return (fitness,)

def randFun():
    return random.random()

def makeAttributeList():
    attributes = []
    attributes.append(random.uniform(MIN_boreWidth, MAX_boreWidth))
    attributes.append(random.uniform(MIN_boreLength, MAX_boreLength))
    attributes.append(random.uniform(MIN_launchAngle, MAX_launchAngle))
    attributes.append(random.uniform(MIN_platformHeight, MAX_platformHeight))
    attributes.append(random.uniform(MIN_gunPowderMass, MAX_gunPowderMass))
    return attributes

# Fitness model class. Dual minimization problem - minimize hit distance from target and time to hit target. Inhherets from the base Fitness class
#creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("FitnessMulti", base.Fitness, weights=(-1.0,))

# Our individuals are cannons represented by a simple list of specs
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Attributes:  boreWidth, boreLength, gunPowderMass, launchAngle, platformHeight)
#IND_SIZE = 5 # The number of cannon attributes

toolbox = base.Toolbox() # Inheret base toolbox
#toolbox.register("attribute", random.random) # Add tool for attribute initialization
toolbox.register("attribute", randFun) # Add tool for attribute initialization

toolbox.register("attributeList", makeAttributeList) # Add tool for attribute initialization

# Add tool for making a cannon from random attributes
#toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attributeList)

# Add a tool for creating a population of cannons
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# Add standard tools
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def run():
    # initialize population size 50
    pop = toolbox.population(n=1000)

    # crossover probablity, mutation probablity, number of generations
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Iterate through the number of generations
    for gen in range(NGEN):

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))

        # Clone the selected individuals to ensure we
        # aren't working with references to stale individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values # Invalidate fitness for newbies
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness (the newbies from mutation and crossover)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    return pop

def main():
    print('Running Simulation')

    pop = list(run())
    #for ind in pop:
    #    print(ind)

    print("_______________________")
    print("best fitness:")
    fits = [ind.fitness.values[0] for ind in pop]
    bestIndex = fits.index(min(fits))
    print(fits[bestIndex])
    print("best individual:")
    print(pop[bestIndex])
    print("confirm fitness:")
    print(evaluate(pop[bestIndex]))
    #print(pop[0])
    print("Done")

if __name__ == "__main__":
    main()
