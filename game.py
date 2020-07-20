import pygame
import sys
import os
import random

# Setting game window in the middle of the screen(optional)
x = 600
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


# To display consecutive floor surface
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 703))
    screen.blit(floor_surface, (floor_x_pos + 450, 703))


# Creation of pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (490, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (490, random_pipe_pos - 210))
    return bottom_pipe, top_pipe


# To move pipes to the left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


# Drawing pipes on the screen
# One pipe is flipped and is added on top
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# To check collision of the bird with the top/bottom/pipes
def check_collision(pipes):
    global game_state
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            over_sound.play()
            game_state = "game_over"
            return False

    if bird_rect.top <= -79 or bird_rect.bottom >= 703:
        if bird_rect.bottom >= 703:
            fall_sound.play()
        game_state = "game_over"
        return False

    return True


# To rotate the bird in the direction it is going(up or down)
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# To provide the flapping effect by changing images
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (79, bird_rect.centery))
    return new_bird, new_bird_rect


# To display scores during start time/main game/game over
def score_display(game_state):
    if game_state == "start_score":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (225, 79))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(highscore)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center = (177, 660))
        screen.blit(high_score_surface, high_score_rect)

    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (225, 79))
        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (225, 79))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High Score: {int(highscore)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center = (177, 460))
        screen.blit(high_score_surface, high_score_rect)
        restart = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
        restart_rect = restart.get_rect(center = (227, 680))
        screen.blit(restart, restart_rect)

        
# To update the highscore if the current score is greater
def update_score(score, highscore):
    if score >= highscore:
        highscore = score
    return highscore


# Initialising pygame and pygame.mixer(for sounds)
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()


# Defining the default Screen Size, Font and Clock
pygame.display.set_icon(pygame.image.load("assets/favicon.ico"))
pygame.display.set_caption("FlapPy Bird")
screen = pygame.display.set_mode((450, 800))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)
restart_font = pygame.font.Font("04B_19.TTF", 36)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = False
game_state = "start_score"
score = 0
highscore = 0

# Background Image(Converted to double size to fit display)
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())


# Floor
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0


# Bird Modes
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 400))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


# Pipe
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png'))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = random.sample(range(250, 450), 20)


# Start and Game Over Screens
game_start_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center = (225, 370))
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (225, 370))


# Sound Files
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
over_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
fall_sound = pygame.mixer.Sound("sound/sfx_die.wav")


# Game Loop
while True:
    for event in pygame.event.get():
        # If "cross" button presses then quit from game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Game event checking
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                score = 0
                pipe_list.clear()
                bird_movement = 0
                bird_rect.center = (79, 400)

        # Adding new pipes to pipe_list
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        # Changing bird wing position
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()


    screen.blit(bg_surface, (0, 0))

    # This is the Main Game Screen
    if game_active:
        bird_mid = bird_rect.left + bird_rect.width / 2
        for pipe in pipe_list:
            pipe_mid = pipe.left + pipe.width / 2
            if pipe_mid <= bird_mid < pipe_mid + 4.5:
                score += 0.5
                if not isinstance(score, int):
                    score_sound.play()

        # Bird Movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score_display("main_game")

    # Showing Start Screen
    elif not game_active and game_state == "start_score":
        screen.blit(game_start_surface, game_start_rect)
        score_display("start_score")

    # Updating High Score if needed
    # Showing Game Over Screen
    # Press Space to Restart
    else:
        screen.blit(game_over_surface, game_over_rect)
        highscore = update_score(score, highscore)
        score_display("game_over")

    # Floor Movement
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -450:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
