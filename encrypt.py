import cv2
import numpy as np
import hashlib

def encrypt():
    try:
        img = cv2.imread("img.jpg")
        if img is None:
            raise Exception("Could not read image")
    except:
        print("Error: Make sure 'img.jpg' exists in the current directory")
        return

    message = input("Enter secret message: ")
    password = input("Set a passcode for decryption: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()[:16]  # Store only first 16 characters
    message = password_hash + message  
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    img_copy = img.copy()
    max_bytes = (img.shape[0] * img.shape[1] * 3) // 8
    if len(message) > max_bytes:
        print("Error: Message too long for this image")
        return

    length = format(len(message), '016b')
    binary_message = length + binary_message
    index = 0
    for i in range(len(binary_message)):
        row = index // (img.shape[1] * 3)
        col = (index % (img.shape[1] * 3)) // 3
        channel = index % 3
        
        pixel = img_copy[row, col, channel]
        if binary_message[i] == '1':
            pixel = pixel | 1  # Set LSB to 1
        else:
            pixel = pixel & 254  # Set LSB to 0
            
        img_copy[row, col, channel] = pixel
        index += 1
    try:
        cv2.imwrite("encryptedImage.png", img_copy)  # Using PNG to avoid compression
        print("Message encrypted successfully!")
    except:
        print("Error saving the encrypted image")

if __name__ == "__main__":
    encrypt()
