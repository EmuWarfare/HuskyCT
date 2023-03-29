from flask import render_template, redirect, request, flash, make_response
from flask_wtf import Form
import json
from webapp.input import TransferInput, UserPageLogout
from webapp import cwd, sep, lab_4, transferLock
import hashlib


class Q4index():
    def __init__(self):
        with open(f"{cwd}{sep}webapp{sep}JSONs{sep}cookies.json", "r") as jFile:
            self.cookies = json.load(jFile)
    def loadPage(self, ip, suffix):
        if self.cookies[ip]["Q4"] == suffix:
            return render_template(f"index.html", cookie=self.cookies[ip]["cookie"])
        return render_template(f"index.html", cookie="Try again, not the correct site")


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