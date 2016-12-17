from src.GeneticLabClient import GeneticLabClient

def main():

    #geneticLabClient = GeneticLabClient(9000, "127.0.0.1")
    geneticLabClient = GeneticLabClient(9000, "172.22.71.28")

    #geneticLabClient.run()
    geneticLabClient.runExperimentMenu()


if __name__ == "__main__":
    main()
