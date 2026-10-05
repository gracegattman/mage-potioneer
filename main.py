import pygame, asyncio
from character import Character
from ingredient import add_ingredients, all_inventory
from map import *
from main_collection import *
from main_mixing import *
from progress import level_complete, power_ups

pygame.font.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mage Potioneer")
clock = pygame.time.Clock()

font_60 = pygame.font.SysFont("Arial", 60, bold=True)
font_40 = pygame.font.SysFont("Arial", 40, bold=True)
font_20 = pygame.font.SysFont("Arial", 20, bold=True)
font_16 = pygame.font.SysFont("Arial", 16)

# button class assuming button is image with hover variant in color as well
class Button:
    def __init__(self, img_path, hover_path, pos):
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (200,100))
        self.hover_img = pygame.image.load(hover_path).convert_alpha()
        self.hover_img = pygame.transform.scale(self.hover_img, (200,100))
        self.changeimg = self.img
        self.rect = self.changeimg.get_rect(center=pos)
    
    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.changeimg = self.hover_img
        else:
            self.changeimg = self.img
        surface.blit(self.changeimg, self.rect)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
        else:
            return False

# added extra screen for instructions to guide new players! :^)
def instruct_screen():
    running = True

    # use same bg as main menu for consistency
    bg_img = pygame.image.load("assets/background_default.jpeg").convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (800,600))
    bg_rect = bg_img.get_rect(topleft=(0,0))

    title = font_60.render("Instructions", True, (0,0,0))
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))

    instructions = [
        "Move with your arrow keys.",
        "Collect ingredients before time runs out!",
        "Create unique potions combinations!",
        "Create all 4 potions to gain a power-up",
        "and unlock the next level!"
    ]

    back_btn = Button("assets/buttons/Back.png", "assets/buttons/BackHover.png", (SCREEN_WIDTH//2, 450))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if back_btn.click(event):
                return
        
        screen.blit(bg_img, bg_rect)
        screen.blit(title, title_rect)

        start_y = 200
        for i in instructions:
            text = font_40.render(i, True, (0,0,0))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, start_y))
            start_y += 40

        back_btn.draw(screen)

        pygame.display.update()
        clock.tick(60)
               
# initial interface for users, can choose to view instructions before playing
def main_menu():
    # title image
    title_img = pygame.image.load("assets/MagePotioneer.png").convert_alpha()
    title_rect = title_img.get_rect(center=(SCREEN_WIDTH//2, 150))

    # credit to me :)
    creator_credit = font_20.render("Made by Grace Gattman", True, (30,30,30))
    creator_cred_rect = creator_credit.get_rect(center = (SCREEN_WIDTH//2, 560))

    # background image
    bg_img = pygame.image.load("assets/background_default.jpeg").convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (800,600))
    bg_rect = bg_img.get_rect(topleft=(0,0))


    # buttons
    play_btn = Button("assets/buttons/Play.png", "assets/buttons/PlayHover.png", (SCREEN_WIDTH//2, 300))

    instruct_btn = Button("assets/buttons/Instructions.png", "assets/buttons/InstructionsHover.png", (SCREEN_WIDTH//2, 400))

    quit_btn = Button("assets/buttons/Quit.png", "assets/buttons/QuitHover.png", (SCREEN_WIDTH//2, 500))

    # main loop for this screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # buttons implemented
            if play_btn.click(event):
                return # moves on to rest of calls in main_game_loop
            if instruct_btn.click(event):
                x = instruct_screen()
                pygame.event.clear()
                if x == "exit":
                    pygame.quit()
                    sys.exit()
            if quit_btn.click(event):
                pygame.quit()
                sys.exit()
        
        screen.blit(bg_img, bg_rect)
        screen.blit(title_img, title_rect)
        screen.blit(creator_credit, creator_cred_rect)

        play_btn.draw(screen)
        instruct_btn.draw(screen)
        quit_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

            
# MOST IMPORTANT
# main game loop
async def main_game_loop():
    while True:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/main_menu.ogg")
        pygame.mixer.music.play(-1)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mage Potioneer")
        main_menu()

        # intentionally allows players who had game over midway through the game to keep power-ups, making regaining their spot easier

        for level in range(1,5):
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/collection.ogg")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            run_collection(level)

            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/mixing.ogg")
            pygame.mixer.music.play(-1)
            i = run_mix(level)
            if i == "over":
                break
        # back to main menu if game over
        if i == "over":
            continue

        pygame.quit()
        await asyncio.sleep(0)

asyncio.run(main_game_loop())