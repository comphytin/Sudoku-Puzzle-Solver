import pygame
from sys import exit

from level_selection import LevelSelection
from background import Background
from text import Text, MovingText
from image import Image, MovingImage, ImageButton
from NumInput import NumInput
from sudoku_func import SudokuFunctions

pygame.init()  

##### CONSTANTS FOR THE ENTIRE GAME #####

GAME_WIDTH = 800
GAME_HEIGHT = 600
GRID_SQUARE_SIZE = 50
FRAMES_PER_SECOND = 60

##### CONSTANTS FOR THE ENTIRE GAME #####

##### FUNCTIONS FOR GAME LOOP #####

def expand_button(button, mouse, rect, og_rect, og_width, og_height):
    if button.get_rect(button.x_position, button.y_position).collidepoint(mouse):
            button.expand()
            
            delta_width = int(og_width * 1.5) - rect.width
            delta_height = int(og_height * 1.5) - rect.height

            rect.x -= delta_width // 2
            rect.y -= delta_height // 2

            rect.width = int(og_width * 1.5)
            rect.height = int(og_height * 1.5)
    else:
        button.resize_image(og_width, og_height)
        rect = og_rect


digit_x_pos = 42 + int(GRID_SQUARE_SIZE) / 2
digit_y_pos = 105 + int(GRID_SQUARE_SIZE) / 2

def updated_board(puzzle_num, digits_matrix):
    board = open("sudoku_boards/" + str(puzzle_num) + ".txt", "r")
    row_num = 1
    column_num = 1
    for row in board:
        for digit in row:
            if column_num <= 9:
                if digit != ".":
                    digits_matrix[row_num - 1][column_num - 1].change_text(str(digit), (0, 0, 0))
                    digits_matrix[row_num - 1][column_num - 1].changeable = False
                else:
                    digits_matrix[row_num - 1][column_num - 1].change_text("", (255, 0, 0))
                    
            column_num += 1
        row_num += 1
        column_num = 1

def emptied_board(digits_matrix):
    for row in digits_matrix:
        for digit in row:
            digit.changeable = True
            digit.change_text(str(0), (0, 0, 0))
        

'''
digit_x_pos = 42 + int(GRID_SQUARE_SIZE) / 2
digit_y_pos = 105 + int(GRID_SQUARE_SIZE) / 2
for row in digits_matrix:
    for i in range(0, 9):
        row.append(Text(str(i + 1), 'Pixeltype.ttf', (255, 0, 0), 50, digit_x_pos, digit_y_pos, 255, False))
        digit_x_pos += GRID_SQUARE_SIZE
        if digit_x_pos > 462 + int(GRID_SQUARE_SIZE) / 2:
            digit_x_pos = 42 + int(GRID_SQUARE_SIZE) / 2
            digit_y_pos += GRID_SQUARE_SIZE
'''
##### FUNCTIONS FOR GAME LOOP #####

'''
Automatically runs the game at screen resolution 
(by detecting the computer screen's current resolution)
infoObject = pygame.display.Info()
pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
'''
    
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption('Sudoku Puzzle')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/edosz.ttf', 50)
default_color = (255, 255, 255)

# Variables for Intro Screen

sudoku_img = MovingImage("sudokuboardimg.jpeg", "title_decoration")
sudoku_img_rect = sudoku_img.get_rect(170, 230)
sudoku_img.resize_image(210, 210)

game_title = Text('Sudoku Game ', 'edosz.ttf', (0, 0, 0), 50, 400, 80, 255, True)
press_to_play = Text(' Press c to Play ', 'edosz.ttf', (0, 0, 255), 50, 400, 400, 255, True)
press_to_quit = Text(' Press q to Exit ', 'edosz.ttf', (255, 0, 0), 50, 400, 470, 255, True)

title_active = True
game_active = False
level_select_active = False

background = Background(screen, default_color, False, False)

c_pressed = False
q_pressed = False

################################### TEMPORARY CODE ###################################
print("Image Width: " + str(sudoku_img.img_width) + " Image Height: " + str(sudoku_img.img_height))
infoObject = pygame.display.Info()
print("Screen Width: " + str(infoObject.current_w) + "px")
print("Screen Height: " + str(infoObject.current_h) + "px")
################################### TEMPORARY CODE ###################################

