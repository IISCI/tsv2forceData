# env! Python 3

import os
from zipfile import ZipFile

# Let's add key:value to a dictionary, the functional way

# Create your dictionary class


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, dataPairList):
        self[dataPairList[0]] = dataPairList[1]


tsvFiles = []

for file in os.listdir():
    if file.endswith(".tsv"):
        tsvFiles.append(os.path.join('', file))


# pass non-forces files
for tsvFile in tsvFiles:
    if '_f_' not in tsvFile:
        # print (tsvFile) # debug
        tsvFiles.remove(tsvFile)

print(tsvFiles)

lineData = []  # list separeted by \t of one line data from .tsv
forceData = []  # list of all frames data
frameData = {}  # one frame data {SAMPLE#:[TIME,Force_Z]}

# create a ZipFile object
zipObj = ZipFile('Z.zip', 'w')

# Scan all files in current directory and write each file to fileDict
for file in tsvFiles:
    
    print ('Parsing ', file)

    f = open(file, 'r')
    fileData = f.readlines()
    f.close()
    fileDict = my_dictionary()
    for index, line in enumerate(fileData):
        lineData = line.split('\t')
        if lineData[0] == 'FREQUENCY':
            lineData[1] = lineData[1][:-1]
            fileDict.add(lineData)
            continue
        if lineData[0] == 'TIME_STAMP':
            fileDict.add(lineData)
            continue
        if lineData[0] == 'FORCE_PLATE_NAME':  # todo write LEFT or RIGHT instead of FP number
            lineData[1] = lineData[1][:-1]
            fileDict.add(lineData)
            continue
        if lineData[0] == 'SAMPLE':  # header ends
            # collect all frames in one list forceData of dicts frameData{time:Force_Z} under 'SAMPLE' key
            for i in range(index+1, len(fileData)):
                tmpFrameData = fileData[i].split('\t')
                frameData[tmpFrameData[0]] = [tmpFrameData[1],
                                              tmpFrameData[4]]  # {SAMPLE#:[TIME,Force_Z]} dict
                forceData.append(frameData)
            fileDict.add(['SAMPLE', forceData])
            break
            # now fileDict contains all neccessary data to export to .txt file

    # debug first frame data: list(time, Force_Z)
    # print(file, fileDict['SAMPLE'][-1]['1'], '\n')

    # construct fileName
    fileName = file.split(' ')[0]+' '+str(
        fileDict['TIME_STAMP'].split(',')[0])+' ' + str(
        fileDict['FREQUENCY'])+'Hz '+str(
        fileDict['FORCE_PLATE_NAME'])+'.csv'

    f = open(fileName, 'w')
    dataFrames = fileDict['SAMPLE'][0]
    for key in dataFrames:
        f.write(key+','+dataFrames[key][0]+','+dataFrames[key][1]+'\n')
        print ('.', end='')
    f.close()
    zipObj.write(fileName)
    print ('Done!\n\n')

zipObj.close()
print ('Finished!')
