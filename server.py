import socket
import pickle
import random
from card import Card

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 5000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(2)
print('Waiting for connections...')

# Accept player connections
player1_socket, player1_address = server_socket.accept()
print('Player 1 connected:', player1_address)

player2_socket, player2_address = server_socket.accept()
print('Player 2 connected:', player2_address)

# Create the deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [Card(suit, rank) for suit in suits for rank in ranks]
random.shuffle(deck)

# Send the initial hands to the players
player1_hand = deck[:26]
player2_hand = deck[26:]
player1_socket.sendall(pickle.dumps(player1_hand))
player2_socket.sendall(pickle.dumps(player2_hand))

# Send and receive data with the players
while True:
    try:
        # Receive card choice from player 1
        player1_choice = pickle.loads(player1_socket.recv(1024))
        print('Player 1 chose:', player1_choice)

        # # Remove chosen card from player 1's hand
        # player1_hand.remove(player1_choice)

        # Receive card choice from player 2
        player2_choice = pickle.loads(player2_socket.recv(1024))
        print('Player 2 chose:', player2_choice)

        # # Remove chosen card from player 1's hand
        # player1_hand.remove(player1_choice)

        # Compare the card choices and determine the winner
        if player1_choice == player2_choice:
            result = 'It\'s a tie!'
            print("tie")
        elif player1_choice > player2_choice:
            result = 'Player 1 wins!'
            print("player 1 wins")
        else:
            result = 'Player 2 wins!'
            print("player 2 wins")

        # Send the result to both players
        player1_socket.sendall(result.encode())
        player2_socket.sendall(result.encode())

    except Exception as e:
        print('Error:', e)
        break

# Close the connections
player1_socket.close()
player2_socket.close()
server_socket.close()
