# L1Setup.py
import json
import os
import random
import shutil
import socket
import string
import pandas as pd


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
        self.test = False
        self.dictAccount = {}
        self.imageDict = {}
        self.solutionsDict = {}
        self.tokenDataFrame = pd.DataFrame(columns=["ip", "Q3", "Q4", "Q5", "Q6"], index=range(256))

        #===|[ Constant Open files and directories ]|===#
        print("Beginning automated setup...\n")

        self.web_wd = cwd + f"{sep}HuskyBanking Website{sep}webapp"

        self.password_list = open(cwd + f"{sep}Resources{sep}passwords.txt", "r", errors='ignore').read().split()
        self.username_list = open(cwd + f"{sep}Resources{sep}names.txt", "r").read().split()
    
    #===|[ Generates a singular account with a random custom username. Also generates account metadata. ]|===#
    def randomAccount(self, victim, vm_IP:str):
        balance = random.randint(100, 100000)
        username = random.choice(self.username_list) + vm_IP.split(".")[-1]  #username has subnet IP that way its unique for everyone
        password = random.choice(self.password_list)

        if victim:
            username = "V_" + username
        self.dictAccount.update({
            username:
            {
                "password" : password, 
                "balance" : balance, 
                "ipAddress" : vm_IP
            }})
        
        if self.test: return username, vm_IP

        if not victim:
            self.solutionsDict.update(
                {
                    "Q1A": username,
                    "Q1B": balance
                }
            )
            self.imageDict[username] = {}
        
        if victim:
            self.solutionsDict.update(
                {
                    "Q2": password
                }
            )
        
        return username


    def rearange(self, imageType, imageBase):
        match imageType:
            case "Background":
                return imageBase[0] + imageBase[2] + imageBase[1] + imageBase[3]
            case "Blob":
                return imageBase[0] + imageBase[2] + imageBase[3] + imageBase[1]
            case "Icon":
                return imageBase[0] + imageBase[1] + imageBase[2] + imageBase[3]
    
    #===|[ Choose a random image to be used, create a custom label for the image using a mixed version of students IP, 
    # finally save that label as a mapping to the random image chosen ]|===#
    def customImages(self, imageType, imageBase, username, letter):
        images_list = os.listdir(self.web_wd + f"{sep}static{sep}images{sep}" + imageType)
        original_Image_Label = random.choice(images_list)

        rearanged_Image_Label = self.rearange(imageType, imageBase)

        newUrl = imageType + "/" + original_Image_Label

        if self.test: return newUrl

        self.imageDict[username].update({rearanged_Image_Label : newUrl})

        self.solutionsDict.update(
            {
                f"Q5{letter}": newUrl
            }
        )

    
    #===|[ Updates the constants used by functions such as IP, and custom image path ]|===#
    def IPSetup(self, i):
        vm_IP = self.baseIP + str(i)
        fuzzedIP = vm_IP.split(".")
        fuzzedIP = fuzzedIP[::-1]
        fuzzedIP[2] += "k"
        return vm_IP, fuzzedIP
    
    def tokenGeneration(self, ip):
        gen = lambda : ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        genList = (ip, gen(), gen(), gen(), gen())
        self.tokenDataFrame.iloc[ip] = genList
        self.solutionsDict.update(
            {
                "Q3": genList[1],
                "Q4": genList[2],
                "Q5A": genList[3],
                "Q6": genList[4]
            }
        )

    #===|[ Creates files and folders, allowing for the complete generation of the lab for a singular group ]|===#
    def labGen(self, ipSubdomain):
        vm_IP, fuzzedIP = self.IPSetup(ipSubdomain)


        groupWD = cwd + f"{sep}Student Related Content{sep}LabGen{sep}Lab4{sep}" + vm_IP
        solutionsWD = cwd + f"{sep}Student Related Content{sep}Solutions{sep}Lab4"
        #===|[ Directory creation ]|===#
        if (not os.path.exists(groupWD)): os.makedirs(groupWD)
        if (not os.path.exists(solutionsWD)): os.makedirs(solutionsWD)

        #===|[ Benign Users ]|===#
        #write usernames, passwords to solution and q1Login
        username = None
        with open(groupWD + f"{sep}Q1login", "w") as q1:
            username = self.randomAccount(False, vm_IP)
            q1.write(username + "," + self.dictAccount.get(username).get("password") + "\n")


        #===|[ Victim user ]|===#
        with open(groupWD + f"{sep}Q1", "w") as victim:
            v_username = self.randomAccount(True, vm_IP)
            victim.write(v_username + "\n")

        self.tokenGeneration(ipSubdomain)

        #===|[ Create copy of custom images based on IP ]|===#
        self.customImages("Background", fuzzedIP, username, "B")
        self.customImages("Blob",  fuzzedIP, username, "C")
        self.customImages("Icon",  fuzzedIP, username, "D")

        #===|[ Write solutions for IP from memory to disk ]|===#
        with open(solutionsWD + f"{sep}{vm_IP}_solutions.json", "w") as soltionsJson:
            json.dump(self.solutionsDict, soltionsJson, indent=4)

        print("Finished generating the lab for ip subdomain: " + str(ipSubdomain))



if __name__ == "__main__":
    lg = LocalGeneration()
    #generate the lab for all 256 IP's
    for i in range(256):
        lg.labGen(i)
    
    #===|[ Write global variables from memory to disk ]|===#
    with open(lg.web_wd + f"{sep}JSONs{sep}accountDB.json", "w") as dataBase:
        json.dump(lg.dictAccount, dataBase, indent=4)
    
    with open(lg.web_wd + f"{sep}JSONs{sep}images.json", "w") as imageDict:
        json.dump(lg.imageDict, imageDict, indent=4)

    tokenPath = f"{cwd}{sep}Student Related Content{sep}Tokens"
    
    if (not os.path.exists(tokenPath)): os.mkdir(tokenPath)
        
    lg.tokenDataFrame.to_csv(f"{tokenPath}{sep}Lab_4.csv")
    
    print("Completely finished generating lab.")
    print(cwd)