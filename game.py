import pygame
import time

pygame.init()
pygame.display.set_caption("Finger Warmup")

# CONSTANTS
SCREEN_W, SCREEN_H = 800, 600
GREEN, RED, YELLOW, BLUE = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)
BUTTON_W, BUTTON_H, BUTTON_TOP = 60, 10, SCREEN_H * 4 // 5
GREENx, YELLOWx, REDx, BLUEx = SCREEN_W // 4 - BUTTON_W * 2, SCREEN_W * 3 // 4 - BUTTON_W * 2, SCREEN_W // 2 - BUTTON_W * 2, SCREEN_W - BUTTON_W * 2
FONT = pygame.font.Font(None, 40)
DECAY_TIME = 3
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# GLOBAL VARS
click_times = {pygame.K_x: [], pygame.K_c: [], pygame.K_COMMA: [], pygame.K_PERIOD: []}
clones = []
keys_pressed = {pygame.K_x: False, pygame.K_c: False, pygame.K_COMMA: False, pygame.K_PERIOD: False}
colors = {pygame.K_x: GREEN, pygame.K_c: RED, pygame.K_COMMA: YELLOW, pygame.K_PERIOD: BLUE}
positions = {pygame.K_x: GREENx, pygame.K_c: REDx, pygame.K_COMMA: YELLOWx, pygame.K_PERIOD: BLUEx}

def calculate_cps(click_times):
    current_time = time.time()
    click_times = [click_time for click_time in click_times if current_time - click_time <= DECAY_TIME]
    elapsed_time = max(current_time - min(click_times, default=current_time), 1e-6)
    cps = len(click_times) / elapsed_time if click_times else 0
    return cps, click_times

def handle_click(key):
    current_time = time.time()
    click_times[key].append(current_time)

def spawn_clone(key):
    new_rect = pygame.Rect(positions[key], BUTTON_TOP, BUTTON_W, BUTTON_H)
    clones.append((new_rect, colors[key]))

def draw_text(text, position):
    cps = float(text)
    color = (0, 255, 0) if cps >= 7 else (255, 255, 255) if cps >= 6 else (255, 0, 0)
    rendered_text = FONT.render(text, True, color)
    SCREEN.blit(rendered_text, position)

def draw_clones():
    for rect, color in clones:
        rect.y -= 10
        pygame.draw.rect(SCREEN, color, rect)
    clones[:] = [(rect, color) for rect, color in clones if rect.y + BUTTON_H > 0]

def main():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in keys_pressed:
                keys_pressed[event.key] = True
                handle_click(event.key)  # Add click time once per key press
            elif event.type == pygame.KEYUP and event.key in keys_pressed:
                keys_pressed[event.key] = False

        for key in keys_pressed:
            if keys_pressed[key]:
                spawn_clone(key)

        for key in click_times:
            cps, click_times[key] = calculate_cps(click_times[key])
            draw_text(f"{cps:.2f}", (positions[key], BUTTON_TOP + BUTTON_H))

        draw_clones()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
