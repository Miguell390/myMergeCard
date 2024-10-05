import pygame
import random
# YUNCHE
import sys
import os
import xml.etree.ElementTree as ET

pygame.init()

# set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Target Number Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# do fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

# set game variables
rounds = 3
current_round = 1
target_number = random.randint(80, 120)
choices = []
win_message = ""
ticks = []  # To track wins for each round
selected_choice = None
game_over = False  # New variable for game over state

# to evaluate an arithmetic expression from a string
def evaluate_expression(expression):
    try:
        return eval(expression)
    except:
        return None

# to generate four multiple-choice options
def generate_choices(target):
    # List of random incorrect choices
    incorrect_choices = []
    while len(incorrect_choices) < 3:
        expr = f"{random.randint(70, 150)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)}"
        result = evaluate_expression(expr)
        if result != target and result not in incorrect_choices:  # Ensure unique and incorrect answers
            incorrect_choices.append((expr, result))
    
    # Insert the correct choice randomly
    correct_expr = f"{random.randint(70, 150)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)}"
    while evaluate_expression(correct_expr) != target:
        correct_expr = f"{random.randint(70, 150)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)} {random.choice(['+', '-', '*'])} {random.randint(1, 50)}"
    
    choices_list = incorrect_choices + [(correct_expr, target)]
    random.shuffle(choices_list)
    
    return choices_list

#  to draw the ticks on the screen based on won rounds
def draw_ticks():
    for i in range(len(ticks)):
        if ticks[i]:  # Draw a tick only for rounds won
            tick_x = 20 + i * 30  # Space the ticks horizontally
            pygame.draw.line(screen, GREEN, (tick_x, 20), (tick_x + 20, 40), 5)
            pygame.draw.line(screen, GREEN, (tick_x + 20, 40), (tick_x + 40, 10), 5)

#  to check if the mouse click is on a choice
def check_choice_click(pos):
    for i, choice in enumerate(choices):
        x, y = 20, 160 + i * 50
        if x <= pos[0] <= x + 500 and y <= pos[1] <= y + 40:
            return i
    return None

# to reset for the next round
def reset_round():
    global target_number, choices, win_message, selected_choice
    target_number = random.randint(80, 120)
    choices = generate_choices(target_number)
    win_message = ""
    selected_choice = None

# to draw the "Next Game" button when the game is over
def draw_next_game_button():
    button_text = font.render("Next Game", True, WHITE)
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(button_text, (WIDTH//2 - 80, HEIGHT//2 - 15))
    return button_rect

# YUNCHE
def draw_text(screen, text, size, x, y):
    #font = pygame.font.Font('arial', size)
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)

# YUNCHE: let users to enter their names
def run_splash_screen(screen):
    size = (WIDTH, HEIGHT)
    pygame.display.update()
    input_box = pygame.Rect(WIDTH // 2 - 200 / 2, HEIGHT // 2, 200, 50)
    button_box = pygame.Rect(WIDTH // 2 - 100 / 2, HEIGHT * 3 // 4, 100, 50)
    username = ''
    active = False
    black = (0, 0, 0)
    gray = (128, 128, 128)
    while True:
        # clock.tick(cfg.fps)
        # get keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if button_box.collidepoint(event.pos):
                    print(f"Username: {username}")
                    return username
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(f"Username: {username}")
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
        # draw back ground
        bg = pygame.Surface((size))
        bg.fill((255, 255, 255))
        screen.blit(bg, (0,0))
        draw_text(screen, 'NumberCombat', 64, WIDTH // 2, HEIGHT // 4)

        # Draw input box
        pygame.draw.rect(screen, gray if active else black, input_box, 2)
        txt_surface = pygame.font.Font(None, 50).render(username, True, black)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)
        
        # Draw button
        pygame.draw.rect(screen, gray, button_box)
        draw_text(screen, "Submit", 32, button_box.centerx, button_box.topleft[1])
        
        pygame.display.flip()

# YUNCHE: update result to an xml file
def update_result(fname, user_name, lv0_total, lv0_correct):
    # Check if the file exists
    root = None
    if not os.path.exists(fname):
        # Create the root element
        root = ET.Element('users')
        tree = ET.ElementTree(root)
        tree.write(fname)
    else:
        # Parse the existing XML file
        tree = ET.parse(fname)
        root = tree.getroot()

    # Check if the user already exists
    user_exists = False
    for user in root.findall('user'):
        name = user.find('name').text
        if name == user_name:
            user_exists = True
            # Get existing values
            existing_lv0_total = int(user.find('lv0_total').text)
            existing_lv0_correct = int(user.find('lv0_correct').text)
            # Update if the new ratio is better
            if lv0_correct / lv0_total > existing_lv0_correct / existing_lv0_total:
                user.find('lv0_total').text = str(lv0_total)
                user.find('lv0_correct').text = str(lv0_correct)
            break

    # If the user does not exist, add a new user
    if not user_exists:
        new_user = ET.SubElement(root, 'user')
        ET.SubElement(new_user, 'name').text = user_name
        ET.SubElement(new_user, 'lv0_total').text = str(lv0_total)
        ET.SubElement(new_user, 'lv0_correct').text = str(lv0_correct)

    # Write the changes back to the file
    tree.write(fname)

# initialize the first round
choices = generate_choices(target_number)

# main game loop
running = True
is_login = True
username = ''
lv0_correct = 0
while running:
    screen.fill(WHITE)

    if is_login: # YUNCHE
        username = run_splash_screen(screen)
        is_login = username == ''
    elif game_over:
        # show the "Next Game" button when the game is over
        button_rect = draw_next_game_button()
    else:
        # draw round and target number
        round_text = font.render(f'Round {current_round} / {rounds}', True, BLACK)
        screen.blit(round_text, (20, 60))

        target_text = font.render(f'Target: {target_number}', True, BLACK)
        screen.blit(target_text, (20, 100))

        # draw the multiple-choice options
        for i, (expr, result) in enumerate(choices):
            color = GRAY if selected_choice == i else BLACK
            choice_text = small_font.render(f'{expr} = ?', True, color)
            screen.blit(choice_text, (20, 160 + i * 50))

        # get win message
        if win_message:
            win_text = font.render(win_message, True, BLACK)
            screen.blit(win_text, (20, 300))

        # draw ticks for rounds won
        draw_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = pygame.mouse.get_pos()

            if game_over:
                # check if the "Next Game" button is clicked
                if button_rect.collidepoint(pos):
                    # reset the game variables for the next game
                    current_round = 1
                    ticks = []
                    reset_round()
                    game_over = False  # Exit the game-over state
            else:
                # check if the player clicked a choice
                selected_choice = check_choice_click(pos)
                if selected_choice is not None:
                    expr, result = choices[selected_choice]
                    if result == target_number:
                        win_message = f"You win round {current_round}!"
                        ticks.append(True)  # add a tick for the current round
                        lv0_correct += 1    # YUNCHE: record winning count
                        #print(f'win cnt = {lv0_win_cnt}')
                    else:
                        win_message = "Try again!"
                        ticks.append(False)  # add no tick for the current round

                    if current_round < rounds:
                        current_round += 1
                        reset_round()
                    else:
                        game_over = True  # Game ends after the last round
                        update_result('record.xml', username, rounds, lv0_correct)

    
    pygame.display.update()

# Quit Pygame
pygame.quit()