import pygame
from character import Character
from ingredient import add_ingredients, all_inventory
from map import *
from progress import power_ups

pygame.init()
pygame.font.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def handle_player(player, keys, tilemap):
    # get direction and state
    direction = None
    state = "idle"

    if keys[pygame.K_LEFT]:
        direction = "left"
        state = "run"
    elif keys[pygame.K_RIGHT]:
        direction = "right"
        state = "run"
    elif keys[pygame.K_UP]:
        direction = "up"
        state = "run"
    elif keys[pygame.K_DOWN]:
        direction = "down"
        state = "run"

    # update player anim
    if direction != None:
        # keep player facing same way if not changing direction
        player.direction = direction
    player.update(state, player.direction, tilemap.do_not_walk)


def run_collection(level_num):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Collection Mode")

    # load glow
    glow_anim = []
    for i in range(5):
        frame = pygame.image.load(f"assets/effects/overhead/frame{i}.png").convert_alpha()
        glow_anim.append(frame)

    glow_vis = False
    glow_ind = 0
    glow_sep = 0

    # change timer based on level for higher difficulty
    if level_num == 1:
        countdown_sec = 30
    elif level_num == 2:
        countdown_sec = 25
    elif level_num == 3:
        countdown_sec = 20
    elif level_num == 4:
        countdown_sec = 15
    
    timer_event = pygame.USEREVENT + 10 # event id just in case
    pygame.time.set_timer(timer_event, 1000) #1000 ms = 1 s
    font = pygame.font.SysFont("Arial", size=60)

    # load in character, positioned at middle of map (level-dependent)
    if level_num != 4:
        player = Character((800, 800))
    else:
        player = Character((400, 400))

    # load map, reset inventory, and scatter ingredients
    tilemap = TileMap(f"map/Level{level_num}/level{level_num}.tmx")
    all_inventory.refresh()
    ing_group, ing_list = add_ingredients(f"assets/ingredients/Level{level_num}", tilemap)

    # reset camera
    cam_x, cam_y = 0, 0

    running = True
    while running:
        dt = clock.tick(60)  # 60 FPS cap

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == timer_event:
                if countdown_sec > 0:
                    countdown_sec -= 1
                else:
                    pygame.time.set_timer(timer_event, 0)
                    running = False
        
        # use this instead of handle event for smoother movement input
        keys = pygame.key.get_pressed()
        handle_player(player, keys, tilemap)

        # collision
        collided = pygame.sprite.spritecollide(player, ing_group, dokill=True)

        for ingre in collided:
            if power_ups["double_coll"]:
                all_inventory.add(ingre.name)
            all_inventory.add(ingre.name)

            glow_vis = True
            glow_ind = 0
            glow_sep = 0

        # move camera if necessary to follow player movement
        cam_x = player.rect.centerx - screen.get_width() // 2
        cam_y = player.rect.centery - screen.get_height() // 2

        cam_x = max(0, min(cam_x, tilemap.map_w - screen.get_width()))
        cam_y = max(0, min(cam_y, tilemap.map_h - screen.get_height()))

        # handle glow fx if player collided w ingredient
        if glow_vis:
            glow_sep += 1
            if glow_sep >= 5:
                glow_sep = 0
                glow_ind += 1
                if glow_ind >= len(glow_anim):
                    glow_vis = False


        # timer + done text prep
        bg_timer_rend = font.render(f"{countdown_sec:02d}", True, (255,255,255))
        bg_timer_rect_r = bg_timer_rend.get_rect(center=(SCREEN_WIDTH // 2 + 1, 100))
        bg_timer_rect_l = bg_timer_rend.get_rect(center=(SCREEN_WIDTH // 2 - 1, 100))
        bg_timer_rect_u = bg_timer_rend.get_rect(center=(SCREEN_WIDTH // 2, 99))
        bg_timer_rect_d = bg_timer_rend.get_rect(center=(SCREEN_WIDTH // 2, 101))

        timer_rend = font.render(f"{countdown_sec:02d}", True, (0,0,0))
        timer_rect = timer_rend.get_rect(center = (SCREEN_WIDTH // 2, 100))
        
        final_bg = font.render("Collection done!", True, (255,255,255))
        final_bg_rect_r = final_bg.get_rect(center = (SCREEN_WIDTH // 2 + 1, 100))
        final_bg_rect_l = final_bg.get_rect(center=(SCREEN_WIDTH // 2 - 1, 100))
        final_bg_rect_u = final_bg.get_rect(center=(SCREEN_WIDTH // 2, 99))
        final_bg_rect_d = final_bg.get_rect(center=(SCREEN_WIDTH // 2, 101))

        final_text = font.render("Collection done!", True, (0,0,0))
        final_text_rect = final_text.get_rect(center = (SCREEN_WIDTH // 2, 100))

        # draw everything to screen
        screen.fill((0, 0, 0))
        tilemap.draw_map(screen, cam_x, cam_y)
        for ingredient in ing_group:
            screen.blit(ingredient.image, (ingredient.rect.x - cam_x, ingredient.rect.y - cam_y))
        screen.blit(player.image, (player.rect.x-cam_x, player.rect.y-cam_y))
        
        #draw glow
        if glow_vis:
            glow_img = glow_anim[glow_ind]
            glow_x = player.rect.centerx - glow_img.get_width()//2 - cam_x
            glow_y = player.rect.top - glow_img.get_height() - 10 - cam_y
            screen.blit(glow_img, (glow_x, glow_y))

        #draw timer
        if countdown_sec > 0:
            screen.blit(bg_timer_rend, bg_timer_rect_r)
            screen.blit(bg_timer_rend, bg_timer_rect_l)
            screen.blit(bg_timer_rend, bg_timer_rect_u)
            screen.blit(bg_timer_rend, bg_timer_rect_d)
            screen.blit(timer_rend, timer_rect)
        else:
            screen.blit(final_bg, final_bg_rect_r)
            screen.blit(final_bg, final_bg_rect_l)
            screen.blit(final_bg, final_bg_rect_u)
            screen.blit(final_bg, final_bg_rect_d)
            screen.blit(final_text, final_text_rect)
            #to_mix_button.draw(screen)
        pygame.display.flip()
    
    return