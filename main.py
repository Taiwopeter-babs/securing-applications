#!/usr/bin/env python3
"""
Main
"""
from dotenv import load_dotenv
from pki_helpers import generate_private_key, generate_public_key
import os

load_dotenv()

private_key = generate_private_key(
    'ca-private-key.pem', os.getenv('MY_PASSWORD'))
generate_public_key(
    private_key,
    filename='ca-public-key.pem',
    country='NG',
    state='Lagos',
    locality='Ipaja',
    org='My CA Company',
    hostname='ynitaiwo.com'
)
