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
    db = c['omi']
    return db


