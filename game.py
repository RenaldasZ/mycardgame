import pygame
import socket
import pickle
from card import Card

# Initialize pygame
pygame.init()

# Define the screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Card Game')

# Define the card dimensions
card_width, card_height = 100, 140

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 5000)
client_socket.connect(server_address)
print('Connected to:', server_address)

# Receive the initial hand from the server
player_hand = pickle.loads(client_socket.recv(1024))

is_player_turn = True

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the left mouse button was clicked
            if event.button == 1:
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if it's the player's turn
                if is_player_turn:
                    # Check if the mouse click was on a card
                    for i, card in enumerate(player_hand):
                        x = 100 + i * (card_width + 10)
                        y = screen_height - card_height - 100

                        # Check if the mouse click was within the card's boundaries
                        if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                            # Get the chosen card
                            chosen_card = player_hand[i]
                            print("Player chose:", chosen_card)

                            # Serialize the chosen card using pickle
                            serialized_card = pickle.dumps(chosen_card)

                            # Send the serialized card to the server
                            client_socket.sendall(serialized_card)

                            # Remove the chosen card from the player's hand
                            player_hand.pop(i)

                            # It's no longer the player's turn
                            is_player_turn = False
                            


    # Clear the screen
    screen.fill(WHITE)

    # Display the player's hand
    for i, card in enumerate(player_hand):
        x = 100 + i * (card_width + 10)
        y = screen_height - card_height - 100
        pygame.draw.rect(screen, BLACK, (x, y, card_width, card_height))
        pygame.draw.rect(screen, WHITE, (x + 2, y + 2, card_width - 4, card_height - 4))
        font = pygame.font.Font(None, 20)
        text = font.render(str(card), True, BLACK)
        screen.blit(text, (x + 20, y + 20))

    # Update the screen
    pygame.display.flip()

# Close the connection
client_socket.close()

# Quit the game
pygame.quit()
