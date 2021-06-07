from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import logging
import logging.handlers
import requests
#from pushover import Client
import sys, os

def db():
    c = MongoClient(connect=False)
    db = c[os.getenv('db')]
    return db


if __name__ == '__main__':
    print(os.getenv('db'))
