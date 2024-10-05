import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Target Number Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

# Game variables
total_rounds = 0
correct_answers = 0
target_number = random.randint(80, 120)
choices = []
win_message = ""
selected_choice = None
game_over = False

# Timer variables
round_time_limit = 30000  # 30 seconds in milliseconds
start_time = pygame.time.get_ticks()
time_left = round_time_limit

# Function to evaluate an arithmetic expression from a string
def evaluate_expression(expression):
    try:
        return eval(expression)
    except:
        return None

# Function to generate four multiple-choice options
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

# Function to check if the mouse click is on a choice
def check_choice_click(pos):
    for i, choice in enumerate(choices):
        x, y = 20, 200 + i * 50
        if x <= pos[0] <= x + 500 and y <= pos[1] <= y + 40:
            return i
    return None

# Function to reset for the next round
def reset_round():
    global target_number, choices, win_message, selected_choice, start_time, time_left
    target_number = random.randint(80, 120)
    choices = generate_choices(target_number)
    win_message = ""
    selected_choice = None
    start_time = pygame.time.get_ticks()
    time_left = round_time_limit

# Function to draw the stop game button
def draw_stop_game_button():
    button_text = font.render("Stop Game", True, WHITE)
    button_rect = pygame.Rect(WIDTH - 140, 20, 120, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(button_text, (WIDTH - 130, 30))
    return button_rect

# Main game loop
running = True
reset_round()

while running:
    screen.fill(WHITE)

    # Calculate the time left for the current round
    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = round_time_limit - elapsed_time

    # If time runs out, automatically move to the next round
    if time_left <= 0:
        total_rounds += 1
        win_message = "Time's up! Moving to the next round."
        reset_round()

    # Draw target number and round information
    round_text = font.render(f'Rounds Played: {total_rounds}', True, BLACK)
    correct_text = font.render(f'Correct Answers: {correct_answers}', True, BLACK)
    screen.blit(round_text, (20, 60))
    screen.blit(correct_text, (20, 100))

    target_text = font.render(f'Target: {target_number}', True, BLACK)
    screen.blit(target_text, (20, 140))

    # Draw the multiple-choice options
    for i, (expr, result) in enumerate(choices):
        color = GRAY if selected_choice == i else BLACK
        choice_text = small_font.render(f'{expr} = ?', True, color)
        screen.blit(choice_text, (20, 200 + i * 50))

    # Display win message
    if win_message:
        win_text = font.render(win_message, True, BLACK)
        screen.blit(win_text, (20, 300))

    # Draw the stop game button
    stop_game_button_rect = draw_stop_game_button()

    # Draw the timer
    timer_text = font.render(f'Time Left: {time_left // 1000} seconds', True, RED)
    screen.blit(timer_text, (20, 20))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = pygame.mouse.get_pos()

            # Check if the stop game button is clicked
            if stop_game_button_rect.collidepoint(pos):
                win_message = f'Game over! You won {correct_answers} out of {total_rounds} rounds.'
                running = False  # End the game

            # Check if the player clicked a choice
            selected_choice = check_choice_click(pos)
            if selected_choice is not None:
                expr, result = choices[selected_choice]
                if result == target_number:
                    win_message = "Correct!"
                    correct_answers += 1
                else:
                    win_message = "Incorrect!"
                total_rounds += 1
                reset_round()

    pygame.display.update()

# Quit Pygame
pygame.quit()
