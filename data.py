import numpy as np
from copy import copy


class ExpData:
    def __init__(self, filename):
        self.wtFrLiq = []
        self.temperature = []
        self.element = "UNKNOWN"
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
            if "XTEXT" in line:
                self.element = line[line.find(',') + 1 : line.find(')')]
            elif line.endswith("M"):
                read = True
            elif line.startswith("BLOCKEND"):
                read = False
            elif read:
                line = line.split()
                self.wtFrLiq.append(float(line[0]))
                self.temperature.append(float(line[1]))




if __name__ == '__main__':
    # For now, just read in a single file and spit out the outputs (file not accessable to GitHub, but
    # this is ok because this is just temporary behavior for testing)
    data = ExpData("../Homogenize-Solid/Liq-Al.exp")
    print(data.element)
    print(data.wtFrLiq)
    print(data.temperature)

