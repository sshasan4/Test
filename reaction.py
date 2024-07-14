import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Read Test")

# CONSTANTS
SCREEN_W, SCREEN_H = 800, 600
GREEN, RED, YELLOW, BLUE = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)
BUTTON_W, BUTTON_H, BUTTON_TOP = 60, 20, SCREEN_H * 4 // 5
GREENx, YELLOWx, REDx, BLUEx = SCREEN_W // 4 - BUTTON_W * 2, SCREEN_W * 3 // 4 - BUTTON_W * 2, SCREEN_W // 2 - BUTTON_W * 2, SCREEN_W - BUTTON_W * 2
FONT = pygame.font.Font(None, 40)
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# GLOBAL
click_times = []
spawn_times = []
reaction_times = []
avg_reac=0
current_buttons= 0

#LOGIC
def draw_button():
    global current_color
    while current_buttons <= 0:
        color_positions = [(GREEN, GREENx), (RED, REDx), (YELLOW, YELLOWx), (BLUE, BLUEx)]
        color, xPos = random.choice(color_positions)
        pygame.draw.rect(SCREEN, color, (xPos, BUTTON_TOP, BUTTON_W, BUTTON_H))
        current_time = time.time()
        spawn_times.append(current_time)
        current_color = color
        current_buttons += 1

def key_press(event, key, color):
    if event.type == pygame.KEYDOWN and event.key == key and current_color == color:
        reaction_time = time.time() - spawn_times[-1]
        reaction_times.append(reaction_time)
        current_buttons -= 1
    
def calculate_reaction():
    if len(reaction_times) <= 10:
        avg_reac = sum(reaction_times)//len(reaction_times)
    else:
        reaction_times.pop()
    

    
def draw_avg_reaction():
    stat= FONT.render(f"Average Reaction Time: {avg_reac:.2f} seconds", True, (255, 255, 255))
    SCREEN.blit(stat, (SCREEN_W//2, SCREEN_H//2))




def main():
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        
    pygame.quit()

if __name__ == "__main__":
    main()