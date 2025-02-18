import pygame

class Text:
    def __init__(self, text, font_type, font_color, font_size, x, y, opacity, fade_out):
        self.text = text
        self.font_type = "font/" + font_type
        self.font_color = font_color
        self.font_size = font_size
        self.x = x
        self.y = y
        self.opacity = opacity
        self.fade_out = fade_out
        self.fade_speed = 5
        self.fading = False
        self.test_font = pygame.font.Font(self.font_type, self.font_size)
        self.surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.text_rendered = self.test_font.render(self.text, True, self.font_color)
        self.text_rect = self.text_rendered.get_rect(center = (self.x, self.y))
        self.update_surface()
        self.changeable = True
        
    
    #def text_rect(self):
        #return self.text_rendered.get_rect(center = (self.x, self.y))

    def update_surface(self):
        self.surface = pygame.Surface(self.text_rendered.get_size(), pygame.SRCALPHA)
        self.surface.blit(self.text_rendered, (0, 0))
        self.surface.set_alpha(self.opacity)

    def display(self, screen):
        rect = self.surface.get_rect(center=(self.x, self.y))
        screen.blit(self.surface, rect)
    
    def fadeIn(self):
        if self.opacity < 255:
            self.opacity += 15
        self.update_surface()

    def fadeOut(self):
        if self.opacity > 0:
            self.opacity -= 15
        self.update_surface()
    
    def fade_in_and_out(self):
        if self.fade_out:
            self.opacity -= self.fade_speed
            if self.opacity <= 0:
                self.fade_out = False
        else:
            self.opacity += self.fade_speed
            if self.opacity >= 255:
                self.fade_out = True
        self.update_surface()
    
    def change_text(self, new_text, new_color):
        if self.changeable:
            self.text = new_text
            self.text_rendered = self.test_font.render(self.text, True, new_color)
            self.font_color = new_color
            self.update_surface()


class DigitText(Text):
    def __init__(self, text, font_type, font_color, font_size, x, y, opacity, fade_out):
        super().__init__(text, font_type, font_color, font_size, x, y, opacity, fade_out)

class MovingText(Text):
    def __init__(self, text, font_type, font_color, font_size, x, y, opacity, fade_out, type):
        super().__init__(text, font_type, font_color, font_size, x, y, opacity, fade_out)
        self.type = type
        self.velocity = 15
        self.acceleration = 1
    
    def animate(self):
        
        if self.type == "level_select" and self.fade_out is False:
            self.y += self.velocity
            if self.velocity > 0:
                self.velocity -= self.acceleration
            
            
        elif self.type == "level_select" and self.fade_out:
            self.y -= self.velocity
            if self.velocity > 0:
                self.velocity -= self.acceleration
            
            
            
        
        
