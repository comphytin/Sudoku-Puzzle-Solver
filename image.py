import pygame 

class Image:
    def __init__(self, img_name):
        self.path = "img/"
        self.img_name = img_name
        self.image_path = self.path + self.img_name
        self.x_position = 0
        self.y_position = 0
        self.loaded_image = pygame.image.load(self.image_path).convert_alpha()
        self.img_width = self.loaded_image.get_width()
        self.img_height = self.loaded_image.get_height()
        self.resized_image = self.loaded_image
        self.resized = False
        self.opacity = 255
        self.fading = False
        self.invisible = False
        self.fade_out = True
        self.rect = self.get_rect(self.x_position, self.y_position)

    def get_rect(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.img_width = self.loaded_image.get_width()
        self.img_height = self.loaded_image.get_height()
        return self.resized_image.get_rect(center = (x_position, y_position))
    
    def update_surface(self):
        pass
    '''
    self.surface = pygame.Surface(self.text_rendered.get_size(), pygame.SRCALPHA)
    self.surface.blit(self.text_rendered, (0, 0))
    self.surface.set_alpha(self.opacity)
    '''
    
    def resize_image(self, img_width, img_height):
        self.resized = True
        self.img_width = img_width
        self.img_height = img_height
        self.resized_image = pygame.transform.scale(self.loaded_image, (img_width, img_height))
    
    def display(self, screen):
        screen.blit(self.resized_image, self.get_rect(self.x_position, self.y_position))

    def fadeOut(self):
        if self.opacity > 0:
            self.opacity -= 15
        self.resized_image.set_alpha(self.opacity)
    
    def fadeIn(self):
        if self.opacity < 255:
            self.opacity += 15
        self.resized_image.set_alpha(self.opacity)

class ImageButton(Image):
    def __init__(self, img_name):
        super().__init__(img_name)
    
    def expand(self, scale_factor):
        self.resized_image = pygame.transform.scale(self.loaded_image, (int(self.img_width * scale_factor), int(self.img_height * scale_factor)))
    
    def change_image(self, new_img_path):
        self.image_path = self.path + new_img_path
    
class MovingImage(Image):
    def __init__(self, img_name, type):
        super().__init__(img_name)
        self.type = type
        self.move_right = True
        self.move_left = False
        self.velocity = 0
        self.acceleration = 0.25

    def animate(self):
        if self.type == "button":
            pass
        # 50 <= x_position <= 550
        if self.type == "title_decoration":
            if self.move_right:
                self.x_position += self.velocity
                if self.x_position >= 170 and self.x_position <= 400:
                    self.velocity += self.acceleration
                elif self.x_position > 400 and self.x_position < 650:
                    self.velocity -= self.acceleration
                else:
                    self.move_right = False
                    self.move_left = True
            if self.move_left:
                self.x_position -= self.velocity
                if self.x_position >= 400 and self.x_position <= 650:
                    self.velocity -= self.acceleration
                elif self.x_position > 170 and self.x_position < 400:
                    self.velocity += self.acceleration
                else:
                    self.move_right = True
                    self.move_left = False

        if self.type == "level_button":
            pass
