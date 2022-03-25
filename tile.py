import pygame

import config

class Tile:
    GRID_SIZE = 50
    
    Tiles = []

    def __init__(self, x=0, y=0, xGrid=None, yGrid=None, img=None, tile=None):
        self.x = x
        self.y = y

        self.tile = tile

        self.img = img

        if xGrid != None:
            self.x = xGrid * Tile.GRID_SIZE * config.size
        if yGrid != None:
            self.y = yGrid * Tile.GRID_SIZE * config.size

    @classmethod
    def Create(self, x=0, y=0, xGrid=None, yGrid=None, img=None):
        Tile.Tiles.append(Tile(x, y, xGrid, yGrid, img))

    @classmethod
    def Draw(self, size=1):
        surf = pygame.Surface((int(800*config.size), int(550*config.size)))

        for t in Tile.Tiles:
            surf.blit(t.img, (t.x, t.y))

        surf = pygame.transform.scale(surf, (int(surf.get_width()*size), int(surf.get_height()*size)))

        return surf
