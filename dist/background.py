class Background:
    def __init__(self, screen, background_color, level_select_active, game_active):
        self.screen = screen
        self.background_color = background_color
        self.level_select_active = level_select_active
        self.game_active = game_active
        self.transition_speed = 4
        self.fullscreen = False
        
    def color_transition(self, target_color):
        self.background_color = list(self.background_color)
        if self.background_color != target_color:
            for i in range(3):  # Loop through R, G, B components
                if self.background_color[i] < target_color[i]:
                    self.background_color[i] += self.transition_speed
                    if self.background_color[i] > target_color[i]:
                        self.background_color[i] = target_color[i]
                elif self.background_color[i] > target_color[i]:
                    self.background_color[i] -= self.transition_speed
                    if self.background_color[i] < target_color[i]:
                        self.background_color[i] = target_color[i]
        self.background_color = tuple(self.background_color)

    def intro_to_levelselect(self):
        target_color = [45, 252, 242]
        self.color_transition(target_color)
    
    def levelselect_to_intro(self):
        target_color = [255, 255, 255]
        self.color_transition(target_color)
    
    def levelselect_to_sudokuboard(self):
        target_color = [130, 191, 120] # RGB 143, 149, 201
        self.color_transition(target_color)
    
    def sudokuboard_to_levelselect(self):
        target_color = [45, 252, 242]
        self.color_transition(target_color)
    
    def render(self):
         self.screen.fill(self.background_color)