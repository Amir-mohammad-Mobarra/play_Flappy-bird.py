# libraries
import pygame
import random
import time

# start pygame modules
pygame.init()

# variables -----
screen_width, screen_height = 576, 700
status = True
x_y_bird_rect = (100, 288)
bird_movement = 0
gravity = 0.25
speed = 90
pipe_list = []
floor_x = 0
game_status = True
bird_list_index = 0
x_y_score_true = (300, 50)
score = 0
high_sore = 0
active_score = True
# user event variables
creat_pipe = pygame.USEREVENT
flap = pygame.USEREVENT + 1
reset_game_show = pygame.USEREVENT + 2
pygame.time.set_timer(creat_pipe, 1200)
pygame.time.set_timer(flap, 100)
pygame.time.set_timer(reset_game_show, 15)
# font variable
game_font = pygame.font.Font('assets/font/Flappy.TTF', 40)


# functions
# move the floor image
def check_floor_x():
    global floor_x
    if floor_x == -576:
        floor_x = 0
    floor_x -= 3


# apply the gravity
def apply_gravity():
    global bird_movement, bird_image_rect
    bird_movement += gravity
    bird_image_rect.centery += bird_movement


# move the bird image rect
def move_bird():
    global bird_movement
    bird_movement = 0
    bird_movement -= 8
    bird_image_rect.centery += bird_movement


# creat x-y the top pipes and the bottom pipes
def generate_pipes_rects():
    r_pipe = random.randrange(270, 550)
    top_pipes_rects = pipe_image.get_rect(midbottom=(700, r_pipe - 250))
    bottom_pipes_rects = pipe_image.get_rect(midtop=(700, r_pipe))
    return top_pipes_rects, bottom_pipes_rects


# move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


# blit the pipes
def blit_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_image, pipe)
        else:
            screen.blit(pygame.transform.flip(pipe_image, flip_x=False, flip_y=True), pipe)


# check collisions
def check_collision(pipes):
    global game_status, active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            active_score = True
            game_over_sound.play()
            time.sleep(3)
            return False
        if bird_image_rect.top <= 0 or bird_image_rect.bottom >= 600:
            active_score = True
            game_over_sound.play()
            time.sleep(3)
            return False
    return True


# reset the game
def reset_game():
    global game_status, pipe_list, bird_image_rect, bird_movement, score
    game_status = True
    pipe_list.clear()
    bird_image_rect.center = x_y_bird_rect
    bird_movement = 0
    score = 0
    # one move bird
    move_bird()


# show the birds images
def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(x_y_bird_rect[0], bird_image_rect.centery))
    return new_bird, new_bird_rect


# show the score and the show score with the high score
def show_score(status_of_game):
    color_score = (255, 255, 255)
    bold = True
    if status_of_game:
        # score
        score_text = game_font.render(f'{score}', bold, color_score)
        score_text_rect = score_text.get_rect(center=x_y_score_true)
        screen.blit(score_text, score_text_rect)
    else:
        # score
        score_text = game_font.render(f'Score: {score}', bold, color_score)
        score_text_rect = score_text.get_rect(center=(200, 200))
        screen.blit(score_text, score_text_rect)
        # high score
        high_score_text = game_font.render(f'High Score: {high_sore}', bold, color_score)
        high_score_text_rect = score_text.get_rect(center=(200, 350))
        screen.blit(high_score_text, high_score_text_rect)


# add score
def update_score():
    global score, high_sore, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                score += 1
                take_sound.play()
                active_score = False
            if pipe.centerx < 0:
                active_score = True
    if score > high_sore:
        high_sore = score
    return high_sore


# show text game over
def game_over():
    game_over_text = game_font.render('game over', True, 'red')
    game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, 70))
    screen.blit(game_over_text, game_over_text_rect)


# show text reset game
def show_reset_game():
    for_reset_text = game_font.render('for reset\nclick <r>', True, 'yellow')
    for_reset_text_rect = for_reset_text.get_rect(center=(300, 500))
    screen.blit(for_reset_text, for_reset_text_rect)


# load images and get rect for some they -----
# load background image
background_image = pygame.transform.scale(pygame.image.load('assets/img/bg2.png')
                                          , (screen_width, screen_height))
# load floor image
floor_image = pygame.transform.scale2x(pygame.image.load('assets/img/floor.png'))
# load bird images
bird_image_down = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_down_flap.png'))
bird_image_mid = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_mid_flap.png'))
bird_image_up = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_up_flap.png'))

bird_list = [bird_image_down, bird_image_mid, bird_image_up]

bird_image = bird_list[bird_list_index]
bird_image_rect = bird_image.get_rect(center=x_y_bird_rect)
# load pipe image
pipe_image = pygame.transform.scale2x(pygame.image.load('assets/img/pipe_green.png'))

# load sounds -----
# add score sound
take_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')
# game over sound
game_over_sound = pygame.mixer.Sound('assets/sound/smb_mario_die.wav')

# important modules of pygame library -----
# make screen
screen = pygame.display.set_mode((screen_width, screen_height))
# control speed of the game
clock = pygame.time.Clock()

# move the bird image rect
move_bird()

# while loop for run the game
while True:
    # blit background image
    screen.blit(background_image, (0, 0))

    # check events of the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # move the bird image rect and reset game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_bird()
            if event.key == pygame.K_r and not game_status:
                reset_game()

        # blit images ----- without background image
        # creat the pipes and move pipes with timer
        if event.type == creat_pipe:
            pipe_list.extend(generate_pipes_rects())

        # choose the bird index of the bird list and choose image and image rect for show flap the bird with timer
        if event.type == flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0
            bird_image, bird_image_rect = bird_animation()

        # show the text for reset the game with timer
        if event.type == reset_game_show and not game_status:
            show_reset_game()

    # check game status
    if game_status:
        # blit the floor image
        screen.blit(floor_image, (floor_x, 600))
        screen.blit(floor_image, (floor_x + 576, 600))
        check_floor_x()
        # check collisions
        game_status = check_collision(pipe_list)
        # blit the bird image
        screen.blit(bird_image, bird_image_rect)
        apply_gravity()
        # blit the pipe list
        pipe_list = move_pipes(pipe_list)
        blit_pipes(pipe_list)
        # update the score and the high score
        update_score()
        # show the score
        show_score(True)
    else:
        # show the score and the high score
        show_score(False)
        # blit the floor image
        screen.blit(floor_image, (floor_x, 600))
        screen.blit(floor_image, (floor_x + 576, 600))
        # move the floor image
        check_floor_x()
        game_over()

    # update the display of game
    pygame.display.update()

    # control the speed of the game
    clock.tick(speed)