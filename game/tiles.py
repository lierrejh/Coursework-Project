# Write up:
# Tile map based game allows for a lot more customisability with generation
# Describe struggles of doing it this way

#For loading map

import pygame, csv, os
from tilesheet import Tilesheet

tilesheet = Tilesheet('assets/sprites+items/0x72_16x16DungeonTileset.v4.png', 16, 16, 16, 16)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tilesheet):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y

    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Tilemap(pygame.sprite.Sprite):
    def __init__(self, filename, tilesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.tilesheet = tilesheet
        self.tiles,self.tile_wall, self.collision_list = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
        

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface) 

    def read_csv(self, filename): #algorithm taken from Pygame Tile Based Game Tutorial: Tilemaps
        map_list = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map_list.append(list(row))
        return map_list

    def load_tiles(self, filename):
        tiles = []
        tile_wall = []
        collision_list = []

        mapList = self.read_csv(filename)
        x,y = 0,0
        for row in mapList:
            x = 0
            for tile in row:
                if tile == '0':
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/WallTop.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
                elif tile == '50': #filling 
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/WallFilling.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
                elif (tile == '16') or (tile == '18'): #wall 
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/Wall.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
                    #*2.5
                    tile_wall.append(Tile('assets/sprites+items/individual_sprites/USED/Wall.png', x * self.tile_size , y * self.tile_size , self.tilesheet))
                    collision_list.append(Tile('assets/sprites+items/individual_sprites/USED/Wall.png', x * self.tile_size * 2.5 , y * self.tile_size * 2.5, self.tilesheet))
                elif tile == '125': #wall skirt
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/0x72_16x16DungeonTileset-125.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
         
                elif tile == '122': #wall skirt
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/0x72_16x16DungeonTileset-122.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
                elif tile == '121': #wall skirt
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/0x72_16x16DungeonTileset-121.png', x * self.tile_size, y * self.tile_size, self.tilesheet))
                elif tile == '21': #path
                    tiles.append(Tile('assets/sprites+items/individual_sprites/USED/0x72_16x16DungeonTileset-21.png', x * self.tile_size, y * self.tile_size, self.tilesheet))

                x += 1
            y += 1
        
                
        tile_wall = pygame.sprite.Group(tile_wall)
        collision_list = pygame.sprite.Group(collision_list)
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles, tile_wall, collision_list

    
   