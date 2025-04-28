from PIL import Image
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def extract_signature_lsb(image_path: str, signature_length=512) -> bytes:
    image_path = f'images/{image_path}'
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = image.load()

    width, height = image.size
    total_pixels = width * height

    if signature_length * 8 > total_pixels:
        raise ValueError("Signature length is out of range")

    bits = []
    bit_idx = 0

    for y in range(height):
        for x in range(width):
            if bit_idx >= signature_length * 8:
                break

            r, g, b = pixels[x, y]
            bits.append(str(r & 1))
            bit_idx += 1

        if bit_idx >= signature_length * 8:
            break

    signature_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte = int(''.join(bits[i:i + 8]), 2)
        signature_bytes.append(byte)

    return bytes(signature_bytes)


def verify_image_signature(image_path: str, public_key_path: str, signature: bytes) -> bool:
    with open(f'keys/{public_key_path}', "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    with open(f'images/{image_path}', "rb") as image_file:
        image_data = image_file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(image_data)
    image_hash = digest.finalize()

    try:
        public_key.verify(
            signature,
            image_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False
