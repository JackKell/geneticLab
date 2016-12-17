import os
from src.GeneticLabNode import GeneticLabNode


class GeneticLabClient(GeneticLabNode):
    def __init__(self, port, serverAddress):
        super().__init__(port)
        self.mainMenuOptions = ["Run Experiment", "View Running", "Exit"]
        self.runExperimentOptions = ["Cannon", "Back to Main Menu"]
        self.serverAddress = serverAddress

    def getUserOption(self, optionList):
        while True:
            try:
                userInput = int(input("  >> "))
                if userInput not in range(0, len(optionList)):
                    raise ValueError("Invalid range input")
            except ValueError:
                print("This is not a valid input")
            else:
                return userInput

    def getNumberInput(self, message, lower=None, upper=None, castToType=float):
        while True:
            try:
                userInput = castToType(input(message + "\n  >> "))
                if lower is not None:
                    if userInput < lower:
                        raise ValueError
                if upper is not None:
                    if userInput > upper:
                        raise ValueError
            except ValueError:
                print("This is not a valid input")
            else:
                return userInput

    def getBooleanInput(self, message):
        while True:
            try:
                userInput = str(input(message + "\n  >> ")).lower()
                if userInput in ["false", "no", "n", "0"]:
                    return False
                elif userInput in ["true", "yes", "y", "1"]:
                    return True
                else:
                    raise ValueError
            except ValueError:
                print("This is not a valid input")

    def printOptions(self, options):
        for i in range(0, len(options)):
            print("  ", i, ")", options[i])

    def mainMenu(self):
        self.clear()
        print("Genetic Lab - Main Menu")
        self.printOptions(self.mainMenuOptions)
        optionIndex = self.getUserOption(self.mainMenuOptions)
        optionChosen = self.mainMenuOptions[optionIndex]
        if optionChosen == "Run Experiment":
            self.runExperimentMenu()
        elif optionChosen == "View Running":
            self.viewExperimentsMenu()
        elif optionChosen == "Exit":
            self.close()

    def runExperimentMenu(self):
        self.clear()
        print("Genetic Lab - Run Experiment")
        self.printOptions(self.runExperimentOptions)
        optionIndex = self.getUserOption(self.runExperimentOptions)
        optionChosen = self.runExperimentOptions[optionIndex]
        if optionChosen == "Cannon":
            print("Build a cannon Simulation")
            useDefault = self.getBooleanInput("Do you want to use the default cannon settings (y/n)")
            minBoreLength = 1
            maxBoreLength = 3
            minBoreWidth = 0.10
            maxBoreWidth = 0.30
            minLaunchAngle = 20
            maxLaunchAngle = 90
            minPlatformHeight = 0
            maxPlatformHeight = 1
            minGunPowderMass = 1
            maxGunPowderMass = 10
            crossoverRate = 0.65
            mutationRate = 0.05
            populationSize = 100
            numberOfGenerations = 1000
            if not useDefault:
                minBoreLength = self.getNumberInput("Min cannon length (meters)", 0)
                maxBoreLength = self.getNumberInput("Max cannon length (meters)", minBoreLength)
                minBoreWidth = self.getNumberInput("Min bore width (meters)", 0)
                maxBoreWidth = self.getNumberInput("Max bore width (meters)", minBoreWidth)
                minLaunchAngle = self.getNumberInput("Min launch angle (degrees)", 0, 180)
                maxLaunchAngle = self.getNumberInput("Max launch angle (degrees)", minLaunchAngle, 180)
                minPlatformHeight = 0
                maxPlatformHeight = 1
                minGunPowderMass = 1
                maxGunPowderMass = 10
                crossoverRate = self.getNumberInput("Crossover rate (float between 0 and 1)", 0, 1)
                mutationRate = self.getNumberInput("Mutation rate (float between 0 and 1)", 0, 1)
                populationSize = self.getNumberInput("Population size", 5, castToType=int)
                numberOfGenerations = self.getNumberInput("Number of generations", 1, castToType=int)
            print("The current settings: ")
            print("minBoreLength", minBoreLength)
            print("maxBoreLength", maxBoreLength)
            print("minBoreWidth", minBoreWidth)
            print("maxBoreWidth", maxBoreWidth)
            print("maxLaunchAngle", maxLaunchAngle)
            print("minPlatformHeight", minPlatformHeight)
            print("maxPlatformHeight", maxPlatformHeight)
            print("minGunPowderMass", minGunPowderMass)
            print("maxGunPowderMass", maxGunPowderMass)
            print("crossoverRate", crossoverRate)
            print("mutationRate", mutationRate)
            print("populationSize", populationSize)
            print("numberOfGenerations", numberOfGenerations)
            print("")
            print("Running Simulation on cluster please wait...")
            data = {"requestType": "cannonSimulation",
                    "minBoreLength": minBoreLength,
                    "maxBoreLength": maxBoreLength,
                    "minBoreWidth": minBoreWidth,
                    "maxBoreWidth": maxBoreWidth,
                    "minLaunchAngle": minLaunchAngle,
                    "maxLaunchAngle": maxLaunchAngle,
                    "minPlatformHeight": minPlatformHeight,
                    "maxPlatformHeight": maxPlatformHeight,
                    "minGunPowderMass": minGunPowderMass,
                    "maxGunPowderMass": maxGunPowderMass,
                    "crossoverRate": crossoverRate,
                    "mutationRate": mutationRate,
                    "populationSize": populationSize,
                    "numberOfGenerations": numberOfGenerations,
                    "distr": True}

            message = self.encodeMessage(data)
            returnMessage = self.sendMessage(message, self.serverAddress)
            print(returnMessage)
            print("Finished")

            input("Press Enter to go back to the main menu\n>> ")
            self.mainMenu()

        elif optionChosen == "Back to Main Menu":
            self.mainMenu()

    def viewExperimentsMenu(self):
        self.clear()
        print("Genetic Lab - View Experiments")

    def close(self):
        self.clear()
        print("Closing Genetic Lab")

    def clear(self):
        os.system('cls' if os.name == "nt" else "clear")

    def run(self):
        #self.mainMenu()
        print("temp send message")
        data = {"requestType": "cannonSimulation",
                "minBoreWidth": 1,
                "maxBoreWidth": 1,
                "minBoreLength": 1,
                "maxBoreLength": 1,
                "minLaunchAngle": 1,
                "maxLaunchAngle": 1,
                "minPlatformHeight": 1,
                "maxPlatformHeight": 1,
                "minGunPowderMass": 1,
                "maxGunPowderMass": 1,
                "crossoverRate": 1,
                "mutationRate": 1,
                "populationSize": 1,
                "numberOfGenerations": 1,
                "targetDistance": 1}
        message = self.encodeMessage(data)
        returnMessage = self.sendMessage(message, self.serverAddress)
        print(returnMessage)


    def getSimulationResults(self):
        pass
