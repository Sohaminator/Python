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
            kwargCount = len(kwargs.iteritems())
            matchCount = 0
            for key, value in kwargs.iteritems():
                if key in row and row[key] == value:
                    matchCount += 1
                    if(matchCount == kwargCount):
                        return row
    return None
 
# Number of messages to print per file write
messagePrintCount = 5000         
               
# Function to write to file
def fileWrite(inputList, filename, mode = "at", encoding = "utf8"):
    with open(filename, mode, encoding) as outfile:
        for l in inputlist:
            outfile.write(l)
               
# End Common
 
# HL7 processing code
 
class segment:
    fields = {}
    fieldDelim = "|"
    segment = ""
    def toString():
        segmentText = segment + fieldDelim
        for k in fields:
            segmentText = fields[k] + fieldDelim
        return segmentText
                               
# End HL7 processing code
 
# MT Allergies
 
def mtAllergyResult():
    return
 
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
 
menuElements = {"MT General Lab (Discrete)":mtGenLabDiscreteResult\
, "MT General Lab (Non - Discrete)":mtGenLabNonDiscreteResult\
, "MT Allergy":mtAllergyResult\
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