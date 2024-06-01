from PIL import Image
import numpy as np

def embed_message(image_path, message, output_path):
    image = Image.open(image_path).convert('RGB')
    pixels = np.array(image, dtype=np.uint8)
    
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(message_bits)
    
    max_capacity = (pixels.shape[0] * pixels.shape[1] * 3) // 8  # Kapasitas dalam byte
    if message_length > max_capacity:
        raise ValueError("Message is too long to be embedded in the image.")
    
    message_index = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):  # Loop through each channel (R, G, B)
                if message_index < message_length:
                    p = int(pixels[i, j, k])
                    bit = int(message_bits[message_index])
                    message_index += 1
                    
                    if bit == 1:
                        p = p | 1  # Set LSB to 1
                    else:
                        p = p & ~1  # Set LSB to 0
                    
                    pixels[i, j, k] = np.clip(p, 0, 255)
    
    embedded_image = Image.fromarray(pixels)
    embedded_image.save(output_path)

def extract_message(image_path, message_length):
    image = Image.open(image_path).convert('RGB')
    pixels = np.array(image, dtype=np.uint8)
    
    message_bits = ""
    message_index = 0
    total_bits = message_length * 8
    
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):  # Loop through each channel (R, G, B)
                if message_index < total_bits:
                    p = int(pixels[i, j, k])
                    message_bits += str(p & 1)  # Get LSB
                    message_index += 1
    
    message = ''.join(chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8))
    return message

