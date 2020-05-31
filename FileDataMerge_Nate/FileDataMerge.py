import os
import pathlib

filePath = pathlib.Path(__file__).parent.absolute()

logEnabled = True
logLevel = 0

directory = None
lambdasParsed = False
roundTo = 2

lambdas = []
allCountsR = [] # a list of lists - each list gathered from 1 file
allCountsT = [] # a list of lists - each list gathered from 1 file

allr0 = []
aver0 = []

allr1 = []
aver1 = []

allt0 = []
avet0 = []

allt1 = []
avet1 = []

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


def parseData(dataFolder, dataFile):
    print(f"\tparsing {dataFolder} data file: " + dataFile)
    file = open(directory + "\\" + dataFolder + "\\" + dataFile, 'r')
    line = file.readline()
    data = []
    while line:
        if not line.startswith('#'):
            global lambdasParsed
            if not lambdasParsed:
                lambdas.append(getLambdas(line))
            data.append(getCounts(line))
        line = file.readline()
    lambdasParsed = True
    return data

def calcMR(r, r0, r1):
    rstd = 1
    mR = []
    if len(r) == len(r0) == len(r1):
        for i in range(len(r)):
            mR.append(rstd * (r[i] - r0[i])/(r1[i] - r0[i]))
    else:
        print("ERROR: not all lists are the same size")
    return mR


def calcMT(t, t0, t1):
    mT = []
    if len(t) == len(t0) == len(t1):
        for i in range(len(t)):
            mT.append((t[i] - t0[i])/(t1[i] - t0[i]))
    else:
        print("ERROR: not all lists are the same size")
    return mT


def directoryScanner(path):
    cd = path.split("\\")[-1]
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file)):
            if cd == "R":
                if file.startswith("cal-r0"):
                    allr0.append(parseData("R", file)) #might need fixing, can't use parseMRData here, should not append to mR
                    print("\t\tallro=" + str(allr0)) #these need to be removed later, don't need a ton of strings being printed
                if file.startswith("cal-r1"):
                    allr1.append(parseData("R", file))
                    print("\t\tallr1=" + str(allr1))
                if file.startswith("sample-"): #this used to say .endswith(".egg"), changed to simplify
                    allCountsR.append(parseData("R", file))
                    print("\t\tallCountsR = " + str(allCountsR))
            if cd == "T":
                if file.startswith("cal-t0"):
                    allt0.append(parseData("T", file))
                    print("\t\tallto=" + str(allt0))
                if file.startswith("cal-t1"):
                    allt1.append(parseData("T", file))
                    print("\t\tallt1=" + str(allt1))
                if file.startswith("sample-"): #used to say .endswith(".egg"), changed to simplify
                    allCountsT.append(parseData("T", file))
                    print("\t\tallCountsT = " + str(allCountsT))
        else:
            directoryScanner(os.path.join(path, file))


def createLineToWrite(i):
    delim = "\t"
    return "TODO"


def printDataToFile(fullPath):
    global aveMR, aveMT, lambdas
    file = open(fullPath, 'w')
    if len(lambdas) == len(aveMR) == len(aveMT):
        for iter in range(len(lambdas)):
            file.write(createLineToWrite(iter))
        print("Output File Created: " + fullPath)
    else:
        print("ERROR: not all data lists are the same size: lambdas = " + str(len(lambdas)) + " | aveMR = " + str(len(aveMR)) + " | aveMT = " + str(len(aveMT)))


def averageAllCounts(list1, list2, roundTo): 
    print("\taveraging r0 data values")
    validData = True
    listSize = len(list1[0])
    for i in range(1, len(list1)):
        if len(list1[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(list1)):
                sum += list1[j][i]
            ave = sum / len(list1)
            list2.append(round(ave, roundTo))
        print("\t\tave = " + str(list1))
    else:
        print("ERROR: invalid data: list sizes in all = [")
        for i in range(0, len(list1)):
            print(str(len(list1[i])))
            if i != len(list1):
                print(", ")
            else:
                print("]")


def main():
    global directory, filePath
    print("\n\n")
    directory = input("Enter Directory: ")
    log("Scanning directory " + directory, 0)
    directoryScanner(directory)
    averageAllCounts(allr0, aver0, roundTo)
    averageAllCounts(allt0, avet0, roundTo)
    averageAllCounts(allr1, aver1, roundTo)
    averageAllCounts(allt1, avet1, roundTo)
    inputFolderName = directory.split("\\")[-1]
    printDataToFile(str(filePath) + r'\Output\output_' + str(inputFolderName) + r".txt")
    print("Process Completed\n")

main()