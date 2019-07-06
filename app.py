from flask import Flask
import requests
import urllib.request
import time
import json
from pprint import pprint
from bs4 import BeautifulSoup
from random import choice, sample
import random
import scrython

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
