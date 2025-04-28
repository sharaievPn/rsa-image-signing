from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys(private_name='private_key', public_name='public_key'):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    with open(f"keys/{private_name}.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f'private key generated: {private_name}.pem')

    public_key = private_key.public_key()

    with open(f"keys/{public_name}.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    print(f'public key generated: {public_name}.pem')
    return f'{private_name}.pem', f'{public_name}.pem'