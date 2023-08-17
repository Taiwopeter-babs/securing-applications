#!/usr/bin/env python3
"""
Public Key Infrastructure module
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography import x509
from cryptography.x509.oid import NameOID

from datetime import datetime, timedelta


def generate_private_key(filename: str, passphrase: str) -> str:
    """Generate private key for Certificate Authority"""
    # private key generation
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend
    )

    # set up encryption algorithm
    utf8_pass = passphrase.encode('utf-8')
    algorithm = serialization.BestAvailableEncryption(utf8_pass)

    # write private key to file protected with passphrase
    with open(filename, 'wb') as privatekey_file:
        privatekey_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=algorithm
            )
        )

    return private_key


def generate_public_key(private_key: RSAPrivateKey, filename: str, **kwargs) -> str:
    """Generate self-signed public key"""

    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME,
                               kwargs.get('country', 'NG')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,
                               kwargs.get('state', 'Lagos')),
            x509.NameAttribute(NameOID.LOCALITY_NAME,
                               kwargs.get('locality', 'Ipaja')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                               kwargs.get('org', ' My CA Company')),
            x509.NameAttribute(NameOID.COMMON_NAME,
                               kwargs.get('hostname', 'ynitaiwo.com')),
        ]
    )
    # issuer is always the subject as it is self-signed
    issuer = subject

    # validity
    valid_from = datetime.now()
    valid_to = valid_from + timedelta(days=30)

    # certificate build
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_to)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None),
                       critical=True)
    )

    # sign public key
    public_key = builder.sign(
        private_key, hashes.SHA256(), default_backend()
    )

    with open(filename, 'wb') as certfile:
        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))

    return public_key
