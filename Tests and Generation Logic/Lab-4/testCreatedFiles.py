import json
import LocalLab4gen
import os
import unittest

cwd = os.getcwd()
sep = os.sep

class TestDatabase(unittest.TestCase):
    def __init__(self):
        self.llg = LocalLab4gen.LocalGeneration()
        self.llg.test = True
        self.cwd = os.getcwd()
        self.database = json.load(open(self.cwd + f"{sep}HuskyBanking Website{sep}webapp{sep}JSONs{sep}accountDB.json", "r"))
        self.images = json.load(open(self.cwd + f"{sep}HuskyBanking Website{sep}webapp{sep}JSONs{sep}images.json", "r"))
    
    def printStart(self, message):
        print("=====================================")
        print(f"Testing {message}.")
    
    def printEnd(self, message):
        print(f"Finished testing {message}")
        print("=====================================\n")

    def checkSolutions(self):
        self.printStart("Solutions")
        for i in range(256):
            full_ip, fuzzedIP = self.llg.IPSetup(i)
            with open(f"{self.cwd}{sep}Student Related Content{sep}Solutions{sep}Lab4{sep}{full_ip}_solutions.json", "r") as solutions:
                solutions = json.load(solutions)

                #checks accounts for every group that they are within the database,
                assert(solutions["Q1A"] in self.database)
                assert(solutions["Q1B"] == self.database[solutions["Q1A"]]["balance"])
                
                username = solutions["Q1A"]

                #checks images for every group
                for letters in ["B", "C", "D"]:
                    imageType, imageName = solutions[f"Q5{letters}"].split("/")
                    obfuscatedImageName = self.llg.rearange(imageType, fuzzedIP)
                    assert(self.images[username][obfuscatedImageName] == f"{imageType}/{imageName}")

        self.printEnd("Solutions")


    def checkQ1login(self):
        self.printStart("Q1Login")
        for i in range(256):
            full_ip, _ = self.llg.IPSetup(i)
            with open(f"{self.cwd}{sep}Student Related Content{sep}LabGen{sep}Lab4{sep}{full_ip}{sep}Q1login", "r") as q1:
                usr, passw = q1.readline().strip().split(",")
                assert(self.database[usr]["password"] == passw)
        self.printEnd("Q1 Login")


if __name__ == "__main__":
    td = TestDatabase()
    td.checkSolutions()
    td.checkQ1login()