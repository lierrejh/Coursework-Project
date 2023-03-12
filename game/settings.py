# Description: This file contains all the settings for the game

import pygame
from os import walk

# Key settings:
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

# Player stats
player_stats = {
    'damage_multiplier' : 1,
    'defense' : 1,
    'health_multiplier' : 1,
    'speed' : 8,
}

# Weapon data:
WEAPON_DATA = {
     #40%
    "wooden-sword" : {'cooldown' : 700, 'damage' : 15, 'image' : 'assets/sprites+items/weapons/wooden-sword.png', 'index' : 0 },
    "iron-sword" : {'cooldown' : 700, 'damage' : 20, 'image' : 'assets/sprites+items/weapons/iron-Sword.png', 'index' : 1 },
    "gem-iron-sword" : {'cooldown' : 700, 'damage' : 25, 'image' : 'assets/sprites+items/weapons/gem-iron-sword.png', 'index' : 2 },
    "blooded-sword" : {'cooldown' : 900, 'damage' : 25, 'image' : 'assets/sprites+items/weapons/blooded-sword.png', 'index' : 3 },

    #30%
    "large-sword" : {'cooldown' : 2000, 'damage' : 40, 'image' : 'assets/sprites+items/weapons/large-sword.png', 'index' : 4 },
    "iron-lance" : {'cooldown' : 900, 'damage' : 30, 'image' : 'assets/sprites+items/weapons/iron-lance.png', 'index' : 5 },
    "training-sword" : {'cooldown' : 800, 'damage' : 25, 'image' : 'assets/sprites+items/weapons/training-sword.png', 'index' : 6 },
    "butchers-knife" : {'cooldown' : 300, 'damage' : 15, 'image' : 'assets/sprites+items/weapons/butchers-knife.png', 'index' : 7 },
    
    #20%
    "golden-sword" : {'cooldown' : 800, 'damage' : 30, 'image' : 'assets/sprites+items/weapons/golden-sword.png', 'index' : 8 },
    "gem-gold-sword" : {'cooldown' : 750, 'damage' : 40, 'image' : 'assets/sprites+items/weapons/gem-gold-sword.png', 'index' : 9 },
    "platinum-lance" : {'cooldown' : 900, 'damage' : 45, 'image' : 'assets/sprites+items/weapons/platinum-lance.png', 'index' : 10 },
    "platinum-sword" : {'cooldown' : 800, 'damage' : 40, 'image' : 'assets/sprites+items/weapons/platinum-sword.png', 'index' : 11 },
    
    #10%
    "gem-platinum-sword" : {'cooldown' : 750, 'damage' : 70, 'image' : 'assets/sprites+items/weapons/gem-platinum-sword.png', 'index' : 12 },
    "moonlight-sword" : {'cooldown' : 800, 'damage' : 80, 'image' : 'assets/sprites+items/weapons/moonlight-sword.png', 'index' : 13 },
}

ITEM_DATA = {
    "small-health-potion" : {'health' : 80, 'image' : 'assets/sprites+items/items/small-healing-potion.png', 'index' : 0 },
    "health-potion" : {'health' : 250, 'image' : 'assets/sprites+items/items/healing-potion.png', 'index' : 1 },
    "damage-potion" : {'damage_increase' : 1.2, 'image' : 'assets/sprites+items/items/damage-potion.png', 'index' : 2 },
}

ENEMY_DATA = {
    'chest' : {'health' : 2500, 'exp' : 0, 'damage' : 0, 'image' : 'assets/sprites+items/chest/idle/0.png', 'speed' : 0, 'knockback' : 0, 'attack_radius' : 100, 'notice_radius' : 0, 'attack_type' : 'slash' },
    'goblin' : {'health' : 60, 'exp' : 50, 'damage' : 150, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-162.png', 'speed' : 2, 'knockback' : 2, 'attack_radius' : 30, 'notice_radius' : 200, 'attack_type' : 'slash' },
    'fire-demon' : {'health' : 75, 'exp' : 110, 'damage' : 200, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-178.png', 'speed' : 2, 'knockback' : 2, 'attack_radius' : 25, 'notice_radius' : 300, 'attack_type' : 'fire' },
    'mage' : {'health' : 90, 'exp' : 180, 'damage' : 150, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-149.png', 'speed' : 1, 'knockback' : 1, 'attack_radius' : 40, 'notice_radius' : 250, 'attack_type' : 'magic' },
    'giant-boss' : {'health' : 180, 'exp' : 750, 'damage' : 250, 'image' : 'assets/sprites+items/enemies/giant-boss/attack/0.png', 'speed' : 1.5, 'knockback' : 0, 'attack_radius' : 60, 'notice_radius' : 450, 'attack_type' : 'magic' },
    'demon-boss' : {'health' : 180, 'exp' : 750, 'damage' : 250, 'image' : 'assets/sprites+items/enemies/demon-boss/attack/0.png', 'speed' : 1.5, 'knockback' : 0, 'attack_radius' : 60, 'notice_radius' : 450, 'attack_type' : 'magic' },
    'goblin-boss' : {'health' : 180, 'exp' : 750, 'damage' : 250, 'image' : 'assets/sprites+items/enemies/goblin-boss/attack/0.png', 'speed' : 1.5, 'knockback' : 0, 'attack_radius' : 60, 'notice_radius' : 450, 'attack_type' : 'magic' }
}

POWER_UP_DATA = {
    'damage-increase' : {'damage' : 0.6, 'image' : 'assets/sprites+items/icons/damage-increase.png', 'index' : 0},
    'defense-increase' : {'defense' : 0.15, 'image' : 'assets/sprites+items/icons/defense-increase.png', 'index' : 1},
    'health-increase' : {'health' : 0.5, 'image' : 'assets/sprites+items/icons/health-increase.png', 'index' : 2},
    'speed-increase' : {'speed' : 1, 'image' : 'assets/sprites+items/icons/speed-increase.png', 'index' : 3},
}

PLAYER_WEAPONS = ['wooden-sword']

PLAYER_ITEMS = ['small-health-potion']

PLAYER_POWER_UPS = []


# Game variables
enemies_killed = 0

waves_completed = 0

current_time = 0

enemy_drop_item_time = 0

enemy_drop_powerup_time = 0

level_finished = False

level_count = 1


# Imports images required for the game
def import_folder(path):
        surface_list = []
        for _,__,img_files in walk(path):
            img_files.sort()
            for image in img_files:
                # Filtering hidden mac files
                if not image.endswith('.DS_Store'):
                    full_path = path + '/' + image
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)

            return surface_list