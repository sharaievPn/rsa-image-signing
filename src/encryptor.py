from PIL import Image


def embed_signature_lsb(image_path: str, signature: bytes, output_path: str):
    image_path = f'images/{image_path}'
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = image.load()

    signature_bits = ''.join(f'{byte:08b}' for byte in signature)

    width, height = image.size
    total_pixels = width * height

    if len(signature_bits) > total_pixels:
        raise ValueError("Signature bits exceeds")

    bit_idx = 0
    for y in range(height):
        for x in range(width):
            if bit_idx >= len(signature_bits):
                break

            r, g, b = pixels[x, y]
            # least significant bit for red channel
            r = (r & ~1) | int(signature_bits[bit_idx])
            bit_idx += 1
            pixels[x, y] = (r, g, b)

        if bit_idx >= len(signature_bits):
            break

    image.save(f'images/{output_path}')
    print(f"Signature incorporated and saved as '{output_path}'.")
