import pygame
import sys
from ingredient import all_inventory
from progress import level_complete, power_ups

class Potion:
    def __init__(self, name, img_path, ing):
        self.name = name
        self.img = pygame.image.load(img_path).convert_alpha()
        self.rect = self.img.get_rect()
        self.ing = ing

POTIONS = {
    # level 1
    ("artichoke", "arugula", "basil"): ("Leafy Brew", "assets/potions/Level1/Icon7.png"),
    ("artichoke", "arugula", "pepper_bell_green"): ("Glimmering Leaves", "assets/potions/Level1/Icon19.png"),
    ("artichoke", "basil", "pepper_bell_green"): ("Dappled Mirth", "assets/potions/Level1/Icon22.png"),
    ("arugula", "basil", "pepper_bell_green"): ("Jewel Beetlewing", "assets/potions/Level1/Icon34.png"),
    # level 2
    ("carrot_yellow", "pepper_bell_orange", "tomato_pear_yellow"): ("Sparkling Sunrise", "assets/potions/Level2/Icon13.png"),
    ("carrot_yellow", "onion", "tomato_pear_yellow"): ("Honey Dew", "assets/potions/Level2/Icon16.png"),
    ("carrot_yellow", "onion", "pepper_bell_orange"): ("Beach Gleam", "assets/potions/Level2/Icon25.png"),
    ("onion", "pepper_bell_orange", "tomato_pear_yellow"): ("Tropical Ichor", "assets/potions/Level2/Icon30.png"),
    # level 3
    ("cauliflower", "chicory", "fennel_florence"): ("Airy Snowdrops", "assets/potions/Level3/Icon8.png"),
    ("cauliflower", "chicory", "squash_white"): ("Extract of Flurry", "assets/potions/Level3/Icon9.png"),
    ("cauliflower", "fennel_florence","squash_white"): ("Sky's Reflection", "assets/potions/Level3/Icon36.png"),
    ("chicory", "fennel_florence", "squash_white"): ("Blizzard Essence", "assets/potions/Level3/Icon26.png"),
    # level 4
    ("cabbage_red", "kohlrabi_purple", "perilla_purple"): ("Arcane Enchancement", "assets/potions/Level4/Icon15.png"),
    ("cabbage_red", "kohlrabi_purple", "rakkyo"): ("Blessed Flask", "assets/potions/Level4/Icon43.png"),
    ("cabbage_red", "perilla_purple", "rakkyo"): ("Awakening Philter", "assets/potions/Level4/Icon12.png"),
    ("kohlrabi_purple", "perilla_purple", "rakkyo"): ("Elixir of the End", "assets/potions/Level4/Icon39.png")
}

# set up font sizing
font_70 = pygame.font.SysFont("Arial", 70)
font_50 = pygame.font.SysFont("Arial", 50)
font_30 = pygame.font.SysFont("Arial", 30)
font_24 = pygame.font.SysFont("Arial", 24)
font_18 = pygame.font.SysFont("Arial", 18)
font_16 = pygame.font.SysFont("Arial", 16)
font_12 = pygame.font.SysFont("Arial", 12)

# ingredient definition for mixing
class IngredientMix:
    def __init__(self, name, count, image_path, pos):
        self.name = name
        self.count = count
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def draw(self, i, surface, font):
        ing_image = pygame.transform.scale(self.image, (80,80))
        ing_rect = ing_image.get_rect(center=(60, 140 + i*120))
        surface.blit(ing_image, ing_rect)

        ing_text = font_16.render(self.name, True, (255,255,255))
        ing_text_rect = ing_text.get_rect(midleft = (ing_rect.right + 10, ing_rect.centery + 10))
        surface.blit(ing_text, ing_text_rect)

        count_txt = font_30.render(f"x{self.count}", True, (255,255,255))
        surface.blit(count_txt, (ing_rect.right + 10, ing_rect.y))

        self.rect = ing_rect

# fx handling... anguish, may still need anim_len adjust
def play_fx(screen, bg, cauldron_img, cauldron_rect, added_ing, fx):
    clock = pygame.time.Clock()

    anim_len = 1000
    begin = pygame.time.get_ticks()
    frame_i = 0

    while pygame.time.get_ticks() - begin < anim_len:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # considered deleting line below so that rest of mix ui is visible
        # decided focus on anim is more important so keep other ui hidden
        screen.blit(bg, (0,0))

        for img, rect in added_ing:
            screen.blit(img, rect)

        screen.blit(cauldron_img, cauldron_rect)

        # add fx
        fx_img = fx[frame_i % len(fx)]
        fx_img = pygame.transform.scale(fx_img, (200,200))
        fx_rect = fx_img.get_rect(center = (cauldron_rect.centerx, cauldron_rect.centery - 100))
        screen.blit(fx_img, fx_rect)

        pygame.display.flip()
        frame_i += 1
        clock.tick(20)



