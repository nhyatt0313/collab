import os

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

class iadReady:
    lambdas = []
    mR = []
    mT = []

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

#needs to be changed
#should not be returning aveMR just yet
#need to write a for-loop which returns allCountsR[i] + allCountsR[i], allCountsR[i]+allCountsT[i+1], etc.
def createLineToWrite(i):
    delim = "\t"
    return "" # this is where out new object will come in handy


#blah

#need to ensure r0, r1 are single average values
#need to ensure r, is the array averageallCountsTCounts
#need to ensure output is an array that is then written into the new file
#r is actually the array averageallCountsRCounts 
def MR(r, r0, r1):
    #rstd, is reflectance of spectralon standard
    #r, is reflectance off sample
    #r0, is R(0,0), empty port reflectance
    #r1, is R(rstd, rstd), spectralon standard in port
    rstd = 1
    mR = []
    if len(r) == len(r0) == len(r1):
        for i in range(len(r)):
            mR.append(rstd * (r[i] - r0[i])/(r1[i] - r0[i]))
    else:
        print("ERROR: not all lists are the same size")
    return mR


#t is actually the array averageallCountsTCounts 
def MT(t, t0, t1):
    #t, transmission through sample, T(ts_direct, ts)
    #t0, Tdark, transmission through port blocked by spectralon standard, T_dark
    #t1, transmission through sphere with empty port, T(0,0)
    mT = []
    if len(t) == len(t0) == len(t1):
        for i in range(len(t)):
            mT.append((t[i] - t0[i])/(t1[i] - t0[i]))
    else:
        print("ERROR: not all lists are the same size")
    return mT


def printDataToFile():
    global lambdas, allCountsR, allCountsT, aver0, aver1, avet0, avet1
    filename = 'output.txt'
    file = open(filename, 'w')
    mR = MR(allCountsR, aver0, aver1)
    mT = MT(allCountsT, avet0, avet1)
    if len(lambdas) == len(mR) == len(mT):
        for iter in range(len(lambdas)):
            file.write(createLineToWrite(iter))
    else:
        print(f"ERROR: not all data lists are the same size: lambdas = {len(lambdas)} | mR = {len(mR)} | mT = {len(mT)}")


#this is wrong, the function will be much simpler as the values do not depend on wavelength.        
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


#The above two functions were also done for t0 and t1. 
#Actually, I realize those two functions are incorrect for what I'm doing here. 
#The function will be much simpler as the values do not depend on wavelength.
#Once I fix that, those average values for r0, r1, t0, t1, will serve as the 
#input into my def MR and def MT equations, along with r and t (which are really the arrays MR and MT).
#*the arrays averageallCountsRCounts and averageallCountsTCounts
#Then, I need to ensure output of def MR and def MT is an array that is then written into the new data file                

def prepareIadReady():
    # find all combinations of mr and mt to return a list of iadReady objects
    readyObjects = []


def main():
    global directory, allr0, aver0, allr1, aver1, allt0, avet0, allt1, avet1, roundTo
    directory = input("Enter Directory: ")
    print("Scanning directory " + directory)
    directoryScanner(directory)
    averageAllCounts(allr0, aver0, roundTo)
    averageAllCounts(allt0, avet0, roundTo)
    averageAllCounts(allr1, aver1, roundTo)
    averageAllCounts(allt1, avet1, roundTo)
    prepareIadReady()
    printDataToFile()

main()