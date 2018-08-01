
class ExpData:
    def __init__(self, filename):
        self.wtFrLiq = []
        self.wtFrSol = [] # to be initialized later during computation
        self.temperature = []
        self.element = "NOT AN ELEMENT"
        self.readFile(filename)
        pass


    def readFile(self, filename):
        """Read in a .exp file given a path to it and initialize the local variables
        element, wtFrLiq, and temperature.
        """
        with open(filename) as f:
            contents = f.read()

        contents = contents.split('\n')

        # Find the important data points, axes are weight fraction liquid against temperature.

        read = False
        for line in contents:
            # Grab element, if possible
            if "XTEXT  W(" in line:
                self.element = line[line.find(',') + 1 : line.find(')')].capitalize()
            elif line.endswith("M"):
                read = True
            elif line.startswith("BLOCKEND"):
                read = False
            elif read:
                line = line.split()
                self.wtFrLiq.append(float(line[0]))
                self.temperature.append(float(line[1]))


def normalize(data):
    """Return a normalized list (Feature scaling) based on https://en.wikipedia.org/wiki/Feature_scaling"""
    large = max(data)
    small = min(data)

    return [(x - small) / (large - small) for x in data]

