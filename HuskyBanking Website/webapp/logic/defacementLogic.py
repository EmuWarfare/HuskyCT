from flask import render_template, redirect, request, flash, make_response
from flask_wtf import Form
import json
from webapp.input import TransferInput, UserPageLogout
from webapp import cwd, sep, lab_4, transferLock
import hashlib


class Q4index():
    def __init__(self):
        self.transferInput = TransferInput()


        with open(f"{cwd}{sep}webapp{sep}JSONs{sep}magicNumber.json", "r") as jFile:
            self.magicNumber = json.load(jFile)


    
    def loadPage(self):
        return render_template(f"Q4.html", transferPg=self.transferInput, 
                               moneyAmount=None, transferHappened=False, badTransfer=False, maliciousTransfer=False, cookieValue=None)
    
    def transfer(self, ip, moneyAmount=None):
        if moneyAmount == None:
            moneyAmount = str(self.transferInput.moneyAmount.data)

        has_magic_number = moneyAmount.startswith(self.magicNumber[ip]["magicNumber"])
        cookie = self.magicNumber[ip]["cookie"]

        #has magic number in begining
        if (has_magic_number):
            return render_template("Q4.html", transferPg=self.transferInput, 
                               moneyAmount=moneyAmount, transferHappened=False, badTransfer=False, maliciousTransfer=True, cookieValue=cookie)
        
        #is a normal digit
        elif (moneyAmount.isdigit()):
            return render_template("Q4.html", transferPg=self.transferInput, 
                               moneyAmount=moneyAmount, transferHappened=True, badTransfer=False, maliciousTransfer=False, cookieValue=None)
        
        #some sort of bad transfer
        else:
            return render_template("Q4.html", transferPg=self.transferInput, 
                               moneyAmount=None, transferHappened=False, badTransfer=True, maliciousTransfer=False, cookieValue=None)
        
    


# class DefacementPage():
#     defacementPath = f"{cwd}/webapp/defacement.json"
#     defacement = open(defacementPath, "r")
#     defacement = json.load(defacement)
#     def getResponse(self, usr, suffix, ip):
#         defacementLock.acquire()
#         correct = str(self.defacement[ip]["suffix"]) == str(suffix)

#         if correct:
#             if self.defacement[ip]["access"] != "True":
#                 self.defacement[ip]["access"] = "True"
#                 with open(self.defacementPath, "w") as f:
#                     print("Writing True\n")
#                     json.dump(self.defacement, f, indent=4)
#             defacementLock.release()
#             return send_file(f"{cwd}\webapp\static\images\staticNames\defacement\cat.jpg")

        
#         defacementLock.release()
#         return send_file(f"{cwd}\webapp\static\images\staticNames\defacement\wrong_string.jpg")
    
#     def wrongPage(self):
#         return send_file(f"{cwd}\webapp\static\images\staticNames\defacement\wrong_route.jpg")