# Variables for Level Selection

#bg_music = pygame.mixer.Sound('audio/beneath_the_mask.mp3')
#bg_music.set_volume(0.5)
#bg_music.play(loops = -1)

select_level_title = MovingText('Select Puzzle', 'edosz.ttf', (0, 0, 0), 50, 400, -32, 0, False, "level_select")

settings_img = ImageButton("sprites/settings.png")
settings_img_rect = settings_img.get_rect(700, 500)
button_disabled = False

level_buttons = []
level_buttons_rects = []
select_xpos = 250
select_ypos = 200

for i in range(1, 10):
    level_buttons.append(ImageButton("sprites/" + str(i) + ".png"))
    level_buttons_rects.append(level_buttons[i - 1].get_rect(select_xpos, select_ypos))
    select_xpos += 150
    if select_xpos == 700:
        select_xpos = 250
        select_ypos += 110 

# Variables for Sudoku Board

sudoku_xpos_initial = 200
sudoku_ypos_initial = 100

sudoku_puzzle_title = Text('Puzzle #', 'Pixeltype.ttf', (0, 0, 0), 50, 400, 60, 255, False)
white_square = NumInput(GRID_SQUARE_SIZE, GRID_SQUARE_SIZE, (255, 255, 255))

digits_matrix = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

current_row = 1
current_column = 1
# Empty Sudoku Board
digit_x_pos = 42 + int(GRID_SQUARE_SIZE) / 2
digit_y_pos = 105 + int(GRID_SQUARE_SIZE) / 2
for row in digits_matrix:
    for i in range(0, 9):
        row.append(Text("0", 'Pixeltype.ttf', (0, 0, 0), 50, digit_x_pos, digit_y_pos, 255, False))
        digit_x_pos += GRID_SQUARE_SIZE
        if digit_x_pos > 462 + int(GRID_SQUARE_SIZE) / 2:
            digit_x_pos = 42 + int(GRID_SQUARE_SIZE) / 2
            digit_y_pos += GRID_SQUARE_SIZE  

current_row = 1
current_column = 1   

# Variables for Settings Tab

settings_active = False

settings_tab = Image("sprites/settings_tab.png")
settings_tab_rect = settings_tab.get_rect(400, 310)

cross_button = ImageButton("sprites/cross.png")
cross_button_rect = cross_button.get_rect(575, 168)

