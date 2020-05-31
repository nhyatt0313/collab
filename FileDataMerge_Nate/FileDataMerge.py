import os
import pathlib

filePath = pathlib.Path(__file__).parent.absolute()

logEnabled = True
logLevel = 0
directory = None
lambdasParsed = False
lambdas = []
aveMT = []
aveMR = []
allMR = [] # a list of lists - each list gathered from 1 file
allMT = [] # a list of lists - each list gathered from 1 file
roundTo = 2

def log(message, level):
    global logEnabled, logLevel
    if log and level <= logLevel:
        print(message)

def getLambdas(line):
    data = line.split('\t')
    return float(data[0])


def getCounts(line):
    data = line.split('\t')
    return float(data[1].replace('\n', ''))


def parseMRData(f):
    log("\tparsing R data file: " + f, 0)
    file = open(directory+"\\R\\"+f, 'r')
    line = file.readline()
    mR = []
    while line:
        if not line.startswith('#'):
            global lambdasParsed
            if not lambdasParsed:
                lambdas.append(getLambdas(line))
            mR.append(getCounts(line))
        line = file.readline()
    lambdasParsed = True
    return mR


def parseMTData(f):
    log("\tparsing T data file: " + f, 0)
    file = open(directory+"\\T\\"+f, 'r')
    line = file.readline()
    mT = []
    while line:
        if not line.startswith('#'):
            mT.append(getCounts(line))
        line = file.readline()
    return mT


def directoryScanner(path):
    cd = path.split("\\")[-1]
    log("\n\n\tList of Paths: " + str(os.listdir(path)), 2)
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file)):
            if cd == "R":
                if file.endswith(".egg"):
                    allMR.append(parseMRData(file))
                    log("\t\tallMR = " + str(allMR), 1)
            if cd == "T":
                if file.endswith(".egg"):
                    allMT.append(parseMTData(file))
                    log("\t\tallMT = " + str(allMT), 1)
        else:
            directoryScanner(os.path.join(path, file))


def createLineToWrite(i):
    delim = "\t"
    return (format(lambdas[i], ".2f") + delim + format(aveMR[i], ".2f") + delim + format(aveMT[i], ".2f") + "\n")


def printDataToFile(fullPath):
    global aveMR, aveMT, lambdas
    file = open(fullPath, 'w')
    if len(lambdas) == len(aveMR) == len(aveMT):
        for iter in range(len(lambdas)):
            file.write(createLineToWrite(iter))
        print("Output File Created: " + fullPath)
    else:
        print("ERROR: not all data lists are the same size: lambdas = " + str(len(lambdas)) + " | aveMR = " + str(len(aveMR)) + " | aveMT = " + str(len(aveMT)))


def averageAllMRCounts():
    log("\taveraging R data values", 0)
    global allMR, aveMR, roundTo
    validData = True
    listSize = len(allMR[0])
    for i in range(1, len(allMR)):
        if len(allMR[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allMR)):
                sum += allMR[j][i]
            ave = sum / len(allMR)
            aveMR.append(round(ave, roundTo))
        log("\t\taveMR = " + str(aveMR), 1)
    else:
        print("ERROR: invalid data: list sizes in allMR = [")
        for i in range(0, len(allMR)):
            print(str(len(allMR[i])))
            if i != len(allMR):
                print(", ")
            else:
                print("]")


def averageAllMTCounts():
    log("\taveraging T data values", 0)
    global allMT, aveMT
    validData = True
    listSize = len(allMT[0])
    for i in range(1, len(allMT)):
        if len(allMT[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allMT)):
                sum += allMT[j][i]
            ave = sum / len(allMT)
            aveMT.append(round(ave, roundTo))
        log("\t\taveMT = " + str(aveMT), 1)
    else:
        print("ERROR: invalid data: list sizes in allMT = [")
        for i in range(0, len(allMT)):
            print(str(len(allMT[i])))
            if i != len(allMT):
                print(", ")
            else:
                print("]")


def main():
    global directory, filePath
    print("\n\n")
    directory = input("Enter Directory: ")
    log("Scanning directory " + directory, 0)
    directoryScanner(directory)
    averageAllMRCounts()
    averageAllMTCounts()
    inputFolderName = directory.split("\\")[-1]
    printDataToFile(str(filePath) + r'\Output\output_' + str(inputFolderName) + r".txt")
    print("Process Completed\n")

main()