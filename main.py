import pygame, sys, random

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
game_font = pygame.font.Font('flappy-bird.ttf', 40)


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f"{int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 30))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 30))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(70, bird_rect.centery))
    return new_bird, new_bird_rect


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

        if bird_rect.top <= -100 or bird_rect.bottom >= 650:
            hit_sound.play()
            return False
    return True


def draw_floor():
    screen.blit(bg_floor, (floor_x, 650))
    screen.blit(bg_floor, (floor_x + 672, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    new_pipe_top = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    new_pipe_bottom = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return new_pipe_top, new_pipe_bottom


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:
            screen.blit(pipe_surface, pipe)
        else:
            flipped = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped, pipe)


# Game Screen
screen = pygame.display.set_mode((576, 720))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Loading images
# Background
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 720))

# Floor
bg_floor = pygame.image.load("assets/base.png").convert()
bg_floor = pygame.transform.scale2x(bg_floor)
floor_x = 0

# Bird
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_uplap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_uplap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(70, 360))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipe
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300, 400, 500]

# Sounds
flap_sound=pygame.mixer.Sound("sounds/wing.wav")
hit_sound=pygame.mixer.Sound("sounds/hit.wav")
point_sound=pygame.mixer.Sound("sounds/point.wav")

# Game over
game_over_surface=pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect=game_over_surface.get_rect(center=(288,340))

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
score_sound_countdown=100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (70, 360)
                bird_movement = 0
                score=0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # Background
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display("main_game")
        score_sound_countdown-=1
        if score_sound_countdown<=0:
            point_sound.play()
            score_sound_countdown=100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score,high_score)
        score_display("game_over")

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -576:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