def level_completion(level_num):
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    
    level_complete[level_num] = True
    
    # display power up potion reward
    completion_potion_path = f"assets/potions/Level{level_num}/Final.png"
    completion_potion = pygame.image.load(completion_potion_path).convert_alpha()
    completion_potion = pygame.transform.scale(completion_potion, (200,200))
    completion_potion_rect = completion_potion.get_rect(center=(400,300))

    # assign power up based on level
    if level_num == 1:
        power_ups["speed_boost"] = True
        reward_text = "POWER UP UNLOCKED: SPEED BOOST"
    elif level_num == 2:
        power_ups["collection_r"] = True
        reward_text = "POWER UP UNLOCKED: COLLECTION RADIUS DOUBLED"
    elif level_num == 3:
        power_ups["double_coll"] = True
        reward_text = "POWER UP UNLOCKED: DOUBLE INGREDIENT COLLECTION"
    elif level_num == 4:
        power_ups["all_done"] = True
        reward_text = "GAME COMPLETE!"

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    show_completion = True
    while show_completion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                show_completion = False
            
            # overlay, darkens bg of mixing ui
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            bg.fill((0,0,0,200))
            screen.blit(bg, (0,0))

            title_text = font_50.render("Level Complete!", True, (255,255,255))
            screen.blit(title_text, (SCREEN_WIDTH//2- title_text.get_width()//2, 60))

            power_up_text = font_30.render(reward_text, True, (255,255,255))
            screen.blit(power_up_text, (SCREEN_WIDTH//2 - power_up_text.get_width()//2, SCREEN_HEIGHT // 2 + 150))

            if level_num != 4:
                cont_text = font_24.render("Click anywhere to continue to next level", True, (200,200,200))
            else:
                cont_text = font_24.render("Click anywhere to exit program. Thanks for playing!", True, (200,200,200))
            screen.blit(cont_text, (SCREEN_WIDTH//2-cont_text.get_width()//2, 500))

            screen.blit(completion_potion, completion_potion_rect)

            pygame.display.flip()
            clock.tick(60)

# func for game over handling
def game_over():
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return "over"
            
            # overlay, darkens bg of mixing ui
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            bg.fill((0,0,0,200))
            screen.blit(bg, (0,0))

            title_text = font_70.render("Game Over", True, (255,255,255))
            screen.blit(title_text, (SCREEN_WIDTH//2- title_text.get_width()//2, SCREEN_HEIGHT // 2 - 100))

            desc_text = font_30.render("You ran out of ingredients.", True, (255,255,255))
            screen.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, SCREEN_HEIGHT // 2 + 40))

            cont_text = font_24.render("Click to return to main menu.", True, (200,200,200))
            screen.blit(cont_text, (SCREEN_WIDTH//2-cont_text.get_width()//2, 500))

            pygame.display.flip()
            clock.tick(60)

# main func for running mixing
def run_mix(level_num):
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mixing Mode")

    # temporary: bg creation
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((30, 20, 40))

    cauldron_img = pygame.image.load("assets/cauldron.png").convert_alpha()
    cauldron_img = pygame.transform.scale(cauldron_img, (350, 350))
    cauldron_rect = cauldron_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

    # set ingredients
    ingredient_mix_list = []
    offset_btwn_ingred = 40

    # initialize potions
    tot_potions = 4
    potions_made = set()
    potion_storage = []

    for name, count in all_inventory.items.items():
        img_path = f"assets/ingredients/All/{name}.png"
        ingredient_mix_list.append(IngredientMix(name, count, img_path, pos = (80, offset_btwn_ingred)))
        offset_btwn_ingred += 50

    # initialize effects
    full_fx = pygame.image.load("assets/effects/63.png").convert_alpha()

    fx_cols = 7
    fx_size = 64
    # based on fx png used, appropriate fx colors chosen by hand
    if level_num == 1:
        row_use = 3
    elif level_num == 2:
        row_use = 0
    elif level_num == 3:
        row_use = 5
    elif level_num == 4:
        row_use = 1

    # make list of frames in fx row
    fx_frames = []
    for col in range(fx_cols):
        frame_r = pygame.Rect(col*fx_size, row_use*fx_size, fx_size, fx_size)
        fx_frames.append(full_fx.subsurface(frame_r))

    # main loop prep
    clock = pygame.time.Clock()
    cauldron_contents = []
    cauldron_ing_icons = []

    potion_display_on = False
    potion_display_img = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if potion_display_on:
                    potion_display_on = False
                    cauldron_contents.clear()
                    cauldron_ing_icons.clear()
                    continue

                pos = pygame.mouse.get_pos()
                for ing in ingredient_mix_list:
                    if ing.rect.collidepoint(pos) and ing.count > 0:
                        ing.count -= 1
                        cauldron_contents.append(ing.name)

                        ing_image = pygame.transform.scale(ing.image, (50,50))
                        x_spot = cauldron_rect.centerx
                        y_spot = cauldron_rect.centery - 400+80*len(cauldron_contents)
                        ing_rect = ing_image.get_rect(center=(x_spot, y_spot))

                        cauldron_ing_icons.append((ing_image, ing_rect))
                        
                        if len(cauldron_contents) == 3:
                            # fx first
                            play_fx(screen, background, cauldron_img, cauldron_rect, cauldron_ing_icons, fx_frames)
                            
                            mix = tuple(sorted(cauldron_contents))
                            result = POTIONS.get(mix)

                            if result:
                                potion_name, potion_img = result
                                if mix not in potions_made:
                                    new_po = Potion(potion_name, potion_img, mix)
                                    potion_storage.append(new_po)
                                    potions_made.add(mix)

                                    # potion display handling
                                    potion_display_on = True
                                    potion_display_img = pygame.image.load(potion_img).convert_alpha()
                                    potion_display_img = pygame.transform.scale(potion_display_img, (100, 100))

                                    if len(potions_made) == tot_potions:
                                        level_completion(level_num)
                                        return
                                                        
                            cauldron_contents.clear()
                            cauldron_ing_icons.clear()
        
        # game over check
        over = all(ing.count <= 0 for ing in ingredient_mix_list)
                
        if over:
            return game_over()

        # draw ingredient inventory
        screen.blit(background, (0, 0))

        ing_title = font_50.render("Ingredients", True, (255,255,255))
        screen.blit(ing_title, (60, 20))

        for i, ing in enumerate(ingredient_mix_list):
            ing.draw(i, screen, font_24)
        
        screen.blit(cauldron_img, cauldron_rect)
        for img, rect in cauldron_ing_icons:
            screen.blit(img, rect)

        # draw potion inventory
        x_offset = SCREEN_WIDTH - 230
        y_offset = 80
        
        title = font_50.render("Potions", True, (255,255,255))
        screen.blit(title, (x_offset+20, 20))

        for po in potion_storage:
            # draw potion
            po.img = pygame.transform.scale(po.img, (70,70))
            po.rect = po.img.get_rect(topleft=(x_offset, y_offset))
            screen.blit(po.img, po.rect)

            # draw potion name under it
            name_text = font_24.render(po.name, True, (255,255,255))
            screen.blit(name_text, (x_offset, y_offset + po.rect.height + 10))
            
            # recipe
            recipe_text = font_12.render(" + ".join(po.ing), True, (200,200,200))
            screen.blit(recipe_text, (x_offset, y_offset+po.rect.height+40))

            y_offset += po.rect.height + 80

        for i, ing_name in enumerate(cauldron_contents):
            text = font_24.render(ing_name, True, (255,255,255))
            text_w, text_h = font_24.size(ing_name)
            screen.blit(text, (cauldron_rect.centerx - text_w//2, cauldron_rect.centery-290+i*80))

        # popup added if new potion has been made
        if potion_display_on:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))

            title = font_50.render("New Potion Discovered!", True, (255,255,255))
            title_w, title_h = font_50.size("New Potion Discovered!")
            screen.blit(title, (SCREEN_WIDTH // 2 - title_w//2, SCREEN_HEIGHT // 2))
            
            big_po_rect = potion_display_img.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
            screen.blit(potion_display_img, big_po_rect)

            click_to_cont_text = font_18.render("Click anywhere to continue", True, (200,200,200))
            click_w, click_h = font_18.size("Click anywhere to continue")
            screen.blit(click_to_cont_text, (SCREEN_WIDTH//2 - click_w//2, SCREEN_HEIGHT//2 + 80))

        pygame.display.flip()
        clock.tick(60)

    return