
import pygame
import sys
import os
import data_model

class Sudoku_Game:

    def __init__(self, board):
        pygame.init()
        self.board = board

        self.rows = 9
        self.cols = 9
        self.grid_width = 71
        self.grid_start_x = 80
        self.grid_start_y = 80
        self.grid_color = (60, 60, 60)
        self.highlight_color = (40, 40, 40)
        # Zahlfarben: fixe (vorgegebene) Zellen vs. vom Spieler eingegebene
        self.number_color = (150, 150, 150)
        self.fixed_number_color = (255, 255, 255)
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Sudoku Game")
        self.icon_path = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Sudoku_icon.png'))
        self.icon_path = pygame.transform.scale(self.icon_path, (400, 400))
        pygame.display.set_icon(self.icon_path)
        self.clock = pygame.time.Clock()
        Welcome_path = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Welcome.png'))
        self.Welcome = pygame.transform.scale(Welcome_path, (400, 400))
        Play_path = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Play.png'))
        self.Play_big = pygame.transform.scale(Play_path, (200, 200))
        self.Play_small = pygame.transform.scale(Play_path, (167, 167))
        self.solved = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Solved.png'))
        self.solved = pygame.transform.scale(self.solved, (400, 400))
        self.main_music_path = os.path.join(os.path.dirname(__file__), 'music', 'sudoku.mp3')
        
        self.fixed_cells = [[value != 0 for value in row] for row in self.board]
        self.start_menu_music_path = os.path.join(os.path.dirname(__file__), 'music', 'start_menu_music.mp3')
        

        self.selected_cell: tuple[int, int] = None

        self.settings_button = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'settings_icon.png'))
        self.settings_button_small = pygame.transform.scale(self.settings_button, (50, 50))
        self.settings_button_big = pygame.transform.scale(self.settings_button, (60, 60))

        self.music_volume = 1


    def menu(self):

        icon_x = 200
        icon_y = 133
        speed = 0
        icon_beschleunigung = 0.3


        
        for i in range(150):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((20, 20, 20))  
            self.screen.blit(self.Welcome, (200, 200))
            pygame.display.flip()
            self.clock.tick(60)
        pygame.mixer.music.load(self.start_menu_music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)
        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 325 <= mouse_x <= 476 and 598 <= mouse_y <= 658:
                        return
                    if 730 <= mouse_x <= 790 and 20 <= mouse_y <= 80:
                        in_settings = True

                        slider = pygame.Rect(160, 260, 480, 10)
                        circle_radius = 12
                        circle_x = 160 + int(max(0.0, min(1.0, self.music_volume)) * 480)
                        pull = False

                        while in_settings:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        in_settings = False

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = event.pos
                                    circle_center = (circle_x, 265)
                                    if slider.collidepoint(mouse_x, mouse_y) or ((mouse_x - circle_center[0]) ** 2 + (mouse_y - circle_center[1]) ** 2) <= circle_radius ** 2:
                                        pull = True
                                        circle_x = max(160, min(640, mouse_x))
                                if event.type == pygame.MOUSEBUTTONUP:
                                    pull = False
                                if event.type == pygame.MOUSEMOTION and pull:
                                    mouse_x, mouse_y = event.pos
                                    circle_x = max(160, min(640, mouse_x))

                            self.music_volume = (circle_x - 160) / 480
                            self.music_volume = max(0.0, min(1.0, self.music_volume))
                            pygame.mixer.music.set_volume(self.music_volume)

                            self.screen.fill((20, 20, 20))
                            font = pygame.font.SysFont(None, 48)
                            text = font.render("Settings Menu - Press ESC to return", True, (200, 200, 200))
                            self.screen.blit(text, (100, 100))

                            label_font = pygame.font.SysFont(None, 36)
                            label = label_font.render("Music Volume", True, (200, 200, 200))
                            self.screen.blit(label, (160, 215))

                            pygame.draw.rect(self.screen, (80, 80, 80), slider, 6)
                            filled_rect = pygame.Rect(160, 260, int((circle_x - 160)), 10)
                            pygame.draw.rect(self.screen, (200, 200, 200), filled_rect, 6)
                            pygame.draw.circle(self.screen, (230, 230, 230), (circle_x, 265), circle_radius)
                            pygame.display.flip()
                            self.clock.tick(60)
            speed += icon_beschleunigung
            icon_y += speed

            if icon_y >= 133:
                icon_y = 133
                speed = -5

            self.screen.fill((20, 20, 20)) 
            self.screen.blit(self.icon_path, (icon_x, icon_y))
            if 325 <= mouse_x <= 476 and 598 <= mouse_y <= 658:
                self.screen.blit(self.Play_big, (300, 533))
            else:
                self.screen.blit(self.Play_small, (317, 550))
            
            if 730 <= mouse_x <= 790 and 20 <= mouse_y <= 80:
                self.screen.blit(self.settings_button_big, (730, 20))
            else:
                self.screen.blit(self.settings_button_small, (735, 25))
            
        
            
           
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        self.menu()
        pygame.mixer.music.load(self.main_music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

        while True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    inside = (self.grid_start_x <= x < self.grid_start_x + self.cols * self.grid_width and self.grid_start_y <= y < self.grid_start_y + self.rows * self.grid_width)

                    if not inside:
                        self.selected_cell = None
                    else:
                        column = (x - self.grid_start_x) // self.grid_width
                        row = (y - self.grid_start_y) // self.grid_width
                        self.selected_cell = (int(row), int(column))

                if event.type == pygame.KEYDOWN and self.selected_cell is not None:
                    row, column = self.selected_cell
                    if self.fixed_cells[row][column]:
                        continue
                    if event.key == pygame.K_1:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 1
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_2:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 2
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_3:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 3
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_4:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 4
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_5:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 5
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_6:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 6
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_7:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 7
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_8:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 8
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_9:
                        if self.board[row][column] == 0:
                            self.board[row][column] = 9
                            if not data_model.rule_check_whole_board(self.board):
                                self.board[row][column] = 0
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.board[row][column] = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 730 <= mouse_x <= 790 and 20 <= mouse_y <= 80:
                        in_settings = True

                        slider = pygame.Rect(160, 260, 480, 10)
                        circle_radius = 12
                        circle_x = 160 + int(max(0.0, min(1.0, self.music_volume)) * 480)
                        pull = False

                        while in_settings:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        in_settings = False

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = event.pos
                                    circle_center = (circle_x, 265)
                                    if slider.collidepoint(mouse_x, mouse_y) or ((mouse_x - circle_center[0]) ** 2 + (mouse_y - circle_center[1]) ** 2) <= circle_radius ** 2:
                                        pull = True
                                        circle_x = max(160, min(640, mouse_x))
                                if event.type == pygame.MOUSEBUTTONUP:
                                    pull = False
                                if event.type == pygame.MOUSEMOTION and pull:
                                    mouse_x, mouse_y = event.pos
                                    circle_x = max(160, min(640, mouse_x))

                            self.music_volume = (circle_x - 160) / 480
                            self.music_volume = max(0.0, min(1.0, self.music_volume))
                            pygame.mixer.music.set_volume(self.music_volume)

                            self.screen.fill((20, 20, 20))
                            font = pygame.font.SysFont(None, 48)
                            text = font.render("Settings Menu Press ESC to return", True, (200, 200, 200))
                            self.screen.blit(text, (100, 100))

                            label_font = pygame.font.SysFont(None, 36)
                            label = label_font.render("Music Volume", True, (200, 200, 200))
                            self.screen.blit(label, (160, 215))

                            pygame.draw.rect(self.screen, (80, 80, 80), slider, 6)
                            filled_rect = pygame.Rect(160, 260, int((circle_x - 160)), 10)
                            pygame.draw.rect(self.screen, (200, 200, 200), filled_rect, 6)
                            pygame.draw.circle(self.screen, (230, 230, 230), (circle_x, 265), circle_radius)
                            pygame.display.flip()
                            self.clock.tick(60)
                




            if data_model.check_game_won(self.board):
                for i in range(300):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    self.screen.fill((20, 20, 20))  
                    self.screen.blit(self.solved, (200, 200))
                    pygame.display.flip()
                    self.clock.tick(60)
                self.menu()
                self.board = data_model.create_sudoku_task()
                self.fixed_cells = [[value != 0 for value in row] for row in self.board]
                self.selected_cell = None
                continue
                
            self.screen.fill((20, 20, 20))

            self.draw_board(self.board)

            if 730 <= mouse_x <= 790 and 20 <= mouse_y <= 80:
                self.screen.blit(self.settings_button_big, (730, 20))
            else:
                self.screen.blit(self.settings_button_small, (735, 25))

            pygame.display.flip()
            self.clock.tick(60)

    def draw_board(self, board: list[list[int]]):
        rows = self.rows
        cols = self.cols
        grid_width = self.grid_width
        start_x = self.grid_start_x
        start_y = self.grid_start_y

        grid_color = self.grid_color

        if self.selected_cell is not None:
            sel_row, sel_col = self.selected_cell
            highlight_rect = pygame.Rect(start_x + sel_col * grid_width,start_y + sel_row * grid_width,grid_width, grid_width)
            pygame.draw.rect(self.screen, self.highlight_color, highlight_rect)

        for i in range(cols + 1):
            line_start_point = (start_x + i * grid_width, start_y)
            line_end_point = (start_x + i * grid_width, start_y + rows * grid_width)
            line_width = 4 if (i % 3 == 0) else 2
            pygame.draw.line(surface=self.screen, color=grid_color, start_pos=line_start_point, end_pos=line_end_point, width=line_width)

        for i in range(rows + 1):
            line_start_point = (start_x, start_y + i * grid_width)
            line_end_point = (start_x + cols * grid_width, start_y + i * grid_width)
            line_width = 4 if (i % 3 == 0) else 2
            pygame.draw.line(surface=self.screen, color=grid_color, start_pos=line_start_point, end_pos=line_end_point, width=line_width)

        font = pygame.font.SysFont(None, int(grid_width * 0.65))

        for row in range(rows):
            for column in range(cols):
                value = board[row][column]

                if value == 0:
                    continue

                is_fixed = self.fixed_cells[row][column]
                color = self.fixed_number_color if is_fixed else self.number_color
                text_surface = font.render(str(value), True, color)
                cell_rect = pygame.Rect(start_x + column * grid_width,start_y + row * grid_width, grid_width, grid_width)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                self.screen.blit(text_surface, text_rect)

