import pygame
import random
import time
from sprite import *
from settings import *
from algo import *
import tkinter as tk
from tkinter import filedialog


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.step = ""
        self.shuffle_time = 0
        self.start_shuffle = False
        self.start_DFS = False
        self.start_IDS = False
        self.start_BFS = False
        self.start_UCS = False
        self.start_A_STAR = False
        self.start_GREEDY = False
        self.start_HILL = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.pieces = []
        self.start_add_image = False
        self.show_number = True
        self.selected_algo = None

    def choose_image(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        return file_path

    def cut_image_into_pieces(self, image, rows, columns):
        piece_width = 128*3 // columns
        piece_height = 128*3 // rows
        pieces = []

        for y in range(rows):
            for x in range(columns):
                left = x * piece_width
                top = y * piece_height
                piece = image.subsurface(pygame.Rect(
                    left, top, piece_width, piece_height))
                pieces.append(piece)

        return pieces

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [
            [x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove(
                "left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove(
                "right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove(
                "down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove(
                "up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        if self.start_add_image:
            for row, x in enumerate(self.tiles_grid):
                self.tiles.append([])
                for col, tile in enumerate(x):
                    i = tile
                    if i == 0:
                        i = 8
                    else:
                        i -= 1
                    if tile != 0:
                        self.tiles[row].append(
                            Tile(self, col, row, None, self.pieces[i]))
                    else:
                        self.tiles[row].append(
                            Tile(self, col, row, "empty", self.pieces[i]))

        else:
            for row, x in enumerate(self.tiles_grid):
                self.tiles.append([])
                for col, tile in enumerate(x):
                    if tile != 0:
                        self.tiles[row].append(Tile(self, col, row, str(tile)))
                    else:
                        self.tiles[row].append(Tile(self, col, row, "empty"))

    def BFS(self):
        solution_path = bfs(self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path

    def DFS(self):
        solution_path = dfs(self.initial_state, self.goal_state)
        if solution_path:
            print("step = ")
            print(len(solution_path))
        return solution_path

    def UCS(self):
        solution_path = ucs(self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path

    def A_STAR(self):
        solution_path = a_star(self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path

    def GREEDY(self):
        solution_path = greedy(
            self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path
    
    def HILL(self):
        solution_path = hill_climbing(
            self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path
    
    def IDS(self):
        solution_path = ids(
            self.initial_state, self.goal_state)
        print("step = ")
        print(len(solution_path))
        return solution_path

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_second = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.picture_list = []
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.initial_state = [row[:] for row in self.tiles_grid]
        self.multi_btn = MultiOptionButton(950, 170, 200, 50, [
                                           "Algorithm", "BFS", "DFS", "IDS", "UCS", "A_STAR", "GREEDY","HILL CLIMBING"], BLACK, WHITE)

        self.buttons_list.append(
            Button(950, 25, 200, 50, "Shuffle", BLACK, WHITE))
        self.buttons_list.append(
            Button(700, 170, 200, 50, "Reset", BLACK, WHITE))
        self.buttons_list.append(
            Button(900, 640, 200, 50, "Quit Game", BLACK, WHITE))
        self.buttons_list.append(
            Button(700, 100, 200, 50, "Add image", BLACK, WHITE))
        self.buttons_list.append(
            Button(700, 25, 200, 50, "Clear image", BLACK, WHITE))
        self.buttons_list.append(
            Button(1000, 100, 100, 50, "SOLVE", BLACK, WHITE))

        self.draw_tiles()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 30:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True
        if self.start_DFS:
            solution_path = self.DFS()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_DFS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_DFS = False
                self.start_game = True
                self.start_timer = True
        if self.start_BFS:
            solution_path = self.BFS()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_BFS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_BFS = False
                self.start_game = True
                self.start_timer = True
        if self.start_UCS:
            solution_path = self.UCS()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_UCS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_UCS = False
                self.start_game = True
                self.start_timer = True
        if self.start_A_STAR:
            solution_path = self.A_STAR()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_A_STAR = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_A_STAR = False
                self.start_game = True
                self.start_timer = True
        if self.start_GREEDY:
            solution_path = self.GREEDY()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_GREEDY = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_GREEDY = False
                self.start_game = True
                self.start_timer = True
        if self.start_HILL:
            solution_path = self.HILL()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_HILL = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_HILL = False
                self.start_game = True
                self.start_timer = True
        if self.start_IDS:
            solution_path = self.IDS()

            if solution_path:
                print("Solution Path:", solution_path)
                for move in solution_path:
                    self.move_tile(move)
                self.start_IDS = False
                self.start_game = True
                self.start_timer = True
            else:
                print("No solution found")
                self.start_IDS = False
                self.start_game = True
                self.start_timer = True       
                
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0),
                             (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col),
                             (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        for pic in self.picture_list:
            pic.draw(self.screen)
        self.multi_btn.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" %
                  (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip()

    def move_tile(self, path):
        initial_state = [row[:] for row in self.tiles_grid]
        # Find the position of the empty tile (0)
        row, col = None, None
        for i in range(3):
            for j in range(3):
                if initial_state[i][j] == 0:
                    row, col = i, j
        if path == "down":
            self.tiles_grid[row][col], self.tiles_grid[row -
                                                       1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
            print(" move down")

        elif path == "up":
            self.tiles_grid[row][col], self.tiles_grid[row +
                                                       1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
            print(" move up")

        elif path == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col -
                                                            1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
            print(" move right")

        elif path == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col +
                                                            1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
            print(" move left")

        else:
            print("Invalid move: Unknown direction")
        self.draw()
        self.draw_tiles()
        self.all_sprites.update()
        pygame.time.delay(350)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col +
                                                                                1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col -
                                                                                1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row -
                                                                           1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row +
                                                                           1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()
                if self.multi_btn.click(mouse_x, mouse_y):
                    self.selected_algo = self.multi_btn.text
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "Add image":
                            selected_image_path = self.choose_image()
                            self.start_add_image = True
                            if selected_image_path:
                                selected_image = pygame.image.load(
                                    selected_image_path)
                                new_image = pygame.image.load(
                                    selected_image_path)
                                my_picture = Picture(
                                    100, 570, 384, 384, new_image)
                                my_picture.resize()
                                self.picture_list.append(my_picture)
                                self.pieces = self.cut_image_into_pieces(
                                    selected_image, 3, 3)
                                self.draw_tiles()

                        if button.text == "Clear image":
                            self.picture_list = []
                            self.start_add_image = False
                            self.show_number = True
                            self.draw_tiles()
                        if button.text == "SOLVE":
                            self.initial_state = [row[:]
                                                  for row in self.tiles_grid]
                            if self.selected_algo == "BFS":
                                self.shuffle_time = 0
                                self.start_BFS = True
                            elif self.selected_algo == "DFS":
                                self.shuffle_time = 0
                                self.start_DFS = True
                            elif self.selected_algo == "IDS":
                                self.shuffle_time = 0
                                self.start_IDS = True
                            elif self.selected_algo == "UCS":
                                self.shuffle_time = 0
                                self.start_UCS = True
                            elif self.selected_algo == "A_STAR":
                                self.shuffle_time = 0
                                self.start_A_STAR = True
                            elif self.selected_algo == "GREEDY":
                                self.shuffle_time = 0
                                self.start_GREEDY = True
                            elif self.selected_algo == "HILL CLIMBING":
                                self.shuffle_time = 0
                                self.start_HILL = True

                        elif button.text == "Quit Game":
                            pygame.quit()
                            quit(0)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


game = Game()
while True:
    game.new()
    game.run()
