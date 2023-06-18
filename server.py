


import socket
import pickle
import random
from card import Card

def create_socket(address, port):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a specific address and port
    server_address = (address, port)
    server_socket.bind(server_address)
    # Listen for incoming connections
    server_socket.listen(2)
    print('Waiting for connections...')
    return server_socket

def accept_connection(server_socket):
    # Accept player connections
    player_socket, player_address = server_socket.accept()
    print('Player connected:', player_address)
    return player_socket, player_address

def create_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def send_initial_hands(player_socket, player_hand):
    player_socket.sendall(pickle.dumps(player_hand))

def receive_card_choice(player_socket):
    card_choice = pickle.loads(player_socket.recv(1024))
    print('Player chose:', card_choice)
    return card_choice

def update_scores(player1_choice, player2_choice, player1_score, player2_score):
    if player1_choice == player2_choice:
        result = 'It\'s a tie!'
    elif player1_choice > player2_choice:
        result = 'Player 1 wins!'
        player1_score += 1
        print(result, "score:", player1_score)
    else:
        result = 'Player 2 wins!'
        player2_score += 1
        print(result, "score:", player2_score)
    return result, player1_score, player2_score

def send_result_and_scores(player1_socket, player2_socket, result, player1_score, player2_score):
    player1_socket.sendall(pickle.dumps((result, player1_score, player2_score)))
    player2_socket.sendall(pickle.dumps((result, player1_score, player2_score)))

def close_connections(player1_socket, player2_socket, server_socket):
    player1_socket.close()
    player2_socket.close()
    server_socket.close()

def main():
    # Create a server socket
    server_socket = create_socket('localhost', 5000)

    # Accept player connections
    player1_socket, player1_address = accept_connection(server_socket)
    player2_socket, player2_address = accept_connection(server_socket)

    # Create the deck
    deck = create_deck()

    # Initialize scores
    player1_score = 0
    player2_score = 0

    # Send the initial hands to the players
    player1_hand = deck[:26]
    player2_hand = deck[26:]
    send_initial_hands(player1_socket, player1_hand)
    send_initial_hands(player2_socket, player2_hand)

    # Send and receive data with the players
    while True:
        try:
            # Receive card choice from player 1
            player1_choice = receive_card_choice(player1_socket)

            # Receive card choice from player 2
            player2_choice = receive_card_choice(player2_socket)

            if player1_choice.rank == player2_choice.rank:
                result = 'It\'s a tie!'
                player1_score += 1
                player2_score += 1
                print(result, "Player 1 score:", player1_score, "Player 2 score:", player2_score)
            else:
                # Update scores based on card choices
                result, player1_score, player2_score = update_scores(player1_choice, player2_choice, player1_score, player2_score)
                
            # Send the result and scores to both players
            send_result_and_scores(player1_socket, player2_socket, result, player1_score, player2_score)

        except Exception as e:
            print('Error:', e)
            break

    # Close the connections
    close_connections(player1_socket, player2_socket, server_socket)

if __name__ == '__main__':
    main()
