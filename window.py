import pygame
from sys import exit

from level_selection import LevelSelection
from background import Background
from text import Text, MovingText
from image import Image, MovingImage, ImageButton
from NumInput import NumInput
from sudoku_func import SudokuFunctions
from music import Music

pygame.init()  

##### CONSTANTS FOR THE ENTIRE GAME #####

GAME_WIDTH = 800
GAME_HEIGHT = 600
GRID_SQUARE_SIZE = 50
FRAMES_PER_SECOND = 60

##### CONSTANTS FOR THE ENTIRE GAME #####

##### FUNCTIONS FOR GAME LOOP #####

def expand_button(button, mouse, rect, og_rect, og_width, og_height, scale_factor):
    if button.get_rect(button.x_position, button.y_position).collidepoint(mouse):
            button.expand(scale_factor)
            
            delta_width = int(float(og_width) * scale_factor) - rect.width
            delta_height = int(float(og_height) * scale_factor) - rect.height

            rect.x -= delta_width // 2
            rect.y -= delta_height // 2

            rect.width = int(float(og_width) * scale_factor)
            rect.height = int(float(og_height) * scale_factor)
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

def display_time():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    time_surf = Text('Time: ' + str(current_time) + ' s', 'Pixeltype.ttf', (0, 0, 0), 50, 104, 60, 255, False)
    time_surf.display(background.screen)
    return current_time

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

sudoku_functions = SudokuFunctions(digits_matrix)

# Variables for Settings Tab

settings_active = False

settings_tab = Image("sprites/settings_tab.png")
settings_tab_rect = settings_tab.get_rect(400, 310)

cross_button = ImageButton("sprites/cross.png")
cross_button_rect = cross_button.get_rect(575, 168)

check_boxes = []
check_boxes_rects = []
ticks = []
ticks_rects = []

check_boxes.append(Image("sprites/checkbox.png"))
check_boxes_rects.append(check_boxes[0].get_rect(565, 210))
ticks.append(Image("sprites/tick.png"))
ticks_rects.append(ticks[0].get_rect(575, 208))

check_boxes.append(Image("sprites/checkbox.png"))
check_boxes_rects.append(check_boxes[1].get_rect(565, 250))
ticks.append(Image("sprites/tick.png"))
ticks_rects.append(ticks[1].get_rect(575, 248))

background_music_played = True
background_transitions_shown = True
background_music_played_temp = True
background_transitions_shown_temp = True

apply_settings_default_img = Image("sprites/apply_settings_default.png")
apply_settings_default_rect = apply_settings_default_img.get_rect(502, 393)

apply_settings_changes_img = Image("sprites/apply_settings_changes.png")
apply_settings_changes_rect = apply_settings_changes_img.get_rect(502, 393)

settings_changes = False

apply_changes_text = Text('Apply', 'edosz.ttf', (255, 255, 255), 30, 502, 373, 255, True)
apply_changes_text_2 = Text('Changes', 'edosz.ttf', (255, 255, 255), 30, 502, 405, 255, True)

# Buttons and Other Variables During the Game Session

restart_level_img = ImageButton("sprites/restart_button.png")
restart_level_rect = restart_level_img.get_rect(620, 128)

validate_button_img = ImageButton("sprites/validate_button.png")
validate_button_rect = validate_button_img.get_rect(620, 228)

solution_button_img = ImageButton("sprites/solution_button.png")
solution_button_rect = solution_button_img.get_rect(620, 328)

exit_button_img = ImageButton("sprites/exit_button.png")
exit_button_rect = exit_button_img.get_rect(620, 522)

start_time = 0
elapsed_time = 0

current_level = 0

bg_music = Music("beneath_the_mask")
bg_music.setVolume()
music_channel = None

