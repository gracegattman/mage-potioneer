import pygame, random, os
from progress import power_ups

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, img_loc, loc, pickup_margin):
        super().__init__()
        self.image = pygame.image.load(img_loc).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.rect = self.rect.inflate(pickup_margin, pickup_margin)
        base = os.path.basename(img_loc)
        self.name = os.path.splitext(base)[0]

class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, name):
        self.items[name] = self.items.get(name, 0) + 1
        #print(self.items)
    
    def remove(self, name):
        if name in self.items:
            self.items[name] -= 1
            if self.items[name] == 0:
                del self.items[name]
    
    def refresh(self):
        self.items.clear()

def add_ingredients(folder, tilemap, num = 10):
    # num_each currently set to spawn 10 of each ingredient
    ingredients = pygame.sprite.Group()
    ingred_list = []

    # get tilemap locs
    tile_locs = list(tilemap.do_walk)
    # get every ingredient from specific folder
    for file in os.listdir(folder):
        for _ in range(num):
            if tile_locs:
                # new method of tile choosing to prevent overlap
                loc = random.choice(tile_locs)
                tile_locs.remove(loc)

                loc_rect = pygame.Rect(loc[0], loc[1], tilemap.tile_size, tilemap.tile_size)
                # also now prevents spawning on top of props, water, etc
                on_bad_tile = False
                for til in tilemap.do_not_walk:
                    if loc_rect.colliderect(til):
                        on_bad_tile = True
                        break
                if on_bad_tile:
                    continue

                full_loc = os.path.join(folder, file)
                if power_ups["collection_r"]:
                    ingred = Ingredient(full_loc, loc, 30)
                else:
                    ingred = Ingredient(full_loc, loc, 15)
                ingredients.add(ingred)
                ingred_list.append(ingred)
            else:
                break

    return ingredients, ingred_list

all_inventory = Inventory()