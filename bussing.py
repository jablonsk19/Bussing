import data
import os
import sys
import argparse

def commandLineRun(args):
    """Perform the steps necessary to bridge the gaps in Thermo-Calc to model heat treatment optimization

    Example:
    """

    args = args[1:]

    parser = argparse.ArgumentParser(description="Perform the steps necessary to bridge the gaps in "
                                                 "Thermo-Calc to model heat treatment optimization.",
                                     prog='bussing')
    parser.add_argument("path", help="The path of the folder conaining necessary .exp files.  The folder must"
                                     "not contain any more .exp files than the ones used to run this tool.")
    parser.add_argument("main", help="The file (in the directory 'path') that plots total mass fraction liquid against "
                                     "temperature.")
    parser.add_argument("homog_dist", help= "The distance over which to homogenize, normally (1/2)*(SDAS)")
    ns = parser.parse_args(args)
    runMain(ns.path, ns.main, ns.homog_dist)





def runMain(filePath, mainFile, homog_dist):
    """read in all exp files in specified directory and produce outputs to the user."""

    # ---=== Parse data files ===---

    dataList = []
    liqData = ""
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
    liqData.wtFrLiq = [1 - x for x in liqData.wtFrLiq]

    # ---=== Output data ===---

    # TODO replace these print statements with the actual functionality of the program
    print("\n\nAFTER\n\n")

    for elem in dataList:
        print(elem.element)
        print(elem.wtFrLiq)
        print(elem.temperature)

    print()
    print(liqData.element)
    print(liqData.wtFrLiq)
    print(liqData.temperature)





if __name__ == '__main__':
    commandLineRun(sys.argv)
