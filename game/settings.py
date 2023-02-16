# Description: This file contains all the settings for the game

# Key settings:
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

# Weapon data:
WEAPON_DATA = {
    "wooden-sword" : {'cooldown' : 2000, 'damage' : 10, 'image' : 'assets/sprites+items/weapons/wooden-sword.png' },
    "iron-sword" : {'cooldown' : 700, 'damage' : 20, 'image' : 'assets/sprites+items/weapons/iron-Sword.png' },
    "gem-iron-sword" : {'cooldown' : 700, 'damage' : 25, 'image' : 'assets/sprites+items/weapons/gem-iron-sword.png' },
    "blooded-sword" : {'cooldown' : 900, 'damage' : 25, 'image' : 'assets/sprites+items/weapons/blooded-sword.png' },
    # ^ give life steal
    "large-sword" : {'cooldown' : 1000, 'damage' : 35, 'image' : 'assets/sprites+items/weapons/large-sword.png' },
    "iron-lance" : {'cooldown' : 900, 'damage' : 30, 'image' : 'assets/sprites+items/weapons/iron-lance.png' },
    "training-sword" : {'cooldown' : 800, 'damage' : 15, 'image' : 'assets/sprites+items/weapons/training-sword.png' },
    "butchers-knife" : {'cooldown' : 500, 'damage' : 15, 'image' : 'assets/sprites+items/weapons/butchers-knife.png' },
    "golden-sword" : {'cooldown' : 800, 'damage' : 30, 'image' : 'assets/sprites+items/weapons/golden-sword.png' },
    "gem-gold-sword" : {'cooldown' : 750, 'damage' : 40, 'image' : 'assets/sprites+items/weapons/gem-gold-sword.png' },
    "platinum-lance" : {'cooldown' : 900, 'damage' : 45, 'image' : 'assets/sprites+items/weapons/platinum-lance.png' },
    "platinum-sword" : {'cooldown' : 800, 'damage' : 40, 'image' : 'assets/sprites+items/weapons/platinum-sword.png' },
    "gem-platinum-sword" : {'cooldown' : 750, 'damage' : 50, 'image' : 'assets/sprites+items/weapons/gem-platinum-sword.png' },
    "moonlight-sword" : {'cooldown' : 800, 'damage' : 60, 'image' : 'assets/sprites+items/weapons/moonlight-sword.png' },

}

ENEMY_DATA = {
    'goblin' : {'health' : 100, 'exp' : 50, 'damage' : 30, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-162.png', 'speed' : 2, 'resistance' : 3, 'attack_radius' : 50, 'notice_radius' : 300 },
    'fire-demon' : {'health' : 200, 'exp' : 110, 'damage' : 50, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-178.png', 'speed' : 3, 'restitance' : 2, 'attack_radius' : 20, 'notice_radius' : 420 },
    'mage' : {'health' : 300, 'exp' : 180, 'damage' : 40, 'image' : 'assets/sprites+items/individual_sprites/0x72_16x16DungeonTileset-149.png', 'speed' : 2, 'restitance' : 1, 'attack_radius' : 60, 'notice_radius' : 400 }
}