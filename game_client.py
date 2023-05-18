"""
Game client for the number guessing game. The client connects to the server and sends a guess to the server. 
Every time the client sends a guess, the server responds with a message indicating whether the guess is too high, 
too low, or correct. The client keeps guessing until it guesses the correct number. When the client guesses the correct 
number, the server sends a congratulatory message to the client and closes the connection.

Author: Pokemon Trainer Red
"""

import socket

def start_client():
    host = 'localhost'
    port = 6969

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    while True:
        guess = input("Enter your guess: ")
        client_socket.send(guess.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if "Congratulations" in response:
            break

    client_socket.close()

if __name__ == '__main__':
    start_client()
