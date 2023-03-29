import os

cwd = os.getcwd()

def printNoContentInFile(filename):
    print(f'''You've made the file {filename} but there seems to be no content within the file -_-. Make sure that this is not an incident.''')

def printFileHasContent(filename, content):
    j = f'''The file {filename} has content within it. The content in the file is as follows :  \n-------------------\n'''
    for k in content:
        j += f'''{k}'''
    print(j)

def printNoFile(filename):
    print(f'''You do not have the file {filename} within your directory :(. It can be either the name of the file is wrong or you still have not made the file yet.''')

def printHasFile(filename):
    print(f'''You have the file {filename} within your directory :D!''')

def printSeperator():
    print("#######################")

def checkFiles(fileName):
    printSeperator()
    isFile = os.path.isfile(f"{cwd}/{fileName}")
    if(isFile):
        printHasFile(fileName)
        checkContent(fileName)
        printSeperator()
        return
    
    printNoFile(fileName)
    printNoContentInFile(fileName)
    printSeperator()

def checkContent(fileName):
    f = open(f"{cwd}/{fileName}", "r")
    lis = f.readlines()
    if (len(lis) == 0):
        printNoContentInFile(fileName)
        return
    printFileHasContent(fileName, lis)

listOfFiles = ["Q1cookie", "Q2conf", "Q3.cookie", "Q4.cookie"]

for k in listOfFiles:
    checkFiles(k)