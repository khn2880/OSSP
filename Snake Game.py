"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random

# 난이도 조절
# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# 창사이즈 조절
# Window size
frame_size_x = 720
frame_size_y = 480

# 에러 있는지 확인
# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# 기본창 설정
# Initialise game window
pygame.display.set_caption('Snake Eater') # 스크린 제목 표시
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# 창 색 설정
# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

# 주사율(초당 몇 번의 이미지를 나타내는지)
# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# 뱀, 먹이 등 기본 설정
# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

food2_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food2_spawn = True

food3_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food3_spawn = True

# 폭탄 블록 설치
bomb_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
bomb_spawn = True

# 장애물 블록 설치
barrier_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
barrier_spawn = True

barrier2_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
barrier2_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

# 게임 오버 시 설정
# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    show_time(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# 스코어 설정
# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/3, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# 시간 추가
def show_time(choice, color, font, size):
    time = pygame.time.get_ticks() // 1000
    time_font = pygame.font.SysFont(font, size)
    time_surface = time_font.render('TIME : ' + str(time) + 's', True, color)
    time_rect = time_surface.get_rect()
    if choice == 1:
        time_rect.midtop = (frame_size_x / 3, 15)
    else:
        time_rect.midtop = (frame_size_x/1.5, frame_size_y/1.25)
    game_window.blit(time_surface, time_rect)

# 기본 게임 설정
# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    elif snake_pos[0] == food2_pos[0] and snake_pos[1] == food2_pos[1]:
        score += 1
        food2_spawn = False
    elif snake_pos[0] == food3_pos[0] and snake_pos[1] == food3_pos[1]:
        score += 1
        food3_spawn = False
    else:
        snake_body.pop()

    # 장애물에 부딪히면 1점 감점 & 뱀의 몸 길이가 1 줄어듦
    if snake_pos[0] == barrier_pos[0] and snake_pos[1] == barrier_pos[1]:
        score -= 1
        snake_body.pop()
        barrier_spawn = False
        # 점수가 마이너스이면 게임종료
        if score < 0:
            game_over()

    if snake_pos[0] == barrier2_pos[0] and snake_pos[1] == barrier2_pos[1]:
        score -= 1
        snake_body.pop()
        barrier2_spawn = False
        # 점수가 마이너스이면 게임종료
        if score < 0:
            game_over()

    # 3초가 지나면 폭탄 이동
    ttime = pygame.time.get_ticks() / 1000
    tttime = int(ttime % 3)
    if tttime == 0:
        bomb_spawn = False
    else:
        if not bomb_spawn:
            bomb_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        bomb_spawn = True


    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    if not food2_spawn:
        food2_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food2_spawn = True
    if not food3_spawn:
        food3_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food3_spawn = True
    if not barrier_spawn:
        barrier_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    barrier_spawn = True
    if not barrier2_spawn:
        barrier2_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    barrier2_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food2_pos[0], food2_pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food3_pos[0], food3_pos[1], 10, 10))

    pygame.draw.rect(game_window, red, pygame.Rect(bomb_pos[0], bomb_pos[1], 10, 10))

    pygame.draw.rect(game_window, yellow, pygame.Rect(barrier_pos[0], barrier_pos[1], 10, 10))

    pygame.draw.rect(game_window, yellow, pygame.Rect(barrier2_pos[0], barrier2_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()

    # 폭탄에 닿으면 게임오버 설정
    if snake_pos[0] == bomb_pos[0] and snake_pos[1] == bomb_pos[1]:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    show_time(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)