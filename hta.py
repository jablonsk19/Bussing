import data
import os
import sys
import argparse
import mainGui

def commandLineRun(args):
    """Perform a command-line version of HTA.

    Arguments:
        args -- all command-line arguments (including the name of the program itself)
    """

    args = args[1:]

    parser = argparse.ArgumentParser(description="Perform the steps necessary to bridge the gaps in "
                                     "Thermo-Calc to model heat treatment optimization.  \n\nOutputs a folder with "
                                     "multiple files.  Matrix.dat contains the distance at which each data point "
                                     "is calculated.  All other files contain their instantaneous percent solid by "
                                     "weight relative to the distance given by the SDAS.  ",
                                     prog='Hta')
    parser.add_argument("path", help="The path of the folder conaining necessary .exp files.  The folder must"
                                     "not contain any more .exp files than the ones used to run this tool.")
    parser.add_argument("main", help="The file (in the directory 'path') that plots total mass fraction liquid against "
                                     "temperature.")
    parser.add_argument("homog_dist", help= "The distance over which to homogenize, normally (1/2)*(SDAS)")

    ns = parser.parse_args(args)
    # TODO add check to find if output folder already exists
    runMain(ns.path, ns.main, float(ns.homog_dist))


def runMain(filePath, mainFile, homog_dist):
    """read in all exp files in specified directory and produce outputs to the user.

    Arguments:
        filePath -- The path of the folder conaining necessary .exp files.  The folder must not contain any more
            .exp files than the ones used to run this tool.
        mainFile -- The file (in the directory 'path') that plots total mass fraction liquid against temperature
        homog_dist -- the distance over which to homogenize, usually (1/2)*(SDAS)
    """

    # ---=== Parse data files ===---

    dataList = []
    liqData = ""
    if not filePath.endswith("/"):
        filePath += "/"
    for path in os.listdir(filePath):

        if path == mainFile:
            liqData = filePath + mainFile
            continue

        path = filePath + path
        if path.endswith("exp"):
            dataList.append(data.ExpData(os.path.abspath(path)))

    liqData = data.ExpData(liqData)

    # ---=== Massage data ===---

    # delete repeated elements
    for i in range(len(liqData.wtFrLiq) - 1):
        try:
            while liqData.wtFrLiq[i] == liqData.wtFrLiq[i + 1]:
                del liqData.wtFrLiq[i]
                del liqData.temperature[i]
                for elem in dataList:
                    del elem.wtFrLiq[i]
                    del elem.temperature[i]
        except IndexError:
            break
    liqData.wtFrLiq = data.normalize(liqData.wtFrLiq)

    # Implemented eq 1 and eq 2 from https://link.springer.com/article/10.1007/s11665-016-2451-3

    for elem in dataList:
        incFrSol = 0
        startPoint = 0
        lastFracLiq = 0
        for eLiq, tLiq in zip(elem.wtFrLiq, liqData.wtFrLiq):
            if(tLiq == 1.0):
                startPoint = eLiq
            else:
                incFrSol = lastFracLiq - tLiq
                elem.wtFrSol.append((startPoint - tLiq * eLiq ) / incFrSol)
                startPoint = tLiq * eLiq
            lastFracLiq = tLiq

        # Duplicate item at position 0 to have some value for pre-solidification
        elem.wtFrSol.insert(0, elem.wtFrSol[0])

    # ---=== Output data ===---

    # output Matrix.dat (validated against previous versions' outputs)
    # TODO maybe add an option to name output folder
    if not os.path.isdir("./HTA Outputs"):
        os.mkdir("./HTA Outputs")
    with open("./HTA Outputs/Matrix.dat", "w") as f:
        for num in liqData.wtFrLiq:
            f.write(str(num*homog_dist) + "\n")

    # output element-specific data files (percent solid against distance provided in Matrix.dat)
    for elem in dataList:
        with open("./HTA Outputs/" + elem.element + "-matrix.txt", "w") as f:
            for num in elem.wtFrSol:
                f.write(str(num*100) + "\n")

    # Sanity check:
    # sumLists = []
    # for elem in dataList:
    #     for i, num in enumerate(elem.wtFrSol):
    #         try:
    #             sumLists[i] += num
    #         except IndexError:
    #             sumLists.append(num)
    # print(sumLists)

    print("Outputs written (" + str(len(liqData.temperature)) + " lines each).  ")
    print("The solidus is " + str(liqData.temperature[1]) + ".")

    return (str(len(liqData.temperature)), str(liqData.temperature[1]))


if __name__ == '__main__':
    # If no args, run gui, else run cli instance
    if len(sys.argv) == 1:
        mainGui.runGui()
    else:
        commandLineRun(sys.argv)
