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

def buildTxa(fields):
    segmentLength = 24
    fieldNames = {"Set ID":1
    , "Document Type":2
    , "Document Content Presentation":3
    , "Activity Date/Time":4
    , "Primary Activity Provider":5
    , "Origination Date/Time":6
    , "Transcription Date/Time":7
    , "Edit Date/Time":8
    , "Originator Code/Name":9
    , "Assigned Document Authenticator":10
    , "Transcriptionist":11
    , "Unique Document Number":12
    , "Parent Document Number":13
    , "Placer Order Number":14
    , "Filler Order Number":15
    , "Unique Document File Name":16
    , "Document Completion Status":17
    , "Document Confidentiality Status":18
    , "Document Availability Status":19
    , "Document Storage Status":20
    , "Document Change Reason":21
    , "Authentication Person, Time Stamp":22
    , "Distributed Copies":23
    }
    return buildSegment("TXA", fieldNames, fields, segmentLength)

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
    fieldNames = {"Set ID":1
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
    segmentLength = 44
    fieldNames = {"Set ID":1
    , "Placer Order Number":2
    , "Filler Order Number":3
    , "Universal Service ID":4
    , "Priority":5
    , "Requested Date/Time":6
    , "Observation Date/Time":7
    , "Observation End Date/Time":8
    , "Collection Volume":9
    , "Collector Identifier":10
    , "Specimen Action Code":11
    , "Danger Code":12
    , "Relevant Clinical info":13
    , "Specimen Received Date/Time":14
    , "Specimen Source":15
    , "Ordering Provider":16
    , "Order Callback Phone Number":17
    , "Placer field 1":18
    , "Placer field 2":19
    , "Filler Field 1":20
    , "Filler Field 2":21
    , "Request Change Date/Time":22
    , "Change to Practice":23
    , "Diagnostic Serv Sect ID":24
    , "Result Status":25
    , "Parent Result":26
    , "Quantity/Timing":27
    , "Result Copies To":28
    , "Parent":29
    , "Transportaion Mode":30
    , "Reason for Study":31
    , "Principal Result Interpreter":32
    , "Assistant Result Interpreter":33
    , "Technician":34
    , "Transcriptionist":35
    , "Scheduled Date/Time":36
    , "Number of Sample Containers":37
    , "Transport Logistics of Collected Sample":38
    , "Collector's Comment":39
    , "Transport Arrangement Responsibility":40
    , "Transport Arranged": 41
    , "Escort Required":42
    , "Planned Patient Transport Comment":43
    }
    return buildSegment("OBR", fieldNames, fields, segmentLength)

def buildObx(fields):
    segmentLength = 18
    fieldNames = {"Set ID":1
    , "Value Type":2
    , "Observation Identifier":3
    , "Observation Sub-Id":4
    , "Observation Value":5
    , "Units":6
    , "Reference Range":7
    , "Abnormal Flags":8
    , "Probability":9
    , "Nature of Abnormal Test":10
    , "Observation Result Status":11
    , "Data Last Observation Normal Values":12
    , "User Defined Access Checks":13
    , "Date/Time of the Observation":14
    , "Producer's Id":15
    , "Responsible Observer":16
    , "Observation Method":17
    }
    return buildSegment("OBX", fieldNames, fields, segmentLength)

def buildObxs(obxs):
    obxSet = []
    for obx in obxs:
        obxSet.append(buildObx(obx))
    return "".obxSet.join()

def buildPv1(fields):
    segmentLength = 53
    fieldNames = {"Set ID":1
    , "Patient Class":2
    , "Patient Location":3
    , "Admission Type":4
    , "Preadmit Number":5
    , "Prior Patient Location":6
    , "Attending Doctor":7
    , "Referring Doctor":8
    , "Consulting Doctor":9
    , "Hospital Service":10
    , "Temporary Location":11
    , "Preadmit Test Indicator":12
    , "Re-admission Indicator":13
    , "Admit Source":14
    , "Ambulance Status":15
    , "Vip Indicator":16
    , "Admitting Doctor":17
    , "Patient Type":18
    , "Visit Number":19
    , "Financial Class":20
    , "Charge Price Indicator":21
    , "Courtesy Code":22
    , "Credit Rating":23
    , "Contract Code":24
    , "Contract Effective Date":25
    , "Contract Amount":26
    , "Contract Period":27
    , "Interest Code":28
    , "Transfer to Bad Debt Code":29
    , "Transfer to Bad Debt Date":30
    }
    return buildSegment("PV1", fieldNames, fields, segmentLength)

def indexCompare(indexes, cols, indexValues):
    for i in indexes:
        if(cols[i] != indexValues[i]):
            return True
    return False

def messageFilter(message, filters):
    for filter in filters:
        message = filter(message)
        if(message == ""):
            break
    return message

def removeNulls(cols):
    for col in cols:
        if col.upper() == "NULL":
            col = ""
    return cols

def csvToHl7Main(inputFilename, outputFilename, hl7Generator, filters, expectedColCount, grouperIndexes):
    isFirstLine = True
    grouperIndexValues = []
    colSet = []
    message = ""
    messageCount = 0
    messages = []
    with open(inputFilename, "r", "utf-8-sig") as inputfile:
        for row in inputfile:
            row = row.split
            cols = row.split(colDelimiter)
            if(len(cols) < expectedColCount):
                continue
            cols = removeNulls(cols)
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

def parseMeditechName(name):
    nameArray = []
    tuple = name.split(",")
    lastName = tuple[0]
    if(len(tuple) < 2):
        return [lastName]
    firstMiddle = tuple[1]
    lastThree = firstMiddle[-3:]
    lastThree = lastThree.strip().upper()
    if(lastThree == "JR"
    or lastThree == "SR"
    or lastThree == "II"
    or lastThree == "IV"
    or lastThree == "VI"
    or lastThree == "III"):
        firstMiddle = firstMiddle[:-3]
    lastTwo = firstMiddle[-2:]

    if(lastTwo[:1] == " "):
        middle = lastTwo[-1:]
        firstMiddle = firstMiddle[:-2] 
        return lastName + "^" + firstMiddle + "^" + middle
    return lastName + "^" + firstMiddle
                               
# End HL7 processing code

# MT Transcription

def mtTranscription():
    inputFilename = "Transcription Results Extract Small Scale.txt"
    outputFilename = "FF Meditech Transcription HL7.txt"
    csvToHl7Main(inputFilename, outputFilename, mtTranscriptionGenerator, [], 19, [13])

def mtTranscriptionGenerator(rowSet):
    firstLine = True
    pidFields = {}
    pv1Fields = {}
    txaFields = {}
    obxs = []
    count = 0
    dictatingProvider = ""
    for row in rowSet:
        count += 1
        for col in row:
            if(firstLine == True):
                # PID
                pidFields["Set ID"] = "1"
                pidFields["Patient Name"] = parseMeditechName(row[1])
                pidFields["Sex"] = row[3]
                pidFields["Date/Time of Birth"] = 
                pidFields["Internal ID"] = 
                pidFields["Patient Account Number"] = row[6]
                # PV1
                pv1Fields["Set ID"] = 
                pv1Fields["Patient Location"] = row[5]
                pv1Fields["Visit Number"] = row[6]
                # TXA
                txaFields["Set ID"] = "1"
                txaFields["Document Type"] = row[7]
                txaFields["Primary Activity Provider"] =
                txaFields["Origination Date/Time"] =
                txaFields["Transcription Date/Time"] = 
                txaFields["Activity Date/Time"] = 
                txaFields["Originator Code/Name"] = 
                txaFields["Unique Document Number"] = "^^" + row[11]
                txaFields["Document Availability Status"] = "AV"
                txaFields["Document Completion Status"] = "AU"
                dictatingProvider = row[19]
            obxFields = {}
            obxFields["Set ID"] = str(count)
            obxFields["Value Type"] = "TX"
            obxFields["Observation Value"] = row[18]
            obxs.append(obxFields)
    count += 1
    obxFields = {}
    obxFields["Set ID"] = str(count)
    obxFields["Value Type"] = "TX"
    obxFields["Observation Value"] = "<Electronically signed by " + dictatingProvider + " >"
    obxs.append(obxFields)
    return

# End MT Transcription
 
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
    , "MT Transcription":mtTranscription
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