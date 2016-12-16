from src.GeneticLabClient import GeneticLabClient

def main():
    geneticLabClient = GeneticLabClient(9000, "127.0.0.1")
    geneticLabClient.run()


if __name__ == "__main__":
    main()
