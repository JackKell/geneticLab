import random
#import numpy
from deap import creator, base, tools, algorithms
from cannon import Cannon
from math import cos
from math import sqrt
from math import sin
from math import pi
from src.gravity import Gravity

# Fitness algorithm
# def evaluate(individual):
#    return sum(individual), sum(individual)

targetDistance = 25 # Meters
gravity = Gravity.EARTH

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
    print(getDistanceShot(cannon))
    print(muzzleVelocity)
    print(cos(angleRadians))
    flightTime = getDistanceShot(cannon) / (muzzleVelocity * cos(angleRadians))
    if isnan(flightTime):
        flightTime = 0
    return flightTime


#boreWidth, boreLength, launchAngle, platformHeight, gunPowderMass
# Fitness algorithm
def evaluate(individual):
    cannon = Cannon(*individual)
    print(str(cannon.chargeLength))
    print(str(cannon.muzzleVelocity))
    print(str(cannon.ballMass))
    print(str(cannon.startHeight))
    print(individual)

    fitness = None

    distanceToTarget = getDistanceToTarget(cannon)
    flightTime = getFlightTime(cannon)
    if (flightTime != 0 & distanceToTarget != targetDistance):
        fitness = distanceToTarget + flightTime * 70
    else:
        fitness = DBL_MAX

    return fitness, 1

def bob():
    return 1

# Fitness model class. Dual minimization problem - minimize hit distance from target and time to hit target. Inhherets from the base Fitness class
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))

# Our individuals are cannons represented by a simple list of specs
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Attributes:  boreWidth, boreLength, gunPowderMass, launchAngle, platformHeight)
IND_SIZE = 5 # The number of cannon attributes

toolbox = base.Toolbox() # Inheret base toolbox
#toolbox.register("attribute", random.random) # Add tool for attribute initialization
toolbox.register("attribute", bob) # Add tool for attribute initialization
# Add tool for making a cannon from random attributes
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
# Add a tool for creating a population of 100 cannons
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# Add standard tools
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def run():
    # initialize population size 50
    pop = toolbox.population(n=2)

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
    print(pop)
    fits = [ind.fitness.values[0] for ind in pop]
    print(fits)
    print("Done")

if __name__ == "__main__":
    main()