from pysyncobj import SyncObj, replicated
from src.GeneticLabNode import GeneticLabNode
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from threading import Thread
from queue import Queue
from deap import creator, base, tools
from cannon import Cannon
from math import cos, sqrt, sin, pi, isnan
import random


class GeneticLabServer(SyncObj, GeneticLabNode):
    def __init__(self, port, servers):
        SyncObj.__init__(self, 'localhost:1337', [])
        GeneticLabNode.__init__(self, port)
        self.cannonResults = []
        self.tcpSocket = socket()
        self.workerThreads = list()
        self.connections = Queue()
        self.servers = servers

    @replicated
    def __saveResult(self, request, results):
        self.cannonResults.append((request, results))

    def runCannonSimulation(self, data):
        def getDistanceShot(cannon):
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
            flightTime = None
            den = muzzleVelocity * cos(angleRadians)

            if (den == 0):
                flightTime = 0
            else:
                flightTime = getDistanceShot(cannon) / den
            if isnan(flightTime):
                flightTime = 0
            return flightTime

        # boreWidth, boreLength, launchAngle, platformHeight, gunPowderMass
        # Fitness algorithm
        def evaluate(individual):

            cannon = Cannon(*individual)

            if (individual[0] > maxBoreWidth) | (individual[1] > maxBoreLength) | (individual[2] > maxLaunchAngle) | (individual[3] > maxPlatformHeight) | (individual[4] > maxGunPowderMass):
                return (float("inf"),)
            if (individual[0] < minBoreWidth) | (individual[1] < minBoreLength) | (individual[2] < minLaunchAngle) | (individual[3] < minPlatformHeight) | (individual[4] < minGunPowderMass):
                return (float("inf"),)

            fitness = None

            distanceToTarget = getDistanceToTarget(cannon)
            flightTime = getFlightTime(cannon)
            if (flightTime != 0) & (distanceToTarget != targetDistance):
                fitness = distanceToTarget + flightTime * 70
            else:
                fitness = float("inf")

            return (fitness,)

        def makeAttributeList(minBoreWidth, maxBoreWidth, minBoreLength, maxBoreLength, minLaunchAngle, maxLaunchAngle,
                      minPlatformHeight, maxPlatformHeight, minGunPowderMass, maxGunPowderMass):
            attributes = []
            attributes.append(random.uniform(minBoreWidth, maxBoreWidth))
            attributes.append(random.uniform(minBoreLength, maxBoreLength))
            attributes.append(random.uniform(minLaunchAngle, maxLaunchAngle))
            attributes.append(random.uniform(minPlatformHeight, maxPlatformHeight))
            attributes.append(random.uniform(minGunPowderMass, maxGunPowderMass))
            return attributes

        minBoreWidth = data["minBoreWidth"]
        maxBoreWidth = data["maxBoreWidth"]
        minBoreLength = data["minBoreLength"]
        maxBoreLength = data["maxBoreLength"]
        minLaunchAngle = data["minLaunchAngle"]
        maxLaunchAngle = data["maxLaunchAngle"]
        minPlatformHeight = data["minPlatformHeight"]
        maxPlatformHeight = data["maxPlatformHeight"]
        minGunPowderMass = data["minGunPowderMass"]
        maxGunPowderMass = data["maxGunPowderMass"]
        crossoverRate = data["crossoverRate"]
        mutationRate = data["mutationRate"]
        numberOfGenerations = data["numberOfGenerations"]
        populationSize = data["populationSize"]
        targetDistance = data["targetDistance"]
        gravity = 9.807

        # Fitness model class. Dual minimization problem - minimize hit distance from target and time to hit target. Inhherets from the base Fitness class
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0,))

        # Our individuals are cannons represented by a simple list of specs
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        # Inheret base toolbox
        toolbox = base.Toolbox()

        # Add tool for attribute initialization
        toolbox.register("attributeList", makeAttributeList, minBoreWidth, maxBoreWidth, minBoreLength, maxBoreLength, minLaunchAngle, maxLaunchAngle,
                      minPlatformHeight, maxPlatformHeight, minGunPowderMass, maxGunPowderMass)

        # Add tool for making a cannon from random attributes
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attributeList)

        # Add a tool for creating a population of cannons
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        # Add standard tools
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # initialize population size 50
        pop = toolbox.population(n=populationSize)

        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Iterate through the number of generations
        for gen in range(numberOfGenerations):

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))

            # Clone the selected individuals to ensure we
            # aren't working with references to stale individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < crossoverRate:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values # Invalidate fitness for newbies
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < mutationRate:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness (the newbies from mutation and crossover)
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(toolbox.evaluate, invalid_ind))
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            print("_______________________")
            print("best fitness:")
            fits = [ind.fitness.values[0] for ind in pop]
            bestIndex = fits.index(min(fits))
            # best fitness
            bestFitness = fits[bestIndex]
            # best individual
            bestInividual = pop[bestIndex]
            return (bestInividual, bestFitness)

    def openSocket(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind(("", self.port))
        self.tcpSocket.listen(self.backlog)

    def run(self):
        self.openSocket()
        for i in range(0, 10):
            workerThread = Thread(target=self.requestHandler)
            workerThread.start()
            self.workerThreads.append(workerThread)
        print("Running Server")
        while True:
            readyInputs, readyOutputs, readyExcepts = select([self.tcpSocket], [], [])
            for readyInput in readyInputs:
                if readyInput == self.tcpSocket:
                    self.connections.put(self.tcpSocket.accept())

    def requestHandler(self):
        while True:
            if not self.connections.empty():
                connection, address = self.connections.get()
                data = connection.recv(self.bufferSize)
                request = self.decodeMessage(data)
                returnMessage = []
                if request["requestType"] == "cannonSimulation":
                    if request["distr"] == True:
                        request["distr"] = False
                        message = self.encodeMessage(request)
                        for server in servers:
                            tcpSocket = socket(AF_INET, SOCK_STREAM)
                            tcpSocket.connect((server, self.port))
                            #tcpSocket.settimeout(self.timeout)
                            tcpSocket.send(message)
                            data = tcpSocket.recv(self.bufferSize)
                            data = self.decodeMessage(data)
                            tcpSocket.close()
                            returnMessage.append(data)

                    # run request itself
                    #bestIndividual, bestFitness = self.runCannonSimulation(request)

                    # put ours in at the end
                    #returnMessage.append((bestIndividual, bestFitness))


                    response = self.encodeMessage(returnMessage)
                    connection.sendall(response)
                    self.connections.task_done()


                # return responses/response to client or source server
                #print(request)
                #response = self.encodeMessage({"requestType": "cannonResult"})
                #connection.sendall(response)
                #self.connections.task_done()
