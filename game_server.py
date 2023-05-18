"""
A simple game server that allows two players to connect and play a game of guessing a 
number between a range of numbers. The first player to guess the number correctly wins the game. 
The server will send a welcome message to each player when they connect.

Steps: 
1. Create a socket object
2. Bind the socket to a host and port
3. Start listening for connections from clients
4. Accept connections from clients
5. Start a new thread for each player
6. Generate a random number between a range of numbers
7. Send a welcome message to each player
8. Send a message to each player to enter their guess
9. Receive the guess from the player
10. Check if the guess is correct
11. If the guess is correct, send a message to all players that the player has won
12. Close the connection

Steps to run the server:
1. Open a terminal window
2. Run the server: python3 game_server.py (it is important to run the server first)
3. Open another terminal window
4. Run the client: python3 game_client.py
5. Repeat step 3 and 4 to start another client (the server will wait for two clients to connect)

Author: Pokemon Trainer Red
"""

import socket
import random
from threading import Thread

game_finished = False
connections = []

# Function to generate a random number within a given range
def generate_number(start, end):
    return random.randint(start, end)

# Function to handle client connections and game logic
def handle_client(conn, player_num, number_to_guess):

    # Use the global variables game_finished and connections
    global game_finished
    global connections

    welcome_message = "Welcome, Player {}! Guess a number between 1 and 20.".format(player_num)
    conn.send(welcome_message.encode())

    # Add the connection to the list of connections if it is not already in the list
    if conn not in connections:
        connections.append(conn)

    while game_finished == False:
        guess = conn.recv(1024).decode()

        if guess.isdigit():
            guess = int(guess)
            if guess == number_to_guess:
                message = "Congratulations, Player {}! has guessed the correct number first.".format(player_num)
                game_finished = True
                congratulate_all_players(message)
                break
            elif guess < number_to_guess:
                message = "Your guess is too low. Try again."
                conn.send(message.encode())
            else:
                message = "Your guess is too high. Try again."
                conn.send(message.encode())
        else:
            message = "Invalid input. Please enter a number."
            conn.send(message.encode())

    # Close the connection
    conn.close()

def congratulate_all_players(message):
    global connections

    # Send congratulations message to all connected players
    for conn in connections:
        conn.send(message.encode())

    # Clear the list of connections
    connections = []

def start_server():
    host = 'localhost'
    port = 6969

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Start listening for connections from clients (max 2)
    server_socket.listen(2)

    print("Waiting for players to connect...")

    player_num = 1
    players = []

    # Accept connections from clients
    for player_num in range(1, 3):
        conn, addr = server_socket.accept()
        print("Player {} connected.".format(player_num))
        players.append((conn, player_num))

    # Start a new thread for each player
    threads = []

    for player_conn, player_num in players:
        thread = Thread(target=handle_client, args=(player_conn, player_num, number_to_guess))
        thread.start()
        threads.append(thread)

    # Wait for either player to win
    for thread in threads:
        thread.join()

    server_socket.close()

if __name__ == '__main__':
    number_to_guess = generate_number(1, 20)
    start_server()
