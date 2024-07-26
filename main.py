import pygame,sys,os
from random import random
os.chdir(r'C:\Users\91861\Documents\coding\python\flappy bird game\sprites')
from pygame.constants import USEREVENT
pygame.mixer.pre_init(frequency=44100,size=8,channels=1,buffer=256)
pygame.init()

def draw_floor():
    screen.blit(fl_surface,(fl_x_pos,450))
    screen.blit(fl_surface,(fl_x_pos+288,450))

def create_pipe():
    random_pipe_pos = 200+random()*200
    bottom_pipe = pipe_surface.get_rect(midtop=(400,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400,random_pipe_pos-150))
    return top_pipe,bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sd.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        death_sd.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bd_move*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_surf = new_bird.get_rect(center=(57.6,bird_rect.centery))
    return new_bird,new_surf

def display_score(state):
    if state == 'main game':
        sc_surf = game_font.render(str(int(score)),True,(255,255,255))
        sc_rect = sc_surf.get_rect(center=(144,50))
        screen.blit(sc_surf,sc_rect)
    if state == 'game over':
        sc_surf = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        sc_rect = sc_surf.get_rect(midtop=(144,10))
        screen.blit(sc_surf,sc_rect)

        sc_surf = game_font.render(f'Best: {int(high_score)}',True,(255,255,255))
        sc_rect = sc_surf.get_rect(midbottom=(144,440))
        screen.blit(sc_surf,sc_rect)

def update_score(score,high):
    if score > high:
        high = score
    return high

def check_score(pipes):
    global score,pipe_index
    for pipe in pipes:
        if bird_rect.left == pipe.right:
            score_sd.play()
            score += 0.5
            pipe_index += 1
fl_x_pos = 0
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('background-day.png').convert()
fl_surface = pygame.image.load('base.png').convert()
pipe_surface = pygame.image.load('pipe-green.png').convert()
pipe_list = []

game_font = pygame.font.Font('04B_19.ttf',22)
score = 0
high_score = 0

# message
mess_surf = pygame.image.load('message.png').convert_alpha()
mess_rect = mess_surf.get_rect(center=(144,256))

# bird_surface = pygame.image.load('redbird-midflap.png').convert_alpha( )
# bird_rect = bird_surface.get_rect(center=(57.6,256))

# bird
bird_up = pygame.image.load('redbird-upflap.png').convert_alpha()
bird_mid = pygame.image.load('redbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('redbird-downflap.png').convert_alpha()
bird_frames = [bird_up,bird_mid,bird_down]
bird_index = 1
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(57.6,200))

# user events
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(FLAP,200)

# sounds
flap_sd = pygame.mixer.Sound('sfx_wing.wav')
death_sd = pygame.mixer.Sound('sfx_hit.wav')
score_sd = pygame.mixer.Sound('sfx_point.wav')
pipe_index = 1
bd_move = 0
g = 0.25
game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (57.6,200)
                bd_move = 0
                score = 0
            elif event.key == pygame.K_SPACE and game_active:
                bd_move = 0
                bd_move -= 6
                flap_sd.play()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()
    screen.blit(bg_surface,(0,0))
    if game_active:
        # bird
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bd_move
        screen.blit(rotated_bird,bird_rect)
        bd_move += g
        # if pipe_list and bird_rect.bottom >= pipe_list[pipe_index].top-20:
        #     flap_sd.play()
        #     bd_move = 0
        #     bd_move -= 6

        # pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipe(pipe_list)
        # if len(pipe_list) >= 10:
        #     pipe_list.pop(0)
        game_active = check_collision(pipe_list)
        check_score(pipe_list)
        display_score('main game')
    else:
        screen.blit(mess_surf,mess_rect)
        high_score = update_score(score,high_score)
        display_score('game over')

    # floor
    draw_floor()
    fl_x_pos -= 1
    if fl_x_pos <= -288:
        fl_x_pos = 0
    pygame.display.update()
    clock.tick(120)