'''
Main Tab
Width: 400 px
Height: 320 px

X button to close tab
Width: 24 px
Height: 24 px
'''
settings_active = False

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        ####################################FULLSCREEN_MODE####################################

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if background.fullscreen is False:
                background.fullscreen = True
                background.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.FULLSCREEN)
            else:
                background.fullscreen = False
                background.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        ####################################FULLSCREEN_MODE####################################

        if title_active is True and game_title.fade_out is True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                game_title.fading = True
                sudoku_img.fading = True   
                select_level_title.fading = True                                       
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                exit()
        elif level_select_active is True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # RETURN => ENTER
                level_select_active = False # Not Final
                game_active = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                game_title.fading = True
                sudoku_img.fading = True
                select_level_title.fading = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if settings_img_rect.collidepoint(event.pos) and settings_active is False:
                    settings_active = True
                    button_disabled = True
                elif settings_img_rect.collidepoint(event.pos) and settings_active is True:
                    settings_active = False
                    button_disabled = False
                if button_disabled is False and settings_active is False:
                    for i in range(0, 9):
                        if level_buttons_rects[i].collidepoint(event.pos): 
                            sudoku_puzzle_title.change_text("Puzzle #" + str(i + 1), (0, 0, 0))
                            level_select_active = False
                            game_active = True
                            updated_board(i + 1, digits_matrix)
                if cross_button_rect.collidepoint(event.pos) and settings_active is True:
                    settings_active = False
                    button_disabled = False
            
        elif game_active is True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                print("0")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                game_active = False
                level_select_active = True
                emptied_board(digits_matrix)
                white_square.reset_position(background.screen)
                current_row = 1
                current_column = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and white_square.x > 40:
                white_square.x -= GRID_SQUARE_SIZE
                current_column -= 1
               
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and white_square.x < 440:
                white_square.x += GRID_SQUARE_SIZE
                current_column += 1
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and white_square.y > 100:
                white_square.y -= GRID_SQUARE_SIZE
                current_row -= 1
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and white_square.y < 490:
                white_square.y += GRID_SQUARE_SIZE
                current_row += 1
                
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed
                if pygame.K_1 <= event.key <= pygame.K_9 and digits_matrix[current_row - 1][current_column - 1].changeable:
                    digits_matrix[current_row - 1][current_column - 1].change_text(str(chr(event.key)), (255, 0, 0))
                if pygame.K_BACKSPACE == event.key and digits_matrix[current_row - 1][current_column - 1].changeable:
                    digits_matrix[current_row - 1][current_column - 1].change_text("", (255, 0, 0))
    
    mouse = pygame.mouse.get_pos()
    background.render()
    
    if game_active is True:
        background.levelselect_to_sudokuboard()
        
        initial_x_pos = 40
        initial_y_pos = 100
        sudoku_puzzle_title.display(background.screen)
        white_square.display(background.screen)
        for row in digits_matrix:
            for digit in row:
                digit.display(background.screen)
        # Draws the Sudoku Board
        for i in range(0, 10):
            pygame.draw.line(background.screen, (0, 0, 0), [initial_x_pos, 100], [initial_x_pos, 550], 5) # Draws a vertical line
            pygame.draw.line(background.screen, (0, 0, 0), [40, initial_y_pos], [40 + int(9 * GRID_SQUARE_SIZE), initial_y_pos], 5) # Draws a horizontal line
            initial_x_pos += GRID_SQUARE_SIZE
            initial_y_pos += GRID_SQUARE_SIZE
        
        #settings_img.display(background.screen)
        

    elif level_select_active is True:   

        background.intro_to_levelselect()
        
        if select_level_title.fading is True:
            if select_level_title.fade_out is True:
                select_level_title.fadeOut()
            else:
                select_level_title.fadeIn()
            select_level_title.animate()
        
        if select_level_title.opacity == 0 and select_level_title.velocity == 0:
            level_select_active = False
            select_level_title.fading = False
            game_title.fadeIn()
            sudoku_img.fadeIn()
            title_active = True
            select_level_title.fade_out = False
            select_level_title.velocity = 15
        
        if select_level_title.opacity == 255 and select_level_title.velocity == 0:
            select_level_title.fading = False
            select_level_title.fade_out = True
            select_level_title.velocity = 15

        select_level_title.display(background.screen)
        settings_img.display(background.screen)

        for i in range(0, 9):
            level_buttons[i].display(background.screen)
            expand_button(level_buttons[i], mouse, level_buttons_rects[i], level_buttons_rects[i], 50, 50)
        
        expand_button(settings_img, mouse, settings_img_rect, settings_img_rect, 50, 50)
        expand_button(cross_button, mouse, cross_button_rect, cross_button_rect, 24, 24)
        
        if settings_active:
            settings_tab.display(background.screen)
            cross_button.display(background.screen)

    elif title_active is True: 
        # Displaying the title screen
        background.levelselect_to_intro()
        
        if game_title.fading is True:
            if game_title.fade_out is True:
                game_title.fadeOut()
                select_level_title.fadeIn()
            else:
                game_title.fadeIn()
        if sudoku_img.fading is True:
            if sudoku_img.fade_out is True:
                sudoku_img.fadeOut()
            else:
                sudoku_img.fadeIn()

        if game_title.opacity == 0 and game_title.fading is True and game_title.fade_out is True:
            title_active = False
            game_title.fading = False
            level_select_active = True
            game_title.fade_out = False
            sudoku_img.fading = False
            sudoku_img.fade_out = False
        elif game_title.opacity == 255 and game_title.fading is True and game_title.fade_out is False:
            level_select_active = False
            game_title.fading = False
            game_title.fade_out = True
            sudoku_img.fading = False
            sudoku_img.fade_out = True
        
        #if sudoku_img.get_rect(sudoku_img.x_position, sudoku_img.y_position).collidepoint(mouse):
            #print("YOUR MOM")   
        
        press_to_play.fade_in_and_out()
        press_to_quit.fade_in_and_out()

        game_title.display(background.screen)
        press_to_play.display(background.screen)
        press_to_quit.display(background.screen)
        sudoku_img.display(background.screen)
        sudoku_img.animate()
    
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

