import pygame

class UI:
    '''
    UI class for rendering and managing the graphical interface of the stock prediction
    '''
    def __init__(self, screen, screen_width, screen_height):
        """
        Initialize the UI class with screen dimensions and set up graphical components.

        Args:
            screen (pygame.Surface): The display surface for rendering.
            screen_width (int): Width of the screen in pixels.
            screen_height (int): Height of the screen in pixels.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.button_padding = 20  
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72) 

        self.button_width = 150
        self.button_height = 50

        self.home_button = pygame.Rect(self.screen_width - 170, self.screen_height - 95, self.button_width, self.button_height)
        self.end_button = pygame.Rect(20, self.screen_height - 95, self.button_width, self.button_height)
        self.watchlist_button = pygame.Rect(self.screen_width // 2 - self.button_width // 2, 200, self.button_width, self.button_height)
        self.your_stocks_button = pygame.Rect(self.screen_width // 2 - self.button_width // 2, 300, self.button_width, self.button_height)
        self.tutorial_button = pygame.Rect(self.screen_width // 2 - self.button_width // 2, 400, self.button_width, self.button_height)

        self.input_box = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
        self.input_text = ""
        self.active = False
        self.clear_button = pygame.Rect(self.input_box.right + 10, self.screen_height // 2 + 50, self.input_box.width, 50)

        self.watchlist = []

        try:
            self.background_image = pygame.image.load("assets/stockBackground.png")
            self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        except pygame.error:
            print("Error loading the background image for 'Your Stocks'.")
            self.background_image = None

    def draw_home_screen(self, mouse_pos, center_x):
        """
        Draw the home screen with buttons and a title.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).
            center_x (int): x-coordinate of the screen's center.
        """
        title = self.title_font.render("Stock Predictor", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, 50))

        self.draw_button(self.watchlist_button, "Watchlist", mouse_pos)
        self.draw_button(self.your_stocks_button, "Your Stocks", mouse_pos)
        self.draw_button(self.tutorial_button, "Tutorial", mouse_pos)

    def draw_tutorial_screen(self, mouse_pos):
        """
        Draw the tutorial screen, including instructions and navigation buttons.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).
        """
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

        title = self.title_font.render("Tutorial", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 10))

        try:
            instruction = pygame.image.load('assets/instruction.png')
            instruction = pygame.transform.smoothscale(instruction, (self.screen_width, int(self.screen_height / 1.2)))
            self.screen.blit(instruction, (0, 0))
        except pygame.error:
            print("Error loading the tutorial image.")

        pygame.display.flip()

    def draw_your_stocks_screen(self, mouse_pos, user_input, response_message, center_x, center_y, graph_data=None):
        """
        Draw the "Your Stocks" screen with input fields, response messages, and an optional graph.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).
            user_input (str): Text entered by the user.
            response_message (str): Response to the user's input.
            center_x (int): X-coordinate of the screen's horizontal center.
            center_y (int): Y-coordinate of the screen's vertical center.
            graph_data (dict, optional): Data for rendering a stock graph.
        """
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        question_text = self.font.render("Enter a stock ticker:", True, (255, 255, 255))
        self.screen.blit(question_text, (self.screen_width // 2 - question_text.get_width() // 2, self.screen_height // 2 - 100))

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)

        input_text = self.font.render(user_input, True, (0, 0, 0))
        self.screen.blit(input_text, (self.input_box.x + 5, self.input_box.y + 10))

        if response_message:
            color = (0, 255, 0) if response_message.startswith("Ticker valid") else (255, 0, 0)
            response_text = self.font.render(response_message, True, color)
            self.screen.blit(response_text, (self.screen_width // 2 - response_text.get_width() // 2, self.screen_height // 2 + 150))

        if graph_data:
            graph_area = pygame.Rect(50, self.screen_height // 2 + 200, self.screen_width - 100, 300)
            pygame.draw.rect(self.screen, (0, 0, 0), graph_area)
            self.draw_stock_graph(graph_data, graph_area)

        self.draw_button(self.clear_button, "Clear", mouse_pos, clear_button=True)
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

    def draw_watchlist_screen(self, mouse_pos, watchlist):
        """
        Draw the watchlist screen with the list of stocks and navigation buttons.

        Args:
            mouse_pos (tuple): Current mouse position (x, y).
            watchlist (list): List of stocks to display.
        """
        title = self.title_font.render("Watchlist", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 10))

        if not watchlist:
            no_stocks_text = self.font.render("No stocks in watchlist.", True, (255, 255, 255))
            self.screen.blit(no_stocks_text, (self.screen_width // 2 - no_stocks_text.get_width() // 2, 150))
        else:
            y_offset = 150
            for i, (stock, days) in enumerate(watchlist):
                stock_text = self.font.render(f"{stock} - {days} days", True, (255, 255, 255))
                stock_rect = pygame.Rect(self.screen_width // 2 - 150, y_offset, 300, 50)

                if stock_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (0, 255, 255), stock_rect)  
                else:
                    pygame.draw.rect(self.screen, (0, 0, 255), stock_rect) 

                pygame.draw.rect(self.screen, (0, 0, 0), stock_rect, 2)  
                self.screen.blit(stock_text, (self.screen_width // 2 - stock_text.get_width() // 2, y_offset + 10))

                y_offset += 60  

        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

    def draw_button(self, button, text, mouse_pos, home_button=False, end_button=False, clear_button=False):
        """
        Draw a button with dynamic hover effects and labels.

        Args:
            button (pygame.Rect): Rectangle defining the button area.
            text (str): Text to display on the button.
            mouse_pos (tuple): Current mouse position (x, y).
            home_button (bool): Whether this button is the "Home" button.
            end_button (bool): Whether this button is the "End" button.
            clear_button (bool): Whether this button is the "Clear" button.
        """
        label = self.font.render(text, True, (255, 255, 255))

        shadow_offset = 5
        shadow_color = (50, 50, 50)
        border_radius = 15

        pygame.draw.rect(self.screen, shadow_color, button.move(shadow_offset, shadow_offset), border_radius=border_radius)

        if button.collidepoint(mouse_pos):
            if home_button:
                button_color = (0, 255, 0)
            elif clear_button:
                button_color = (211, 211, 211)
            elif end_button:
                button_color = (255, 69, 0)
            else:
                button_color = (0, 255, 255)
        else:
            if home_button:
                button_color = (34, 139, 34)
            elif clear_button:
                button_color = (169, 169, 169)
            elif end_button:
                button_color = (255, 0, 0)
            else:
                button_color = (0, 0, 255)

        pygame.draw.rect(self.screen, button_color, button, border_radius=border_radius)
        pygame.draw.rect(self.screen, (0, 0, 0), button, 2, border_radius=border_radius)

        self.screen.blit(label, (button.x + (button.width - label.get_width()) // 2, button.y + (button.height - label.get_height()) // 2))
