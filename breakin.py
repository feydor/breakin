from dataclasses import dataclass
import sys, pygame

pygame.init()

WINDOW_HEIGHT = 640
WINDOW_WIDTH = 800
COLOR_BG = 0x24, 0x24, 0x24
BAR_BG = 0xFF, 0, 0
BAR_WIDTH = 150
BAR_HEIGHT = 50
PROJ_BG = 0, 0xFF, 00
PROJ_HEIGHT = BAR_HEIGHT
PROJ_WIDTH = PROJ_HEIGHT
BOUNCE_CONSTANT = 2
COLLISION_PADDING = 10
BAR_SPEED = 2
TARGET_BG = 0, 0, 0xFF
TARGET_WIDTH = 100
TARGET_HEIGHT = 50
TARGET_PADDING = 25

# x,y = left,top
bar_x = WINDOW_WIDTH/2 - BAR_WIDTH/2
bar_y = WINDOW_HEIGHT - 3*BAR_HEIGHT
bar_dx = 2
bar_dy = 1
proj_x = WINDOW_WIDTH/2 - PROJ_HEIGHT/2
proj_y = WINDOW_HEIGHT - 3*BAR_HEIGHT - PROJ_HEIGHT
proj_dx = 1
proj_dy = 1

@dataclass
class Target:
    x: float
    y: float
    dead: bool = False
targets = [
    Target(x=100, y=100),
    Target(x=100 + TARGET_WIDTH + TARGET_PADDING, y=100),
    Target(x=100 + 2*(TARGET_WIDTH + TARGET_PADDING), y=100),
    Target(x=100 + 3*(TARGET_WIDTH + TARGET_PADDING), y=100),
    Target(x=100 + 4*(TARGET_WIDTH + TARGET_PADDING), y=100),
]

paused = True
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def clamp(val, lower_bound, upper_bound):
    return max(lower_bound, min(val, upper_bound))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                paused = False
                bar_dx = BAR_SPEED
            if event.key == pygame.K_a:
                paused = False
                bar_dx = -BAR_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                bar_dx = 0
    
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        paused = True
    if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]:
        bar_dx = 0

    if not paused:
        nproj_x = proj_x + proj_dx
        nproj_y = proj_y + proj_dy

        # collison detection of projectile
        if nproj_x < 0 or nproj_x > WINDOW_WIDTH - PROJ_WIDTH:
            nproj_x = proj_x - proj_dx
            proj_dx *= -1
        if proj_y < 0 or proj_y > WINDOW_HEIGHT - PROJ_HEIGHT:
            nproj_y = proj_y - proj_dy
            proj_dy *= -1

        # check proj collision with bar
        bar_rect = pygame.Rect(bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT);
        nproj_rect = pygame.Rect(nproj_x, nproj_y, PROJ_WIDTH, PROJ_HEIGHT);
        if nproj_rect.colliderect(bar_rect):
            # from right
            if nproj_x < bar_x + BAR_WIDTH and nproj_x + PROJ_WIDTH > bar_x + BAR_WIDTH:
                nproj_x += COLLISION_PADDING
                proj_dx = BOUNCE_CONSTANT
            #from left
            elif nproj_x < bar_x + BAR_WIDTH and nproj_x + PROJ_WIDTH < bar_x + BAR_WIDTH:
                nproj_x -= COLLISION_PADDING
                proj_dx = -BOUNCE_CONSTANT
            
            # influence projectile refraction with bar
            if bar_dx > 0:
                proj_dx = BOUNCE_CONSTANT
            elif bar_dx < 0:
                proj_dx = -BOUNCE_CONSTANT

            proj_dy *= -1
        
        for target in targets:
            if not target.dead:
                target_rect = pygame.Rect(target.x, target.y, TARGET_WIDTH, TARGET_HEIGHT)
                if nproj_rect.colliderect(target_rect):
                    proj_dy *= -1
                    target.dead = True
                    break

        proj_x = nproj_x
        proj_y = nproj_y
        bar_x = clamp(bar_x + bar_dx, 0, WINDOW_WIDTH - BAR_WIDTH)

    window.fill(COLOR_BG)
    pygame.draw.rect(window, BAR_BG, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(window, PROJ_BG, (proj_x, proj_y, PROJ_WIDTH, PROJ_HEIGHT))
    for target in targets:
        if not target.dead:
            pygame.draw.rect(window, TARGET_BG, (target.x, target.y, TARGET_WIDTH, TARGET_HEIGHT))
    pygame.display.flip()