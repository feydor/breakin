from dataclasses import dataclass
import sys, pygame
pygame.init()

WINDOW_HEIGHT = 640
WINDOW_WIDTH = 800
COLOR_BG = 0x24, 0x24, 0x24
BAR_BG = 0xa5, 0x42, 0x42
PROJ_BG = 0xF0, 0xC6, 0x74
TARGET_BG = 0xB9, 0xCA, 0x4A
BAR_WIDTH = 150
BAR_HEIGHT = 25
PROJ_HEIGHT = 30
PROJ_WIDTH = PROJ_HEIGHT
PROJ_SPEED = 120
BOUNCE_CONSTANT = 2
COLLISION_PADDING = 10
BAR_SPEED = 180
TARGET_WIDTH = 75
TARGET_HEIGHT = 25
TARGET_PADDING = 15
FPS = 60
DELTA_TIME_SEC = 1.0/FPS
BAR_Y = WINDOW_HEIGHT - 3*BAR_HEIGHT
TARGET_GROUP_LEFT = 100
TARGET_GROUP_TOP = 75

# x,y = left,top
bar_x = WINDOW_WIDTH/2 - BAR_WIDTH/2
bar_dx = 0
bar_dy = 0
proj_x = WINDOW_WIDTH/2 - PROJ_HEIGHT/2
proj_y = WINDOW_HEIGHT - 3*BAR_HEIGHT - PROJ_HEIGHT
proj_dx = 0
proj_dy = -1
paused = True
started = False
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

@dataclass
class Target:
    x: float
    y: float
    dead: bool = False

targets = []

TARGETS_PER_ROW = 7
NROWS = 4
for i in range(0, NROWS):
    for j in range(0, TARGETS_PER_ROW):
        targets.append(Target(x=TARGET_GROUP_LEFT + j*(TARGET_WIDTH + TARGET_PADDING), y=TARGET_GROUP_TOP + i*(TARGET_HEIGHT + TARGET_PADDING)))

def bar_rect(x):
    global BAR_Y
    return pygame.Rect(x, BAR_Y, BAR_WIDTH, BAR_HEIGHT)

def proj_rect(x, y):
    return pygame.Rect(x, y, PROJ_WIDTH, PROJ_HEIGHT)

def target_rect(x, y):
    return pygame.Rect(x, y, TARGET_WIDTH, TARGET_HEIGHT)

def overlap(r1, r2):
    return r1.colliderect(r2)

def bar_collision(dt):
    global bar_x
    bar_nx = clamp(bar_x + bar_dx*BAR_SPEED*dt, 0, WINDOW_WIDTH - BAR_WIDTH)
    if (overlap(bar_rect(bar_nx), proj_rect(proj_x, proj_y))):
        return
    bar_x = bar_nx

def horiz_collision(dt):
    global bar_x
    global proj_x
    global proj_dx
    proj_nx = proj_x + proj_dx*PROJ_SPEED*dt
    if proj_nx < 0 or proj_nx + PROJ_WIDTH > WINDOW_WIDTH or overlap(proj_rect(proj_nx, proj_y), bar_rect(bar_x)):
        proj_dx *= -1
        return

    for target in targets:
        if not target.dead:
            if overlap(proj_rect(proj_nx, proj_y), target_rect(target.x, target.y)):
                target.dead = True
                proj_dx *= -1
                return
    proj_x = proj_nx
    return None

def vert_collision(dt):
    global bar_x
    global proj_y
    global proj_dy
    global proj_dx
    proj_ny = proj_y + proj_dy*PROJ_SPEED*dt
    if proj_ny < 0 or proj_ny + PROJ_HEIGHT > WINDOW_HEIGHT or overlap(proj_rect(proj_x, proj_ny), bar_rect(bar_x)):
        # bar DI
        if bar_dx > 0 and proj_dx < 0 or bar_dx < 0 and proj_dx > 0:
            proj_dx *= -1
        proj_dy *= -1
        return
    
    for target in targets:
        if not target.dead:
            if overlap(proj_rect(proj_x, proj_ny), target_rect(target.x, target.y)):
                target.dead = True
                proj_dy *= -1
                return
    proj_y = proj_ny
    return None

def update(dt):
    if not paused:
        bar_collision(dt)
        horiz_collision(dt)
        vert_collision(dt)

def render(window):
    window.fill(COLOR_BG)
    pygame.draw.rect(window, BAR_BG, bar_rect(bar_x))
    pygame.draw.rect(window, PROJ_BG, proj_rect(proj_x, proj_y))
    for target in targets:
        if not target.dead:
            pygame.draw.rect(window, TARGET_BG, (target.x, target.y, TARGET_WIDTH, TARGET_HEIGHT))
    pygame.display.flip()

def clamp(val, lower_bound, upper_bound):
    return max(lower_bound, min(val, upper_bound))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    bar_dx = 0
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        paused = True
    if pygame.key.get_pressed()[pygame.K_d]:
        bar_dx += 1
        if not started:
            started = True
            proj_dx = 1
        if paused:
            paused = False
    if pygame.key.get_pressed()[pygame.K_a]:
        bar_dx -= 1
        if not started:
            started = True
            proj_dx = -1
        if paused:
            paused = False

    
    update(DELTA_TIME_SEC)

    render(window)