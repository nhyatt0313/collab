import os
import pathlib

filePath = pathlib.Path(__file__).parent.absolute()

logEnabled = True
logLevel = 0

directory = None
lambdasParsed = False

lambdas = []
allCountsR = [] # a list of lists - each list gathered from 1 file
allCountsT = [] # a list of lists - each list gathered from 1 file

allr0 = []
allr1 = []
allt0 = []
allt1 = []

header = ""
with open("header.txt", 'r') as file:
    header = file.read()

M_U =0.0000
r_w =0.9788
t_w = 0.9788
rstd = 0.9800
tstd = 1.0000

class IadReady:
    def __init__(self, lambdas, mR, mT, fileName):
        self.lambdas = lambdas
        self.mR = mR
        self.mT = mT
        self.fileName = fileName

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
    filePath = f"{directory}\\{dataFolder}\\{dataFile}".replace("\\", "/")
    file = open(filePath, 'r')
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
                    allr0.append(parseData("R", file))
                if file.startswith("cal-r1"):
                    allr1.append(parseData("R", file))
                if file.startswith("sample-"):
                    allCountsR.append(parseData("R", file))
            if cd == "T":
                if file.startswith("cal-t0"):
                    allt0.append(parseData("T", file))
                if file.startswith("cal-t1"):
                    allt1.append(parseData("T", file))
                if file.startswith("sample-"):
                    allCountsT.append(parseData("T", file))
        else:
            directoryScanner(os.path.join(path, file))


def createLineToWrite(iadReady, i):
    return f"{iadReady.lambdas[i]}\t{iadReady.mR[i]}\t{iadReady.mT[i]}\t{M_U}\t{r_w}\t{t_w}\t{rstd}\t{tstd}\n"


def printDataToFile(iadReady, fullPath):
    global header
    fullPath = f"{fullPath}/{iadReady.fileName}.rxt"
    file = open(fullPath, 'w')
    if len(iadReady.lambdas) == len(iadReady.mR) == len(iadReady.mT):
        file.write(header)
        for i in range(len(iadReady.lambdas)):
            file.write(createLineToWrite(iadReady, i))
        print("Output File Created: " + fullPath)
    else:
        print(f"ERROR: not all data lists are the same size: iadReady.lambdas = {len(iadReady.lambdas)} | iadReady.mR = {len(iadReady.mR)} | iadReady.mT = {len(iadReady.mT)}")


def averageAllCounts(allList): 
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
            ave = sum / len(allList)
            aveList.append(ave)
        return aveList
    else:
        print("ERROR: invalid data: list sizes in all = [")
        for i in range(0, len(allList)):
            print(str(len(allList[i])))
            if i != len(allList):
                print(", ")
            else:
                print("]")
        return None

def createIadReadyListForOutFiles():
    global lambdas, allr0, allt0, allr1, allt1
    iadReadyList = []
    averageR0 = averageAllCounts(allr0)
    averageT0 = averageAllCounts(allt0)
    averageR1 = averageAllCounts(allr1)
    averageT1 = averageAllCounts(allt1)
        
    allMRs = []
    # perform calculation for MR values
    for countsR in allCountsR:
        allMRs.append(calcMR(countsR, averageR0, averageR1))

    allMTs = []
    # perform calculation for MT values
    for countsT in allCountsT:
        allMTs.append(calcMT(countsT, averageT0, averageT1))

    # create all combinations
    allCombosPerLambda = [] #( ([mR col from file_1],[mT col from file_1]), ... ([mR col from file_n],[mT col from file_n]) )
    for r in allMRs:
        for t in allMTs:
            allCombosPerLambda.append((r, t))

    for i, combo in enumerate(allCombosPerLambda):
        iadReadyList.append(IadReady(lambdas, combo[0], combo[1], f"combo_{i}"))
        
    return iadReadyList
    

def writeAllCombinationsToFiles(iadReadyList, fullPath):
    global lambdas
    for iadReady in iadReadyList:
        printDataToFile(iadReady, fullPath)

def main():
    global directory, filePath
    print("\n\n")
    directory = input("Enter Directory: ")
    log("Scanning directory " + directory, 0)
    directoryScanner(directory)
    iadReadyList = createIadReadyListForOutFiles()
    nestedDir = r"\Output"
    writeAllCombinationsToFiles(iadReadyList, f"{filePath}{nestedDir}")

    print("Process Completed\n")

main()