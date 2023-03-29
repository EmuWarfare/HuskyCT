# Husky Banking


Husky banking is a web application which is supposed to simulate a basic login screen for a banking website. This webiste does not actually connect to any form of banking, and is made simply for educational purposes.

## Local Setup

The following steps describe how to setup a python virtual enviroment, install required dependices, and get the website running. To properly follow these instructions open a terminal within the directory where the webapp folder is located, and execute all commands listed within this termianl.

1. 'python3 -m pip install virtualenv'
2. 'python3 -m venv bankVenv'
3. 'bankVenv/Scripts/activate'
4. 'pip install flask'
5. 'pip install python-dotenv'
6. 'pip install flask-wtf'
7. 'flask run'

Now the husky banking website should be running on local host port 5000. This can be accessed by inputing "http://127.0.0.1:5000" into your browser.

Further readings:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment
