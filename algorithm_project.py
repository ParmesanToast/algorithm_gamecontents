import pygame #파이 게임 모듈 임포트
import random

#화면정의
pygame.init() #파이 게임 초기화
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AVOIDING BOMBS")
# 기본 변수
STAGE = 1
CAR_COUNT = 5
SCORE = 0
DIFFICULTY = 0
LIFE = 5
# 색 정의
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# 사운드 정의
pygame.mixer.init() # 효과음 초기화
pygame.mixer.pre_init(44100,-16,2,512) # 버퍼 설정
bomb_sound = pygame.mixer.Sound('bomb.wav')
stage_sound = pygame.mixer.Sound('stage.wav')
heart_sound = pygame.mixer.Sound('heart.wav')
# 이미지 정의
bomb_image = pygame.image.load('bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (50, 50))
bombs = []

heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (50, 50))
hearts = []

def score_screen():
    font_01 = pygame.font.SysFont("FixedSsy", 70, True, False)
    text_score = font_01.render("Score : " + str(SCORE) , True, WHITE)
    SCREEN.blit(text_score, [120, 360])
    pygame.mixer.stop()
def win_screen():
    screen.fill(WHITE)
    font_01 = pygame.font.SysFont("FixedSsy", 120, True, False)
    text_score = font_01.render("You Win ", True, RED)
    SCREEN.blit(text_score, [115, 240])
    score_screen()
def lose_screen():
    screen.fill(BLACK)
    font_01 = pygame.font.SysFont("FixedSsy", 120, True, False)
    text_score = font_01.render("You Lose ", True, WHITE)
    SCREEN.blit(text_score, [80, 240])
    score_screen()
def draw_score():
    # SCORE 기록
    font_01 = pygame.font.SysFont("FixedSsy", 30, True, False)
    text_score = font_01.render("Score : " + str(SCORE), True, WHITE)
    SCREEN.blit(text_score, [15, 25])

    # STAGE 기록
    text_stage = font_01.render("STAGE : " + str(STAGE), True, YELLOW)
    # 화면 가운데 위치
    text_stage_rect = text_stage.get_rect()
    text_stage_rect.centerx = round(SCREEN_WIDTH / 2)
    SCREEN.blit(text_stage, [text_stage_rect.x, 25])

    # 플레이어 Life 기록
    for i in range(LIFE):
        text_LIFE = font_01.render("Life : " + str(LIFE), True, RED)
        text_LIFE_x = SCREEN_WIDTH - 100
        SCREEN.blit(text_LIFE, [text_LIFE_x, 25])

for i in range(5 + DIFFICULTY):
    rect = pygame.Rect(bomb_image.get_rect())
    rect.left = random.randint(0, SCREEN_WIDTH)
    rect.top = -100
    dy = random.randint(1, 5) + DIFFICULTY
    bombs.append({'rect': rect, 'dy': dy})

for i in range(3):
    rect2 = pygame.Rect(heart_image.get_rect())
    rect2.left = random.randint(0, SCREEN_WIDTH)
    rect2.top = -100
    dy = random.randint(1, 8)
    hearts.append({'rect2': rect2, 'dy': dy})

person_image = pygame.image.load('person.png')
person_image= pygame.transform.scale(person_image, (100, 100))
person = pygame.Rect(person_image.get_rect())
person.left = SCREEN_WIDTH // 2 - person.width // 2
person.top = SCREEN_HEIGHT - person.height
person_dx = 0
person_dy = 0

done = False
# global done
while not done: #게임 루프
    pygame.display.update()
    screen.fill(GRAY) #단색으로 채워 화면 지우기
    draw_score() # 점수 표시
    event = pygame.event.poll() #이벤트 처리
    if SCORE == 10000:
        STAGE = 1
        DIFFICULTY = 4
    elif SCORE == 20000:
        STAGE = 2
        DIFFICULTY = 6
        stage_sound.play()
    elif SCORE == 30000:
        STAGE = 3
        DIFFICULTY = 7
        stage_sound.play()
    elif SCORE == 40000:
        STAGE = 4
        DIFFICULTY = 8
        stage_sound.play()
    elif SCORE == 50000:
        STAGE = 5
        DIFFICULTY = 9
        stage_sound.play()
    elif SCORE == 60000:
        STAGE = 6
        DIFFICULTY = 10
        stage_sound.play()
    elif SCORE == 70000:
        STAGE = 7
        DIFFICULTY = 11
        stage_sound.play()
    elif SCORE >= 80000:
        win_screen()


    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            person_dx = -5
        elif event.key == pygame.K_RIGHT:
            person_dx = 5
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            person_dx = 0
        elif event.key == pygame.K_RIGHT:
            person_dx = 0

    for bomb in bombs:
        bomb['rect'].top += bomb['dy']
        if bomb['rect'].top > SCREEN_HEIGHT:
            bombs.remove(bomb)
            rect = pygame.Rect(bomb_image.get_rect())
            rect.left = random.randint(0, SCREEN_WIDTH)
            rect.top = -100
            dy = random.randint(1, 5) + DIFFICULTY
            bombs.append({'rect': rect, 'dy': dy})
        if SCORE >= 80000:
            break

    for heart in hearts:
        heart['rect2'].top += heart['dy']
        if heart['rect2'].top > SCREEN_HEIGHT:
            hearts.remove(heart)
            rect2 = pygame.Rect(heart_image.get_rect())
            rect2.left = random.randint(0, SCREEN_WIDTH)
            rect2.top = -100
            dy = random.randint(1, 8)
            hearts.append({'rect2': rect2, 'dy': dy})

    person.left = person.left + person_dx

    if person.left < 0:
        person.left = 0
    elif person.left > SCREEN_WIDTH - person.width:
        person.left = SCREEN_WIDTH - person.width



    for bomb in bombs: # 폭탄이 플레이어 접촉시
        if bomb['rect'].colliderect(person):
            bomb_sound.play() # 효과음 재생
            LIFE = LIFE -1 # 플레이어 체력감소
            bomb['rect'].top += 1000 # 충돌한 폭탄 사라짐
            SCORE -= 3000
            print(LIFE)
        if LIFE <= 0: # 체력이 0이 되면 게임종료
            lose_screen()
            break
        elif SCORE <= -1:
            lose_screen()
            break
        elif SCORE >= 80000:
            person.top += 100000
            break
        else:
            SCORE += 10
        screen.blit(bomb_image, bomb['rect'])

    for heart in hearts:  # 체력이 플레이어 접촉시
        if heart['rect2'].colliderect(person):
            heart_sound.play()  # 효과음 재생
            heart['rect2'].top += 1000  # 충돌한 체력 사라짐
            if LIFE <= 4: # 최대체력은 10까지
                LIFE = LIFE + 1  # 플레이어 체력증가
                print(LIFE)
        if LIFE <= 0:
            person.top += 100000
            break
        elif SCORE <= 0:
            person.top += 100000
            break
        elif SCORE >= 80000:
            person.top += 100000
            break

        screen.blit(heart_image, heart['rect2'])

    screen.blit(person_image, person)
    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값