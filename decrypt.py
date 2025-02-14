import cv2
import numpy as np

def decrypt():
    # Read the encrypted image
    try:
        img = cv2.imread("encryptedImage.png")  # Read PNG file
        if img is None:
            raise Exception("Could not read image")
    except:
        print("Error: Make sure 'encryptedImage.png' exists in the current directory")
        return

    # Get password
    password = input("Enter passcode for decryption: ")
    verify_password = input("Re-enter passcode used during encryption: ")

    if password != verify_password:
        print("YOU ARE NOT AUTHORIZED!")
        return

    # Extract the binary message
    binary_data = ''
    index = 0
    
    # First get the length (16 bits)
    for i in range(16):
        row = index // (img.shape[1] * 3)
        col = (index % (img.shape[1] * 3)) // 3
        channel = index % 3
        
        binary_data += str(img[row, col, channel] & 1)
        index += 1
    
    # Convert first 16 bits to integer (message length)
    message_length = int(binary_data, 2)
    binary_data = ''
    
    # Extract the actual message
    for i in range(message_length * 8):
        row = (i + 16) // (img.shape[1] * 3)
        col = ((i + 16) % (img.shape[1] * 3)) // 3
        channel = (i + 16) % 3
        
        binary_data += str(img[row, col, channel] & 1)

    # Convert binary to text
    message = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        message += chr(int(byte, 2))
    
    print("Decrypted message:", message)

if __name__ == "__main__":
    decrypt()
