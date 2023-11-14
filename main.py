import pygame
import random
import time

from sprite import *
from settings import *
from algo import *
from split_img import *
from hover import *

# import tkinter as tk
# from tkinter import filedialog

# block open Add image many times
icheck = 0

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
        multi = None

#region Old image handle
    # def choose_image(self):
    #     root = tk.Tk()
    #     root.withdraw()  # Hide the main tkinter window
    #     file_path = filedialog.askopenfilename(
    #         filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    #     return file_path

    # def cut_image_into_pieces(self, image, rows, columns):
    #     piece_width = 128*3 // columns
    #     piece_height = 128*3 // rows
    #     pieces = []

    #     for y in range(rows):
    #         for x in range(columns):
    #             left = x * piece_width
    #             top = y * piece_height
    #             piece = image.subsurface(pygame.Rect(left, top, piece_width, piece_height))
    #             pieces.append(piece)

    #     return pieces

#endregion

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
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
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

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

    #region Algorithms
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

    def IDS(self):
        solution_path = ids(
            self.initial_state, self.goal_state)
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
    #endregion

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_second = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        # self.buttons_list = []
        self.picture_list = []
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.initial_state = [row[:] for row in self.tiles_grid]

        #region Button creation
        button4 = Button("Clear image",200,50,(700,25),5)
        button5 = Button("Add image",200,50,(700,100),5)
        button6 = Button("Reset",200,50,(700,170),5)
        button7 = Button("Shuffle",200,50,(950,25),5)
        button8 = Button("SOLVE",100,50,(1000,100),5)
        button9 = Button("Quit Game",200,50,(900,640),5)

        name_button = ["BFS", "DFS", "IDS", "UCS", "A_STAR", "GREEDY","HILL CLIMBING"]
        multi_btn = MultiOptionButton(name_button, "Algorithm", 200, 50, (950, 170), 5)
        #endregion

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
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        #set background
        bg = pygame.image.load("images/bgmain.jpg").convert()
        self.screen.blit(bg,(0,0))

        #draw buttons
        buttons_draw()

        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for pic in self.picture_list:
            pic.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip()

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
                        self.tiles[row].append(Tile(self, col, row, None, self.pieces[i]))
                    else:
                        self.tiles[row].append(Tile(self, col, row, "empty", self.pieces[i]))

        else:
            for row, x in enumerate(self.tiles_grid):
                self.tiles.append([])
                for col, tile in enumerate(x):
                    if tile != 0:
                        self.tiles[row].append(Tile(self, col, row, str(tile)))
                    else:
                        self.tiles[row].append(Tile(self, col, row, "empty"))

    def move_tile(self, path):
        initial_state = [row[:] for row in self.tiles_grid]
        # Find the position of the empty tile (0)
        row, col = None, None
        for i in range(3):
            for j in range(3):
                if initial_state[i][j] == 0:
                    row, col = i, j
        if path == "down":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
            print(" move down")

        elif path == "up":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
            print(" move up")

        elif path == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
            print(" move right")

        elif path == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
            print(" move left")

        else:
            print("Invalid move: Unknown direction")
        self.draw()
        self.draw_tiles()
        self.all_sprites.update()
        pygame.time.delay(350)

    def return_picture_list(self):
        # Use a list comprehension to filter files with .png extension
        directory_path = "D:/UNIVERSITY/3rd/Semester 1/Artificial Intelligence/FINAL PROJECT/8-Puzzle/output_images/"
        picture_list_save = [f"output_images/{file}" for file in os.listdir(directory_path) if file.endswith(f".jpg")]
        return picture_list_save

    def events(self):
        global output_images_path
        output_images_path = 'output_images/'
        
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
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

        global icheck #limit the auto press of button Add image avoid error
        clicked_button_text = get_clicked_button_text()
        multi = get_clicked_button_text_multi()

        if clicked_button_text == "Shuffle":
            self.shuffle_time = 0
            self.start_shuffle = True

        if clicked_button_text == "Reset":
            self.new()

        if clicked_button_text == "Add image":
            if icheck == 0:
                icheck = 1
                self.start_add_image = True
                selected_image_path = split(self.start_add_image)
                if self.start_add_image:  
                    # Display the original image                     
                    # new_image = pygame.image.load(path)
                    # my_picture = Picture(100, 570, 384, 384, new_image)
                    # my_picture.resize()                               
                    # self.picture_list.append(my_picture)

                    # Convert pictures to surfaces
                    image_surfaces = self.return_picture_list()
                    self.pieces = [pygame.image.load(image_path).convert_alpha() for image_path in image_surfaces]

                    self.draw_tiles()

        if clicked_button_text == "Clear image":
            icheck = 0
            self.picture_list = []
            self.start_add_image = False
            self.show_number = True
            
            # Delete images in folder output_images
            delete_files_in_directory(output_images_path)

            self.draw_tiles()

        if clicked_button_text == "SOLVE":
            self.initial_state = [row[:]for row in self.tiles_grid]
            if multi == "BFS":
                self.shuffle_time = 0
                self.start_BFS = True
            elif multi == "DFS":
                self.shuffle_time = 0
                self.start_DFS = True
            elif multi == "IDS":
                self.shuffle_time = 0
                self.start_IDS = True
            elif multi == "UCS":
                self.shuffle_time = 0
                self.start_UCS = True
            elif multi == "A_STAR":
                self.shuffle_time = 0
                self.start_A_STAR = True
            elif multi == "GREEDY":
                self.shuffle_time = 0
                self.start_GREEDY = True
            elif multi == "HILL CLIMBING":
                self.shuffle_time = 0
                self.start_HILL = True

        if clicked_button_text == "Quit Game":
            delete_files_in_directory(output_images_path)
            pygame.quit()
            quit(0)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
def delete_files_in_directory(directory):
    # Get the list of files in the directory
    file_list = os.listdir(directory)

    # Iterate over the files and delete each one
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Not a file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

game = Game()

while True:
    game.new()
    game.run()
    delete_files_in_directory(output_images_path)
