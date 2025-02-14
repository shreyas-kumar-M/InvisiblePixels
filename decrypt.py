import cv2
import numpy as np
import hashlib

def decrypt():
    try:
        img = cv2.imread("encryptedImage.png")  # Read PNG file
        if img is None:
            raise Exception("Could not read image")
    except:
        print("Error: Make sure 'encryptedImage.png' exists in the current directory")
        return
    password = input("Enter passcode for decryption: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()[:16]
    binary_data = ''
    index = 0
    
    for i in range(16):
        row = index // (img.shape[1] * 3)
        col = (index % (img.shape[1] * 3)) // 3
        channel = index % 3
        
        binary_data += str(img[row, col, channel] & 1)
        index += 1
    
    message_length = int(binary_data, 2)
    binary_data = ''
    
    for i in range(message_length * 8):
        row = (i + 16) // (img.shape[1] * 3)
        col = ((i + 16) % (img.shape[1] * 3)) // 3
        channel = (i + 16) % 3
        
        binary_data += str(img[row, col, channel] & 1)

    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message += chr(int(byte, 2))

    extracted_hash = message[:16]
    original_message = message[16:]
    if extracted_hash != password_hash:
        print("YOU ARE NOT AUTHORIZED!")
        return
    print("Decrypted message:", original_message)

if __name__ == "__main__":
    decrypt()
