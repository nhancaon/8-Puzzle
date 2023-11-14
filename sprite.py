import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text=None, image=None):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if image == None:
            if self.text != "empty":
                self.font = pygame.font.SysFont("Consolas", 50)
                font_surface = self.font.render(self.text, True, WHITE)
                self.image.fill(BLACK)
                self.font_size = self.font.size(self.text)
                draw_x = (TILESIZE / 2) - self.font_size[0] / 2
                draw_y = (TILESIZE / 2) - self.font_size[1] / 2
                self.image.blit(font_surface, (draw_x, draw_y))

            else:
                self.image.fill(BGCOLOUR)
        else:
            if self.text == None:
                self.image = image
            elif self.text != "empty":
                self.font = pygame.font.SysFont("Consolas", 50)
                font_surface = self.font.render(self.text, True, WHITE)

                self.font_size = self.font.size(self.text)
                draw_x = (TILESIZE / 2) - self.font_size[0] / 2
                draw_y = (TILESIZE / 2) - self.font_size[1] / 2
                self.image.blit(font_surface, (draw_x, draw_y))
                self.image = image
            else:
                self.image.fill(BGCOLOUR)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


# class Button:
#     def __init__(self, x, y, width, height, text, colour, text_colour):
#         self.colour, self.text_colour = colour, text_colour
#         self.width, self.height = width, height
#         self.x, self.y = x, y
#         self.text = text

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.colour,
#                          (self.x, self.y, self.width, self.height))
#         font = pygame.font.SysFont("Consolas", 30)
#         text = font.render(self.text, True, self.text_colour)
#         self.font_size = font.size(self.text)
#         draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
#         draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
#         screen.blit(text, (draw_x, draw_y))

#     def click(self, mouse_x, mouse_y):
#         return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


class Picture:
    def __init__(self, x, y, width, height, image):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.image = image # Set the image directly
        self.rect = self.image.get_rect()

    def draw(self, screen):
        # Update the picture's rect position
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)  # Blit the image onto the screen

    def resize(self):
        self.image = pygame.transform.scale(self.image, (self.width/3, self.height/3))
        self.width, self.height = self.width/3, self.width/3


# class MultiOptionButton(Button):
#     def __init__(self, x, y, width, height, options, colour, text_colour):
#         self.colour, self.text_colour = colour, text_colour
#         self.x, self.y = x, y
#         self.width, self.height = width, height
#         self.options = options
#         self.current_option_index = 0
#         self.text = self.options[self.current_option_index]

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.colour,
#                          (self.x, self.y, self.width, self.height))
#         font = pygame.font.SysFont("Consolas", 30)
#         text = font.render(self.text, True, self.text_colour)
#         self.font_size = font.size(self.text)
#         draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
#         draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
#         screen.blit(text, (draw_x, draw_y))

#     def click(self, mouse_x, mouse_y):
#         if super().click(mouse_x, mouse_y):
#             self.current_option_index = (
#                 self.current_option_index + 1) % len(self.options)
#             self.text = self.options[self.current_option_index]
#             return self.text
