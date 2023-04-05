# L1Setup.py
from http import cookies
import json
import os
import random
import shutil
import socket
import hashlib
import pandas as pd
import string

cwd = os.getcwd()
sep = os.sep

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
        self.tokenDataFrame = pd.DataFrame(columns=["ip", "Q2", "Q3", "Q4", "Q5"], index=range(256))

        #===|[ Constant Open files ]|===#
        print("Beginning automated setup...\n")

        self.web_wd = cwd + f"{sep}HuskyBanking Website{sep}webapp"
        self.password_list = open(f"{cwd}{sep}Resources{sep}passwords.txt", "r", errors='ignore').read().split()
        self.username_list = open(f"{cwd}{sep}Resources{sep}names.txt", "r").read().split()

    
    #===|[ Generates a singular account with a random custom username. Also generates account metadata. ]|===#
    def randomAccount(self, victim, ipSuffix):
        balance = random.randint(100, 100000)
        username = random.choice(self.username_list) + str(ipSuffix) #username has subnet IP that way its unique for everyone
        password = random.choice(self.password_list)
        if victim:
            username = "B_" + username
            h = hashlib.sha256()
            h.update(password.encode())

            #-----[Benign users login cookie, Q1A answer]-----#
            self.solutionsDict.update(
                {
                    "Q1A": h.hexdigest()
                }
            )
        elif not victim:
            username = "A_" + username
        self.dictAccount.update({
            username:
            {
                "password" : password, 
                "balance" : balance,
                "ipAddress": (self.baseIP + str(ipSuffix))
            }
            })
        
        return username
    
    #===|[ Generates addresses for Q4, and the special cookie for Q3 ]|===#
    def cookiesJson(self, ipSuffix):



        #write in dictionary
        cook_q4 = random.randint(100, 100000)
        q3_cook = random.randint(100, 100000)
        magic_number = random.randint(0, 1000)

        ip = self.baseIP
        ip += ipSuffix
        
        self.cookiesDict.update({
            ip:
            {
                "magicNumber": magic_number,
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
        
    
    
    def tokenGen(self, ip, subdomain):
        gen = lambda : ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        genList = (ip, gen(), gen(), gen(), gen())
        self.tokenDataFrame.iloc[subdomain] = genList
        self.solutionsDict.update(
            {
                "Q2_token": genList[1],
                "Q3_token": genList[2],
                "Q4_token": genList[3],
                "Q5_token": genList[4]
            }
        )

    def lab6Gen(self):
        print("Begining Generation")
        for ipSubdomain in range(256):
            print(f"Generating for ip {ipSubdomain}")
            self.solutionsDict = {}

            groupWD = f"{cwd}{sep}Student Related Content{sep}LabGen{sep}Lab6{sep}{self.baseIP}{ipSubdomain}"

            #===|[ Directory creation ]|===#
            if (not os.path.exists(groupWD)): os.makedirs(groupWD)

            #===|[ Question 1 ]|===#
            # generate account names, passwords, balance, and cookies
            with open(f"{groupWD}{sep}Q1Login", "w") as q1:
                #Attacker
                username = self.randomAccount(False, ipSubdomain)
                q1.write(username + "," + self.dictAccount.get(username).get("password") + "\n")
                #Benign
                username = self.randomAccount(True, ipSubdomain)
                q1.write(username + "," + self.dictAccount.get(username).get("password") + "\n")

            #===|[ Question 3, 4 ]|===#
            # make the custom page for Q4
            self.cookiesJson(str(ipSubdomain))
            
            #===|[ Question 2,3,4,5 ]|===#
            # Generate the tokens for them

            self.tokenGen(self.baseIP + str(ipSubdomain), ipSubdomain)

            with open(f"{cwd}{sep}Student Related Content{sep}Solutions{sep}Lab6{sep}172.16.50.{ipSubdomain}_solutions.json", "w") as solutionJson:
                json.dump(self.solutionsDict, solutionJson, indent=4)
        

        #========[Write final JSONs]===========#
        with open(f"{self.web_wd}{sep}JSONs{sep}accountDB.json", "w") as dataBase:
            json.dump(self.dictAccount, dataBase, indent=4)

        with open(f"{self.web_wd}{sep}JSONs{sep}magicNumber.json", "w") as cookieDB:
            json.dump(self.cookiesDict, cookieDB, indent=4)
        
        tokenPath = f"{cwd}{sep}Student Related Content{sep}Tokens"
        self.tokenDataFrame.to_csv(f"{tokenPath}{sep}Lab_6.csv")
    

if __name__ == "__main__":
    lg = LocalGeneration()
    lg.lab6Gen()
    print("Completely finished generating lab.")