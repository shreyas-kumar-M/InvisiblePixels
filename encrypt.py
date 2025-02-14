import cv2
import numpy as np

def encrypt():
    # Read the image
    try:
        img = cv2.imread("img.jpg")
        if img is None:
            raise Exception("Could not read image")
    except:
        print("Error: Make sure 'img.jpg' exists in the current directory")
        return

    # Get user input
    message = input("Enter secret message: ")
    password = input("Set a passcode for decryption: ")

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Prepare image
    img_copy = img.copy()
    max_bytes = (img.shape[0] * img.shape[1] * 3) // 8
    
    if len(message) > max_bytes:
        print("Error: Message too long for this image")
        return

    # Add length at the start
    length = format(len(message), '016b')
    binary_message = length + binary_message

    index = 0
    for i in range(len(binary_message)):
        # Get the pixel location
        row = index // (img.shape[1] * 3)
        col = (index % (img.shape[1] * 3)) // 3
        channel = index % 3
        
        # Get the current pixel value
        pixel = img_copy[row, col, channel]
        
        # Set the least significant bit
        if binary_message[i] == '1':
            pixel = pixel | 1  # Set LSB to 1
        else:
            pixel = pixel & 254  # Set LSB to 0
            
        # Store the modified pixel value
        img_copy[row, col, channel] = pixel
        index += 1

    # Save the image
    try:
        cv2.imwrite("encryptedImage.png", img_copy)  # Using PNG to avoid compression
        print("Message encrypted successfully!")
    except:
        print("Error saving the encrypted image")

if __name__ == "__main__":
    encrypt()
