from ast import arg
from cmath import log
from distutils.log import Log
import json
from webapp.input import LoginInput
from webapp.logic.loginLogic import LoginPage
from webapp.logic.userPageLogic import TransferPage, PlainUserPage
from webapp.logic.defacementLogic import Q4index, DefacementPage
from flask import render_template, redirect, request, flash, make_response
from flask_wtf import Form
from flask_wtf.csrf import CSRFError
from flask_cors import cross_origin
from webapp import app, csrf, lab_4
import os


###############################################################
## Custom Javascript login page. Image changes based on user ##
###############################################################

@app.route("/JS", methods=['GET', 'POST'])
def obfuscatedImages():

    #if its not lab 4, don't make this page accessable, boot them back to the initial page
    if not lab_4:
        return redirect("/")
    loginClass = LoginPage()
    if request.method == 'POST' and "submit" in request.form: #if a POST method is given then test determine if it is a proper login
        if (loginClass.validateLogin()):
            return loginClass.redirect_to_login_page()
        return loginClass.custom_login_page(alert=True)
    return loginClass.custom_login_page()


#############################################
## Completed User Page With Money Transfer ##
#############################################
@csrf.exempt
@app.route('/loggedIn', methods=['GET', 'POST'])
@cross_origin()
def loggedIn():
    pageLogic = None
    if lab_4:
        pageLogic = PlainUserPage(request)
    if not lab_4:
        pageLogic = TransferPage()

    user = pageLogic.getCookie(request, pageLogic.userCookieName)
    if user == None:
        return pageLogic.notLoggedIn()
        
    #only allow transfer capabilites if it is not lab 4
    elif (not lab_4) and (pageLogic.transferInput.validate_on_submit()) and ("transfer" in request.form.keys()):
        return pageLogic.transferMoney(user)
    
    elif request.method == 'POST' and "logOut" in request.form:
        return pageLogic.logOut()

    
    elif (not lab_4) and request.method == "GET" and ("username" in request.args.keys()):
        response = pageLogic.transferMoney(user, request.args["username"], request.args["money"])
        print(response)
        return response

    else:
        return pageLogic.loadPage(user)


@app.errorhandler(CSRFError)
def checkIfCRSF(e):
    print(e)
    user = request.cookies.get('Username')
    args = request.args
    print(args)


#####################################
## Custom Q4 Directories For Lab 6 ##
#####################################
@csrf.exempt
@app.route('/Q4', methods=['GET', 'POST'])
@cross_origin(supports_credentials=False, origins="*")
def cookieIndex():
    if lab_4:
        return redirect("/")
    q4 = Q4index()
    ip = request.remote_addr

    #Post request for transfer
    if (request.method == "POST"):
        return q4.transfer(ip, request.form["money"])
    
    #Get request for transfer
    elif(request.method == "GET" and len(request.args) != 0):
        try:
            return q4.transfer(ip, request.args["money"])
        except:
            return q4.loadPage()
    
    #Just load the page
    return q4.loadPage()


# ######################
# ## Custom Q5 Routes ##
# ######################
@app.route('/Q5', methods=['GET', 'POST'])
def wrongPage():
    if lab_4:
        return redirect("/")
    

    q5 = DefacementPage()

    if request.method == 'GET' and len(request.args) != 0:
        try:
            return q5.transfer(request.args["money"])
        except:
            return q5.load_page()  

    elif request.method == 'POST':
        return q5.transfer()
    
    else:
        return q5.load_page()

# @app.route('/Q5xss', methods=['GET'])
# def Q5xss():
#     cookies=request.cookies
#     if "referrer" in cookies:
#         with open(cwd + "/webapp/Q5log", "a") as f:
#                 f.write("\n referrer:"+request.referrer+", reflecting webpage:"+cookies["referrer"])
#         return "referrer:"+request.referrer+", reflecting webpage:"+cookies["referrer"]
#     return "Not reflecting??"

# @app.route('/Q5<suffix>', methods=['GET'])
# def defacement(suffix):
#     q5 = DefacementPage()
#     user = None if "Username" not in request.cookies else request.cookies.get('Username').split(",")[0]
#     ip = request.remote_addr
#     response = q5.getResponse(user, suffix, ip)
#     return response



#######################################
## Completed Login Page With Cookies ##
#######################################
#If there is a the custom button, then
@csrf.exempt
@app.route('/', methods=['GET', 'POST'])
def doneLoginPage():
    loginPage = LoginPage()

    if loginPage.validateCookie(request): return loginPage.redirect_to_login_page()

    print(request.form)

    if request.method == 'POST':
        if "submit" in request.form:
            if (loginPage.validateLogin()):
                return loginPage.setRedirectCookies("/loggedIn")
            return loginPage.login_page(customLoginButton=lab_4, alert=True)
        
        #Only accessiable if this is lab 4 which custom page is required
        elif "customPage" in request.form and lab_4:
            if (loginPage.validateLogin()):
                return loginPage.custom_login_page()
            return loginPage.custom_login_page(alert=True)

    
    return loginPage.login_page(customLoginButton=lab_4)




@app.errorhandler(500)
def server_error(e):
    return "An internal error occurred", 500

#https://flask-wtf.readthedocs.io/en/1.0.x/csrf/#csrf-protection
#https://webomnizz.com/secure-form-with-csrf-token-in-flask/