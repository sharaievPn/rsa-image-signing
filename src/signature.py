from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


def sign_image(image_path: str, private_key_path: str) -> bytes:
    with open(f'keys/{private_key_path}', "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    with open(f'images/{image_path}', "rb") as image_file:
        image_data = image_file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(image_data)
    image_hash = digest.finalize()

    signature = private_key.sign(
        image_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature
