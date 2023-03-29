from ast import For
from cmath import log
import imp
import json
from flask import render_template, redirect, request, flash, make_response
from flask_wtf import Form
from webapp import app, cwd, sep
from webapp import input
from webapp.logic.userPageLogic import CoreUserFunctionality
import hashlib

class LoginPage(CoreUserFunctionality):
    def __init__(self):
        super().__init__()
        self.loginInput = input.LoginInput()
        self.username = None
        self.passw = None

        self.JAVA_LOGINPAGE = 1
        self.USERPAGE = 2

        self.imageDict = json.load(open(cwd + f"{sep}webapp{sep}JSONs{sep}images.json", "r"))
        self.dataBase = json.load(open(cwd + f"{sep}webapp{sep}JSONs{sep}accountDB.json", "r"))
    
    def hash(self, string:str):
        h = hashlib.sha256()
        h.update(string.encode())
        return h.hexdigest()
    
    def setRedirectCookies(self, page):
        resp = make_response(redirect(page))
        resp.set_cookie(self.userCookieName, self.username, httponly=False)
        resp.set_cookie(self.passCookieName, self.hash(self.passw), httponly=False)
        return resp


    def login_page(self, customLoginButton=False, alert=False):
        return render_template("loginPage.html", login=self.loginInput, alert=alert, basicLogin=customLoginButton)
    
    def custom_login_page(self, alert=False):
        self.username = self.loginInput.username.data
        return render_template("customLoginPage.html", login=self.loginInput, alert=alert, basicLogin=False, ipAddress=self.dataBase[self.username]["ipAddress"], imageDict=self.imageDict[self.username])
    
    def redirect_to_login_page(self):
        resp = make_response(redirect('/loggedIn'))
        return resp
    
    def get_students_IP(self):
        user = request.cookies.get(self.userCookieName)
        return self.dataBase[user]["ipAddress"]
    
    def login_redirection(self, page):
        if(page == self.JAVA_LOGINPAGE) : 
                return self.setRedirectCookies("/JS")
        elif(page == self.USERPAGE): 
                return self.setRedirectCookies("/loggedIn")
    
    def validateCookie(self, request):
        user = self.getCookie(request, self.userCookieName)
        hashed_passw = self.getCookie(request, self.passCookieName)

        if (user in self.dataBase and self.hash(self.dataBase[user]["password"]) == hashed_passw):
            return True
        return False
            

    def validateLogin(self):
        self.username = self.loginInput.username.data
        self.passw = self.loginInput.password.data

        #check username and password, and if in database then go to loginPage, otherwise stay in original page
        print(self.username)
        if (self.username in self.dataBase and str(self.dataBase[self.username]["password"]) == str(self.passw)):
            return True
        return False