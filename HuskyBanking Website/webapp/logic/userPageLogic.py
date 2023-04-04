from flask import render_template, redirect, request, flash, make_response
from flask_wtf import Form
import json
from webapp.input import TransferInput, UserPageLogout
from webapp import cwd, sep, lab_4, transferLock
import hashlib




class CoreUserFunctionality():
    def __init__(self) -> None:
        self.userCookieName = 'USER'
        self.passCookieName = "LOGIN_INFO"
        self.userPageLogout = UserPageLogout()
        self.accountsPath = f"{cwd}{sep}webapp{sep}JSONs{sep}accountDB.json"
        self.magicNumbersPath = f"{cwd}{sep}webapp{sep}JSONs{sep}magicNumber.json"

    def logOut(self):
        resp = make_response(redirect('/'))
        resp.delete_cookie(self.userCookieName)
        resp.delete_cookie(self.passCookieName)
        print("Logout")
        return resp
    
    def notLoggedIn(self):
        return '''
        <html>
        <body>
            <h1>Login before accessing website.<h1>
        <body>
        <html>'''
    
    def getCookie(self, request, cookieName):
        cookie = None if cookieName not in request.cookies else request.cookies.get(cookieName)
        return cookie




####################
## Used for Lab 4 ##
####################
class PlainUserPage(CoreUserFunctionality):
    def __init__(self, request) -> None:
        super().__init__()
        self.accountDB = json.load(open(self.accountsPath, "r"))
        self.user = self.getCookie(request, self.userCookieName)
    


    def loadPage(self, username, alert=False):
        return make_response(render_template('userPage.html', balance=self.accountDB[username]['balance'], user=self.user, lg=self.userPageLogout, alert=alert))








####################
## Used for Lab 6 ##
####################
class TransferPage(CoreUserFunctionality):
    def __init__(self):
        super().__init__()
        self.transferInput = TransferInput()
        self.dataBase = json.load(open(self.accountsPath, "r"))
        self.magicNumbers = json.load(open(self.magicNumbersPath, "r"))
    

    def loadPage(self, username, script="", transfer=False, moneyAmount=None, invalidTransfer=None, alert=False):
        return make_response(render_template('transferPage.html', balance=self.dataBase[username]['balance'], 
        transferPg=self.transferInput, lg=self.userPageLogout, alert=alert, script=script,transferHappened=transfer, moneyAmount=moneyAmount, user=username, invalidTransfer=invalidTransfer))
    
    def transferMoney(self, user, recipient=None, money=None, ip=None):
        recipient = recipient if recipient != None else self.transferInput.username.data
        moneyAmount = money if money != None else self.transferInput.moneyAmount.data
        try:
            if recipient in self.dataBase:
                #put lock
                moneyAmount = int(moneyAmount)
                transferLock.acquire()


                with open(self.accountsPath, "r") as f:
                    self.dataBase = json.load(f)

                with open(self.accountsPath, "w") as f:
                    self.dataBase[user]['balance'] -= moneyAmount
                    self.dataBase[recipient]['balance'] += moneyAmount
                    f.write(json.dumps(self.dataBase, indent=4))
                #end lock

                transferLock.release()

                return self.loadPage(user, transfer=True, moneyAmount=moneyAmount)
            else:
                #make this the only vulnerble input box, specifically does not escape characters, https://flask.palletsprojects.com/en/2.2.x/templating/
                self.alert = False
                cookieValue = str(self.magicNumbers[ip]["Q3Cookie"])
                resp = make_response(self.loadPage(user, script=recipient, transfer=True, moneyAmount=moneyAmount))
                resp.set_cookie("Q3Cookie", cookieValue)
                return resp
        except:
            return self.loadPage(user, transfer=False, moneyAmount=moneyAmount)
    
    def validate_cookie(self):
        return True