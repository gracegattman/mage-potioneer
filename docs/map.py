import pygame
from pytmx import load_pygame
import random

class TileMap():
    def __init__(self, tiles_file):
        # new method for loading map based on online tutorial
        # should make code easier to follow + more applicable
        self.tmx = load_pygame(tiles_file)
        # now supports both 16x16 and 32x32 tiles, necessary for different maps
        self.tile_size = self.tmx.tilewidth

        # with props and bounds now added instead of simple + flat terrain,
        # it's now necessary to develop locations player cannot walk over
        self.do_not_walk = []
        self.do_walk = []
        self.get_collisions()

        self.map_w = self.tmx.width * self.tile_size
        self.map_h = self.tmx.height * self.tile_size
        self.map_surface = pygame.Surface((self.map_w, self.map_h)).convert_alpha()
        self.map_surface.fill((0,0,0,0))

        self.load_map_layers()

    # new method using tiled tsx exports + custom properties to find tiles
    # where movement should be restricted
    def get_collisions(self):
        for layer_i, layer in enumerate(self.tmx.visible_layers):
            if layer_i == 0:
                for row, col, tile_img in layer.tiles():
                    if tile_img:
                        self.do_walk.append((row*self.tile_size, col*self.tile_size))

            else:
                for row, col, tile_img in layer.tiles():
                    if tile_img:
                        rect = pygame.Rect(row*self.tile_size, col*self.tile_size, self.tile_size, self.tile_size)
                        self.do_not_walk.append(rect)
        
    
    def load_map_layers(self):
        for layer in self.tmx.visible_layers:
            for row, col, tile in layer.tiles():
                if tile:
                    self.map_surface.blit(tile, (row*self.tile_size, col*self.tile_size))
    
    # draw tiles based on camera position so that area around player shown
    def draw_map(self, surface, cam_x, cam_y):
        surface.blit(self.map_surface, (-cam_x, -cam_y))
    