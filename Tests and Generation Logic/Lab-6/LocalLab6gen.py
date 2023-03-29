# L1Setup.py
from http import cookies
import json
from msilib.schema import Class
import os
import random
import shutil
import socket
import hashlib
import pandas as pd
import string

cwd = os.getcwd()
sep = os.sep()

# NOTE WARNING!!! DO NOT EXECUTE THIS FILE IN MAIN Lab4 DIRECTORY!!!
# For testing purposes, go to the "LabGen" folder

#[]====================[]
#||  SETUP AUTOMATION  ||
#[]====================[]

#===|[ Summary ]|===#
# This file should create three accounts for each VM, two being given to the students and a third is a victim account.
# All of these accounts are written into the main websites database, which will hold all this information, and into solutions.txt
# Create custom image paths for each VM as well, with its own directory and set of images within this directory.
# In total this file should generate 256 custom pages for this website, and 768 different accounts
class LocalGeneration():
    def __init__(self):

        #===|[ Constants ]|===#
        self.baseIP = "172.16.50."
        self.dictAccount = {}
        self.solutionsDict = None
        self.cookiesDict= dict()
        self.defacementDict = dict()
        self.tokenDataFrame = pd.DataFrame(columns=["ip", "Q2", "Q5"], index=range(256))

        #===|[ Constant Open files ]|===#
        print("Beginning automated setup...\n")

        self.web_wd = cwd + f"{sep}HuskyBanking Website{sep}webapp"
        self.password_list = open(f"{cwd}{sep}Resources{sep}passwords.txt", "r", errors='ignore').read().split()
        self.username_list = open(f"{cwd}{sep}Resources{sep}names.txt", "r").read().split()

    
    #===|[ Generates a singular account with a random custom username. Also generates account metadata. ]|===#
    def randomAccount(self, victim, i, ipSuffix):
        balance = random.randint(100, 100000)
        username = random.choice(self.username_list) + str(ipSuffix) #username has subnet IP that way its unique for everyone
        password = random.choice(self.password_list)
        if victim:
            username = "B"+ str(i) + username
            h = hashlib.sha256()
            h.update(password.encode())

            #-----[Benign users login cookie, Q1A answer]-----#
            self.solutionsDict.update(
                {
                    "Q1A": h.hexdigest()
                }
            )
        elif not victim:
            username = "A" + str(i) + username
        self.dictAccount.update({
            username:
            {
                "password" : password, 
                "balance" : balance
            }
            })
        
        return username

    def lenThreeSuffix(self):
        i = random.randrange(0, 1000)
        suffix = ""

        #make all strings equal to 3 chars length
        match len(str(i)):
            case 1:
                suffix = "00" + str(i)
            case 2:
                suffix = "0" + str(i)
            case 3:
                suffix = str(i)
        return suffix
    
    #===|[ Generates addresses for Q4, and the special cookie for Q3 ]|===#
    def cookiesJson(self, ipSuffix):
        
        suffix = self.lenThreeSuffix()

        #write in dictionary
        cook_q4 = random.randint(100, 100000)
        q3_cook = random.randint(100, 100000)

        ip = self.baseIP
        ip += ipSuffix
        
        self.cookiesDict.update({
            ip:
            {
                "Q4": suffix,
                "cookie": cook_q4,
                "Q3Cookie": q3_cook
            }
        })

        self.solutionsDict.update(
            {
                "Q3": q3_cook,
                "Q4": cook_q4
            }
        )
        
    
    
    def tokenGen(self, ip):
        gen = lambda : ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        genList = (ip, gen(), gen())
        self.tokenDataFrame.iloc[ip] = genList
        self.solutionsDict.update(
            {
                "Q2": genList[1],
                "Q5": genList[2]
            }
        )
    
    def generateCustomString(self, ipSuffix, groupWD):
        suffix = self.lenThreeSuffix()
        ip = self.baseIP + str(ipSuffix)
        self.defacementDict.update({
            ip: {
                "suffix": suffix,
                "access": "False"
            }
        })

    def lab6Gen(self):
        for ipSubdomain in range(256):
            self.solutionsDict = {}

            groupWD = f"{cwd}{sep}Student Related Content{sep}LabGen{sep}Lab6{sep}{self.baseIP}{ipSubdomain}"
            solutionsWD = self.cwd + "\\Solutions\\" + self.baseIP + str(ipSubdomain)

            #===|[ Directory creation ]|===#
            if (not os.path.exists(groupWD)): os.makedirs(groupWD)
            if (not os.path.exists(solutionsWD)): os.makedirs(solutionsWD)

            #===|[ Question 1 ]|===#
            # generate account names, passwords, balance, and cookies
            with open(f"{groupWD}{sep}Q1Login", "w") as q1:
                for i in range(1, 3):
                    username = self.randomAccount(False, i, ipSubdomain)
                    q1.write(username + "," + self.dictAccount.get(username).get("password") + "\n")
                for i in range(1, 3):
                    username = self.randomAccount(True, i, ipSubdomain)
                    q1.write(username + "," + self.dictAccount.get(username).get("password") + "\n")

            #===|[ Question 2 ]|===#
            # custom token for Q2
            self.tokenGen(ipSubdomain, self.baseIP + str(ipSubdomain))

            #===|[ Question 3, 4 ]|===#
            # make the custom page for Q4
            self.cookiesJson(str(ipSubdomain))

            #===|[ Question 5 ]|===#
            self.generateCustomString(ipSubdomain)
            
            #===|[ Question 5/6 ]|===#
            # Generate the tokens for them

            with open(f"{cwd}{sep}Student Related Content{sep}Solutions{sep}Lab6{sep}172.16.50.{ipSubdomain}_solutions.json") as solutionJson:
                json.dump(self.solutionsDict, solutionJson, indent=4)
        

        #========[Write final JSONs]===========#
        with open(f"{self.web_wd}{sep}JSONs{sep}database.json", "w") as dataBase:
            json.dump(self.dictAccount, dataBase, indent=4)

        with open(f"{self.web_wd}{sep}JSONs{sep}cookies.json", "w") as cookieDB:
            json.dump(self.cookiesDict, cookieDB, indent=4)
        
        with open(f"{self.web_wd}{sep}JSONs{sep}defacement.json", "w") as dataBase:
            json.dump(self.defacementDict, dataBase, indent=4)
    

if __name__ == "__main__":
    lg = LocalGeneration()
    lg.lab6Gen()
    print("Completely finished generating lab.")