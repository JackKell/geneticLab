from src.GeneticLabClient import GeneticLabClient

def main():
    servers = []
    servers.append("172.22.71.28")
    servers.append("172.22.71.29")
    geneticLabClient = GeneticLabClient(9000, "127.0.0.1")
    geneticLabClient.run()


if __name__ == "__main__":
    main()
