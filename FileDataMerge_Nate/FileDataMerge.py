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
allr1 = []
allt0 = []
allt1 = []

class IadReady:
    def __init__(self, lambdas, mR, mT, outFileName):
        self.lambdas = lambdas
        self.mR = mR
        self.mT = mT

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


def createLineToWrite(iadReady, i):
    delim = "\t"
    return "TODO"


def printDataToFile(iadReady, fullPathPrefix):
    fullPath = f"{fullPathPrefix}_{iadReady.comboId}.txt"
    file = open(fullPath, 'w')
    if len(iadReady.lambdas) == len(iadReady.mR) == len(iadReady.mT):
        for i in range(len(iadReady.lambdas)):
            file.write(createLineToWrite(iadReady, i))
        print("Output File Created: " + fullPath)
    else:
        print(f"ERROR: not all data lists are the same size: iadReady.lambdas = {len(iadReady.lambdas)} | iadReady.mR = {len(iadReady.mR)} | iadReady.mT = {len(iadReady.mT)}")


def averageAllCounts(allList, roundTo): 
    print("\taveraging data values")
    aveList = []
    validData = True
    listSize = len(allList[0])
    for i in range(1, len(allList)):
        if len(allList[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allList)):
                sum += allList[j][i]
            ave = sum / len(list)
            aveList.append(round(ave, roundTo))
        print("\t\tave = " + str(list))
        return aveList
    else:
        print("ERROR: invalid data: list sizes in all = [")
        for i in range(0, len(list)):
            print(str(len(allList[i])))
            if i != len(list):
                print(", ")
            else:
                print("]")
        return None

def createIadReadyListForOutFiles():
    global lambdas, allr0, allt0, allr1, allt1, roundTo
    iadReadyList = []
    allMTCombosPerLambda = set() # this is a set of tuples of lists ( ([mR col from file_1],[mT col from file_1]), ... ([mR col from file_n],[mT col from file_n]) ) all combos
    # this double for loop is not the most efficient, but works for now
    for r in allCountsR:
        for t in allCountsT:
            # can't add duplicates to set
            # note that r ant t are colums from a file
            allMTCombosPerLambda.add((r, t))
    for i, lambdaList in enumerate(lambdas):
        # averaging a row across all files
        averageR0 = averageAllCounts(allr0[i], roundTo)
        averageT0 = averageAllCounts(allt0[i], roundTo)
        averageR1 = averageAllCounts(allr1[i], roundTo)
        averageT1 = averageAllCounts(allt1[i], roundTo)
        




        mR = 1 # TODO use above values to calculate with calculateMR function
        mT = 1
        
        iadReadyList.append(IadReady(lambdaList, mR, mT, ""))

    return iadReadyList
    

def writeAllCombinationsToFiles(fullPathPrefix):
    # TODO
    global lambdas
    mR = []
    mT = []
    comboId = 34
    iadReady = IadReady(lambdas, mR, mT, comboId)
    printDataToFile(iadReady, fullPathPrefix)
    return None

def main():
    global directory, filePath
    print("\n\n")
    directory = input("Enter Directory: ")
    log("Scanning directory " + directory, 0)
    directoryScanner(directory)

    inputFolderName = directory.split("\\")[-1]

    iadReadyList = createIadReadyListForOutFiles()

    nestedDir = r"\Output"
    outFileNamePrefix = f"\\output_{inputFolderName}"
    writeAllCombinationsToFiles(f"{filePath}{nestedDir}{outFileNamePrefix}")

    print("Process Completed\n")

main()