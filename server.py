from src.GeneticLabServer import GeneticLabServer

def main():
    servers = []
    servers.append("172.22.71.28")
    servers.append("172.22.71.29")
    geneticLabServer = GeneticLabServer(9000, servers)
    geneticLabServer.run()


if __name__ == "__main__":
    main()
