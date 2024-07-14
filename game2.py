import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Read Reaction Test")

# CONSTANTS
SCREEN_W, SCREEN_H = 800, 600
GREEN, RED, YELLOW, BLUE = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)
BUTTON_W, BUTTON_H, BUTTON_TOP = 60, 60, SCREEN_H * 4 // 5
GREENx, YELLOWx, REDx, BLUEx = SCREEN_W // 4 - BUTTON_W * 2, SCREEN_W * 3 // 4 - BUTTON_W * 2, SCREEN_W // 2 - BUTTON_W * 2, SCREEN_W - BUTTON_W * 2
FONT = pygame.font.Font(None, 60)
FONTsml = pygame.font.Font(None, 30)
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# GLOBAL

spawn_times = []
reaction_times = []
avg_reac = 0
current_buttons = 0
current_color = None
current_xPos = None
last_color = None
last_xPos = None
alpha = 0.1 
# LOGIC
def choose_button():
    global current_color, current_xPos, current_buttons, last_color, last_xPos
    if current_buttons <= 0:
        color_positions = [(GREEN, GREENx), (RED, REDx), (YELLOW, YELLOWx), (BLUE, BLUEx)]
        while True:
            current_color, current_xPos = random.choice(color_positions)
            if current_color != last_color or current_xPos != last_xPos:
                break
        current_time = time.time()
        spawn_times.append(current_time)
        current_buttons += 1
        last_color, last_xPos = current_color, current_xPos

def draw_button():
    if current_buttons > 0:
        pygame.draw.ellipse(SCREEN, current_color, (current_xPos, BUTTON_TOP, BUTTON_W, BUTTON_H))

def key_press(event, key, color):
    global current_buttons, avg_reac
    if event.type == pygame.KEYDOWN and event.key == key and current_color == color:
        reaction_time = time.time() - spawn_times[-1]
        reaction_times.append(reaction_time)
        current_buttons -= 1
        calculate_reaction()
        choose_button()
    


def calculate_reaction():
    global avg_reac
    if len(reaction_times) > 0:
        last_reaction = reaction_times[-1]
        avg_reac = avg_reac * (1 - alpha) + last_reaction * alpha

def draw_avg_reaction():
    if len(reaction_times) > 0:
        last_reaction = reaction_times[-1]
        last_reac_text = FONT.render(f"+ {last_reaction:.2f} seconds", True, (255, 255, 255))
        SCREEN.blit(last_reac_text, (SCREEN_W//2 - last_reac_text.get_width()//2, SCREEN_H//2 - 50))
    if avg_reac <= .25 and avg_reac>= .1:
        color = (0,255,255)
    elif avg_reac <= .29 and avg_reac>= .1:
        color = (0,255,0)
    else:
        color = (255,255,255)
    stat = FONT.render(f"Average: {avg_reac:.2f} seconds", True, (color))
    SCREEN.blit(stat, (SCREEN_W//2 - stat.get_width()//2, SCREEN_H//2))
    
def button_location(xPos, key):
    letters = FONTsml.render(key, True, (255, 255, 255))
    pygame.draw.ellipse(SCREEN, (20,20,20), (xPos, BUTTON_TOP, BUTTON_W, BUTTON_H))
    SCREEN.blit(letters,(xPos+BUTTON_W*2//5,BUTTON_TOP+BUTTON_H+10))

def main():
    choose_button()
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        button_location(GREENx,"X")
        button_location(REDx,"C")
        button_location(YELLOWx,",")
        button_location(BLUEx,".")
        draw_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key_press(event, pygame.K_x, GREEN)
            key_press(event, pygame.K_c, RED)
            key_press(event, pygame.K_COMMA, YELLOW)
            key_press(event, pygame.K_PERIOD, BLUE)
       
        draw_avg_reaction()
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
