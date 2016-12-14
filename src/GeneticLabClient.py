import os
from time import sleep

class GeneticLabClient:
    def __init__(self):
        self.mainMenuOptions = ["Run Experiment", "View Running", "Exit"]
        self.runExperimentOptions = ["Cannon", "Back to Main Menu"]

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
            minCannonLength = 1
            maxCannonLength = 3
            minBoreWidth = 0.10
            maxBoreWidth = 0.30
            maxAngle = 90
            crossOverRate = 0.65
            mutationRate = 0.01
            populationSize = 100
            numberOfGenerations = 1000
            if not useDefault:
                minCannonLength = self.getNumberInput("Min cannon length (meters)", 0)
                maxCannonLength = self.getNumberInput("Max cannon length (meters)", minCannonLength)
                minBoreWidth = self.getNumberInput("Min bore width (meters)", 0)
                maxBoreWidth = self.getNumberInput("Max bore width (meters)", minBoreWidth)
                maxAngle = self.getNumberInput("Max launch angle (degrees)", 0, 180)
                crossOverRate = self.getNumberInput("Crossover rate (float between 0 and 1)", 0, 1)
                mutationRate = self.getNumberInput("Mutation rate (float between 0 and 1)", 0, 1)
                populationSize = self.getNumberInput("Population size", castToType=int)
                numberOfGenerations = self.getNumberInput("Number of generations", castToType=int)
            print("The current settings: ")
            print("minCannonLength", minCannonLength)
            print("maxCannonLength", maxCannonLength)
            print("minBoreWidth", minBoreWidth)
            print("maxBoreWidth", maxBoreWidth)
            print("maxAngle", maxAngle)
            print("crossOverRate", crossOverRate)
            print("mutationRate", mutationRate)
            print("populationSize", populationSize)
            print("numberOfGenerations", numberOfGenerations)

            runSim = self.getBooleanInput("Do you want to send this cannon simulation to be ran by the server (y/n)")
            if runSim:
                print("Sending simulation to server")
            else:
                print("The simulation will not be sent to the server")

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
        self.mainMenu()

