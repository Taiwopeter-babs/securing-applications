#!/usr/bin/env python3
"""
client module
"""
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import requests
from server import my_cipher

load_dotenv()


def get_secret_messsage() -> None:
    """
    queries an endpoint and prints result
    """
    resp = requests.get('http://127.0.0.1:5000')

    decrypted_msg = my_cipher.decrypt(resp.content)

    print("The decrypted secret message is: {}".format(decrypted_msg))


if __name__ == '__main__':
    get_secret_messsage()
