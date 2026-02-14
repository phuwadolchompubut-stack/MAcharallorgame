import pygame
import sys
import random

pygame.init()

# -----------------------
# ตั้งค่าหน้าจอ
# -----------------------
WIDTH = 576
HEIGHT = 1024
FLOOR = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MaChaAlhor")

icon = pygame.image.load("iconplane.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# -----------------------
# โหลดภาพ (กำหนดขนาดเอง)
# -----------------------
bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

plane_img = pygame.image.load("plane.png").convert_alpha()
plane_img = pygame.transform.scale(plane_img, (80, 60))  # ขนาดคงที่
plane_rect = plane_img.get_rect(center=(120, 400))

pipe_img = pygame.image.load("base.png").convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (100, 600))  # ขนาดท่อคงที่

# -----------------------
# ตัวแปรเกม
# -----------------------
gravity = 0.5
plane_movement = 0
game_active = True
score = 0
pipe_list = []

# -----------------------
# สร้างท่อ
# -----------------------
def create_pipe():
    height = random.randint(300, 700)
    bottom = pipe_img.get_rect(midtop=(WIDTH + 100, height))
    top = pipe_img.get_rect(midbottom=(WIDTH + 100, height - 250))
    return bottom, top

# -----------------------
# วาดท่อ
# -----------------------
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= FLOOR:
            screen.blit(pipe_img, pipe)
        else:
            flipped = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped, pipe)

# -----------------------
# เคลื่อนท่อ
# -----------------------
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > -50]

# -----------------------
# ตรวจชน (แก้ให้ปลอดภัย)
# -----------------------
def check_collision(pipes):
    for pipe in pipes:
        if plane_rect.colliderect(pipe):
            return False

    if plane_rect.top <= 0:
        return False

    if plane_rect.bottom >= FLOOR:
        return False

    return True

# -----------------------
# แสดงคะแนน
# -----------------------
def show_score():
    text = font.render(f"Score: {int(score)}", True, (255,255,255))
    screen.blit(text, (WIDTH//2 - 80, 50))

# -----------------------
# ตั้งเวลา spawn ท่อ
# -----------------------
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# -----------------------
# GAME LOOP
# -----------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                plane_movement = -10

            if event.key == pygame.K_SPACE and not game_active:
                # รีเซ็ตเกม
                game_active = True
                pipe_list.clear()
                plane_rect.center = (120, 400)
                plane_movement = 0
                score = 0

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    screen.blit(bg, (0,0))

    if game_active:

        # Gravity
        plane_movement += gravity
        plane_rect.centery += plane_movement
        screen.blit(plane_img, plane_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)

        score += 0.01
        show_score()

    else:
        over = font.render("GAME OVER", True, (255,0,0))
        screen.blit(over, (WIDTH//2 - 150, HEIGHT//2))

    pygame.display.update()
    clock.tick(60)
