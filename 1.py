import socket
import pyautogui
import numpy as np
import cv2
import time
from PIL import ImageGrab

# Self-viewing configuration
HOST = '127.0.0.1'  # Always connect to itself (localhost)
PORT = 12345        # Port number (make sure it's not in use by other applications)

# Create a socket to communicate with itself
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server started on {HOST}:{PORT}...")

# Accept the connection (from itself)
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

def send_screen():
    """Capture the screen and send it continuously to the client (itself)"""
    while True:
        screen = np.array(ImageGrab.grab())  # Capture the screen
        _, encoded_img = cv2.imencode('.jpg', screen)  # Encode the image
        img_data = encoded_img.tobytes()  # Convert to bytes
        
        # Send the length of the image data first
        client_socket.sendall(len(img_data).to_bytes(4, byteorder='big'))
        client_socket.sendall(img_data)  # Send the image data
        time.sleep(0.1)  # Limit the capture rate for better performance

def display_screen():
    """Display the captured screen continuously"""
    while True:
        # First, receive the length of the image data
        img_len = int.from_bytes(client_socket.recv(4), byteorder='big')
        img_data = b""
        
        # Receive the image data
        while len(img_data) < img_len:
            img_data += client_socket.recv(4096)
        
        # Decode the image data
        img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        
        # Display the received screen
        cv2.imshow('Self-View Screen', img)
        
        # Exit the display window when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    client_socket.close()

# Start sending the screen to itself in one thread
send_screen()

# Start displaying the screen in another thread
display_screen()