bg_music2 = Music("alleycat")
bg_music2.setVolume()
music_channel2 = None
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                            current_level = i + 1
                            level_select_active = False
                            game_active = True
                            updated_board(i + 1, digits_matrix)
                            start_time = int(pygame.time.get_ticks() / 1000)
                if cross_button_rect.collidepoint(event.pos) and settings_active is True:
                    settings_active = False
                    button_disabled = False
                if check_boxes_rects[0].collidepoint(event.pos) and settings_active is True:
                    if background_music_played:
                        background_music_played = False
                    else:
                        background_music_played = True
                    settings_changes = True
                if check_boxes_rects[1].collidepoint(event.pos) and settings_active is True:
                    if background_transitions_shown:
                        background_transitions_shown = False
                    else:
                        background_transitions_shown = True
                    settings_changes = True
                if apply_settings_changes_rect.collidepoint(event.pos) and settings_active is True:
                    print("Settings has been Saved")
                    settings_active = False
                    button_disabled = False
                    pass
            
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_level_rect.collidepoint(event.pos):
                    updated_board(current_level, digits_matrix)
                    white_square.reset_position(background.screen)
                    current_row = 1
                    current_column = 1
                
                if validate_button_rect.collidepoint(event.pos):
                    pass

                if solution_button_rect.collidepoint(event.pos):
                    pass

                if exit_button_rect.collidepoint(event.pos):
                    game_active = False
                    level_select_active = True
                    emptied_board(digits_matrix)
                    white_square.reset_position(background.screen)
                    current_row = 1
                    current_column = 1
    
    mouse = pygame.mouse.get_pos()
    background.render()
    
    if game_active is True:
        #if background_music_played and bg_music.music_started is False:
        if background_music_played:
            if current_level >= 1 and current_level <= 5 and bg_music.music_started is False:
                music_channel = bg_music.track.play(loops=-1)
                bg_music.music_started = True
            elif current_level >= 6 and current_level <= 9 and bg_music2.music_started is False:
                music_channel2 = bg_music2.track.play(loops=-1)
                bg_music2.music_started = True

        if background_transitions_shown:
            background.levelselect_to_sudokuboard()
        
        initial_x_pos = 40
        initial_y_pos = 100
        current_time = display_time()
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

        expand_button(restart_level_img, mouse, restart_level_rect, restart_level_rect, 200, 60, 1.2)
        expand_button(validate_button_img, mouse, validate_button_rect, validate_button_rect, 200, 60, 1.2)
        expand_button(solution_button_img, mouse, solution_button_rect, solution_button_rect, 200, 60, 1.2)
        expand_button(exit_button_img, mouse, exit_button_rect, exit_button_rect, 200, 60, 1.2)
        
        #settings_img.display(background.screen)

        restart_level_img.display(background.screen)
        validate_button_img.display(background.screen)
        solution_button_img.display(background.screen)
        exit_button_img.display(background.screen)

    elif level_select_active is True:  
        
        if music_channel is not None:
            music_channel.stop()
            bg_music.music_started = False
        
        if music_channel2 is not None:
            music_channel2.stop()
            bg_music2.music_started = False
        
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
            expand_button(level_buttons[i], mouse, level_buttons_rects[i], level_buttons_rects[i], 50, 50, 1.5)
        
        expand_button(settings_img, mouse, settings_img_rect, settings_img_rect, 50, 50, 1.5)
        expand_button(cross_button, mouse, cross_button_rect, cross_button_rect, 24, 24, 1.5)
        
        if settings_active:
            settings_tab.display(background.screen)
            cross_button.display(background.screen)
            check_boxes[0].display(background.screen)
            check_boxes[1].display(background.screen)

            if background_music_played and settings_active is True:
                ticks[0].display(background.screen)
                
            if background_transitions_shown and settings_active is True:
                ticks[1].display(background.screen)
            if settings_changes:
                apply_settings_changes_img.display(background.screen)
                apply_changes_text.change_text("Apply", (0, 0, 0))
                apply_changes_text_2.change_text("Changes", (0, 0, 0))
                no_of_changes += 1
            else: 
                apply_settings_default_img.display(background.screen)
                apply_changes_text.change_text("Apply", (255, 255, 255))
                apply_changes_text_2.change_text("Changes", (255, 255, 255))
                no_of_changes -= 1
            
            apply_changes_text.display(background.screen)
            apply_changes_text_2.display(background.screen)
        else:
            settings_changes = False
            no_of_changes = 0

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

