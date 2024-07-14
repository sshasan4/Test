import pygame
import time

pygame.init()
pygame.display.set_caption("Finger Warmup")

# CONSTANTS
SCREEN_W, SCREEN_H = 800, 600
GREEN, RED, YELLOW, BLUE = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)
BUTTON_W, BUTTON_H, BUTTON_TOP = 60, 20, SCREEN_H * 4 // 5
GREENx, YELLOWx, REDx, BLUEx = SCREEN_W // 4 - BUTTON_W * 2, SCREEN_W * 3 // 4 - BUTTON_W * 2, SCREEN_W // 2 - BUTTON_W * 2, SCREEN_W - BUTTON_W * 2
FONT = pygame.font.Font(None, 40)
decay_time = 3
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# GLOBAL VARS
Gclick_times = []
Rclick_times = []
Yclick_times = []
Bclick_times = []
clones = []  

def calculate_cps(click_times):
    current_time = time.time()
    click_times = [click_time for click_time in click_times if current_time - click_time <= decay_time]
    if click_times:
        elapsed_time = max(current_time - min(click_times), 1e-6)
        clicks_per_second = len(click_times) / elapsed_time
    else:
        clicks_per_second = 0
    return clicks_per_second, click_times


def handle_click(event, key, click_times, color, Xpos):
    if event.type == pygame.KEYDOWN and event.key == key:
        current_time = time.time()
        click_times.append(current_time)
        new_rect = pygame.Rect(Xpos, BUTTON_TOP, BUTTON_W, BUTTON_H)
        clones.append((new_rect, color))  
    return click_times


def draw_text(text, position):
    cps = float(text)
    if cps >= 7:
        color = (0, 255, 0)
    elif cps >= 6:
        color = (255, 255, 255)
    else:
        color = (255, 0, 0)

    rendered_text = FONT.render(text, True, color)
    SCREEN.blit(rendered_text, position)


def main():
    running = True
    while running:
        SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            Gclick_times[:] = handle_click(event, pygame.K_x, Gclick_times, GREEN, GREENx)
            Rclick_times[:] = handle_click(event, pygame.K_c, Rclick_times, RED, REDx)
            Yclick_times[:] = handle_click(event, pygame.K_COMMA, Yclick_times, YELLOW, YELLOWx)
            Bclick_times[:] = handle_click(event, pygame.K_PERIOD, Bclick_times, BLUE, BLUEx)

        Gcps, Gclick_times[:] = calculate_cps(Gclick_times)
        Rcps, Rclick_times[:] = calculate_cps(Rclick_times)
        Ycps, Yclick_times[:] = calculate_cps(Yclick_times)
        Bcps, Bclick_times[:] = calculate_cps(Bclick_times)

        draw_text(f"{Gcps:.2f}", (GREENx, BUTTON_TOP + BUTTON_H))
        draw_text(f"{Rcps:.2f}", (REDx, BUTTON_TOP + BUTTON_H))
        draw_text(f"{Ycps:.2f}", (YELLOWx, BUTTON_TOP + BUTTON_H))
        draw_text(f"{Bcps:.2f}", (BLUEx, BUTTON_TOP + BUTTON_H))

        
        for rect, color in clones:
            rect.y -= 5
            pygame.draw.rect(SCREEN, color, rect)

        # Remove rectangles that are off-screen
        clones[:] = [(rect, color) for rect, color in clones if rect.y + BUTTON_H > 0]

        pygame.display.flip()
        pygame.time.Clock().tick(120)

if __name__ == "__main__":
    main()
    pygame.quit()
