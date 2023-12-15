#!/usr/bin/python

from flask import Flask

from app.config.init import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Makes the server accessible from the host machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#%%
# from config.init import *
