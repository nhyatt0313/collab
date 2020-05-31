import os

directory = None
lambdasParsed = False
lambdas = []
aveMT = [] #all instances of MT should be understood to mean 'Transmittance', not measured total transmission MT
aveMR = [] ##all instances of MR should be understood to mean 'Reflectance', not measured total reflection MR
allMR = [] # a list of lists - each list gathered from 1 file
allMT = [] # a list of lists - each list gathered from 1 file
roundTo = 2


def getLambdas(line):
    data = line.split('\t')
    return float(data[0])


def getCounts(line):
    data = line.split('\t')
    return float(data[1].replace('\n', ''))


def parseMRData(f):
    print("\tparsing R data file: " + f)
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
    print("\tparsing T data file: " + f)
    file = open(directory+"\\T\\"+f, 'r')
    line = file.readline()
    mT = []
    while line:
        if not line.startswith('#'):
            mT.append(getCounts(line))
        line = file.readline()
    return mT

allr0 = []
aver0 = []

allr1 = []
aver1 = []

allt0 = []
avet0 = []

allt1 = []
avet1 = []

def directoryScanner(path):
    cd = path.split("\\")[-1]
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file)):
            if cd == "R":
                if file.startswith("cal-r0"):
                    allr0.append(parseMRData(file)) #might need fixing, can't use parseMRData here, should not append to mR
                    print("\t\tallro=" + str(allr0)) #these need to be removed later, don't need a ton of strings being printed
                if file.startswith("cal-r1"):
                    allr1.append(parseMRData(file))
                    print("\t\tallr1=" + str(allr1))
                if file.startswith("sample-"): #this used to say .endswith(".egg"), changed to simplify
                    allMR.append(parseMRData(file))
                    print("\t\tallMR = " + str(allMR))
            if cd == "T":
                if file.startswith("cal-t0"):
                    allt0.append(parseMTData(file))
                    print("\t\tallto=" + str(allt0))
                if file.startswith("cal-t1"):
                    allt1.append(parseMTData(file))
                    print("\t\tallt1=" + str(allt1))
                if file.startswith("sample-"): #used to say .endswith(".egg"), changed to simplify
                    allMT.append(parseMTData(file))
                    print("\t\tallMT = " + str(allMT))
        else:
            directoryScanner(os.path.join(path, file))

#needs to be changed
#should not be returning aveMR just yet
#need to write a for-loop which returns allMR[i] + allMR[i], allMR[i]+allMT[i+1], etc.
def createLineToWrite(i):
    delim = "\t"
    return str(lambdas[i]) + delim + str(aveMR[i]) + delim + str(aveMT[i]) + "\n"


#need to ensure r0, r1 are single average values
#need to ensure r, is the array averageAllMTCounts
#need to ensure output is an array that is then written into the new file
#r is actually the array averageAllMRCounts 
def MR(rstd, r, r0, r1):
    #rstd, is reflectance of spectralon standard
    #r, is reflectance off sample
    #r0, is R(0,0), empty port reflectance
    #r1, is R(rstd, rstd), spectralon standard in port
    rstd = 1
    return rstd * (r - r0)/(r1 - r0)

#t is actually the array averageAllMTCounts 
def MT(t, t0, t1):
    #t, transmission through sample, T(ts_direct, ts)
    #t0, Tdark, transmission through port blocked by spectralon standard, T_dark
    #t1, transmission through sphere with empty port, T(0,0)
    return (t - t0)/(t1 - t0)



def printDataToFile():
    global aveMR, aveMT, lambdas
    filename = 'output.txt'
    file = open(filename, 'w')
    if len(lambdas) == len(aveMR) == len(aveMT):
        for iter in range(len(lambdas)):
            file.write(createLineToWrite(iter))
    else:
        print("ERROR: not all data lists are the same size: lambdas = " + str(len(lambdas)) + " | aveMR = " + str(len(aveMR)) + " | aveMT = " + str(len(aveMT)))


#this is wrong, the function will be much simpler as the values do not depend on wavelength.        
def averageAllr0Counts(): 
    print("\taveraging r0 data values")
    global allr0, aver0, roundTo
    validData = True
    listSize = len(allr0[0])
    for i in range(1, len(allr0)):
        if len(allr0[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allr0)):
                sum += allr0[j][i]
            ave = sum / len(allr0)
            aver0.append(round(ave, roundTo))
        print("\t\taver0 = " + str(aver0))
    else:
        print("ERROR: invalid data: list sizes in allr0 = [")
        for i in range(0, len(allr0)):
            print(str(len(allr0[i])))
            if i != len(allr0):
                print(", ")
            else:
                print("]")

#this is wrong, the function will be much simpler as the values do not depend on wavelength. 
def averageAllr1Counts():
    print("\taveraging r1 data values")
    global allr1, aver1, roundTo
    validData = True
    listSize = len(allr1[0])
    for i in range(1, len(allr1)):
        if len(allr1[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allr1)):
                sum += allr1[j][i]
            ave = sum / len(allr1)
            aver1.append(round(ave, roundTo))
        print("\t\taver1 = " + str(aver1))
    else:
        print("ERROR: invalid data: list sizes in allr1 = [")
        for i in range(0, len(allr1)):
            print(str(len(allr1[i])))
            if i != len(allr1):
                print(", ")
            else:
                print("]")
                
 #this is wrong, the function will be much simpler as the values do not depend on wavelength.        
def averageAllt0Counts():
    print("\taveraging t0 data values")
    global allt0, avet0, roundTo
    validData = True
    listSize = len(allt0[0])
    for i in range(1, len(allt0)):
        if len(allt0[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allt0)):
                sum += allt0[j][i]
            ave = sum / len(allt0)
            avet0.append(round(ave, roundTo))
        print("\t\tavet0 = " + str(avet0))
    else:
        print("ERROR: invalid data: list sizes in allt0 = [")
        for i in range(0, len(allt0)):
            print(str(len(allt0[i])))
            if i != len(allt0):
                print(", ")
            else:
                print("]")

#this is wrong, the function will be much simpler as the values do not depend on wavelength. 
def averageAllt1Counts():
    print("\taveraging t1 data values")
    global allt1, avet1, roundTo
    validData = True
    listSize = len(allt1[0])
    for i in range(1, len(allt1)):
        if len(allt1[i]) != listSize:
            validData = False
    if validData:
        for i in range(listSize):
            sum = 0
            for j in range(len(allt1)):
                sum += allt1[j][i]
            ave = sum / len(allt1)
            avet1.append(round(ave, roundTo))
        print("\t\tavet1 = " + str(avet1))
    else:
        print("ERROR: invalid data: list sizes in allt1 = [")
        for i in range(0, len(allt1)):
            print(str(len(allr1[i])))
            if i != len(allt1):
                print(", ")
            else:
                print("]")

#The above two functions were also done for t0 and t1. 
#Actually, I realize those two functions are incorrect for what I'm doing here. 
#The function will be much simpler as the values do not depend on wavelength.
#Once I fix that, those average values for r0, r1, t0, t1, will serve as the 
#input into my def MR and def MT equations, along with r and t (which are really the arrays MR and MT).
#*the arrays averageAllMRCounts and averageAllMTCounts
#Then, I need to ensure output of def MR and def MT is an array that is then written into the new data file                
        
def averageAllMRCounts():
    print("\taveraging R data values")
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
        print("\t\taveMR = " + str(aveMR))
    else:
        print("ERROR: invalid data: list sizes in allMR = [")
        for i in range(0, len(allMR)):
            print(str(len(allMR[i])))
            if i != len(allMR):
                print(", ")
            else:
                print("]")


def averageAllMTCounts():
    print("\taveraging T data values")
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
        print("\t\taveMT = " + str(aveMT))
    else:
        print("ERROR: invalid data: list sizes in allMT = [")
        for i in range(0, len(allMT)):
            print(str(len(allMT[i])))
            if i != len(allMT):
                print(", ")
            else:
                print("]")


def main():
    global directory
    directory = input("Enter Directory: ")
    print("Scanning directory " + directory)
    directoryScanner(directory)
    averageAllMRCounts()
    averageAllMTCounts()
    printDataToFile()

main()