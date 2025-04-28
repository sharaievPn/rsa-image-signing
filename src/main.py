from key_generator import generate_keys
from signature import sign_image
from encryptor import embed_signature_lsb
from signature_checker import extract_signature_lsb
from signature_checker import verify_image_signature


def main(in_img, out_img):
    in_img = in_img
    out_img = out_img
    # generate private and public keys
    pv_key, pb_key = generate_keys()

    # create signature and save it
    signature = sign_image(in_img, pv_key)
    with open("data/signature.bin", "wb") as sig_file:
        sig_file.write(signature)
        sig_file.close()

    # embed signature
    embed_signature_lsb(in_img, signature, out_img)

    # check signature
    extracted_signature = extract_signature_lsb(out_img)
    valid_sign = verify_image_signature(in_img, pb_key, extracted_signature)
    if valid_sign:
        print("Sign is valid")
    else:
        print("Sign is invalid")


main('original_labrador.png', 'encrypted_labrador.png')
