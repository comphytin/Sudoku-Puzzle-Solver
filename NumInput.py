import pygame

class NumInput:
    def __init__(self, width, height, color):
        self.default_x = 40 
        self.default_y = 100
        self.width = width
        self.height = height
        self.color = color
        self.x = self.default_x
        self.y = self.default_y
    
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def reset_position(self, screen):
        self.x = self.default_x
        self.y = self.default_y
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    

    
