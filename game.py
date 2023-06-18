import pygame
import socket
import pickle
from card import Card

class CardGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set up the game window
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Card Game')

        # Set up card dimensions
        self.card_width, self.card_height = 100, 140

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 5000)

        try:
            self.client_socket.connect(self.server_address)
            print('Connected to:', self.server_address)
        except ConnectionRefusedError:
            print('Failed to connect to the server. Please make sure the server is running.')
            pygame.quit()
            return

        # Receive the initial hand from the server
        try:
            self.player_hand = pickle.loads(self.client_socket.recv(1024))
        except pickle.UnpicklingError:
            print('Failed to receive the initial hand from the server.')
            self.client_socket.close()
            pygame.quit()
            return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the mouse click was on a card
                    for i, card in enumerate(self.player_hand):
                        x = 100 + i * (self.card_width + 10)
                        y = self.screen_height - self.card_height - 100

                        if x <= mouse_x <= x + self.card_width and y <= mouse_y <= y + self.card_height:
                            chosen_card = self.player_hand[i]
                            print("Player chose:", chosen_card)

                            # Serialize and send the chosen card to the server
                            try:
                                serialized_card = pickle.dumps(chosen_card)
                                self.client_socket.sendall(serialized_card)
                            except (pickle.PickleError, socket.error):
                                print('Failed to send the chosen card to the server.')
                                self.client_socket.close()
                                pygame.quit()
                                return

                            # Remove the chosen card from the player's hand
                            self.player_hand.pop(i)

    def display_cards(self):
        self.screen.fill(self.WHITE)

        # Display the player's hand
        for i, card in enumerate(self.player_hand):
            x = 100 + i * (self.card_width + 10)
            y = self.screen_height - self.card_height - 100
            pygame.draw.rect(self.screen, self.BLACK, (x, y, self.card_width, self.card_height))
            pygame.draw.rect(self.screen, self.WHITE, (x + 2, y + 2, self.card_width - 4, self.card_height - 4))
            font = pygame.font.Font(None, 20)
            text = font.render(str(card), True, self.BLACK)
            self.screen.blit(text, (x + 20, y + 20))

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.display_cards()

        self.client_socket.close()
        pygame.quit()

if __name__ == '__main__':
    game = CardGame()
    game.run()
