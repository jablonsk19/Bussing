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
    dataList = []
    totalLiq = ""
    for path in os.listdir(filePath):

        if path == mainFile:
            totalLiq = filePath + mainFile
            continue

        path = filePath + path
        if path.endswith("exp"):
            dataList.append(data.ExpData(os.path.abspath(path)))

    # TODO replace these print statements with the actual functionality of the program
    for el in dataList:
        print(el.element)
        print(el.wtFrLiq)
        print(el.temperature)

    print(totalLiq)

if __name__ == '__main__':
    commandLineRun(sys.argv)
