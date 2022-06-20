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
BOUNCE_CONSTANT = 9.8

# x,y = left,top
bar_x = WINDOW_WIDTH/2 - BAR_WIDTH/2
bar_y = WINDOW_HEIGHT - 2*BAR_HEIGHT
bar_dx = 1
bar_dy = 1

proj_x = WINDOW_WIDTH/2 - PROJ_HEIGHT/2
proj_y = 0
proj_dx = 0
proj_dy = 1

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def clamp(val, lower_bound, upper_bound):
    """
    returns val constrained by an upper and lower bound
    """
    return max(lower_bound, min(val, upper_bound))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if pygame.key.get_pressed()[pygame.K_d]:
        bar_x = clamp(bar_x + bar_dx, 0, WINDOW_WIDTH - BAR_WIDTH)
    if pygame.key.get_pressed()[pygame.K_a]:
        bar_x = clamp(bar_x - bar_dx, 0, WINDOW_WIDTH - BAR_WIDTH)

    # update projectile
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
    proj_rect = pygame.Rect(proj_x, proj_y, PROJ_WIDTH, PROJ_HEIGHT);
    nproj_rect = pygame.Rect(nproj_x, nproj_y, PROJ_WIDTH, PROJ_HEIGHT);
    if nproj_rect.colliderect(bar_rect):
        proj_dx *= -1
        proj_dy *= -1

    proj_x = nproj_x
    proj_y = nproj_y

    window.fill(COLOR_BG)
    pygame.draw.rect(window, BAR_BG, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(window, PROJ_BG, (proj_x, proj_y, PROJ_WIDTH, PROJ_HEIGHT))
    pygame.display.flip()