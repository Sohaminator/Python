import os
 
# Common
 
# Test if the given string is an integer
def isInteger(v):
    try:
        int(v)
        return True
    except Exception as e:
        return False
 
# Fetch the dictionary key at a given index. The index starts form 0
def getDictionaryKey(index, dictionaryObj):
    count = 0
    for d in dictionaryObj:
        if count == index:
            return d
        count += 1
    return None
               
# Build a dictionary out of a csv file
def buildDictionaryFromFile(filename, delimiter = ","):
    returnVal = {}
    with open(filename) as file:
        for line in file:
            tuple = line.strip().split(delimiter)
            returnVal[tuple[0].upper()] = tuple[1].upper()
    return returnVal

# Csv file containing MT patient Id types and their corresponding epic mnemonic
mtPatientIdTypeFile = "MeditechIdType.csv"
 
# Build a dictionary of MT Patient Id Types
def buildMeditechPatIdTypes():
    return buildDictionaryFromFile(mtPatientIdTypeFile)
 
# Build a table from a csv file. Assumes that the first row contains column headers.
# Returns a list of dictionary objects. Each row is represented by a dictionary object
# with the column headers as keys
def buildTableFromFile(filename, delimiter = ","):
    count = 1
    headers = []
    table = []
    colCount = 0
    with open(filename,"w") as inputFile:
        for line in inputFile:  
            if count == 1:
                headers = line.split(delimiter)
                count += 1
                colCount = len(headers)
            else:
                colValues = line.split(delimiter)
                column = {}
                for i in range(0, colCount):
                    column[headers[i]] = colValues[i]
                table.append(column)
    return table       
 
# Query a list of dictionary values. Returns the first matching dictionary value
# or None if no matching dictionary object is found
def queryTable(tableObj, **kwargs):
    if tableObj is not None\
    and kwargs is not None:
        for row in tableObj:
            kwargCount = len(kwargs.items())
            matchCount = 0
            for key, value in kwargs.items():
                if key in row and row[key] == value:
                    matchCount += 1
                    if(matchCount == kwargCount):
                        return row
    return None         
               
# Function to write to file
def fileWrite(inputList, filename, mode = "at", encoding = "utf8"):
    with open(filename, mode, encoding) as outfile:
        for l in inputlist:
            outfile.write(l)
               
# End Common
 
# HL7 processing code

# Number of messages to print per file write
messagePrintCount = 5000

# Csv file delimiter
colDelimiter = "\t"

def buildSegment(segName, fieldNames, fields, segmentLength):
    fieldDelimiter = "|"
    segmentDelimiter = "\r"
    segment = [""] * segmentLength
    segment[0] = segName
    for fieldName, index in fieldNames.items():
        if fieldName in fields:
            segment[index] = fields[fieldName]
    return fieldDelimiter.join(segment) + segmentDelimiter      

def buildMsh(fields):
    segmentLength = 13
    fieldNames = {"Encoding Characters":1
        , "Sending Application":2
        , "Sending Facility":3
        , "Receiving Application":4
        , "Receiving Facility":5
        , "Date/Time of Message":6
        , "Security":7
        , "Message Type":8
        , "Message Control Id":9
        , "Processing Id":10
        , "Version Id":11
        , "Sequence Number":12
        }
    return buildSegment("MSH", fieldNames, fields, segmentLength)

def buildPid(fields):
    segmentLength = 31
    fieldNames = {"Set ID – Patient ID":1
    , "External ID":2
    , "Internal ID":3
    , "Alternate ID":4
    , "Patient Name":5
    , "Mother's Maiden Name":6
    , "Date/Time of Birth":7
    , "Sex":8
    , "Patient Alias": 9
    , "Race":10
    , "Patient Address":11
    , "Country Code": 12
    , "Home Phone":13
    , "Business Phone":14
    , "Primary Language":15
    , "Marital Status":16
    , "Religion":17
    , "Patient Account Number":18
    , "SSN":19
    , "Patient Death Date and Time":29
    , "Patient Death Indicator":30
    }
    return buildSegment("PID", fieldNames, fields, segmentLength)

def buildObr(fields):
    return

def indexCompare(indexes, cols, indexValues):
    for i in indexes:
        if(cols[i] != indexValues[i])
            return True
    return False

def messageFilter(message, filters):
    for filter in filters:
        message = filter(message)
        if(message == ""):
            break
    return message

def csvToHl7Main(inputFilename, outputFilename, hl7Generator, filters, expectedColCount, *grouper):
    isFirstLine = True
    grouperIndexes = []
    grouperIndexValues = []
    colSet = []
    message = ""
    messageCount = 0
    messages = []
    for i in grouper:
        grouperIndexes.append(int(i))
    with open(inputFilename, "r", "utf-8-sig") as inputfile:
        for row in inputfile:
            cols = row.split(colDelimiter)
            if(len(cols) < expectedColCount):
                continue
            if(isFirstLine == False):
                if(indexCompare(grouperIndexes, cols, grouperIndexValues)):
                    message = hl7Generator(colSet)
                    message = messageFilter(message, filters)
                    if(message != ""):
                        messages.append(message)
                        messageCount += 1
                        if(messageCount >= messagePrintCount):
                            fileWrite(messages, outputFilename)
                            messages = []
                            messageCount = 0
                    colSet = []
            else:
                isFirstLine = False
            colSet.append(cols)
            grouperIndexValues = []
            for i in grouperIndexes:
                grouperIndexValues.append(cols[i])
    if(len(colSet) > 0):
        message = hl7Generator(colSet)
        message = messageFilter(message, filters)
        if(message != ""):
            messages.append(message)
        fileWrite(messages, outputFilename)
                               
# End HL7 processing code
 
# MT Allergies
 
def mtAllergyResult():
    return

def mtAllergyGenerator(rowSet):
    message = ""
    for row in rowSet:
        for col in row:
            continue
    return message
 
# End MT Allgeries
 
# MT General Lab Discrete
 
def mtGenLabDiscreteResult():
    print("mtGenLabDiscreteResult")
    return
 
# End MT General Lab Discrete
 
# MT General Lab Non-Discrete
 
def mtGenLabNonDiscreteResult():
    print("mtGenLabNonDiscreteResult")
    return
 
# End MT General Lab Non-Discrete
 
# Program starter code
 
def main():
    menu()
 
menuElements = {"MT General Lab (Discrete)":mtGenLabDiscreteResult
    , "MT General Lab (Non - Discrete)":mtGenLabNonDiscreteResult
    , "MT Allergy":mtAllergyResult
    }
 
def menu():
    while (True):
        count = 1
        os.system("cls")
        for m in menuElements:
            print(str(count) + " - " + m)
            count += 1
        print("0 - Exit")
        choice = input("? ")
        if isInteger(choice):
            i = int(choice)
            if i > 0 and i <= len(menuElements):
                key = getDictionaryKey(i-1, menuElements)
                if(key is not None):
                    menuAction(key)
                    continue
        break
    os.system("cls")
 
def menuAction(menuCommand):
    try:
        os.system("cls")
        menuElements[menuCommand]()
        input("Process complete, press any key to continue.")
    except Exception as e:
        print(e.toString())
        input("Press any key to continue.")
 
if __name__ == '__main__':
    main()
 
# End Program starter code