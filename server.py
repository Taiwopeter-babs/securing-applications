#!/usr/bin/env python3
"""
App Server Module
"""
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask
import os

load_dotenv()

# data to be encrypted must be in bytes
SECRET_MESSAGE = os.getenv('SECRET_MESSAGE').encode('utf-8')
SECRET_KEY = os.environb[b'SECRET_KEY']
app = Flask(__name__)
app.url_map.strict_slashes = False

# initialize the encryption engine
my_cipher = Fernet(SECRET_KEY)


@app.route('/')
def get_secret_message() -> str:
    """
    returns the SECRET_MESSAGE
    """
    return my_cipher.encrypt(SECRET_MESSAGE)
