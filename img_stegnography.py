from PIL import Image
import numpy as np

def hide_image_gray(cover_image_path, secret_image_path, output_image_path):

    cover_image = Image.open(cover_image_path).convert('L')
    secret_image = Image.open(secret_image_path).convert('L')

    if cover_image.size < secret_image.size:
        raise ValueError("Cover image dimensions are smaller than secret image dimensions.")

    secret_image = secret_image.resize(cover_image.size)

    cover_data = np.array(cover_image)
    secret_data = np.array(secret_image)

    for i in range(cover_data.shape[0]):
        for j in range(cover_data.shape[1]):
            cover_data[i, j] = (cover_data[i, j] & 0xFE) | (secret_data[i, j] >> 7)

    modified_image = Image.fromarray(cover_data)
    modified_image.save(output_image_path)

def extract_image_gray(stego_image_path, output_image_path):

    stego_image = Image.open(stego_image_path).convert('L')
    stego_data = np.array(stego_image)
    extracted_data = np.zeros_like(stego_data)

    for i in range(stego_data.shape[0]):
        for j in range(stego_data.shape[1]):
            extracted_data[i, j] = (stego_data[i, j] & 0x01) << 7
    
    extracted_image = Image.fromarray(extracted_data)
    extracted_image.save(output_image_path)


cover_image='cover_img.png'
secret_image='secret_img.png'
stego_image='stego_image.png'
# Hide a secret image (converted to grayscale) under a cover image (converted to grayscale)
hide_image_gray(cover_image, secret_image, stego_image)
img1=Image.open('stego_image.png')
display(img1)

extracted_secret_image='extracted_secret_image.png'
# Extract the hidden secret image from the stego image
extract_image_gray(stego_image, extracted_secret_image)
img2=Image.open('extracted_secret_image.png')
display(img2)

