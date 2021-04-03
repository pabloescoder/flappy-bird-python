import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, screen_height - (infoObject.current_h // 10)))
    screen.blit(floor_surface, (floor_x_pos + screen_width, screen_height - (infoObject.current_h // 10)))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(screen_width * (6 / 5), random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(screen_width * (6 / 5), random_pipe_pos - (screen_height // 100) * 23))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height - (infoObject.current_h // 10):
        death_sound.play()
        can_score = True
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2.5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird = pygame.transform.scale(new_bird, (screen_width // 10, screen_height // 20))
    new_bird_rect = new_bird.get_rect(center=(screen_width // 10, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'playing':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 20))
        screen.blit(score_surface, score_rect)

    if game_state == 'over':
        score_surface = game_font.render("Score = {}".format(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 20))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("Highscore = {}".format(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(screen_width // 2, screen_height // 1.2))
        screen.blit(high_score_surface, high_score_rect)
        screen.blit(game_over_screen, game_over_rect)


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if (screen_width // 10) - 1 < pipe.centerx < (screen_width // 10) + 1 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()
infoObject = pygame.display.Info()
screen_width = infoObject.current_w // 3
screen_height = infoObject.current_h - 50
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.TTF', 40)
game_over_screen = pygame.image.load('assets/message.png').convert_alpha()
game_over_screen = pygame.transform.scale(game_over_screen, (screen_width // 2, screen_height // 2))
game_over_rect = game_over_screen.get_rect(center=(screen_width // 2, screen_height // 2))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# Game Variables
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (screen_width, screen_height))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (screen_width, screen_height // 5))
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = pygame.transform.scale(bird_frames[bird_index], (screen_width // 10, screen_height // 20))
bird_rect = bird_surface.get_rect(center=(screen_width // 10, screen_height // 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (screen_width // 6, screen_height))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height_bottom_half = [screen_height // (i / 10) for i in range(13, 16)]
pipe_height_top_half = [screen_height * (i / 10) for i in range(3, 8)]
pipe_height = pipe_height_bottom_half + pipe_height_top_half

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (screen_width // 10, screen_height // 2)
                bird_movement = -4
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            if len(pipe_list) >= 8:
                pipe_list.pop(0)
                pipe_list.pop(1)

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        if score > high_score:
            high_score = score
        score_display('playing')
    else:
        score_display('over')

    # Floor
    floor_x_pos -= 0.8
    draw_floor()
    if floor_x_pos < -screen_width:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
