import pygame
import sys
import random
import socket
import threading
import json
import os
import math
import urllib.request
import datetime
import base64
import io
import time
import array

CURRENT_VERSION = "0.42"
DEFAULT_PORT = 5000

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 980
BG_COLOR = (15, 18, 25)
ACCENT_COLOR = (0, 220, 180)
HOVER_COLOR = (0, 250, 210)
PANEL_COLOR = (25, 30, 40)
TEXT_COLOR = (240, 240, 240)
ALERT_COLOR = (255, 80, 80)
FONT_SIZE = 30

SETTINGS_FILE = "world_rush_settings.json"
HISTORY_FILE = "game_history.json"
AVATARS = [
    "🙂", "😎", "🤖", "👽", "🦊", "🐱", "🐶", "🦁", "🦄", "💀", "👻", "💩", "👾", "🤡", "🤠", "👺",
    "😊", "😂", "🤣", "😍", "😒", "😘", "😜", "🤔", "🙄", "😴", "😷", "🤒", "🤕", "🤢", "🤧", "😇",
    "🥳", "🥺", "🤬", "😈", "👿", "👹", "👺", "☠️", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
    "😾", "🙈", "🙉", "🙊", "🐵", "🐺", "🐯", "🦒", "🦝", "🐷", "🐗", "🐭", "🐹", "🐰", "🐻", "🐨",
    "🐼", "🐸", "🦓", "🐴", "🐔", "🐲", "🐾", "🐒", "🦍", "🦧", "🦮", "🐕", "🐩", "🐈", "🐅", "🐆",
    "⚡", "🔥", "💧", "❄️", "🌈", "☀️", "🌙", "⭐", "🌟", "🍀", "🍄", "🌵", "🌴", "🌲", "🍁", "🍂",
    "🍔", "🍕", "🍟", "🌭", "🍿", "🍩", "🍪", "🎂", "🍰", "🧁", "🍫", "🍬", "🍭", "🎮", "🕹️", "🎲"
]

# Catégories de mots
WORD_CATEGORIES = {
    "GÉNÉRAL": ["Ferme", "Tracteur", "Plage", "Informatique", "Cuisine", "Voiture", "Montagne", "Pizza", "École", "Musique", "Cinéma", "Sport", "Voyage", "Livre", "Téléphone"],
    "ANIMAUX": ["Chien", "Chat", "Éléphant", "Lion", "Tigre", "Oiseau", "Poisson", "Cheval", "Vache", "Singe", "Girafe", "Dauphin", "Aigle", "Loup", "Ours"],
    "OBJETS": ["Chaise", "Table", "Lampe", "Stylo", "Ordinateur", "Télévision", "Montre", "Sac", "Chaussure", "Lunettes", "Clé", "Bouteille", "Tasse", "Couteau", "Fenêtre"],
    "MÉTIERS": ["Pompier", "Policier", "Médecin", "Professeur", "Boulanger", "Cuisinier", "Agriculteur", "Astronaute", "Acteur", "Chanteur", "Juge", "Avocat", "Plombier", "Électricien", "Coiffeur"],
    "PAYS": ["France", "Espagne", "Italie", "Japon", "Chine", "États-Unis", "Brésil", "Canada", "Allemagne", "Australie", "Russie", "Inde", "Mexique", "Égypte", "Maroc"],
    "SPORT": ["Football", "Tennis", "Basketball", "Rugby", "Natation", "Athlétisme", "Judo", "Boxe", "Golf", "Ski", "Volleyball", "Handball", "Cyclisme", "Escalade", "Surf"], # Ajout de catégories
    "MARQUES": ["Nike", "Adidas", "Apple", "Samsung", "Coca-Cola", "McDonald's", "Disney", "Google", "Amazon", "Tesla", "Microsoft", "Sony", "Lego", "Ikea", "Netflix"],
    "VILLES": ["Paris", "Londres", "New York", "Tokyo", "Rome", "Berlin", "Madrid", "Pékin", "Moscou", "Sydney", "Le Caire", "Rio", "Dubaï", "Amsterdam", "Séoul"],
    "ANIMAUX MARINS": ["Requin", "Dauphin", "Baleine", "Poisson-clown", "Crabe", "Méduse", "Pieuvre", "Étoile de mer", "Hippocampe", "Tortue de mer", "Phoque", "Loutre", "Corail", "Anémone", "Crevette"],
    "INSTRUMENTS": ["Guitare", "Piano", "Batterie", "Violon", "Trompette", "Flûte", "Saxophone", "Clarinette", "Harmonica", "Ukulélé", "Harpe", "Contrebasse", "Synthétiseur", "Accordéon", "Tambour"]
}

# Couleurs d'ambiance par catégorie
CATEGORY_COLORS = {
    "GÉNÉRAL": (20, 25, 35), "ANIMAUX": (34, 80, 34), "OBJETS": (60, 70, 80),
    "MÉTIERS": (100, 70, 40), "PAYS": (30, 40, 90), "SPORT": (120, 30, 30),
    "MARQUES": (150, 50, 20), "VILLES": (80, 30, 100), "ANIMAUX MARINS": (0, 60, 100),
    "INSTRUMENTS": (120, 60, 20), "JEUX VIDÉO": (60, 20, 100), "NOURRITURE": (140, 70, 0),
    "SUPER-HÉROS": (140, 20, 20), "HORREUR": (30, 5, 5)
}

# Couleurs de rareté (Fond de carte)
RARITY_COLORS = {
    "COMMON": (35, 40, 50),      # Gris/Bleu sombre
    "RARE": (20, 50, 90),        # Bleu profond
    "EPIC": (60, 20, 80),        # Violet profond
    "LEGENDARY": (80, 50, 10)    # Or/Orange sombre
}

# Catalogue du Magasin
SHOP_CATALOG = {
    "border_gold": {"type": "border", "name": "Bordure OR", "price": 200, "color": (255, 215, 0), "rarity": "RARE"},
    "border_neon": {"type": "border", "name": "Bordure NÉON", "price": 150, "color": (0, 255, 255), "rarity": "COMMON"},
    "border_fire": {"type": "border", "name": "Bordure FEU", "price": 150, "color": (255, 69, 0), "rarity": "COMMON"},
    "border_royal": {"type": "border", "name": "Bordure ROYALE", "price": 300, "color": (138, 43, 226), "rarity": "EPIC"},
    "border_rainbow": {"type": "border", "name": "Bordure RAINBOW", "price": 400, "color": (255, 0, 255), "rarity": "EPIC"},
    "border_ice": {"type": "border", "name": "Bordure GLACE", "price": 250, "color": (100, 200, 255), "rarity": "RARE"},
    "border_nature": {"type": "border", "name": "Bordure NATURE", "price": 200, "color": (50, 200, 50), "rarity": "COMMON"},
    "border_galaxy": {"type": "border", "name": "Bordure GALAXY", "price": 500, "color": (100, 0, 150), "rarity": "LEGENDARY"},
    "border_pixel": {"type": "border", "name": "Bordure PIXEL", "price": 300, "color": (50, 200, 50), "rarity": "RARE"},
    "border_diamond": {"type": "border", "name": "Bordure DIAMANT", "price": 600, "color": (185, 242, 255), "rarity": "LEGENDARY"},
    "border_lava": {"type": "border", "name": "Bordure LAVE", "price": 450, "color": (207, 16, 32), "rarity": "EPIC"},
    "border_electric": {"type": "border", "name": "Bordure ÉLECTRIQUE", "price": 350, "color": (50, 50, 255), "rarity": "EPIC"},
    "border_shadow": {"type": "border", "name": "Bordure OMBRE", "price": 300, "color": (50, 50, 50), "rarity": "RARE"},
    "border_sun": {"type": "border", "name": "Bordure SOLEIL", "price": 400, "color": (255, 255, 100), "rarity": "EPIC"},
    "border_toxic": {"type": "border", "name": "Bordure TOXIQUE", "price": 350, "color": (100, 255, 50), "rarity": "RARE"},
    "border_double": {"type": "border", "name": "Bordure DOUBLE", "price": 450, "color": (255, 255, 255), "rarity": "EPIC"},
    "border_glitch": {"type": "border", "name": "Bordure GLITCH", "price": 550, "color": (0, 255, 100), "rarity": "EPIC"},
    "border_plasma": {"type": "border", "name": "Bordure PLASMA", "price": 600, "color": (200, 0, 255), "rarity": "LEGENDARY"},
    "border_pulse": {"type": "border", "name": "Bordure PULSE", "price": 550, "color": (0, 255, 200), "rarity": "EPIC"},
    "color_red": {"type": "name_color", "name": "Pseudo ROUGE", "price": 100, "color": (255, 80, 80), "rarity": "COMMON"},
    "color_blue": {"type": "name_color", "name": "Pseudo BLEU", "price": 100, "color": (80, 150, 255), "rarity": "COMMON"},
    "color_gold": {"type": "name_color", "name": "Pseudo OR", "price": 500, "color": (255, 215, 0), "rarity": "EPIC"},
    "color_green": {"type": "name_color", "name": "Pseudo VERT", "price": 100, "color": (80, 255, 80), "rarity": "COMMON"},
    "color_pink": {"type": "name_color", "name": "Pseudo ROSE", "price": 150, "color": (255, 100, 200), "rarity": "COMMON"},
    "color_purple": {"type": "name_color", "name": "Pseudo VIOLET", "price": 200, "color": (180, 80, 255), "rarity": "RARE"},
    "color_cyan": {"type": "name_color", "name": "Pseudo CYAN", "price": 150, "color": (0, 255, 255), "rarity": "COMMON"},
    "color_lime": {"type": "name_color", "name": "Pseudo LIME", "price": 150, "color": (50, 255, 50), "rarity": "COMMON"},
    "color_magenta": {"type": "name_color", "name": "Pseudo MAGENTA", "price": 150, "color": (255, 0, 255), "rarity": "COMMON"},
    "color_silver": {"type": "name_color", "name": "Pseudo ARGENT", "price": 300, "color": (192, 192, 192), "rarity": "EPIC"},
    "color_orange": {"type": "name_color", "name": "Pseudo ORANGE", "price": 150, "color": (255, 165, 0), "rarity": "COMMON"},
    "name_color_dark_red": {"type": "name_color", "name": "Pseudo SANG", "price": 250, "color": (139, 0, 0), "rarity": "RARE"},
    "name_color_fire": {"type": "name_color", "name": "Pseudo FEU (Animé)", "price": 750, "color": (255, 69, 0), "rarity": "LEGENDARY"},
    "name_color_glitch": {"type": "name_color", "name": "Pseudo GLITCH (Animé)", "price": 800, "color": (0, 255, 100), "rarity": "LEGENDARY"},
    "name_color_matrix": {"type": "name_color", "name": "Pseudo MATRIX (Animé)", "price": 900, "color": (0, 255, 0), "rarity": "LEGENDARY"},
    "theme_matrix": {"type": "theme", "name": "Thème MATRIX", "price": 500, "color": (0, 20, 0), "rarity": "LEGENDARY"},
    "theme_ocean": {"type": "theme", "name": "Thème OCÉAN", "price": 250, "color": (0, 30, 60), "rarity": "COMMON"},
    "theme_sunset": {"type": "theme", "name": "Thème SUNSET", "price": 250, "color": (60, 20, 40), "rarity": "COMMON"},
    "theme_forest": {"type": "theme", "name": "Thème FORÊT", "price": 300, "color": (20, 40, 20), "rarity": "RARE"},
    "theme_candy": {"type": "theme", "name": "Thème CANDY", "price": 350, "color": (50, 20, 40), "rarity": "RARE"},
    "theme_space": {"type": "theme", "name": "Thème ESPACE", "price": 400, "color": (10, 10, 20), "rarity": "EPIC"},
    "theme_dark": {"type": "theme", "name": "Thème SOMBRE", "price": 400, "color": (10, 10, 10), "rarity": "EPIC"},
    "theme_retro": {"type": "theme", "name": "Thème RÉTRO", "price": 450, "color": (43, 30, 30), "rarity": "EPIC"},
    "theme_cyber": {"type": "theme", "name": "Thème CYBER", "price": 600, "color": (0, 10, 20), "rarity": "LEGENDARY"},
    "theme_desert": {"type": "theme", "name": "Thème DÉSERT", "price": 300, "color": (60, 40, 20), "rarity": "RARE"},
    "theme_arctic": {"type": "theme", "name": "Thème ARCTIQUE", "price": 300, "color": (200, 220, 255), "rarity": "RARE"},
    "theme_volcano": {"type": "theme", "name": "Thème VOLCAN", "price": 450, "color": (40, 10, 10), "rarity": "EPIC"},
    "theme_midnight": {"type": "theme", "name": "Thème MINUIT", "price": 400, "color": (5, 5, 20), "rarity": "EPIC"},
    "theme_blood": {"type": "theme", "name": "Thème SANG", "price": 500, "color": (40, 0, 0), "rarity": "EPIC"},
    "theme_hacker": {"type": "theme", "name": "Thème HACKER", "price": 600, "color": (0, 0, 0), "rarity": "LEGENDARY"},
    "theme_sunset_city": {"type": "theme", "name": "Thème SUNSET CITY", "price": 500, "color": (80, 40, 60), "rarity": "EPIC"},
    "name_color_rainbow": {"type": "name_color", "name": "Pseudo RAINBOW", "price": 1000, "color": (255, 255, 255), "rarity": "LEGENDARY"},
    "border_ghost": {"type": "border", "name": "Bordure FANTÔME", "price": 400, "color": (200, 200, 200), "rarity": "LEGENDARY"},
    "theme_royal": {"type": "theme", "name": "Thème ROYAL", "price": 800, "color": (40, 0, 40), "rarity": "LEGENDARY"},
    "upgrade_freeze": {"type": "upgrade", "name": "Stock Gel Temps (+1)", "price": 300, "color": (100, 200, 255), "rarity": "RARE"},
    "custom_border_color": {"type": "border", "name": "Bordure Personnalisée", "price": 5000, "color": (255, 255, 255), "rarity": "LEGENDARY"},
    "custom_name_color": {"type": "name_color", "name": "Pseudo Personnalisé", "price": 5000, "color": (255, 255, 255), "rarity": "LEGENDARY"},
    "gift_daily": {"type": "gift", "name": "Cadeau du Jour", "price": 0, "color": (255, 255, 255), "rarity": "COMMON"},
    "cat_videogames": {"type": "category", "name": "JEUX VIDÉO", "price": 500, "color": (100, 100, 255), "content": ["Mario", "Zelda", "Minecraft", "Fortnite", "Tetris", "Pac-Man", "Sonic", "GTA", "Call of Duty", "Pokémon", "Sims", "FIFA", "Among Us", "Roblox", "League of Legends"], "rarity": "EPIC"},
    "cat_food": {"type": "category", "name": "NOURRITURE", "price": 400, "color": (255, 150, 50), "content": ["Sushi", "Burger", "Tacos", "Salade", "Pâtes", "Steak", "Frites", "Glace", "Chocolat", "Pomme", "Banane", "Pain", "Fromage", "Oeuf", "Soupe"], "rarity": "EPIC"},
    "cat_superheroes": {"type": "category", "name": "SUPER-HÉROS", "price": 600, "color": (255, 50, 50), "content": ["Batman", "Superman", "Spiderman", "Iron Man", "Wonder Woman", "Thor", "Hulk", "Captain America", "Flash", "Black Panther", "Aquaman", "Wolverine", "Deadpool", "Thanos", "Joker"], "rarity": "LEGENDARY"},
    "cat_horror": {"type": "category", "name": "HORREUR", "price": 666, "color": (100, 0, 0), "content": ["Fantôme", "Vampire", "Zombie", "Sorcière", "Loup-garou", "Momie", "Squelette", "Démon", "Frankenstein", "Clown", "Hache", "Sang", "Cimetière", "Manoir", "Cauchemar"], "rarity": "LEGENDARY"},
    "badge_vip": {"type": "badge", "name": "Badge VIP", "price": 1000, "icon": "👑", "rarity": "LEGENDARY"},
    "badge_star": {"type": "badge", "name": "Badge Star", "price": 500, "icon": "⭐", "rarity": "EPIC"},
    "badge_heart": {"type": "badge", "name": "Badge Cœur", "price": 200, "icon": "❤️", "rarity": "RARE"},
    "badge_fire": {"type": "badge", "name": "Badge Feu", "price": 300, "icon": "🔥", "rarity": "EPIC"},
    "badge_diamond": {"type": "badge", "name": "Badge Diamant", "price": 2000, "icon": "💎", "rarity": "LEGENDARY"},
    "badge_newbie": {"type": "badge", "name": "Badge Nouveau", "price": 10, "icon": "🌱", "rarity": "COMMON"},
    "badge_pro": {"type": "badge", "name": "Badge Pro", "price": 800, "icon": "🏆", "rarity": "EPIC"},
    "badge_rich": {"type": "badge", "name": "Badge Riche", "price": 5000, "icon": "💰", "rarity": "LEGENDARY"},
    "badge_dev": {"type": "badge", "name": "Badge DEV", "price": 99999, "icon": "🛠️", "rarity": "LEGENDARY", "secret": True},
    "title_rainbow": {"type": "title_style", "name": "Titre RAINBOW", "price": 1000, "color": (255, 0, 255), "rarity": "LEGENDARY"},
    "title_gold": {"type": "title_style", "name": "Titre OR", "price": 800, "color": (255, 215, 0), "rarity": "EPIC"},
    "title_fire": {"type": "title_style", "name": "Titre FEU", "price": 600, "color": (255, 69, 0), "rarity": "RARE"},
    "title_neon": {"type": "title_style", "name": "Titre NÉON", "price": 500, "color": (0, 255, 255), "rarity": "RARE"},
    "title_matrix": {"type": "title_style", "name": "Titre MATRIX", "price": 750, "color": (0, 255, 0), "rarity": "EPIC"},
    "title_ice": {"type": "title_style", "name": "Titre GLACE", "price": 500, "color": (100, 200, 255), "rarity": "RARE"},
    "title_void": {"type": "title_style", "name": "Titre NÉANT", "price": 1200, "color": (20, 0, 40), "rarity": "LEGENDARY"},
    "border_season1": {"type": "border", "name": "Bordure SAISON 1", "price": 0, "color": (0, 255, 128), "rarity": "LEGENDARY", "secret": True},
    "theme_season1": {"type": "theme", "name": "Thème SAISON 1", "price": 0, "color": (0, 40, 20), "rarity": "LEGENDARY", "secret": True},
    "badge_season1": {"type": "badge", "name": "Badge SAISON 1", "price": 0, "icon": "🥇", "rarity": "LEGENDARY", "secret": True},
    "name_color_season1": {"type": "name_color", "name": "Pseudo SAISON 1", "price": 0, "color": (0, 255, 128), "rarity": "LEGENDARY", "secret": True}
}

ACHIEVEMENTS = {
    # --- Victoires ---
    "WIN_1": {"name": "Première Victoire", "desc": "Gagner 1 partie", "reward": 50, "stat": "wins", "target": 1},
    "WIN_10": {"name": "Champion", "desc": "Gagner 10 parties", "reward": 200, "stat": "wins", "target": 10},
    "WIN_50": {"name": "Légende", "desc": "Gagner 50 parties", "reward": 1000, "stat": "wins", "target": 50},
    "WIN_100": {"name": "Divinité", "desc": "Gagner 100 parties", "reward": 2000, "stat": "wins", "target": 100},
    "WIN_250": {"name": "Immortel", "desc": "Gagner 250 parties", "reward": 5000, "stat": "wins", "target": 250},
    "PLAY_100": {"name": "Accro", "desc": "Jouer 100 parties", "reward": 1000, "stat": "games", "target": 100},

    # --- Niveaux ---
    "LEVEL_5": {"name": "Apprenti", "desc": "Atteindre le niveau 5", "reward": 100, "stat": "level", "target": 5},
    "LEVEL_10": {"name": "Vétéran", "desc": "Atteindre le niveau 10", "reward": 300, "stat": "level", "target": 10},
    "LEVEL_25": {"name": "Maître", "desc": "Atteindre le niveau 25", "reward": 500, "stat": "level", "target": 25},
    "LEVEL_50": {"name": "Grand Maître", "desc": "Atteindre le niveau 50", "reward": 1000, "stat": "level", "target": 50},
    "LEVEL_100": {"name": "Sage", "desc": "Atteindre le niveau 100", "reward": 2500, "stat": "level", "target": 100},

    # --- Économie ---
    "RICH_500": {"name": "Économe", "desc": "Posséder 500 pièces", "reward": 100, "stat": "coins", "target": 500},
    "RICH_2000": {"name": "Millionnaire", "desc": "Posséder 2000 pièces", "reward": 500, "stat": "coins", "target": 2000},
    "RICH_10000": {"name": "Crésus", "desc": "Posséder 10000 pièces", "reward": 1000, "stat": "coins", "target": 10000},
    "RICH_50000": {"name": "Milliardaire", "desc": "Posséder 50000 pièces", "reward": 5000, "stat": "coins", "target": 50000},
    "SPENDER_1000": {"name": "Dépensier", "desc": "Dépenser 1000 pièces", "reward": 200, "stat": "spent_coins", "target": 1000},
    "SPENDER_5000": {"name": "Mécène", "desc": "Dépenser 5000 pièces", "reward": 1000, "stat": "spent_coins", "target": 5000},
    "SPENDER_20000": {"name": "Philanthrope", "desc": "Dépenser 20000 pièces", "reward": 2000, "stat": "spent_coins", "target": 20000},

    # --- Social ---
    "SOCIAL_1": {"name": "Amical", "desc": "Ajouter 1 ami", "reward": 50, "stat": "friends", "target": 1},
    "SOCIAL_5": {"name": "Populaire", "desc": "Avoir 5 amis", "reward": 200, "stat": "friends", "target": 5},
    "SOCIAL_10": {"name": "Star des réseaux", "desc": "Avoir 10 amis", "reward": 500, "stat": "friends", "target": 10},

    # --- Collection ---
    "SHOPPER_1": {"name": "Client", "desc": "Acheter 1 objet", "reward": 50, "stat": "inventory", "target": 4},
    "COLLECTOR_10": {"name": "Collectionneur", "desc": "Posséder 10 objets", "reward": 300, "stat": "inventory", "target": 10},
    "COLLECTOR_25": {"name": "Collectionneur Émérite", "desc": "Posséder 25 objets", "reward": 500, "stat": "inventory", "target": 25},
    "COLLECTOR_50": {"name": "Archiviste", "desc": "Posséder 50 objets", "reward": 1000, "stat": "inventory", "target": 50},
    "SHOP_KING": {"name": "Roi du Shopping", "desc": "Acheter tous les objets", "reward": 5000, "stat": "shop_king", "target": 1},

    # --- Gameplay ---
    "COMBO_10": {"name": "Speedster", "desc": "Atteindre un combo de 10", "reward": 500, "stat": "max_combo", "target": 10},
    "COMBO_20": {"name": "Dieu du Combo", "desc": "Atteindre un combo de 20", "reward": 1000, "stat": "max_combo", "target": 20},
    "COMBO_30": {"name": "Intouchable", "desc": "Atteindre un combo de 30", "reward": 2000, "stat": "max_combo", "target": 30},
    "SURVIVOR_1": {"name": "Survivant", "desc": "Gagner 1 partie en Survie", "reward": 250, "stat": "wins_per_mode.SURVIVAL", "target": 1},
    "SURVIVOR_10": {"name": "Maître de la Survie", "desc": "Gagner 10 parties en Survie", "reward": 500, "stat": "wins_per_mode.SURVIVAL", "target": 10},
    "TIME_ATTACKER_1": {"name": "Chronométreur", "desc": "Gagner 1 partie Contre-la-montre", "reward": 250, "stat": "wins_per_mode.TIME_TRIAL", "target": 1},
    "TIME_ATTACKER_10": {"name": "Maître du Temps", "desc": "Gagner 10 parties Contre-la-montre", "reward": 500, "stat": "wins_per_mode.TIME_TRIAL", "target": 10},
    "HARDCORE_WIN_1": {"name": "Nerveux", "desc": "Gagner 1 partie en Hardcore", "reward": 500, "stat": "wins_per_mode.HARDCORE", "target": 1},
    "HARDCORE_WIN_10": {"name": "Dieu du Hardcore", "desc": "Gagner 10 parties en Hardcore", "reward": 1000, "stat": "wins_per_mode.HARDCORE", "target": 10},

    # --- Secrets ---
    "SECRET_WIZZ": {"name": "Gênant", "desc": "Utiliser le Wizz pour la première fois", "reward": 25, "stat": "wizz_used", "target": 1, "secret": True},
    "SECRET_LOGIN_7": {"name": "Fidèle", "desc": "Atteindre une série de 7 jours de connexion", "reward": 250, "stat": "login_streak", "target": 7, "secret": True},
    "SECRET_CUSTOM_CAT": {"name": "Créateur", "desc": "Créer une catégorie personnalisée", "reward": 100, "stat": "custom_categories", "target": 1, "secret": True},
    "SECRET_CUSTOM_AVATAR": {"name": "Unique", "desc": "Utiliser un avatar personnalisé", "reward": 100, "stat": "custom_avatar", "target": 1, "secret": True},
    "SECRET_PERFECT_LOSE": {"name": "Humiliation", "desc": "Perdre une partie sans marquer de point", "reward": 50, "stat": "perfect_lose", "target": 1, "secret": True},
    "SECRET_DEV_MODE": {"name": "Curieux", "desc": "Activer le mode développeur", "reward": 10, "stat": "dev_mode", "target": 1, "secret": True},
    "SECRET_TRADE": {"name": "Commerçant", "desc": "Réussir un échange avec un ami", "reward": 100, "stat": "trade_success", "target": 1, "secret": True},
}

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None, font=None, text_color=None, scale_on_hover=False, notification=False, tag=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = font if font else pygame.font.SysFont("Arial", 26, bold=True)
        self.text_color = text_color if text_color else (20, 25, 35)
        self.scale_on_hover = scale_on_hover
        self.notification = notification
        self.hover_progress = 0.0
        self.creation_time = pygame.time.get_ticks()
        self.tag = tag
        self.click_time = 0
        self.click_pos = (0, 0)
        self.cached_surf = None

    def interpolate_color(self, c1, c2, t):
        return (
            max(0, min(255, int(c1[0] + (c2[0] - c1[0]) * t))),
            max(0, min(255, int(c1[1] + (c2[1] - c1[1]) * t))),
            max(0, min(255, int(c1[2] + (c2[2] - c1[2]) * t)))
        )

    def draw(self, screen, offset_y=0):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animation d'apparition (Slide Up)
        now = pygame.time.get_ticks()
        anim_progress = min(1.0, (now - self.creation_time) / 300.0)
        anim_progress = 1 - (1 - anim_progress) ** 3 # Ease Out Cubic
        anim_y = (1.0 - anim_progress) * 50 # Décalage de 50px vers le bas au début

        # Animation fluide
        target = 1.0 if is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.15
        
        current_color = self.interpolate_color(self.color, self.hover_color, self.hover_progress)
        
        # Effet d'enfoncement
        is_pressed = is_hovered and pygame.mouse.get_pressed()[0]
        offset = 3 if is_pressed else 0
        
        # Ombre portée (fixe)
        shadow_rect = self.rect.copy()
        shadow_rect.y += 6 - offset + anim_y + offset_y
        s = pygame.Surface((shadow_rect.w, shadow_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 60), s.get_rect(), border_radius=15)
        screen.blit(s, shadow_rect)

        # Corps du bouton (mobile)
        btn_rect = self.rect.copy()
        btn_rect.y += offset + anim_y + offset_y
        
        # Bordure (plus foncée)
        darker = (max(0, current_color[0]-40), max(0, current_color[1]-40), max(0, current_color[2]-40))
        pygame.draw.rect(screen, darker, btn_rect, border_radius=15)
        
        # Intérieur
        inner_rect = btn_rect.inflate(-4, -4)
        pygame.draw.rect(screen, current_color, inner_rect, border_radius=12)
        
        # Reflet supérieur (Glassy)
        gloss_rect = pygame.Rect(inner_rect.x, inner_rect.y, inner_rect.w, inner_rect.h // 2)
        s_gloss = pygame.Surface((gloss_rect.w, gloss_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s_gloss, (255, 255, 255, 40), s_gloss.get_rect(), border_top_left_radius=12, border_top_right_radius=12)
        screen.blit(s_gloss, gloss_rect)

        # Texte
        lines = self.text.split('\n')
        line_height = self.font.get_height()
        total_height = len(lines) * line_height
        start_y = btn_rect.centery - total_height / 2

        for i, line in enumerate(lines):
            # Optimisation Cache (Si pas d'animation de scale)
            if not self.scale_on_hover and self.cached_surf and len(lines) == 1: text_surf = self.cached_surf
            else:
                text_surf = self.font.render(line, True, self.text_color)
                if not self.scale_on_hover and len(lines) == 1: self.cached_surf = text_surf
            
            # Zoom texte au survol
            if self.scale_on_hover and self.hover_progress > 0.05:
                scale = 1.0 + (0.1 * self.hover_progress)
                w = int(text_surf.get_width() * scale)
                h = int(text_surf.get_height() * scale)
                text_surf = pygame.transform.smoothscale(text_surf, (w, h))
            
            text_rect = text_surf.get_rect(center=(btn_rect.centerx, start_y + i * line_height + line_height / 2))
            
            # Ombre texte si couleur claire
            if sum(self.text_color) > 300: 
                shadow_txt = self.font.render(line, True, (0,0,0))
                if self.scale_on_hover and self.hover_progress > 0.05:
                    shadow_txt = pygame.transform.smoothscale(shadow_txt, (text_surf.get_width(), text_surf.get_height()))
                shadow_txt.set_alpha(80)
                shadow_rect = shadow_txt.get_rect(center=(text_rect.centerx+1, text_rect.centery+2))
                screen.blit(shadow_txt, shadow_rect)
                
            screen.blit(text_surf, text_rect)
            
        # Effet Ripple (Onde de clic)
        if now - self.click_time < 400:
            radius = (now - self.click_time) * 0.8
            alpha = int(max(0, 200 - (now - self.click_time) * 0.5))
            if alpha > 0:
                s_ripple = pygame.Surface((btn_rect.w, btn_rect.h), pygame.SRCALPHA)
                
                # Cercle de l'onde
                pygame.draw.circle(s_ripple, (255, 255, 255, alpha), (self.click_pos[0] - btn_rect.x, self.click_pos[1] - btn_rect.y), int(radius))
                
                # Masque pour arrondir les coins (Clipping)
                mask = pygame.Surface((btn_rect.w, btn_rect.h), pygame.SRCALPHA)
                pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=12)
                s_ripple.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                
                screen.blit(s_ripple, btn_rect, special_flags=pygame.BLEND_RGBA_ADD)

        if self.notification:
            pygame.draw.circle(screen, (255, 50, 50), (btn_rect.right - 10, btn_rect.top + 10), 8 + (2 * math.sin(now * 0.01)))
            pygame.draw.circle(screen, (255, 255, 255), (btn_rect.right - 10, btn_rect.top + 10), 8 + (2 * math.sin(now * 0.01)), 2)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.click_time = pygame.time.get_ticks()
                self.click_pos = event.pos
                if self.action:
                    self.action()
                return True
        return False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Jeu d'Association Rapide")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.title_font = pygame.font.SysFont("Impact", 100)
        try:
            self.emoji_font = pygame.font.SysFont("Segoe UI Emoji", 80)
            self.ui_emoji_font = pygame.font.SysFont("Segoe UI Emoji", 32)
        except:
            self.emoji_font = pygame.font.SysFont("Arial", 80, bold=True)
            self.ui_emoji_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 45, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 38, bold=True)
        self.small_bold_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.timer_font = pygame.font.SysFont("Consolas", 80, bold=True) # Police fixe pour chrono fluide
        
        # Icône de fenêtre (Générée dynamiquement)
        icon = pygame.Surface((32, 32))
        icon.fill(ACCENT_COLOR)
        pygame.draw.circle(icon, (255, 255, 255), (16, 16), 10)
        pygame.display.set_icon(icon)
        
        # États du jeu
        self.state = "INPUT_NAME" # INPUT_NAME, MENU_MAIN, MENU_ONLINE, SETUP, SETTINGS, CONTROLS, LOBBY, HOW_TO, GAME, JUDGMENT, GAME_OVER, ROUND_COUNTDOWN, OPPONENT_LEFT
        
        # Paramètres de la partie
        self.settings = {
            'players': 2,
            'time': 5,
            'mode': 'VOCAL',
            'win_score': 5,
            'category': 'GÉNÉRAL',
            'game_type': 'NORMAL'
        }

        # Touches
        self.keys = {
            "VALIDATE": pygame.K_RETURN,
            "CONTEST": pygame.K_LSHIFT,
            "VOCAL_VALIDATE": pygame.K_SPACE
        }

        self.current_word = ""
        self.user_text = ""
        self.start_ticks = 0
        self.round_duration = 5.0
        self.time_left = 0
        self.opponent_text = "" # Texte de l'adversaire en temps réel
        self.opponent_name = "Adversaire"
        self.score = [0, 0] # Joueur 1, Joueur 2
        self.opponent_level = 1
        self.avatar = AVATARS[0]
        self.opponent_avatar = "🙂"
        self.opponent_border = "border_default"
        self.opponent_name_color = "name_color_default"
        self.opponent_badge = "badge_default"
        self.opponent_win_streak = 0
        self.current_player = 0 # 0 (Host) ou 1 (Client)
        self.my_id = 0 # Mon identité
        self.winner_text = ""
        self.username = ""
        self.rematch_ready = [False, False] # [Host, Client] ou [J1, J2...]
        self.judge_id = -1
        self.round_num = 1
        self.turn_count = 0 # Compteur d'échanges dans la manche (pour Survival)
        self.rally_combo = 0 # Compteur de combo (réponses rapides)
        self.countdown_start = 0
        self.last_round_reason = "" # TIMEOUT ou NORMAL
        self.last_round_winner = -1
        self.particles = []
        self.public_ip = None
        self.local_ip = ""
        self.upnp_status = "Non tenté"
        self.upnp_control_url = None
        self.upnp_service_type = None
        self.chat_messages = []
        self.chat_input = ""
        self.ready_status = [False, False] # [J1, J2]
        self.first_run = True
        self.bot_msg_index = 0
        self.friends = []
        self.friend_name_input = ""
        self.friend_code_input = ""
        self.cat_name_input = ""
        self.cat_words_input = ""
        self.custom_categories = {}
        self.all_categories = WORD_CATEGORIES.copy()
        self.sound_on = True
        self.used_words = []
        self.feedback_msg = ""
        self.feedback_timer = 0
        self.prev_state = "MENU_MAIN"
        self.shake_timer = 0
        self.chat_scroll = 0
        self.avatar_scroll = 0
        self.avatar_grid_buttons = []
        self.menu_particles = []
        self.theme_particles = []
        self.last_click = 0
        self.trade_amount = "0"
        self.shop_scroll = 0
        self.shop_tab = "ALL" # ALL, BORDER, THEME
        self.inventory_scroll = 0
        self.inventory_tab = "ALL"
        self.achievements_scroll = 0
        self.achievements_filter = "ALL"
        self.shop_sort = "TYPE"
        self.card_hover_anims = {}
        self.current_frame_card_offsets = {}
        self.current_freezes = 0
        self.freeze_until = 0
        self.global_timer_start = 0
        self.paused_at = 0
        self.opponent_left_time = 0
        
        # Daily Login
        self.login_streak = 0
        self.last_login_date = ""
        # Notifications
        self.notifications = []
        self.coin_particles = []
        
        # Crop Avatar
        self.crop_image = None
        self.crop_scale = 1.0
        self.crop_offset = [0, 0]
        self.crop_dragging = False
        self.crop_last_mouse = (0, 0)

        # Color Picker
        self.custom_colors = {"border": (255, 255, 255), "name_color": (255, 255, 255)}
        self.color_picker_target = None # 'border' or 'name_color'
        self.color_picker_sliders = {} # Will hold rects for sliders
        self.color_picker_values = {'r': 255, 'g': 255, 'b': 255}
        self.active_slider = None
        
        self.game_emotes = [] # Liste des emotes flottantes en jeu
        self.floating_texts = [] # Textes flottants (Combo, etc.)
        self.last_wizz_time = 0 # Cooldown Wizz
        self.last_heartbeat = 0 # Pour le son du chrono
        # Animation XP
        self.anim_xp_val = 0.0
        self.anim_level_val = 1
        self.target_xp_val = 0
        self.target_level_val = 1
        self.xp_animating = False
        
        self.avatar_cache = {} # Cache pour les images décodées
        # Économie
        self.coins = 100
        self.xp = 0
        self.level = 1
        self.last_shop_date = ""
        self.last_gift_date = ""
        self.inventory = ["border_default", "theme_default"]
        self.equipped = {"border": "border_default", "theme": "theme_default", "badge": "badge_default", "title_style": "title_default"}
        self.last_daily_challenge_date = ""
        self.achievements_unlocked = []
        self.stats = {"wins": 0, "games": 0, "history": [], "max_combo": 0, "spent_coins": 0, "wizz_used": False, "wins_per_mode": {}, "custom_avatar": False, "perfect_lose": False, "dev_mode": False, "trade_success": False, "border_xp": {}, "win_streak": 0, "season": {"level": 1, "xp": 0, "claimed": []}, "used_codes": []}
        self.local_player_names = []
        self.coin_fly_particles = []
        self.temp_coin_display_timer = 0
        self.display_coins = self.coins
        self.custom_cats_scroll = 0
        self.season_scroll = 0
        self.active_local_name_idx = -1
        
        self.achievement_queue = []
        self.current_achievement = None
        
        # Vignette (Modern UI)
        self.create_vignette()
        
        # Transition
        self.transition_alpha = 0
        self.transition_state = None
        self.next_state = None
        self.transition_color = (0, 0, 0)
        self.update_available = False
        self.is_updating = False
        self.update_progress_text = ""
        self.update_ready_to_restart = False
        
        # Réseau
        self.server = None
        self.conn = None
        self.input_ip = "127.0.0.1"
        self.network_queue = []
        self.is_host = False
        self.connected = False
        self.clients = [] # Liste des clients connectés (Host)
        # RLock pour éviter les deadlocks en cas d'appels imbriqués (ex: broadcast -> send_data)
        self.clients_lock = threading.RLock()
        self.is_local_game = False
        self.is_connecting = False
        self.is_training = False
        self.bot_difficulty = "MOYEN"
        self.connect_status = "" # "", "CONNECTING", "FAILED"
        
        # Mode Test / Debug
        self.test_mode = False
        self.t_press_count = 0
        self.last_t_press = 0
        self.bot_timer = 0
        self.bot_next_move_time = 0
        self.cheat_buffer = ""
        pygame.scrap.init()
        
        # --- NOUVEAU SYSTÈME (Popup, Trade, Listener) ---
        self.popup = None # {title, msg, avatar, yes, no}
        self.friend_req_event = threading.Event()
        self.friend_req_result = None
        self.lobby_cache = {} # Cache des joueurs pour le client
        self.trade_lobby_data = {"me": {"coins": 0, "items": [], "locked": False}, "them": {"coins": 0, "items": [], "locked": False}, "countdown": None}
        self.trade_coin_particles = []
        self.trade_finalize_at = 0
        self.friends_menu_from_lobby = False
        self.hovered_friend_idx = -1
        self.selected_lobby_player_id = None
        self.lobby_player_rects = {}
        self.upnp_enabled = True
        self.refresh_btn_rect = None
        self.tooltip_rect = None
        self.friends_status = {}
        self.is_fetching_ip = False
        self.server_port = DEFAULT_PORT
        self.external_port = DEFAULT_PORT
        
        # --- Custom Port Support ---
        self.join_custom_port = False
        self.friend_custom_port = False
        self.input_port_val = str(DEFAULT_PORT)
        self.friend_port_val = str(DEFAULT_PORT)
        self.active_input_field = None
        
        # --- INITIALISATION RÉSEAU AU DÉMARRAGE ---
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.local_ip = s.getsockname()[0]
            s.close()
        except:
            self.local_ip = socket.gethostbyname(socket.gethostname())

        # --- MINI-JEU BONUS ---
        self.bonus_targets = []
        self.bonus_end_time = 0
        
        # Roue de la Fortune
        self.last_spin_date = ""
        self.wheel_angle = 0
        self.wheel_velocity = 0
        self.wheel_spinning = False
        self.spin_result = None
        self.wheel_segments = ["50", "100", "200", "500", "1000", "JACKPOT", "ITEM", "25"]
        self.wheel_colors = [(200, 50, 50), (50, 200, 50), (50, 50, 200), (200, 200, 50), (200, 50, 200), (255, 215, 0), (0, 255, 255), (100, 100, 100)]
        
        # Audio Cross-Platform (Génération des sons)
        self.generate_default_sounds()

        # Résolutions
        self.resolutions = [(1280, 720), (1600, 900), (1800, 980), (1920, 1080)]
        self.res_index = 2

        self.daily_reward_claimed = False
        self.load_settings()
        self.external_port = self.server_port # Init external to internal before UPnP

        # Démarrage du listener global pour recevoir des demandes n'importe où
        threading.Thread(target=self.start_global_listener, daemon=True).start()
        threading.Thread(target=self.get_public_ip, daemon=True).start()
        if self.upnp_enabled:
            threading.Thread(target=self.try_upnp, daemon=True).start()
        
        # Ajustement automatique de la résolution si l'écran est trop petit (Laptop)
        info = pygame.display.Info()
        sw, sh = info.current_w, info.current_h
        current_res = self.resolutions[self.res_index]
        if current_res[0] > sw or current_res[1] > sh:
            best_idx = 0
            for i, res in enumerate(self.resolutions):
                if res[0] <= sw and res[1] <= sh:
                    best_idx = i
            self.res_index = best_idx
            
        self.apply_resolution() # Appliquer la résolution chargée

        # Animation de démarrage
        self.startup_start_time = 0 # 0 pour démarrer au premier frame de la boucle
        self.state = "STARTUP_ANIM"
        if self.first_run:
            self.post_anim_state = "TUTORIAL"
        elif self.username:
            self.post_anim_state = "MENU_MAIN"
        else:
            self.post_anim_state = "INPUT_NAME"
            
        # Pré-rendu Animation (Plus fiable et performant)
        try: self.anim_font_obj = pygame.font.SysFont("Impact", 150)
        except: self.anim_font_obj = pygame.font.SysFont("Arial", 150, bold=True)
        self.anim_surf = self.anim_font_obj.render("dodosi", True, ACCENT_COLOR)
        self.anim_surf_white = self.anim_font_obj.render("dodosi", True, (255, 255, 255))
        self.anim_glow = self.anim_font_obj.render("dodosi", True, (255, 255, 255))
        self.anim_glow.set_alpha(60)
            
        # UI
        self.buttons = []
        self.create_menu_buttons()
        
        # Fonctionnalités Cool
        self.konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
        self.konami_index = 0
        self.news_scroll = SCREEN_WIDTH
        self.news_items = [
            "Astuce : Le mode Survie rapporte plus d'XP.", 
            "Psst... Essayez le code RUSH2024 !", 
            "Le pseudo du créateur (dodosiiii) est un code magique...", 
            "Nouveau ? Tapez WELCOME dans les options !",
            "Invitez vos amis pour échanger des objets !", 
            "Nouveau thème Matrix disponible !", 
            "Essayez le Konami Code...", 
            "Tapez /help dans le chat !", 
            "Devenez une LÉGENDE au niveau 100 !",
            "Aussi disponible sur grille-pain !",
            "Ne mangez pas la neige jaune.",
            "Creeper ? Aw man.",
            "Le gâteau est un mensonge.",
            "World Rush > Les devoirs.",
            "100% Python, 0% Gluten.",
            "Attention derrière toi !",
            "Si vous lisez ceci, vous ne jouez pas.",
            "Mieux que Fortnite (selon ma mère).",
            "Erreur 404 : Skill non trouvé.",
            "N'oubliez pas de boire de l'eau.",
            "Le mode Chaos est imprévisible !",
            "Wizz ton adversaire avec Ctrl+B !",
            "Appuyez sur Alt+F4 pour un bonus (non je rigole).",
            "Chargement des textures... 99%...",
            "Ne nourrissez pas les trolls.",
            "J'ai perdu The Game.",
            "May the Force be with you.",
            "Winter is coming.",
            "Il n'y a pas de cuillère.",
            "Je suis ton père.",
            "Vers l'infini et au-delà !",
            "C'est pas faux.",
            "On en a gros !",
            "Le gras, c'est la vie.",
            "Coucou maman, je passe à la télé !",
            "Sponsorisé par la flemme.",
            "Si ça bug, c'est une feature.",
            "Ctrl+Z ne marche pas dans la vraie vie.",
            "N'oubliez pas de cligner des yeux.",
            "Respirez manuellement maintenant.",
            "Vous lisez encore ça ?",
            "Allez jouer au lieu de lire !",
            "Le niveau 100 est un mythe.",
            "Attention, ce jeu rend accro.",
            "Plus de 8000 lignes de code (et de bugs).",
            "Un jour je serai le meilleur dresseur.",
            "Pika Pika !",
            "Hadouken !",
            "It's a me, Mario !",
            "Snake ? Snake ? SNAAAAAAKE !",
            "All your base are belong to us.",
            "Do a barrel roll !",
            "Fus Ro Dah !",
            "Je s'appelle Groot.",
            "Wakanda Forever.",
            "Hakuna Matata.",
            "Libérée, délivrée...",
            "Mon précieux...",
            "Vous ne passerez pas !",
            "Run, Forrest, Run !",
            "Houston, on a un problème.",
            "Hasta la vista, baby.",
            "I'll be back.",
            "E.T. téléphone maison.",
            "Nom de Zeus !"
        ]
        random.shuffle(self.news_items)
        self.news_items.insert(0, "Bienvenue sur World Rush !")
        self.news_ticker_finished = False
        
        # Formes flottantes (Amélioration Graphique)
        self.cached_sun_surf = None # Cache pour le soleil (Optimisation)
        self.gift_code_input = ""
        self.floating_shapes = []
        for _ in range(20):
            self.floating_shapes.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(20, 100),
                'speed': random.uniform(0.2, 0.8),
                'angle': random.uniform(0, 360),
                'rot_speed': random.uniform(-0.5, 0.5),
                'shape': random.choice(['rect', 'circle', 'triangle'])
            })
        self.daily_challenge_active = False
        self.snake_data = {}
        self.panel_cache = {}

    def interpolate_color(self, c1, c2, t):
        return (
            max(0, min(255, int(c1[0] + (c2[0] - c1[0]) * t))),
            max(0, min(255, int(c1[1] + (c2[1] - c1[1]) * t))),
            max(0, min(255, int(c1[2] + (c2[2] - c1[2]) * t)))
        )

    def parse_address(self, addr_str, default_port=DEFAULT_PORT):
        ip = addr_str
        port = default_port
        if ":" in addr_str:
            try:
                parts = addr_str.split(":")
                ip = parts[0]
                port = int(parts[1])
            except:
                pass
        return ip, port

    def toggle_join_port(self):
        self.join_custom_port = not self.join_custom_port
        self.create_menu_buttons()

    def toggle_friend_port(self):
        self.friend_custom_port = not self.friend_custom_port
        self.create_menu_buttons()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self.username = data.get("username", "")
                    self.avatar = data.get("avatar", AVATARS[0])
                    self.sound_on = data.get("sound", True)
                    self.first_run = data.get("first_run", True)
                    # Charger les touches si elles existent
                    saved_keys = data.get("keys", {})
                    self.friends = data.get("friends", [])
                    for k, v in saved_keys.items():
                        self.keys[k] = v
                    self.custom_categories = data.get("custom_categories", {})
                    self.xp = data.get("xp", 0)
                    self.level = data.get("level", 1)
                    self.coins = data.get("coins", 100)
                    self.upnp_enabled = data.get("upnp_enabled", True)
                    self.inventory = data.get("inventory", ["border_default", "theme_default", "name_color_default"])
                    self.equipped = data.get("equipped", {"border": "border_default", "theme": "theme_default", "name_color": "name_color_default", "badge": "badge_default", "title_style": "title_default"})
                    if "name_color" not in self.equipped: self.equipped["name_color"] = "name_color_default"
                    if "badge" not in self.equipped: self.equipped["badge"] = "badge_default"
                    if "title_style" not in self.equipped: self.equipped["title_style"] = "title_default"
                    if "name_color_default" not in self.inventory: self.inventory.append("name_color_default")
                    if "badge_default" not in self.inventory: self.inventory.append("badge_default")
                    if "title_default" not in self.inventory: self.inventory.append("title_default")
                    self.settings['game_type'] = data.get("game_type", "NORMAL")
                    self.last_shop_date = data.get("last_shop_date", "")
                    self.last_gift_date = data.get("last_gift_date", "")
                    self.last_daily_challenge_date = data.get("last_daily_challenge_date", "")
                    self.achievements_unlocked = data.get("achievements", [])
                    self.stats = data.get("stats", self.stats) # Garde la structure par défaut si non trouvé
                    if "history" not in self.stats: self.stats["history"] = []
                    if "max_combo" not in self.stats: self.stats["max_combo"] = 0
                    self.server_port = data.get("server_port", DEFAULT_PORT)
                    if "spent_coins" not in self.stats: self.stats["spent_coins"] = 0
                    if "wizz_used" not in self.stats: self.stats["wizz_used"] = False
                    if "wins_per_mode" not in self.stats: self.stats["wins_per_mode"] = {}
                    if "custom_avatar" not in self.stats: self.stats["custom_avatar"] = False
                    if "perfect_lose" not in self.stats: self.stats["perfect_lose"] = False
                    if "dev_mode" not in self.stats: self.stats["dev_mode"] = False
                    if "trade_success" not in self.stats: self.stats["trade_success"] = False
                    if "border_xp" not in self.stats: self.stats["border_xp"] = {}
                    if "win_streak" not in self.stats: self.stats["win_streak"] = 0
                    if "used_codes" not in self.stats: self.stats["used_codes"] = []
                    if "season" not in self.stats: self.stats["season"] = {"level": 1, "xp": 0, "claimed": []}
                    self.res_index = data.get("res_index", 2)
                    self.custom_colors = data.get("custom_colors", {"border": (255, 255, 255), "name_color": (255, 255, 255)})
                    self.login_streak = data.get("login_streak", 0)
                    self.last_spin_date = data.get("last_spin_date", "")
                    self.last_login_date = data.get("last_login_date", "")
            except:
                pass
        self.refresh_categories()

    def refresh_categories(self):
        self.all_categories = WORD_CATEGORIES.copy()
        self.all_categories.update(self.custom_categories)
        # Ajouter les catégories achetées (Source de vérité : Inventaire)
        for item_id in self.inventory:
            if item_id in SHOP_CATALOG and SHOP_CATALOG[item_id].get('type') == 'category':
                self.all_categories[SHOP_CATALOG[item_id]['name']] = SHOP_CATALOG[item_id]['content']

    def save_settings(self):
        # Sauvegarder pseudo et touches
        data = {
            "username": self.username, "avatar": self.avatar, "sound": self.sound_on, 
            "keys": self.keys, "first_run": self.first_run, "friends": self.friends, 
            "xp": self.xp, "level": self.level, "custom_categories": self.custom_categories,
            "coins": self.coins, "inventory": self.inventory, "equipped": self.equipped, "game_type": self.settings.get('game_type', 'NORMAL'), "last_daily_challenge_date": self.last_daily_challenge_date,
            "last_shop_date": self.last_shop_date, "last_gift_date": self.last_gift_date, "res_index": self.res_index, "custom_colors": self.custom_colors,
            "achievements": self.achievements_unlocked, "stats": self.stats, "last_spin_date": self.last_spin_date,
            "login_streak": self.login_streak, "last_login_date": self.last_login_date,
            "upnp_enabled": self.upnp_enabled,
            "server_port": self.server_port
        }
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def confirm_reset(self):
        self.popup = {
            "type": "RESET_CONFIRM",
            "title": "RÉINITIALISATION",
            "msg": "Suppression complète des données locales.",
            "avatar": "⚠️",
            "yes_text": "OUI, TOUT EFFACER",
            "no_text": "ANNULER",
            "yes": self.perform_reset,
            "no": lambda: setattr(self, 'popup', None)
        }

    def perform_reset(self):
        self.reset_network()
        # Suppression des fichiers
        if os.path.exists(SETTINGS_FILE):
            try: os.remove(SETTINGS_FILE)
            except: pass
        if os.path.exists(HISTORY_FILE):
            try: os.remove(HISTORY_FILE)
            except: pass
        
        # Remise à zéro des variables
        self.username = ""
        self.avatar = AVATARS[0]
        self.xp = 0
        self.level = 1
        self.coins = 100
        self.inventory = ["border_default", "theme_default", "name_color_default", "title_default"]
        self.equipped = {"border": "border_default", "theme": "theme_default", "name_color": "name_color_default", "badge": "badge_default", "title_style": "title_default"}
        self.achievements_unlocked = []
        self.all_categories = WORD_CATEGORIES.copy()
        self.custom_categories = {}
        self.friends = []
        self.stats = {"wins": 0, "games": 0, "history": [], "max_combo": 0, "spent_coins": 0, "wizz_used": False, "wins_per_mode": {}, "custom_avatar": False, "perfect_lose": False, "dev_mode": False, "trade_success": False, "border_xp": {}, "win_streak": 0, "used_codes": [], "season": {"level": 1, "xp": 0, "claimed": []}}
        self.settings['players'] = 2
        self.settings['win_score'] = 5
        self.settings['game_type'] = 'NORMAL'
        self.first_run = True
        self.login_streak = 0
        self.last_login_date = ""
        self.last_spin_date = ""
        self.last_gift_date = ""
        self.last_daily_challenge_date = ""
        
        self.popup = None
        self.state = "INPUT_NAME"
        self.create_menu_buttons()
        self.show_notification("Jeu réinitialisé à neuf !", "success")

    def close_tutorial(self):
        self.first_run = False
        self.save_settings()
        if not self.username:
            self.state = "INPUT_NAME"
        else:
            self.state = "MENU_MAIN"
        self.create_menu_buttons()

    def create_vignette(self):
        self.vignette_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Dégradé vertical pour le fond
        for y in range(SCREEN_HEIGHT):
            alpha = int((y / SCREEN_HEIGHT) * 100)
            pygame.draw.line(self.vignette_surf, (0, 0, 0, alpha), (0, y), (SCREEN_WIDTH, y))
        pygame.draw.rect(self.vignette_surf, (0, 0, 0, 40), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 30)
        pygame.draw.rect(self.vignette_surf, (0, 0, 0, 80), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)

    def apply_resolution(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        if 0 <= self.res_index < len(self.resolutions):
            SCREEN_WIDTH, SCREEN_HEIGHT = self.resolutions[self.res_index]
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            self.create_vignette()

    def cycle_resolution(self):
        self.res_index = (self.res_index + 1) % len(self.resolutions)
        self.apply_resolution()
        self.save_settings()
        self.create_menu_buttons()

    def set_laptop_mode(self):
        self.res_index = 0 # 1280x720
        self.apply_resolution()
        self.save_settings()
        self.create_menu_buttons()

    def add_particles(self, x, y, color):
        for _ in range(30):
            self.particles.append({
                'x': x, 'y': y,
                'vx': random.uniform(-6, 6),
                'vy': random.uniform(-6, 6),
                'life': 255,
                'color': color,
                'size': random.randint(4, 10)
            })

    def update_draw_particles(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 4
            p['size'] -= 0.05
            if p['life'] <= 0 or p['size'] <= 0:
                self.particles.remove(p)
            else:
                s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], int(p['life'])), (int(p['size']), int(p['size'])), int(p['size']))
                self.screen.blit(s, (p['x'] - p['size'], p['y'] - p['size']))

    def update_draw_coin_particles(self):
        for p in self.coin_particles[:]:
            p['vy'] += 0.3 # Gravity
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            if p['y'] > SCREEN_HEIGHT + p['size']:
                self.coin_particles.remove(p)
            else:
                # Draw coin particle
                pygame.draw.circle(self.screen, p['color'], (p['x'], p['y']), p['size'])
                # Simple shine effect
                pygame.draw.circle(self.screen, (255, 255, 200), (p['x'] - p['size']*0.2, p['y'] - p['size']*0.2), p['size']*0.4)

    def update_draw_floating_texts(self):
        # Textes flottants (Combo, Dégâts, etc.)
        for ft in self.floating_texts[:]:
            ft['life'] -= 1
            ft['y'] -= ft['speed']
            if ft['life'] <= 0:
                self.floating_texts.remove(ft)
            else:
                alpha = min(255, ft['life'] * 5)
                surf = self.small_bold_font.render(ft['text'], True, ft['color'])
                surf.set_alpha(alpha)
                rect = surf.get_rect(center=(ft['x'], ft['y']))
                self.screen.blit(surf, rect)

    def spawn_coin_fly(self, amount, x, y):
        self.display_coins = self.coins - amount
        self.temp_coin_display_timer = pygame.time.get_ticks() + 3000
        
        count = min(amount, 20)
        if count <= 0: return
        val_per = amount // count
        rem = amount % count
        
        dest_x = SCREEN_WIDTH - 100
        dest_y = 50
        
        for i in range(count):
            val = val_per + (1 if i < rem else 0)
            self.coin_fly_particles.append({
                'x': x + random.randint(-20, 20), 'y': y + random.randint(-20, 20),
                'tx': dest_x, 'ty': dest_y, 'val': val,
                'speed': random.uniform(12, 20), 'size': random.randint(10, 16), 'color': (255, 215, 0)
            })

    def update_draw_coin_fly(self):
        # Affichage du compteur temporaire
        if self.coin_fly_particles or pygame.time.get_ticks() < self.temp_coin_display_timer:
            tx, ty = SCREEN_WIDTH - 100, 50
            bg_rect = pygame.Rect(tx - 80, ty - 30, 160, 60)
            s = pygame.Surface((bg_rect.w, bg_rect.h), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 180), s.get_rect(), border_radius=30)
            self.screen.blit(s, bg_rect)
            self.draw_coin_ui(tx, ty, self.display_coins)
            
        for p in self.coin_fly_particles[:]:
            dx, dy = p['tx'] - p['x'], p['ty'] - p['y']
            dist = math.hypot(dx, dy)
            if dist < p['speed']: self.display_coins += p['val']; self.coin_fly_particles.remove(p)
            else:
                p['x'] += (dx/dist)*p['speed']; p['y'] += (dy/dist)*p['speed']; p['speed'] *= 1.08
                pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
                pygame.draw.circle(self.screen, (255, 255, 200), (int(p['x'])-3, int(p['y'])-3), p['size']//3)

    def spawn_coin_fall(self, amount):
        num_particles = min(50, 5 + amount // 10)
        for _ in range(num_particles):
            self.coin_particles.append({
                'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(-100, -20), 'vx': random.uniform(-1, 1),
                'vy': random.uniform(2, 5), 'size': random.randint(10, 20), 'color': random.choice([(255, 215, 0), (218, 165, 32), (255, 225, 50)])
            })

    def update_draw_menu_particles(self):
        # --- SYSTÈME DE SAISONS ---
        month = datetime.date.today().month
        
        # Configuration selon la saison
        if month in [12, 1, 2]: # Hiver (Neige)
            p_color = (240, 240, 255)
            p_vy_range = (1, 3)
            p_vx_range = (-1, 1)
            p_size_range = (2, 4)
        elif month in [3, 4, 5]: # Printemps (Pétales roses)
            p_color = (255, 180, 200)
            p_vy_range = (0.5, 2)
            p_vx_range = (-1, 1)
            p_size_range = (3, 5)
        elif month in [6, 7, 8]: # Été (Pollen/Soleil)
            p_color = (255, 255, 100)
            p_vy_range = (-1, -0.5) # Monte doucement
            p_vx_range = (-0.5, 0.5)
            p_size_range = (2, 4)
        else: # Automne (Feuilles oranges)
            p_color = (200, 100, 50)
            p_vy_range = (1, 2.5)
            p_vx_range = (-2, 2)
            p_size_range = (3, 6)

        if len(self.menu_particles) < 60:
            self.menu_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': -10 if p_vy_range[0] > 0 else SCREEN_HEIGHT + 10,
                'vx': random.uniform(*p_vx_range),
                'vy': random.uniform(*p_vy_range),
                'size': random.randint(*p_size_range),
                'color': p_color,
                'alpha': random.randint(100, 200)
            })

        for p in self.menu_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['x'] += math.sin(p['y'] * 0.05) * 0.5 # Oscillation naturelle
            
            if not (-20 < p['y'] < SCREEN_HEIGHT + 20):
                self.menu_particles.remove(p)
            else:
                s = pygame.Surface((int(p['size']*2), int(p['size']*2)), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], int(p['alpha'])), (int(p['size']), int(p['size'])), int(p['size']))
                self.screen.blit(s, (p['x'], p['y']))

    def update_draw_floating_shapes(self):
        # Dessine des formes géométriques subtiles en arrière-plan
        for s in self.floating_shapes:
            s['y'] -= s['speed']
            s['angle'] += s['rot_speed']
            if s['y'] < -150:
                s['y'] = SCREEN_HEIGHT + 150
                s['x'] = random.randint(0, SCREEN_WIDTH)
            
            surf = pygame.Surface((s['size'], s['size']), pygame.SRCALPHA)
            color = (255, 255, 255, 15) # Très transparent
            
            if s['shape'] == 'rect':
                pygame.draw.rect(surf, color, (0,0,s['size'],s['size']), border_radius=10)
            elif s['shape'] == 'circle':
                pygame.draw.circle(surf, color, (s['size']//2, s['size']//2), s['size']//2)
            elif s['shape'] == 'triangle':
                pts = [(s['size']//2, 0), (0, s['size']), (s['size'], s['size'])]
                pygame.draw.polygon(surf, color, pts)
                
            rotated = pygame.transform.rotate(surf, s['angle'])
            self.screen.blit(rotated, (s['x'] - rotated.get_width()//2, s['y'] - rotated.get_height()//2))

    def generate_flame_particles(self):
        # Génère des flammes sur les bords de l'écran
        sides = [
            (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, random.uniform(-1, 1), random.uniform(-3, -7)), # Bas
            (random.randint(0, SCREEN_WIDTH), 0, random.uniform(-1, 1), random.uniform(3, 7)), # Haut
            (0, random.randint(0, SCREEN_HEIGHT), random.uniform(3, 7), random.uniform(-1, 1)), # Gauche
            (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT), random.uniform(-3, -7), random.uniform(-1, 1)) # Droite
        ]
        for x, y, vx, vy in sides:
            if random.random() < 0.3: # Densité
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': vx, 'vy': vy,
                    'life': random.randint(100, 200), 'color': (255, random.randint(50, 150), 0), 'size': random.randint(5, 15)
                })

    def update_draw_game_emotes(self):
        # Gère les émojis flottants pendant la partie
        for e in self.game_emotes[:]:
            e['y'] -= e['speed']
            e['life'] -= 1
            e['x'] += math.sin(e['y'] * 0.05) * 0.5 # Petit mouvement ondulatoire
            
            if e['life'] <= 0:
                self.game_emotes.remove(e)
            else:
                # Fade out
                alpha = min(255, e['life'] * 5)
                surf = self.ui_emoji_font.render(e['emoji'], True, (255, 255, 255))
                surf.set_alpha(alpha)
                self.screen.blit(surf, (e['x'], e['y']))

    def update_draw_matrix_rain(self):
        font = self.small_bold_font
        font_height = font.get_height()
        
        if len(self.theme_particles) < 100:
            self.theme_particles.append({
                'x': random.randint(0, SCREEN_WIDTH // 20) * 20,
                'y': random.randint(-500, 0),
                'speed': random.uniform(5, 15),
                'length': random.randint(8, 25),
                'chars': [random.choice("01") for _ in range(25)]
            })

        for stream in self.theme_particles:
            stream['y'] += stream['speed']
            for i in range(stream['length']):
                char_y = stream['y'] - i * font_height
                if 0 < char_y < SCREEN_HEIGHT:
                    color = (200, 255, 200) if i == 0 else (0, 100 + int(155 * (1 - i/stream['length'])), 0)
                    self.draw_text(stream['chars'][i], font, color, stream['x'], char_y)
                if random.randint(0, 20) == 0:
                    stream['chars'][i] = random.choice("01")
            if stream['y'] - stream['length'] * font_height > SCREEN_HEIGHT:
                stream['y'] = random.randint(-200, 0)
                stream['x'] = random.randint(0, SCREEN_WIDTH // 20) * 20

    def update_draw_starfield(self):
        if len(self.theme_particles) < 200:
            self.theme_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 3),
                'brightness': random.randint(50, 150),
                'speed': random.uniform(0.1, 0.5)
            })

        for p in self.theme_particles:
            p['x'] -= p['speed']
            if p['x'] < 0:
                p['x'] = SCREEN_WIDTH
                p['y'] = random.randint(0, SCREEN_HEIGHT)

            twinkle = random.randint(-20, 20)
            brightness = max(0, min(255, p['brightness'] + twinkle))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (p['x'], p['y']), p['size'])

    def draw_scanlines(self):
        # Lignes horizontales statiques (Cache)
        if not hasattr(self, 'scanline_surf') or self.scanline_surf.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
            self.scanline_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for y in range(0, SCREEN_HEIGHT, 4):
                pygame.draw.line(self.scanline_surf, (0, 0, 0, 40), (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(self.scanline_surf, (0, 0))
        
        # Barre de balayage verticale (Effet CRT)
        t = pygame.time.get_ticks()
        bar_h = 150
        bar_y = (t * 0.15) % (SCREEN_HEIGHT + bar_h) - bar_h
        
        if not hasattr(self, 'crt_bar_surf') or self.crt_bar_surf.get_width() != SCREEN_WIDTH:
            self.crt_bar_surf = pygame.Surface((SCREEN_WIDTH, bar_h), pygame.SRCALPHA)
            for i in range(bar_h):
                alpha = int(15 * math.sin((i / bar_h) * math.pi)) # Dégradé sinusoïdal
                pygame.draw.line(self.crt_bar_surf, (255, 255, 255, alpha), (0, i), (SCREEN_WIDTH, i))
        
        self.screen.blit(self.crt_bar_surf, (0, bar_y))

    def draw_news_ticker(self):
        if self.news_ticker_finished:
            return

        # Barre semi-transparente en bas
        s = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, SCREEN_HEIGHT - 115))
        
        # Texte défilant
        full_text = "   |   ".join(self.news_items)
        text_surf = self.small_bold_font.render(full_text, True, (200, 200, 200))
        
        self.news_scroll -= 2
        if self.news_scroll < -text_surf.get_width():
            self.news_ticker_finished = True
        self.screen.blit(text_surf, (self.news_scroll, SCREEN_HEIGHT - 110))

    def check_daily_login(self):
        today = str(datetime.date.today())
        if self.last_login_date == today:
            return # Already checked today

        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        
        if self.last_login_date == yesterday:
            self.login_streak += 1
        else:
            self.login_streak = 1 # Reset streak
        
        self.last_login_date = today
        self.save_settings()
        if self.login_streak >= 7:
            self.unlock_achievement("SECRET_LOGIN")

        reward = 50 + (self.login_streak * 10)
        
        def claim_reward():
            self.add_coins(reward, animate=True)
            self.show_notification(f"+{reward} pièces !", type="success")
            self.popup = None
            self.save_settings()

        self.popup = { "title": "BONUS DE CONNEXION", "msg": f"Série de {self.login_streak} jours ! Vous gagnez {reward} pièces.", "avatar": "??",
            "single_button_text": "RÉCUPÉRER", "action": claim_reward }

    def generate_hardcore_win_particles(self):
        # Explosion rouge et noire pour le mode Hardcore
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for _ in range(150):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 25)
            self.particles.append({
                'x': cx, 'y': cy,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(100, 255),
                'color': random.choice([(255, 0, 0), (0, 0, 0), (100, 0, 0)]),
                'size': random.randint(5, 20)
            })

    # --- SYSTÈME GLOBAL D'ÉCOUTE (AMIS / TRADE) ---
    def start_global_listener(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(('0.0.0.0', self.server_port))
            except OSError:
                # Si le port est pris (ex: 2ème instance), on essaie les suivants
                for p in range(self.server_port + 1, self.server_port + 20):
                    try:
                        s.bind(('0.0.0.0', p))
                        self.server_port = p
                        self.external_port = p # Mise à jour du port externe par défaut
                        break
                    except OSError: continue
            s.listen(5)
            while True:
                conn, addr = s.accept()
                try:
                    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                except: pass
                threading.Thread(target=self.handle_incoming_connection, args=(conn,), daemon=True).start()
        except Exception as e: print(f"Listener Error: {e}")

    def handle_incoming_connection(self, conn):
        try:
            # Lecture robuste pour supporter les gros avatars (PDP)
            conn.settimeout(15)
            buffer = b""
            while b"\n" not in buffer:
                chunk = conn.recv(16384)
                if not chunk: break
                buffer += chunk
                if len(buffer) > 5000000: break # Sécurité
            
            if b"\n" not in buffer: conn.close(); return
            data = buffer.split(b"\n", 1)[0].decode('utf-8').strip()
            conn.settimeout(None)
            
            parts = data.split('|')
            intent = parts[0]
            
            if intent == "INTENT_GAME":
                allowed_state = (self.state == "LOBBY") or (self.state == "MENU_FRIENDS" and self.friends_menu_from_lobby)
                if allowed_state and not self.connected:
                    # Gestion Multi-joueurs (Host)
                    if self.is_host:
                        if len(self.clients) < self.settings['players'] - 1:
                            new_id = len(self.clients) + 1
                            # Accepter et envoyer l'ID
                            conn.sendall(f"ACCEPT|{new_id}\n".encode())
                            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Amélioration latence

                            # Stocker infos client
                            client_data = {
                                "conn": conn, "id": new_id,
                                "name": parts[1] if len(parts) > 1 else f"Joueur {new_id+1}",
                                "avatar": parts[2] if len(parts) > 2 else "🙂",
                                "border": parts[3] if len(parts) > 3 else "border_default", "name_color": parts[4] if len(parts) > 4 else "name_color_default",
                                "level": int(parts[5]) if len(parts) > 5 else 1,
                                "theme": parts[6] if len(parts) > 6 else "theme_default",
                                "badge": parts[7] if len(parts) > 7 else "badge_default",
                                "ready": False,
                                "streak": int(parts[8]) if len(parts) > 8 else 0,
                                "ip": conn.getpeername()[0],
                                "ping": 0,
                                "last_ping_sent": 0
                            }
                            with self.clients_lock:
                                self.clients.append(client_data)

                            # FIX: Synchroniser les infos de l'adversaire pour l'hôte (HUD)
                            if len(self.clients) == 1:
                                self.opponent_name = client_data['name']
                                self.opponent_avatar = client_data['avatar']
                                self.opponent_border = client_data['border']
                                self.opponent_name_color = client_data['name_color']
                                self.opponent_badge = client_data['badge']

                            msg = f"SYSTEM: {client_data['name']} a rejoint."
                            self.chat_messages.append(msg)
                            self.send_data(f"CHAT|{msg}")
                            
                            # Auto-switch to Lobby if in Friends menu
                            if self.state == "MENU_FRIENDS":
                                self.state = "LOBBY"
                                self.friends_menu_from_lobby = False

                            # Thread d'écoute pour ce client
                            threading.Thread(target=self.host_receive_client_data, args=(client_data,), daemon=True).start()
                            self.broadcast_player_list()
                            self.network_queue.append("REFRESH_LOBBY")
                        else:
                            conn.close()
                else:
                    conn.close()
            elif intent == "FRIEND_REQ":
                if len(parts) < 3:
                    conn.close()
                    return
                sender_name = parts[1]
                sender_avatar = parts[2]
                
                try:
                    remote_ip = conn.getpeername()[0]
                    # Vérification si déjà ami
                    if any(f['ip'] == remote_ip for f in self.friends):
                        conn.sendall(b"FRIEND_ALREADY\n")
                        conn.close()
                        return
                except: pass
                
                self.friend_req_result = None
                self.friend_req_event.clear()
                
                def on_accept():
                    self.friend_req_result = "ACCEPT"
                    self.friend_req_event.set()
                    self.popup = None
                
                def on_reject():
                    self.friend_req_result = "REJECT"
                    self.friend_req_event.set()
                    self.popup = None

                self.popup = {
                    "title": "DEMANDE D'AMI", "msg": f"{sender_name} veut vous ajouter !", "avatar": sender_avatar,
                    "yes": on_accept, "no": on_reject
                }
                
                # Attente réponse utilisateur (Bloquant dans le thread réseau)
                self.friend_req_event.wait(30)
                
                if self.friend_req_result == "ACCEPT":
                    conn.sendall(f"FRIEND_OK|{self.username}\n".encode())
                    try:
                        remote_ip = conn.getpeername()[0]
                        if not any(f['ip'] == remote_ip for f in self.friends):
                            self.friends.append({"name": sender_name, "ip": remote_ip})
                            self.save_settings()
                            self.check_achievements()
                            self.show_notification(f"{sender_name} ajouté !")
                    except: pass
                else:
                    conn.sendall(b"FRIEND_NO\n")
                conn.close()
            elif intent == "INTENT_TRADE":
                def accept_trade_request():
                    try: conn.sendall(f"ACCEPT|{self.username}|{self.avatar}\n".encode()) # Envoi confirmation avec infos
                    except: pass
                    self.accept_trade(conn, parts[1], parts[2])
                
                self.popup = {
                    "title": "ECHANGE", "msg": f"{parts[1]} veut échanger !", "avatar": parts[2],
                    "yes": accept_trade_request, "no": lambda: self.reject_request(conn)
                }
            elif intent == "INTENT_INVITE":
                if self.state != "LOBBY" and self.state != "GAME":
                    sender_name = parts[1]
                    host_ip = parts[2]
                    
                    def join():
                        self.accept_game_invite(host_ip)
                        self.popup = None
                    
                    self.popup = { "title": "INVITATION", "msg": f"{sender_name} vous invite à jouer !", "avatar": "GAME",
                        "yes": join, "no": lambda: self.reject_request(conn) }
        except: conn.close()

    def reject_request(self, conn):
        try: conn.sendall(b"REJECT\n"); conn.close()
        except: pass
        self.popup = None

    def start_spin(self):
        if self.last_spin_date != str(datetime.date.today()):
            self.wheel_velocity = random.uniform(25, 40)
            self.wheel_spinning = True
            self.spin_result = None
            self.create_menu_buttons()

    def claim_spin_reward(self, result):
        self.last_spin_date = str(datetime.date.today())
        if result == "JACKPOT":
            self.add_coins(5000); self.show_notification("JACKPOT ! +5000$", "success")
        elif result == "ITEM":
            # Item aléatoire non possédé
            shop_items = [k for k in SHOP_CATALOG.keys() if k not in self.inventory and not SHOP_CATALOG[k].get('secret')]
            if shop_items:
                item = random.choice(shop_items)
                self.inventory.append(item)
                self.show_notification(f"Gagné : {SHOP_CATALOG[item]['name']} !", "success")
            else:
                self.add_coins(500); self.show_notification("Tout possédé ! +500$", "success")
        else:
            amount = int(result)
            self.add_coins(amount); self.show_notification(f"Gagné : {amount}$", "success")
        self.save_settings()
        self.create_menu_buttons()

    def add_coins(self, amount, animate=True):
        if amount <= 0: return
        self.coins += amount
        if animate:
            self.spawn_coin_fall(amount)

    def get_xp_threshold(self, level):
        if level == 1: return 30
        if level == 2: return 60
        if level == 3: return 80
        return level * 50

    def gain_xp(self, amount):
        self.xp += amount
        threshold = self.get_xp_threshold(self.level)
        while self.xp >= threshold:
            self.xp -= threshold
            self.level += 1
            threshold = self.get_xp_threshold(self.level)
            self.play_sound("start") # Son de level up
        
        # Season XP
        if "season" not in self.stats: self.stats["season"] = {"level": 1, "xp": 0, "claimed": []}
        self.stats["season"]["xp"] += amount
        while self.stats["season"]["xp"] >= 200 and self.stats["season"]["level"] < 100:
            self.stats["season"]["xp"] -= 200
            self.stats["season"]["level"] += 1
            
        self.check_achievements()
        self.save_settings()

    def generate_default_sounds(self):
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            def make_tone(freq, duration, vol=0.1):
                if freq in [440, 100]: # FIX: Enlever les BIP horribles (Click 440Hz, Buzz 100Hz)
                    vol = 0.0
                n_steps = int(duration * 44100)
                buf = array.array('h', [int(math.sin(2 * math.pi * freq * x / 44100) * 32767 * vol) for x in range(n_steps)])
                return pygame.mixer.Sound(buffer=buf)

            self.sounds["click"] = make_tone(440, 0.05, 0.0) # Silencieux (Demandé)
            self.sounds["success"] = make_tone(880, 0.2, 0.1)
            self.sounds["error"] = make_tone(150, 0.3, 0.2)
            self.sounds["coin"] = make_tone(1200, 0.1, 0.1)
            self.sounds["start"] = make_tone(600, 0.4, 0.1)
            self.sounds["chat"] = make_tone(1000, 0.05, 0.05)
            self.sounds["buzz"] = make_tone(100, 0.5, 0.2)
            self.sounds["info"] = make_tone(500, 0.1, 0.1)

            # Son spécial CADEAU (Arpège)
            gift_buf = array.array('h')
            freqs = [523.25, 659.25, 783.99, 1046.50] # C E G C
            for f in freqs:
                n = int(0.12 * 44100)
                wave = [int(math.sin(2 * math.pi * f * x / 44100) * 32767 * 0.15) for x in range(n)]
                gift_buf.extend(array.array('h', wave))
            self.sounds["gift"] = pygame.mixer.Sound(buffer=gift_buf)

        except Exception as e:
            print(f"Erreur audio: {e}")

    def play_sound(self, type):
        if self.sound_on and type in self.sounds:
            self.sounds[type].play()

    def show_notification(self, text, type="info"):
        self.notifications.append({"text": text, "type": type, "time": pygame.time.get_ticks(), "duration": 4000, "y": -60})
        self.play_sound(type)

    def draw_notifications(self):
        current_time = pygame.time.get_ticks()
        # Supprimer les anciennes
        self.notifications = [n for n in self.notifications if current_time - n["time"] < n["duration"]]
        
        for i, n in enumerate(self.notifications):
            # Animation slide in
            target_y = 20 + i * 70
            n["y"] += (target_y - n["y"]) * 0.1

            # Définir couleur et icône par type
            notif_type = n.get("type", "info")
            if notif_type == "success":
                color = (100, 255, 100)
                icon = "✔"
            elif notif_type == "error":
                color = ALERT_COLOR
                icon = "✖"
            else: # info
                color = ACCENT_COLOR
                icon = "ℹ"
            
            # Dessin
            s = pygame.Surface((400, 60), pygame.SRCALPHA)
            pygame.draw.rect(s, (30, 35, 45, 240), (0, 0, 400, 60), border_radius=15)
            pygame.draw.rect(s, color, (0, 0, 400, 60), 2, border_radius=15)
            self.screen.blit(s, (SCREEN_WIDTH - 420, n["y"]))
            
            # Icône
            pygame.draw.circle(self.screen, color, (SCREEN_WIDTH - 390, int(n["y"]) + 30), 15)
            self.draw_text(icon, self.ui_emoji_font, (30, 35, 45), SCREEN_WIDTH - 390, int(n["y"]) + 30)
            
            self.draw_text_fit(n["text"], self.small_bold_font, TEXT_COLOR, SCREEN_WIDTH - 200, int(n["y"]) + 30, 340)

    def prepare_xp_animation(self, amount):
        self.anim_xp_val = float(self.xp)
        self.anim_level_val = self.level
        self.gain_xp(amount)
        self.target_xp_val = self.xp
        self.target_level_val = self.level
        self.xp_animating = True

    def get_season_reward(self, level):
        if level == 10: return {"type": "item", "id": "border_season1", "name": "Bordure S1"}
        if level == 20: return {"type": "item", "id": "theme_season1", "name": "Thème S1"}
        if level == 50: return {"type": "item", "id": "badge_season1", "name": "Badge S1"}
        if level == 100: return {"type": "item", "id": "name_color_season1", "name": "Pseudo S1"}
        
        amount = 50
        if level % 10 == 0: amount = 500
        elif level % 5 == 0: amount = 200
        return {"type": "coins", "amount": amount, "name": f"{amount} Pièces"}

    def claim_season_reward(self, level):
        if level <= self.stats["season"]["level"] and level not in self.stats["season"]["claimed"]:
            reward = self.get_season_reward(level)
            if reward["type"] == "coins":
                self.coins += reward["amount"]
                self.add_coins(reward["amount"])
            elif reward["type"] == "item":
                if reward["id"] not in self.inventory:
                    self.inventory.append(reward["id"])
            
            self.stats["season"]["claimed"].append(level)
            self.save_settings()
            self.show_notification(f"Récompense Niv {level} récupérée !", "success")
            if self.state == "MENU_BATTLEPASS":
                self.create_menu_buttons()

    def get_player_title(self, level):
        # Détermine le titre du joueur selon son niveau
        if level >= 100: return "LÉGENDE"
        if level >= 50: return "GRAND MAÎTRE"
        if level >= 25: return "EXPERT"
        if level >= 10: return "HABITUÉ"
        return "NOVICE"

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.save_settings()
        self.create_menu_buttons()

    def toggle_upnp(self):
        self.upnp_enabled = not self.upnp_enabled
        if self.upnp_enabled:
            threading.Thread(target=self.try_upnp, daemon=True).start()
        else:
            self.remove_upnp()
            self.upnp_status = "Désactivé"
        self.save_settings()
        self.create_menu_buttons()

    def validate_gift_code(self):
        code = self.gift_code_input.upper().strip()
        codes = {
            "RUSH2024": 500,
            "DODOSIIII": 1000,
            "RIN": 1000,
            "WELCOME": 200,
            "SUMMER": 300,
            "WINTER": 300,
            "LEGEND": 500,
            "STAR": 250,
            "GIFT": 100,
            "MONEY": 1000,
            "PYTHON": 200
        }
        
        if not code: return
        
        if code == "SNAKE":
            self.start_snake_game()
            return

        if code in self.stats.get("used_codes", []):
            self.show_notification("Code déjà utilisé !", "error")
            return
            
        if code in codes:
            reward = codes[code]
            self.coins += reward
            self.add_coins(reward)
            if "used_codes" not in self.stats: self.stats["used_codes"] = []
            self.stats["used_codes"].append(code)
            self.save_settings()
            self.play_sound("gift")
            self.show_notification(f"Code valide ! +{reward} Pièces", "success")
            self.gift_code_input = ""
            self.set_state("SETTINGS")
        else:
            self.show_notification("Code invalide", "error")

    def start_snake_game(self):
        self.state = "SNAKE_GAME"
        self.snake_data = {
            "body": [(10, 10), (9, 10), (8, 10)],
            "dir": (1, 0),
            "next_dir": (1, 0),
            "food": (15, 10),
            "score": 0,
            "dead": False,
            "last_move": pygame.time.get_ticks(),
            "speed": 100,
            "grid_w": 40,
            "grid_h": 30,
            "cell_size": 20
        }
        self.spawn_snake_food()
        self.create_menu_buttons()

    def spawn_snake_food(self):
        while True:
            x = random.randint(0, self.snake_data["grid_w"] - 1)
            y = random.randint(0, self.snake_data["grid_h"] - 1)
            if (x, y) not in self.snake_data["body"]:
                self.snake_data["food"] = (x, y)
                break

    def update_snake_game(self):
        if self.snake_data["dead"]: return
        now = pygame.time.get_ticks()
        if now - self.snake_data["last_move"] > self.snake_data["speed"]:
            self.snake_data["last_move"] = now
            self.snake_data["dir"] = self.snake_data["next_dir"]
            head_x, head_y = self.snake_data["body"][0]
            dx, dy = self.snake_data["dir"]
            new_head = (head_x + dx, head_y + dy)
            if not (0 <= new_head[0] < self.snake_data["grid_w"] and 0 <= new_head[1] < self.snake_data["grid_h"]):
                self.snake_data["dead"] = True; self.play_sound("error"); return
            if new_head in self.snake_data["body"]:
                self.snake_data["dead"] = True; self.play_sound("error"); return
            self.snake_data["body"].insert(0, new_head)
            if new_head == self.snake_data["food"]:
                self.snake_data["score"] += 10; self.play_sound("coin"); self.spawn_snake_food()
                self.snake_data["speed"] = max(50, 100 - self.snake_data["score"] // 5)
            else: self.snake_data["body"].pop()

    def draw_snake_game(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        gw, gh, cs = self.snake_data["grid_w"], self.snake_data["grid_h"], self.snake_data["cell_size"]
        board_w, board_h = gw * cs, gh * cs
        start_x, start_y = cx - board_w // 2, cy - board_h // 2
        self.draw_panel(start_x - 20, start_y - 80, board_w + 40, board_h + 120)
        self.draw_text_shadow(f"SNAKE - SCORE: {self.snake_data['score']}", self.big_font, ACCENT_COLOR, cx, start_y - 40)
        pygame.draw.rect(self.screen, (20, 25, 30), (start_x, start_y, board_w, board_h))
        pygame.draw.rect(self.screen, (60, 70, 80), (start_x, start_y, board_w, board_h), 2)
        fx, fy = self.snake_data["food"]
        pygame.draw.rect(self.screen, (255, 50, 50), (start_x + fx*cs, start_y + fy*cs, cs, cs), border_radius=4)
        for i, (bx, by) in enumerate(self.snake_data["body"]):
            col = (0, 255, 100) if i == 0 else (0, 200, 80)
            pygame.draw.rect(self.screen, col, (start_x + bx*cs, start_y + by*cs, cs, cs), border_radius=2)
        if self.snake_data["dead"]:
            s = pygame.Surface((board_w, board_h), pygame.SRCALPHA); s.fill((0, 0, 0, 150)); self.screen.blit(s, (start_x, start_y))
            self.draw_text_shadow("GAME OVER", self.big_font, ALERT_COLOR, cx, cy)
            self.draw_text("ENTRÉE pour rejouer", self.font, (255, 255, 255), cx, cy + 50)

    def change_avatar(self, delta):
        idx = AVATARS.index(self.avatar)
        self.avatar = AVATARS[(idx + delta) % len(AVATARS)]

    def random_avatar(self):
        self.avatar = random.choice(AVATARS)
        self.create_menu_buttons()

    def set_avatar(self, avatar):
        self.avatar = avatar
        self.create_menu_buttons()

    def reset_history(self):
        self.used_words = []
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump([], f)
        except: pass

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.used_words, f)
        except: pass
    
    def request_friend(self):
        target = self.friend_code_input
        if self.friend_custom_port and ":" not in target:
            target = f"{target}:{self.friend_port_val}"
        
        if target:
            threading.Thread(target=self._send_friend_req_thread, args=(target,), daemon=True).start()
            self.open_friends_menu(from_lobby=False)

    def _send_friend_req_thread(self, target_ip_str):
        try:
            # S'assurer d'avoir l'IP locale pour l'envoyer (Aide pour le LAN)
            if not self.local_ip:
                try:
                    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); tmp.connect(("8.8.8.8", 80))
                    self.local_ip = tmp.getsockname()[0]; tmp.close()
                except Exception: self.local_ip = "127.0.0.1"

            ip, port = self.parse_address(target_ip_str)

            self.show_notification("Envoi demande...", type="info")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.settimeout(5)
            
            # Tentative de connexion plus robuste
            connected = False
            for _ in range(3): # 3 tentatives suffisent généralement
                try:
                    s.connect((ip, port))
                    connected = True
                    break
                except Exception: time.sleep(1.0)
            
            if not connected:
                self.show_notification("Hôte introuvable (Vérifiez l'IP)", type="error")
                return
            
            s.settimeout(60) # Attente longue pour la réponse utilisateur (augmenté)
            s.sendall(f"FRIEND_REQ|{self.username}|{self.avatar}\n".encode())
            
            resp = s.recv(1024).decode().strip()
            if resp.startswith("FRIEND_OK"):
                # Récupérer le nom réel de l'ami s'il est renvoyé
                parts = resp.split("|")
                friend_name = parts[1] if len(parts) > 1 else "Ami"
                # On stocke l'adresse complète (IP:PORT) si nécessaire
                self.friends.append({"name": friend_name, "ip": target_ip_str})
                self.save_settings()
                self.check_achievements()
                self.show_notification(f"{friend_name} ajouté !", type="success")
            elif resp.startswith("FRIEND_ALREADY"):
                self.show_notification("Déjà ami avec ce joueur !", type="error")
            else:
                self.show_notification("Demande refusée ou expirée", type="error")
            s.close()
        except (OSError, socket.timeout): self.show_notification("Hôte introuvable", type="error")
        except Exception as e:
            self.show_notification(f"Erreur: {e}", type="error")

    def direct_add_friend(self, ip, name=None):
        # Tentative via connexion jeu existante (In-Band) pour contourner NAT/Firewall
        if self.is_host:
            for c in self.clients:
                if c['ip'] == ip:
                    try:
                        c['conn'].sendall(f"LOBBY_FRIEND_REQ|{self.username}|{self.avatar}\n".encode())
                        self.show_notification("Demande envoyée (In-Game)", type="info")
                        return
                    except: pass
        elif self.connected and ip == self.input_ip:
             self.send_data(f"LOBBY_FRIEND_REQ|{self.username}|{self.avatar}")
             self.show_notification("Demande envoyée (In-Game)", type="info")
             return

        # Fallback sur nouvelle connexion socket
        threading.Thread(target=self._send_friend_req_thread, args=(ip,), daemon=True).start()

    def send_game_invite(self, ip):
        threading.Thread(target=self._send_invite_thread, args=(ip,), daemon=True).start()

    def _send_invite_thread(self, ip_str):
        try:
            self.show_notification(f"Invitation envoyée...", type="info")
            ip, port = self.parse_address(ip_str)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            host_ip = self.public_ip if self.public_ip else self.local_ip
            
            # Si l'IP cible est locale (LAN/Localhost), on force l'envoi de notre IP locale
            # pour éviter les problèmes de NAT Loopback avec l'IP publique
            if ip.startswith("127.") or ip.startswith("192.168.") or ip.startswith("10."):
                host_ip = self.local_ip

            # Ajouter le port si différent du défaut
            if self.external_port != DEFAULT_PORT:
                host_ip = f"{host_ip}:{self.external_port}"
                
            s.sendall(f"INTENT_INVITE|{self.username}|{host_ip}\n".encode())
            s.close()
        except:
            self.show_notification("Ami injoignable", type="error")

    def accept_game_invite(self, ip):
        if self.state not in ["GAME", "LOBBY"]:
            self.input_ip = ip
            self.connect_to_host()

    def delete_friend(self, idx):
        if 0 <= idx < len(self.friends):
            del self.friends[idx]
            self.save_settings()
            self.create_menu_buttons()
            
    def broadcast_settings(self):
        if self.is_host:
            msg = f"SETTINGS_UPDATE|{self.settings['mode']}|{self.settings['time']}|{self.settings['win_score']}|{self.settings['category']}|{self.settings['game_type']}|{self.settings['players']}"
            self.send_data(msg)

    def get_player_data_by_id(self, pid):
        if self.is_local_game:
            if pid == 0:
                name = self.local_player_names[0] if self.local_player_names else self.username
                return {"name": name, "avatar": self.avatar, "border": self.equipped['border'], "name_color": self.equipped['name_color'], "level": self.level, "theme": self.equipped['theme'], "badge": self.equipped['badge'], "streak": self.stats.get('win_streak', 0), "ip": "local"}
            else:
                name = self.local_player_names[pid] if self.local_player_names and pid < len(self.local_player_names) else f"Joueur {pid+1}"
                return {"name": name, "avatar": AVATARS[pid % len(AVATARS)], "border": "border_default", "name_color": "name_color_default", "level": 1, "theme": "theme_default", "badge": "badge_default", "streak": 0, "ip": "local"}
        elif self.is_host:
            if pid == 0:
                return {"name": self.username, "avatar": self.avatar, "border": self.equipped['border'], "name_color": self.equipped['name_color'], "level": self.level, "theme": self.equipped['theme'], "badge": self.equipped['badge'], "streak": self.stats.get('win_streak', 0), "ip": self.local_ip}
            elif self.test_mode and pid == 1:
                return {"name": "Bot (Dev)", "avatar": "🤖", "border": "border_neon", "name_color": "name_color_default", "level": 99, "theme": "theme_default", "badge": "badge_dev", "streak": 99, "ip": "local"}
            else:
                client = next((c for c in self.clients if c['id'] == pid), None)
                return client
        else: # Client
            if pid == self.my_id:
                return {"name": self.username, "avatar": self.avatar, "border": self.equipped['border'], "name_color": self.equipped['name_color'], "level": self.level, "theme": self.equipped['theme'], "badge": self.equipped['badge'], "streak": self.stats.get('win_streak', 0), "ip": "local"}
            elif pid in self.lobby_cache:
                return self.lobby_cache[pid]
        return None

    def close_lobby_popup(self):
        self.selected_lobby_player_id = None
        self.update_lobby_buttons()

    def copy_ip(self):
        if self.public_ip:
            txt = self.public_ip
            if self.external_port != DEFAULT_PORT:
                txt += f":{self.external_port}"
            try:
                pygame.scrap.put(pygame.SCRAP_TEXT, txt.encode('utf-8'))
                self.connect_status = "IP Copiée !" # Reuse connect_status for feedback
            except: pass

    def save_custom_category(self):
        if self.cat_name_input and self.cat_words_input:
            words = [w.strip() for w in self.cat_words_input.split(',')]
            if len(words) >= 5:
                self.custom_categories[self.cat_name_input.upper()] = words
                self.refresh_categories()
                self.save_settings()
                self.cat_name_input = ""
                self.cat_words_input = ""
                self.set_state("MENU_CUSTOM_CATS")

    def end_game_time_trial(self):
        # Déterminer le gagnant au score
        max_score = -1
        winner_idx = -1
        tie = False
        
        for i, s in enumerate(self.score):
            if s > max_score:
                max_score = s
                winner_idx = i
                tie = False
            elif s == max_score:
                tie = True
        
        if tie:
            self.winner_text = "ÉGALITÉ"
        else:
            self.winner_text = f"Joueur {winner_idx + 1}" if self.is_local_game else (self.username if winner_idx == self.my_id else self.opponent_name)
            if winner_idx == self.my_id:
                self.stats['wins_per_mode']['TIME_TRIAL'] = self.stats['wins_per_mode'].get('TIME_TRIAL', 0) + 1
        
        self.play_sound("success")
        self.set_state("GAME_OVER")
    
    def delete_custom_category(self, name):
        if name in self.custom_categories:
            del self.custom_categories[name]
            self.refresh_categories()

            # Reset category if current is deleted
            if self.settings['category'] == name:
                self.settings['category'] = 'GÉNÉRAL'
            self.save_settings()
            self.create_menu_buttons()

    def draw_coin_ui(self, x, y, amount, centered=True):
        # Dessine une pièce dorée graphique et le montant
        text_surf = self.font.render(str(amount), True, (255, 215, 0))
        
        # Rayon de la pièce
        r = 15
        padding = 8
        total_w = r*2 + padding + text_surf.get_width()
        
        start_x = x - total_w // 2 if centered else x
        
        # Dessin de la pièce (Cercle Extérieur)
        pygame.draw.circle(self.screen, (218, 165, 32), (start_x + r, y), r) # Or foncé
        pygame.draw.circle(self.screen, (255, 215, 0), (start_x + r, y), r - 2) # Or clair
        # Symbole $
        dollar = self.small_bold_font.render("$", True, (218, 165, 32))
        dollar_rect = dollar.get_rect(center=(start_x + r, y))
        self.screen.blit(dollar, dollar_rect)
        
        # Texte montant
        self.screen.blit(text_surf, (start_x + r*2 + padding, y - text_surf.get_height()//2))

    def choose_custom_avatar(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Choisir une image de profil",
                filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")]
            )
            root.destroy()
            
            if file_path:
                # Chargement et redimensionnement
                try:
                    self.crop_image = pygame.image.load(file_path).convert_alpha()
                    # Adapter la taille initiale si trop grande
                    if self.crop_image.get_width() > 1000 or self.crop_image.get_height() > 1000:
                        scale = 1000 / max(self.crop_image.get_width(), self.crop_image.get_height())
                        new_size = (int(self.crop_image.get_width() * scale), int(self.crop_image.get_height() * scale))
                        self.crop_image = pygame.transform.smoothscale(self.crop_image, new_size)
                    
                    self.crop_scale = 1.0
                    self.crop_offset = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
                    self.set_state("CROP_AVATAR")
                except Exception as e:
                    print(f"Erreur image: {e}")
        except Exception as e:
            print(f"Erreur dialogue: {e}")

    def validate_crop(self):
        if self.crop_image:
            try:
                # Création de la surface de rendu (Taille du cercle de crop : 300px)
                crop_size = 300
                surf = pygame.Surface((crop_size, crop_size), pygame.SRCALPHA)
                
                # Calculs de position relative
                img_w = int(self.crop_image.get_width() * self.crop_scale)
                img_h = int(self.crop_image.get_height() * self.crop_scale)
                
                # Centre de l'écran vs Centre de l'image
                rel_x = self.crop_offset[0] - SCREEN_WIDTH // 2
                rel_y = self.crop_offset[1] - SCREEN_HEIGHT // 2
                
                # Position de l'image sur la surface de crop (centrée)
                blit_x = (crop_size // 2) + rel_x - (img_w // 2)
                blit_y = (crop_size // 2) + rel_y - (img_h // 2)
                
                scaled_img = pygame.transform.smoothscale(self.crop_image, (img_w, img_h))
                surf.blit(scaled_img, (blit_x, blit_y))
                
                # Redimensionnement final pour stockage (100x100)
                final_surf = pygame.transform.smoothscale(surf, (100, 100))
                
                buffer = io.BytesIO()
                pygame.image.save(final_surf, buffer, "PNG")
                img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                self.avatar = "IMG:" + img_str
            except Exception as e:
                print(f"Erreur crop: {e}")
        self.set_state("INPUT_NAME")

    def get_name_color(self, item_id):
        now = pygame.time.get_ticks()
        if item_id == "name_color_rainbow":
            hue = (now // 5) % 360
            c = pygame.Color(0)
            c.hsla = (hue, 100, 50, 100)
            return (c.r, c.g, c.b)
        if item_id == "name_color_fire":
            pulse = (math.sin(now * 0.005) + 1) / 2
            return self.interpolate_color((255, 100, 0), (255, 0, 0), pulse)
        if item_id == "name_color_glitch":
            # Un glitch aléatoire rend le texte illisible, on opte pour un clignotement rapide
            if (now // 150) % 3 == 0:
                return (255, 50, 255)
            elif (now // 150) % 3 == 1:
                return (50, 255, 255)
            else:
                return (255, 255, 255)
        if item_id == "name_color_matrix":
            val = (now // 100) % 2
            return (0, 255, 0) if val else (0, 150, 0)
        if item_id == "custom_name_color":
            return self.custom_colors.get('name_color', TEXT_COLOR)
        if item_id in SHOP_CATALOG and SHOP_CATALOG[item_id]['type'] == 'name_color':
            return SHOP_CATALOG[item_id]['color']
        return TEXT_COLOR

    def unequip_item(self, type_):
        # Déséquiper = remettre par défaut
        default_id = f"{type_}_default"
        self.equipped[type_] = default_id
        self.save_settings()
        self.create_menu_buttons()

    def equip_item(self, item_id):
        # Équipe un objet possédé.
        item = SHOP_CATALOG.get(item_id)
        if not item:
            return
        t = item.get('type')
        if t not in ["border", "theme", "name_color", "badge", "title_style"]:
            return
        if item_id not in self.inventory:
            return
        self.equipped[t] = item_id
        self.save_settings()
        self.create_menu_buttons()

    def buy_item(self, item_id, pos=None):
        # Achète un objet du magasin.
        item = SHOP_CATALOG.get(item_id)
        if not item:
            return

        # Déjà possédé
        if item_id in self.inventory:
            self.show_notification("Déjà possédé", type="error")
            return

        price = int(item.get('price', 0))
        if price > self.coins:
            self.show_notification("Pas assez de pièces", type="error")
            return

        # Débit + ajout
        self.coins -= price
        self.stats["spent_coins"] = self.stats.get("spent_coins", 0) + price
        self.inventory.append(item_id)

        # Mettre à jour les catégories si nécessaire
        if item.get('type') == 'category': self.refresh_categories()

        self.save_settings()
        self.check_achievements()
        self.show_notification("Achat réussi !", type="success")
        self.create_menu_buttons()

    def draw_shop_card(self, x, y, w, h, item_id, item):
        # Carte UI (utilisée par Magasin + Inventaire).
        rect = pygame.Rect(int(x), int(y), int(w), int(h))
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)

        # Fond + ombre
        shadow = rect.move(0, 10)
        s = pygame.Surface((shadow.w, shadow.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 90), s.get_rect(), border_radius=18)
        self.screen.blit(s, (shadow.x, shadow.y))

        card_rect = rect
        
        rarity = item.get('rarity', 'COMMON')
        base_bg = RARITY_COLORS.get(rarity, RARITY_COLORS["COMMON"])
        
        if hovered:
            bg_col = (min(255, base_bg[0] + 15), min(255, base_bg[1] + 15), min(255, base_bg[2] + 15))
        else:
            bg_col = base_bg
            
        pygame.draw.rect(self.screen, bg_col, card_rect, border_radius=18)

        # Bordure accent
        border_col = ACCENT_COLOR if hovered else (80, 90, 110)
        pygame.draw.rect(self.screen, border_col, card_rect, 2, border_radius=18)

        # Header (type)
        type_txt = item.get('type', 'item').upper()
        header_h = 40
        header_rect = pygame.Rect(card_rect.x, card_rect.y, card_rect.w, header_h)
        hs = pygame.Surface((header_rect.w, header_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(hs, (0, 0, 0, 90), hs.get_rect(), border_top_left_radius=18, border_top_right_radius=18)
        self.screen.blit(hs, (header_rect.x, header_rect.y))
        self.draw_text(type_txt, self.small_bold_font, (220, 220, 220), header_rect.centerx, header_rect.centery)

        # Nom
        name = item.get('name', item_id)
        # Gestion débordement texte (Auto-scale)
        name_surf = self.small_bold_font.render(name, True, TEXT_COLOR)
        if name_surf.get_width() > card_rect.w - 20:
            scale = (card_rect.w - 20) / name_surf.get_width()
            new_size = (int(name_surf.get_width() * scale), int(name_surf.get_height() * scale))
            name_surf = pygame.transform.smoothscale(name_surf, new_size)
        name_rect = name_surf.get_rect(center=(card_rect.centerx, card_rect.y + 70))
        self.screen.blit(name_surf, name_rect)

        # Preview (couleur)
        preview_y = card_rect.y + 130
        preview_col = item.get('color', (255, 255, 255))
        if item_id == "custom_border_color":
            preview_col = self.custom_colors.get('border', (255, 255, 255))
        elif item_id == "custom_name_color":
            preview_col = self.custom_colors.get('name_color', (255, 255, 255))

        if item.get('type') == 'border':
            cx, cy = card_rect.centerx, preview_y
            pygame.draw.circle(self.screen, preview_col, (cx, cy), 34, 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), 24)
        elif item.get('type') == 'name_color':
            demo_col = self.get_name_color(item_id)
            demo = self.medium_font.render("Pseudo", True, demo_col)
            # Fond sombre pour contraste
            bg_demo = demo.get_rect(center=(card_rect.centerx, preview_y)).inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), bg_demo, border_radius=8)
            self.screen.blit(demo, demo.get_rect(center=(card_rect.centerx, preview_y)))
        elif item.get('type') == 'theme':
            sw = min(140, card_rect.w - 40)
            theme_rect = pygame.Rect(0, 0, sw, 60)
            theme_rect.center = (card_rect.centerx, preview_y)
            pygame.draw.rect(self.screen, preview_col, theme_rect, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), theme_rect, 2, border_radius=12)
        elif item.get('type') == 'category':
            sw = min(160, card_rect.w - 40)
            chip = pygame.Rect(0, 0, sw, 50)
            chip.center = (card_rect.centerx, preview_y)
            pygame.draw.rect(self.screen, preview_col, chip, border_radius=25)
            pygame.draw.rect(self.screen, (0, 0, 0), chip, 2, border_radius=25)
            self.draw_text("PACK", self.small_bold_font, (0, 0, 0), chip.centerx, chip.centery)
        elif item.get('type') == 'badge':
            icon = item.get('icon', '?')
            self.draw_text(icon, self.emoji_font, (255, 255, 255), card_rect.centerx, preview_y)
        elif item.get('type') == 'title_style':
            # Preview du titre
            font = self.medium_font
            txt = font.render("WORLD", True, preview_col)
            self.screen.blit(txt, txt.get_rect(center=(card_rect.centerx, preview_y)))
        else:
            pygame.draw.circle(self.screen, preview_col, (card_rect.centerx, preview_y), 25)

        # Status / action
        bottom_y = card_rect.bottom - 55
        owned = item_id in self.inventory
        equipped = owned and self.equipped.get(item.get('type')) == item_id

        if self.state == "MENU_SHOP":
            if owned:
                tag = self.small_bold_font.render("POSSÉDÉ", True, (180, 180, 180))
                self.screen.blit(tag, tag.get_rect(center=(card_rect.centerx, bottom_y)))
            else:
                # Afficher le prix si non possédé
                price = item.get('price', 0)
                price_y = bottom_y - 45
                if price > 0:
                    self.draw_coin_ui(card_rect.centerx, price_y, price)
                else:
                    lbl = self.small_bold_font.render("GRATUIT", True, (100, 255, 100))
                    self.screen.blit(lbl, lbl.get_rect(center=(card_rect.centerx, price_y)))

        elif self.state == "MENU_INVENTORY":
            if equipped:
                # Bouton DÉSÉQUIPER
                btn_rect = pygame.Rect(0, 0, card_rect.w - 40, 44)
                btn_rect.center = (card_rect.centerx, bottom_y)
                btn_hovered = btn_rect.collidepoint(pygame.mouse.get_pos())
                col = (255, 80, 80) if btn_hovered else (50, 150, 50)
                txt = "DÉSÉQUIPER" if btn_hovered else "ÉQUIPÉ"
                txt_col = (255, 255, 255) if btn_hovered else (100, 255, 100)
                pygame.draw.rect(self.screen, col, btn_rect, border_radius=12)
                self.draw_text(txt, self.small_bold_font, txt_col, btn_rect.centerx, btn_rect.centery)
            elif owned and item.get('type') in ['border', 'theme', 'name_color', 'badge', 'title_style']:
                # Bouton équiper
                btn_rect = pygame.Rect(0, 0, card_rect.w - 40, 44)
                btn_rect.center = (card_rect.centerx, bottom_y)
                col = (60, 220, 160) if hovered else (50, 200, 145)
                pygame.draw.rect(self.screen, col, btn_rect, border_radius=12)
                self.draw_text("ÉQUIPER", self.small_bold_font, (10, 20, 18), btn_rect.centerx, btn_rect.centery)
            elif owned:
                tag = self.small_bold_font.render("POSSÉDÉ", True, (180, 180, 180))
                self.screen.blit(tag, tag.get_rect(center=(card_rect.centerx, bottom_y)))

        # Clic
        if hovered and pygame.mouse.get_pressed()[0]:
            now = pygame.time.get_ticks()
            if now - self.last_click > 220:
                self.last_click = now
                
                # Shop clicks are handled by Buttons in create_menu_buttons
                if self.state == "MENU_INVENTORY":
                    if item.get('type') in ['border', 'theme', 'name_color', 'badge', 'title_style']:
                        if equipped:
                            self.unequip_item(item.get('type'))
                        elif owned:
                            self.equip_item(item_id)

    def get_sorted_shop_items(self):
        # Retourne la liste triée selon self.shop_sort.
        items = [k for k in SHOP_CATALOG.keys() if not SHOP_CATALOG[k].get('secret', False)]

        def type_rank(t):
            order = {"border": 0, "badge": 1, "name_color": 2, "title_style": 3, "theme": 4, "category": 5, "upgrade": 6, "gift": 7}
            return order.get(t, 99)
        
        def rarity_rank(r):
            order = {"COMMON": 0, "RARE": 1, "EPIC": 2, "LEGENDARY": 3}
            return order.get(r, 0)

        if self.shop_sort == "PRICE_ASC":
            items.sort(key=lambda k: (SHOP_CATALOG[k].get('price', 0), type_rank(SHOP_CATALOG[k].get('type')), SHOP_CATALOG[k].get('name', k)))
        elif self.shop_sort == "PRICE_DESC":
            items.sort(key=lambda k: (-int(SHOP_CATALOG[k].get('price', 0)), type_rank(SHOP_CATALOG[k].get('type')), SHOP_CATALOG[k].get('name', k)))
        elif self.shop_sort == "RARITY_DESC":
            items.sort(key=lambda k: (-rarity_rank(SHOP_CATALOG[k].get('rarity', 'COMMON')), SHOP_CATALOG[k].get('price', 0), SHOP_CATALOG[k].get('name', k)))
        elif self.shop_sort == "RARITY_ASC":
            items.sort(key=lambda k: (rarity_rank(SHOP_CATALOG[k].get('rarity', 'COMMON')), SHOP_CATALOG[k].get('price', 0), SHOP_CATALOG[k].get('name', k)))
        else:  # TYPE
            items.sort(key=lambda k: (type_rank(SHOP_CATALOG[k].get('type')), SHOP_CATALOG[k].get('price', 0), SHOP_CATALOG[k].get('name', k)))
        return items

    def set_shop_tab(self, tab):
        # Fonction magasin - définit l'onglet
        self.shop_tab = tab
        self.shop_scroll = 0
        self.create_menu_buttons()

    def set_inventory_tab(self, tab):
        # Fonction inventaire - définit l'onglet
        self.inventory_tab = tab
        self.inventory_scroll = 0
        self.create_menu_buttons()

    def toggle_shop_sort(self):
        # Bascule le tri du magasin
        sorts = ["TYPE", "PRICE_ASC", "PRICE_DESC", "RARITY_DESC", "RARITY_ASC"]
        current_idx = sorts.index(self.shop_sort) if self.shop_sort in sorts else 0
        self.shop_sort = sorts[(current_idx + 1) % len(sorts)]
        self.create_menu_buttons()

    def open_color_picker(self, target):
        self.color_picker_target = target
        # Load current custom color into picker
        current_color = self.custom_colors.get(target, (255, 255, 255))
        self.color_picker_values = {'r': current_color[0], 'g': current_color[1], 'b': current_color[2]}
        self.set_state("COLOR_PICKER")

    def validate_color_picker(self):
        if self.color_picker_target:
            new_color = (self.color_picker_values['r'], self.color_picker_values['g'], self.color_picker_values['b'])
            self.custom_colors[self.color_picker_target] = new_color
            
            # Equip the custom item
            item_id = f"custom_{self.color_picker_target}_color"
            self.equipped[self.color_picker_target] = item_id
            self.save_settings()
        self.set_state("MENU_INVENTORY")

    def request_trade(self, ip):
        threading.Thread(target=self._send_trade_req_thread, args=(ip,), daemon=True).start()

    def _send_trade_req_thread(self, ip_str):
        success = False
        ip, port = self.parse_address(ip_str)
        for i in range(3):
            try:
                if i == 0: self.show_notification("Envoi demande échange...")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(60) # Augmenté à 60s pour laisser le temps de répondre (Popup)
                s.connect((ip, port))
                s.sendall(f"INTENT_TRADE|{self.username}|{self.avatar}\n".encode())
                # Handshake robuste: peut contenir des messages supplémentaires dans le même paquet
                resp_buffer = b""
                while b"\n" not in resp_buffer:
                    chunk = s.recv(4096)
                    if not chunk:
                        raise ConnectionError("Connexion fermée pendant le handshake trade")
                    resp_buffer += chunk
                    if len(resp_buffer) > 2000000:
                        raise ConnectionError("Handshake trade trop volumineux")
                first_line, leftover = resp_buffer.split(b"\n", 1)
                resp = first_line.decode('utf-8', errors='ignore').strip()
                if resp.startswith("ACCEPT"):
                    parts = resp.split("|")
                    name = parts[1] if len(parts) > 1 else "Ami"
                    avatar = parts[2] if len(parts) > 2 else "🙂"
                    time.sleep(0.1) # Stabilisation socket
                    self.accept_trade(s, name, avatar, initial_buffer=leftover)
                    success = True
                    break
                else:
                    s.close()
                    self.show_notification("Demande refusée", type="error")
                    return
            except:
                time.sleep(0.5)
        if not success: self.show_notification("Joueur introuvable (Réessayez)", type="error")

    def accept_trade(self, conn, name, avatar, initial_buffer=b""):
        self.popup = None # Fermer la popup immédiatement pour éviter qu'elle reste bloquée
        self.conn = conn
        try:
            self.conn.settimeout(None)
        except Exception:
            pass
        self.connected = True
        self.opponent_name = name
        self.opponent_avatar = avatar
        self.trade_lobby_data = {"me": {"coins": 0, "items": [], "locked": False}, "them": {"coins": 0, "items": [], "locked": False}, "countdown": None}
        self.trade_coin_particles = []
        self.trade_finalize_at = 0
        self.set_state("TRADE_LOBBY")
        threading.Thread(target=self.receive_data, args=(initial_buffer,), daemon=True).start()
        # Synchronisation explicite du profil et de l'offre initiale dans le lobby d'échange
        self.send_name()
        self.send_trade_update()

    def refresh_trade_countdown(self):
        both_locked = self.trade_lobby_data["me"]["locked"] and self.trade_lobby_data["them"]["locked"]
        if both_locked:
            if self.trade_lobby_data["countdown"] is None:
                self.trade_lobby_data["countdown"] = pygame.time.get_ticks()
        else:
            self.trade_lobby_data["countdown"] = None

    def spawn_trade_coin_transfer(self, give_amount, receive_amount):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        panel_w, gap = 500, 100
        left_x = cx - (panel_w + gap) // 2
        right_x = cx + (panel_w + gap) // 2
        coin_y = cy - 60

        if give_amount > 0:
            self.floating_texts.append({
                'x': left_x, 'y': coin_y - 30,
                'text': f"-{give_amount}", 'color': (255, 120, 120),
                'life': 90, 'speed': 1.3
            })
        if receive_amount > 0:
            self.floating_texts.append({
                'x': right_x, 'y': coin_y - 30,
                'text': f"+{receive_amount}", 'color': (120, 255, 120),
                'life': 90, 'speed': 1.3
            })

        def add_stream(amount, sx, tx, col):
            if amount <= 0:
                return
            count = min(20, max(6, amount // 10))
            for _ in range(count):
                self.trade_coin_particles.append({
                    'x': sx + random.randint(-35, 35),
                    'y': coin_y + random.randint(-20, 20),
                    'tx': tx + random.randint(-35, 35),
                    'ty': coin_y + random.randint(-20, 20),
                    'speed': random.uniform(8, 14),
                    'size': random.randint(5, 9),
                    'color': col
                })

        add_stream(give_amount, left_x, right_x, (255, 170, 80))
        add_stream(receive_amount, right_x, left_x, (110, 255, 170))

    def update_draw_trade_coin_transfer(self):
        for p in self.trade_coin_particles[:]:
            dx, dy = p['tx'] - p['x'], p['ty'] - p['y']
            dist = math.hypot(dx, dy)
            if dist <= p['speed']:
                self.trade_coin_particles.remove(p)
                continue
            p['x'] += (dx / dist) * p['speed']
            p['y'] += (dy / dist) * p['speed']
            p['speed'] *= 1.03
            pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
            pygame.draw.circle(self.screen, (255, 255, 210), (int(p['x']) - 2, int(p['y']) - 2), max(1, p['size'] // 3))

    def update_trade_lock(self):
        if self.trade_finalize_at:
            return
        self.trade_lobby_data["me"]["locked"] = not self.trade_lobby_data["me"]["locked"]
        self.refresh_trade_countdown()
        self.send_trade_update()


    def add_trade_coin(self, amount):
        if self.trade_finalize_at:
            return
        if not self.trade_lobby_data["me"]["locked"]:
            if self.coins >= self.trade_lobby_data["me"]["coins"] + amount:
                self.trade_lobby_data["me"]["coins"] += amount
                self.send_trade_update()

    def unlock_achievement(self, ach_id):
        if ach_id in ACHIEVEMENTS and ach_id not in self.achievements_unlocked:
            self.achievements_unlocked.append(ach_id)
            reward = ACHIEVEMENTS[ach_id]["reward"]
            self.coins += reward
            self.add_coins(reward)
            # self.show_notification(f"SUCCÈS : {ACHIEVEMENTS[ach_id]['name']} (+{reward}$)") # Remplacé par popup
            self.achievement_queue.append(ACHIEVEMENTS[ach_id])
            self.play_sound("coin")
            self.save_settings()
            
            # Broadcast en ligne
            if self.connected or self.is_host:
                self.send_data(f"CHAT|SYSTEM: {self.username} a débloqué {ACHIEVEMENTS[ach_id]['name']} !")

    def check_achievements(self):
        # --- Victoires ---
        if self.stats["wins"] >= 1: self.unlock_achievement("WIN_1")
        if self.stats["wins"] >= 10: self.unlock_achievement("WIN_10")
        if self.stats["wins"] >= 50: self.unlock_achievement("WIN_50")
        if self.stats["wins"] >= 100: self.unlock_achievement("WIN_100")
        if self.stats["wins"] >= 250: self.unlock_achievement("WIN_250")
        if self.stats["games"] >= 100: self.unlock_achievement("PLAY_100")
        
        # --- Niveaux ---
        if self.level >= 5: self.unlock_achievement("LEVEL_5")
        if self.level >= 10: self.unlock_achievement("LEVEL_10")
        if self.level >= 25: self.unlock_achievement("LEVEL_25")
        if self.level >= 50: self.unlock_achievement("LEVEL_50")
        if self.level >= 100: self.unlock_achievement("LEVEL_100")
        
        # --- Économie ---
        if self.coins >= 500: self.unlock_achievement("RICH_500")
        if self.coins >= 2000: self.unlock_achievement("RICH_2000")
        if self.coins >= 10000: self.unlock_achievement("RICH_10000")
        if self.coins >= 50000: self.unlock_achievement("RICH_50000")
        if self.stats.get("spent_coins", 0) >= 1000: self.unlock_achievement("SPENDER_1000")
        if self.stats.get("spent_coins", 0) >= 5000: self.unlock_achievement("SPENDER_5000")
        if self.stats.get("spent_coins", 0) >= 20000: self.unlock_achievement("SPENDER_20000")
        
        # --- Social ---
        if len(self.friends) >= 1: self.unlock_achievement("SOCIAL_1")
        if len(self.friends) >= 5: self.unlock_achievement("SOCIAL_5")
        if len(self.friends) >= 10: self.unlock_achievement("SOCIAL_10")
        
        # --- Collection ---
        if len(self.inventory) >= 4: self.unlock_achievement("SHOPPER_1")
        if len(self.inventory) >= 10: self.unlock_achievement("COLLECTOR_10")
        if len(self.inventory) >= 25: self.unlock_achievement("COLLECTOR_25")
        if len(self.inventory) >= 50: self.unlock_achievement("COLLECTOR_50")
        
        # --- Gameplay ---
        if self.stats.get("max_combo", 0) >= 10: self.unlock_achievement("SPEEDSTER")
        if self.stats.get("max_combo", 0) >= 20: self.unlock_achievement("COMBO_20")
        if self.stats.get("max_combo", 0) >= 30: self.unlock_achievement("COMBO_30")
        if self.stats.get('wins_per_mode', {}).get('SURVIVAL', 0) >= 1: self.unlock_achievement("SURVIVOR_1")
        if self.stats.get('wins_per_mode', {}).get('SURVIVAL', 0) >= 10: self.unlock_achievement("SURVIVOR_10")
        if self.stats.get('wins_per_mode', {}).get('TIME_TRIAL', 0) >= 1: self.unlock_achievement("TIME_ATTACKER_1")
        if self.stats.get('wins_per_mode', {}).get('TIME_TRIAL', 0) >= 10: self.unlock_achievement("TIME_ATTACKER_10")
        if self.stats.get('wins_per_mode', {}).get('HARDCORE', 0) >= 1: self.unlock_achievement("HARDCORE_WIN_1")
        if self.stats.get('wins_per_mode', {}).get('HARDCORE', 0) >= 10: self.unlock_achievement("HARDCORE_WIN_10")
        
        # Check Shop King
        shop_items = [k for k in SHOP_CATALOG.keys() if k != "gift_daily"]
        owned = [i for i in self.inventory if i in shop_items]
        if len(owned) >= len(shop_items): self.unlock_achievement("SHOP_KING")

    def get_stat_value(self, stat_key):
        """Gets the current value of a player statistic for achievements."""
        if '.' in stat_key:
            # Handles nested stats like "wins_per_mode.SURVIVAL"
            try:
                keys = stat_key.split('.')
                value = self.stats
                for key in keys:
                    value = value[key]
                return value
            except (KeyError, TypeError):
                return 0
        
        # Direct attributes
        if stat_key == "level": return self.level
        if stat_key == "coins": return self.coins
        if stat_key == "friends": return len(self.friends)
        if stat_key == "inventory": return len(self.inventory)
        if stat_key == "login_streak": return self.login_streak
        if stat_key == "custom_categories": return len(self.custom_categories)

        # Special calculated stats
        if stat_key == "shop_king":
            shop_items = [k for k in SHOP_CATALOG.keys() if k != "gift_daily"]
            owned_items = [i for i in self.inventory if i in shop_items]
            return len(owned_items)

        # Boolean stats (return 1 if True for progress bar)
        if stat_key in ["wizz_used", "custom_avatar", "perfect_lose", "dev_mode", "trade_success"]:
             return 1 if self.stats.get(stat_key, False) else 0

        # Default to self.stats dictionary (for "wins", "spent_coins", "max_combo", etc.)
        return self.stats.get(stat_key, 0)

    def send_trade_update(self):
        d = self.trade_lobby_data["me"]
        self.send_data(f"TRADE_UPDATE|{d['coins']}|{','.join(d['items'])}|{int(d['locked'])}")

    def export_save(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            filename = filedialog.asksaveasfilename(
                title="Exporter la sauvegarde",
                defaultextension=".json",
                filetypes=[("Fichier JSON", "*.json")],
                initialfile="wordrush_backup.json"
            )
            root.destroy()
            
            if filename:
                data = {
                    "settings": {
                        "username": self.username, "avatar": self.avatar, 
                        "sound": self.sound_on, "keys": self.keys, 
                        "first_run": self.first_run, "friends": self.friends, 
                        "xp": self.xp, "level": self.level, 
                        "custom_categories": self.custom_categories,
                        "coins": self.coins, "inventory": self.inventory,
                        "equipped": self.equipped, "achievements": self.achievements_unlocked,
                        "stats": self.stats
                    },
                    "history": self.used_words
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                
                self.feedback_msg = "SAUVEGARDE EXPORTÉE !"
                self.feedback_timer = pygame.time.get_ticks()
        except Exception as e:
            print(f"Erreur export: {e}")

    def import_save(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            filename = filedialog.askopenfilename(title="Importer une sauvegarde", filetypes=[("Fichier JSON", "*.json")])
            root.destroy()
            
            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                if "settings" in data:
                    with open(SETTINGS_FILE, 'w') as f:
                        json.dump(data["settings"], f, indent=4)
                if "history" in data:
                    with open(HISTORY_FILE, 'w') as f:
                        json.dump(data["history"], f, indent=4)
                
                self.load_settings()
                self.feedback_msg = "SAUVEGARDE IMPORTÉE !"
                self.feedback_timer = pygame.time.get_ticks()
                self.create_menu_buttons()
        except Exception as e:
            print(f"Erreur import: {e}")
            self.feedback_msg = "ERREUR IMPORT !"
            self.feedback_timer = pygame.time.get_ticks()

    def set_achievements_filter(self, new_filter):
        self.achievements_filter = new_filter
        self.achievements_scroll = 0
        self.create_menu_buttons()

    def join_friend(self, ip):
        self.input_ip = ip
        self.connect_to_host()
        
    def check_friends_online(self):
        self.friends_status = {f['ip']: "..." for f in self.friends}
        def _check():
            for friend in self.friends:
                ip = friend['ip']
                try:
                    target_ip, target_port = self.parse_address(ip)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0)
                    res = s.connect_ex((target_ip, target_port))
                    s.close()
                    self.friends_status[ip] = "En ligne" if res == 0 else "Hors ligne"
                except:
                    self.friends_status[ip] = "Hors ligne"
        threading.Thread(target=_check, daemon=True).start()

    def open_friends_menu(self, from_lobby=False):
        self.friends_menu_from_lobby = from_lobby
        self.set_state("MENU_FRIENDS")
        self.check_friends_online()

    def close_friends_menu(self):
        if self.friends_menu_from_lobby:
            self.friends_menu_from_lobby = False
            self.set_state("LOBBY")
        else:
            self.set_state("MENU_MAIN")

    def is_daily_challenge_done(self):
        return self.last_daily_challenge_date == str(datetime.date.today())

    def prompt_daily_challenge(self):
        reward = 300
        mode = "SPEED"
        cat = random.choice(list(WORD_CATEGORIES.keys()))
        
        def start():
            self.daily_challenge_active = True
            self.setup_local()
            self.settings['mode'] = 'WRITTEN'
            self.settings['game_type'] = mode
            self.settings['category'] = cat
            self.settings['win_score'] = 5
            self.popup = None
            self.start_local_game()
            
        self.popup = {
            "type": "DAILY_CHALLENGE",
            "title": "DÉFI DU JOUR 🏆",
            "avatar": "🔥",
            "mode": mode,
            "category": cat,
            "reward": reward,
            "yes": start,
            "no": lambda: setattr(self, 'popup', None),
            "single_button_text": None,
            "msg": "" # Non utilisé pour ce type
        }

    def create_menu_buttons(self):
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        self.buttons = []
        if self.state == "TUTORIAL":
            main_h = min(840, SCREEN_HEIGHT - 90)
            main_y = (SCREEN_HEIGHT - main_h) // 2
            btn_w = 460
            btn_h = 84
            btn_y = min(SCREEN_HEIGHT - btn_h - 6, main_y + main_h + 8)
            self.buttons = [
                Button("COMMENCER L'AVENTURE", cx - btn_w // 2, btn_y, btn_w, btn_h, (0, 205, 165), (0, 235, 190), self.close_tutorial, font=self.small_bold_font)
            ]
        
        elif self.state == "PAUSED":
            self.buttons = [
                Button("REPRENDRE", cx - 150, cy, 300, 60, ACCENT_COLOR, HOVER_COLOR, self.toggle_pause),
                Button("QUITTER", cx - 150, cy + 80, 300, 60, ALERT_COLOR, (255, 100, 100), self.quit_game)
            ]

        elif self.state == "INPUT_NAME":
            # --- NOUVEAU DESIGN GRAPHIQUE ---
            panel_w, panel_h = 1200, 650
            panel_x, panel_y = cx - panel_w // 2, cy - panel_h // 2
            
            # Zone Gauche (Preview + Input)
            left_w = 400
            left_cx = panel_x + left_w // 2
            
            # Boutons Avatar (Sous l'avatar)
            btn_y = panel_y + 280
            self.buttons.append(Button("🎲", left_cx - 70, btn_y, 60, 60, PANEL_COLOR, HOVER_COLOR, self.random_avatar, font=self.ui_emoji_font, text_color=(255, 255, 255)))
            self.buttons.append(Button("📷", left_cx + 10, btn_y, 60, 60, PANEL_COLOR, HOVER_COLOR, self.choose_custom_avatar, font=self.ui_emoji_font, text_color=(255, 255, 255)))
            
            # Zone Droite (Grille)
            right_x = panel_x + left_w + 20
            right_w = panel_w - left_w - 40
            grid_y = panel_y + 80
            grid_h = panel_h - 160
            
            # Grille d'avatars
            self.avatar_grid_buttons = []
            cols = 8
            btn_size = 60
            gap = 10
            
            # Calculer la hauteur totale pour le scroll
            total_rows = math.ceil(len(AVATARS) / cols)
            total_h = total_rows * (btn_size + gap)
            max_scroll = max(0, total_h - grid_h + 150) # Permet de scroller plus bas pour remonter les items
            
            # Clamp scroll
            if self.avatar_scroll > max_scroll: self.avatar_scroll = max_scroll
            if self.avatar_scroll < 0: self.avatar_scroll = 0

            start_x = right_x + (right_w - (cols * btn_size + (cols - 1) * gap)) // 2
            
            for i, av in enumerate(AVATARS):
                row = i // cols
                col = i % cols
                bx = start_x + col * (btn_size + gap)
                by = grid_y + row * (btn_size + gap) - self.avatar_scroll + 10 # +10 padding top
                
                # Ne créer le bouton que s'il est visible (Optimisation + Clipping logique)
                if by + btn_size > grid_y and by < grid_y + grid_h:
                    color = ACCENT_COLOR if av == self.avatar else (40, 45, 55)
                    self.avatar_grid_buttons.append(Button(av, bx, by, btn_size, btn_size, color, HOVER_COLOR, lambda a=av: self.set_avatar(a), font=self.ui_emoji_font, text_color=(255,255,255), scale_on_hover=True))

            # Bottom buttons
            self.buttons.append(Button("HISTORIQUE", panel_x + 40, panel_y + panel_h - 70, 180, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_HISTORY")))
            self.buttons.append(Button("STATS", panel_x + 240, panel_y + panel_h - 70, 180, 50, (0, 150, 255), HOVER_COLOR, lambda: self.set_state("MENU_STATS")))
            self.buttons.append(Button("VALIDER", panel_x + panel_w - 220, panel_y + panel_h - 70, 180, 50, ACCENT_COLOR, HOVER_COLOR, self.validate_name))

        elif self.state == "MENU_MAIN":
            # Redesign complet du menu principal
            # Centrage dynamique des boutons
            main_btns = []
            
            # 1. Entraînement (Gauche)
            main_btns.append({"text": "ENTRAÎNEMENT\n(Solo vs Bot)", "action": self.setup_training, "col": (50, 200, 100), "hover": (80, 230, 130)})
            # 2. Local (Centre Gauche)
            main_btns.append({"text": "JOUER EN LOCAL\n(Même PC)", "action": self.setup_local, "col": ACCENT_COLOR, "hover": HOVER_COLOR})
            # 3. En Ligne (Centre Droite)
            main_btns.append({"text": "JOUER EN LIGNE\n(Réseau)", "action": lambda: self.set_state("MENU_ONLINE"), "col": (0, 150, 255), "hover": (50, 180, 255)})
            
            if not self.is_daily_challenge_done():
                # 4. Défi (Droite)
                main_btns.append({"text": "DÉFI DU JOUR\n(+300$)", "action": self.prompt_daily_challenge, "col": (255, 100, 50), "hover": (255, 150, 100), "notif": True})

            btn_w = 260
            btn_h = 150
            gap = 20
            total_w = len(main_btns) * btn_w + (len(main_btns) - 1) * gap
            start_x = cx - total_w // 2
            
            for i, b in enumerate(main_btns):
                x = start_x + i * (btn_w + gap)
                self.buttons.append(Button(b["text"], x, 320, btn_w, btn_h, b["col"], b["hover"], b["action"], font=self.small_bold_font, scale_on_hover=True, notification=b.get("notif", False)))
            
            # Barre d'outils en bas
            btn_w = 200
            btn_h = 60
            gap = 20
            start_y = 550
            
            # Ligne 1 : Progression & Économie (Mis en avant)
            self.buttons.extend([
                Button("BATTLE PASS", cx - 430, start_y, btn_w, btn_h, (0, 200, 100), (0, 230, 120), lambda: self.set_state("MENU_BATTLEPASS")),
                Button("MAGASIN", cx - 210, start_y, btn_w, btn_h, (255, 200, 0), (255, 220, 50), lambda: self.set_state("MENU_SHOP"), text_color=(50, 40, 0)),
                Button("INVENTAIRE", cx + 10, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_INVENTORY")),
                Button("SUCCÈS", cx + 230, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_ACHIEVEMENTS")),
            ])

            # Ligne 2 : Social & Système
            start_y += btn_h + gap
            self.buttons.extend([
                Button("MON PROFIL", cx - 430, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("INPUT_NAME")),
                Button("AMIS", cx - 210, start_y, btn_w, btn_h, PANEL_COLOR, HOVER_COLOR, lambda: self.open_friends_menu(from_lobby=False)),
                Button("PARAMÈTRES", cx + 10, start_y, btn_w, btn_h, (100, 100, 120), (140, 140, 160), lambda: self.set_state("SETTINGS")),
                Button("QUITTER", cx + 230, start_y, btn_w, btn_h, ALERT_COLOR, (255, 100, 120), self.ask_quit),
            ])
            
            self.buttons.append(Button("?", SCREEN_WIDTH - 80, 30, 50, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("HOW_TO"), font=self.small_bold_font))

        elif self.state == "MENU_ONLINE":
            self.buttons = [
                Button("HÉBERGER", cx - 250, 350, 240, 60, ACCENT_COLOR, HOVER_COLOR, self.setup_host),
                Button("REJOINDRE", cx + 10, 350, 240, 60, ACCENT_COLOR, HOVER_COLOR, self.setup_join),
                Button("RETOUR", cx - 120, 500, 240, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "SETUP":
            # --- NOUVELLE INTERFACE GRAPHIQUE (GRID LAYOUT) ---
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            
            # Dimensions des cartes
            card_w, card_h = 400, 180
            gap_x, gap_y = 40, 40
            
            # Positions (reorganisées)
            r1_y = cy - 220
            r2_y = cy + 20
            r3_y = cy + 240
            
            # --- ROW 1 ---
            # Joueurs OU Difficulté (Si Training)
            c1_x = cx - card_w // 2 - gap_x // 2
            if self.is_training:
                self.buttons.append(Button("<", c1_x - 185, r1_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('bot_difficulty', -1), text_color=TEXT_COLOR))
                self.buttons.append(Button(">", c1_x + 125, r1_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('bot_difficulty', 1), text_color=TEXT_COLOR))
            elif (self.is_local_game or self.is_host):
                self.buttons.append(Button("-", c1_x - 185, r1_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', -1), text_color=TEXT_COLOR))
                self.buttons.append(Button("+", c1_x + 125, r1_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('players', 1), text_color=TEXT_COLOR))
            
            # Mode (Droite)
            c2_x = cx + card_w // 2 + gap_x // 2
            self.buttons.append(Button("CHANGER", c2_x - 100, r1_y + 45, 200, 40, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('mode', 0), text_color=TEXT_COLOR))

            # --- ROW 2 ---
            # Temps (Gauche)
            c3_x = cx - card_w // 2 - gap_x // 2
            self.buttons.append(Button("-", c3_x - 185, r2_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', -1), text_color=TEXT_COLOR))
            self.buttons.append(Button("+", c3_x + 125, r2_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('time', 1), text_color=TEXT_COLOR))

            # Type de Jeu (Droite)
            c4_x = cx + card_w // 2 + gap_x // 2
            self.buttons.append(Button("<", c4_x - 195, r2_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('game_type', -1), text_color=TEXT_COLOR))
            self.buttons.append(Button(">", c4_x + 135, r2_y + 15, 60, 60, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('game_type', 0), text_color=TEXT_COLOR))

            # --- ROW 3 ---
            # Catégorie (Centre, Large)
            self.buttons.append(Button("<", cx - 380, r3_y - 55, 60, 110, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', -1), text_color=TEXT_COLOR))
            self.buttons.append(Button(">", cx + 320, r3_y - 55, 60, 110, PANEL_COLOR, ACCENT_COLOR, lambda: self.change_setting('category', 1), text_color=TEXT_COLOR))
            
            # Footer Actions
            action = self.start_local_game if self.is_local_game else self.start_host_lobby
            self.buttons = [
                *self.buttons,
                Button("LANCER LA PARTIE", cx - 200, cy + 320, 400, 80, ACCENT_COLOR, HOVER_COLOR, action),
                Button("RETOUR", 60, 60, 140, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "SETTINGS":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            
            # Grid Layout 2 colonnes
            col_w = 400
            gap = 40
            total_w = col_w * 2 + gap
            start_x = cx - total_w // 2
            start_y = cy - 150
            
            # Col 1 (Gauche) - Préférences
            c1_x = start_x
            sound_txt = "SON : ON" if self.sound_on else "SON : OFF"
            sound_col = ACCENT_COLOR if self.sound_on else (100, 100, 100)
            res_txt = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            
            upnp_txt = "UPnP : ON" if self.upnp_enabled else "UPnP : OFF"
            upnp_col = ACCENT_COLOR if self.upnp_enabled else (100, 100, 100)
            port_txt = f"PORT SERVEUR: {self.server_port}"
            
            self.buttons.append(Button(sound_txt, c1_x, start_y, col_w, 60, sound_col, HOVER_COLOR, self.toggle_sound))
            self.buttons.append(Button(upnp_txt, c1_x, start_y + 80, col_w, 60, upnp_col, HOVER_COLOR, self.toggle_upnp))
            self.buttons.append(Button(f"RÉSOLUTION ({res_txt})", c1_x, start_y + 160, col_w, 60, PANEL_COLOR, HOVER_COLOR, self.cycle_resolution))
            self.buttons.append(Button("TOUCHES / CLAVIER", c1_x, start_y + 240, col_w, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("CONTROLS")))
            self.buttons.append(Button("CATÉGORIES PERSO", c1_x, start_y + 320, col_w, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_CUSTOM_CATS")))
            self.buttons.append(Button("CRÉDITS", c1_x, start_y + 400, col_w, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_CREDITS")))

            # Col 2 (Droite) - Données
            c2_x = start_x + col_w + gap
            self.buttons.append(Button("EXPORTER SAUVEGARDE", c2_x, start_y, col_w, 60, PANEL_COLOR, HOVER_COLOR, self.export_save))
            self.buttons.append(Button("IMPORTER SAUVEGARDE", c2_x, start_y + 80, col_w, 60, PANEL_COLOR, HOVER_COLOR, self.import_save))
            self.buttons.append(Button("CODE CADEAU", c2_x, start_y + 160, col_w, 60, (255, 200, 0), (255, 220, 50), lambda: self.set_state("MENU_GIFT_CODE"), text_color=(50, 40, 0)))
            self.buttons.append(Button("RÉINITIALISER TOUT", c2_x, start_y + 240, col_w, 60, ALERT_COLOR, (255, 100, 120), self.confirm_reset))
            
            # Footer
            self.buttons.append(Button("RETOUR", 60, 60, 140, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))
        elif self.state == "MENU_SHOP":
            cx = SCREEN_WIDTH // 2
            
            # Configuration pour centrer tout le menu (Onglets + Tri)
            tab_w = 150
            spacing = 155
            sort_w = 180
            gap = 30
            
            # Largeur totale = (7 onglets) + gap + (sort)
            tabs_w = 6 * spacing + tab_w
            total_w = tabs_w + gap + sort_w
            start_x = cx - total_w // 2

            self.buttons.append(Button("TOUT", start_x, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "ALL" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("ALL")))
            self.buttons.append(Button("BORDURES", start_x + spacing, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "BORDER" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("BORDER")))
            self.buttons.append(Button("COULEURS", start_x + spacing*2, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "COLOR" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("COLOR")))
            self.buttons.append(Button("TITRES", start_x + spacing*3, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "TITLE" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("TITLE")))
            self.buttons.append(Button("THÈMES", start_x + spacing*4, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "THEME" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("THEME")))
            self.buttons.append(Button("BADGES", start_x + spacing*5, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "BADGE" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("BADGE")))
            self.buttons.append(Button("PACKS", start_x + spacing*6, 140, tab_w, 50, ACCENT_COLOR if self.shop_tab == "CATEGORY" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_shop_tab("CATEGORY")))

            # Bouton Tri
            sort_x = start_x + tabs_w + gap
            sort_txt = "TRI: TYPE"
            if self.shop_sort == "PRICE_ASC": sort_txt = "TRI: PRIX ↑"
            elif self.shop_sort == "PRICE_DESC": sort_txt = "TRI: PRIX ↓"
            elif self.shop_sort == "RARITY_DESC": sort_txt = "TRI: RARETÉ ↓"
            elif self.shop_sort == "RARITY_ASC": sort_txt = "TRI: RARETÉ ↑"
            self.buttons.append(Button(sort_txt, sort_x, 140, sort_w, 50, PANEL_COLOR, HOVER_COLOR, self.toggle_shop_sort))

            # Configuration Grille
            card_w, card_h = 260, 320
            # Calcul dynamique des colonnes
            available_w = SCREEN_WIDTH - 100
            cols = max(1, available_w // (card_w + 30))
            gap = 30
            start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
            start_y = 220 - self.shop_scroll # Décalé pour les onglets
            
            # Tous les items du catalogue (Triés par type puis prix)
            all_items = self.get_sorted_shop_items()
            
            # Filtrage
            filtered_items = []
            for item_id in all_items:
                item = SHOP_CATALOG[item_id]
                if self.shop_tab == "ALL": filtered_items.append(item_id)
                elif self.shop_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                elif self.shop_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                elif self.shop_tab == "TITLE" and item['type'] == 'title_style': filtered_items.append(item_id)
                elif self.shop_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                elif self.shop_tab == "BADGE" and item['type'] == 'badge': filtered_items.append(item_id)
                elif self.shop_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)

            for i, item_id in enumerate(filtered_items):
                item = SHOP_CATALOG[item_id]
                row = i // cols
                col = i % cols
                x = start_x + col * (card_w + gap)
                y = start_y + row * (card_h + gap)
                
                # Clipping simple pour ne pas dessiner par dessus le header
                if y + card_h < 200 or y > SCREEN_HEIGHT: continue
                
                # Bouton Action (Acheter / Équiper)
                btn_h = 50
                btn_y = y + card_h - btn_h - 15
                
                if item_id in self.inventory:
                    # Pas de bouton dans le magasin si possédé (géré par draw_shop_card qui affiche "POSSÉDÉ")
                    pass
                else:
                    if item['type'] == 'gift' and self.last_gift_date == str(datetime.date.today()):
                        self.buttons.append(Button("RÉCUPÉRÉ", x + 20, btn_y, card_w - 40, btn_h, (100, 100, 100), (100, 100, 100), None, font=self.small_bold_font, tag=item_id))
                    else:
                        btn_text = "ACHETER"
                        if item['price'] == 0: btn_text = "OBTENIR"
                        can_buy = self.coins >= item['price']
                        color = ACCENT_COLOR if can_buy else (80, 80, 80)
                        center_pos = (x + card_w//2, y + card_h//2)
                        action = lambda id=item_id, p=center_pos: self.buy_item(id, p)
                        self.buttons.append(Button(btn_text, x + 20, btn_y, card_w - 40, btn_h, color, HOVER_COLOR, action, font=self.small_bold_font, tag=item_id))

            self.buttons.append(Button("RETOUR", 40, 40, 120, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))

        elif self.state == "MENU_INVENTORY":
            cx = SCREEN_WIDTH // 2
            
            # Onglets (Tabs) - Centrés
            tab_w = 150
            spacing = 155
            tabs_w = 6 * spacing + tab_w
            start_x = cx - tabs_w // 2

            self.buttons.append(Button("TOUT", start_x, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "ALL" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("ALL")))
            self.buttons.append(Button("BORDURES", start_x + spacing, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "BORDER" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("BORDER")))
            self.buttons.append(Button("COULEURS", start_x + spacing*2, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "COLOR" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("COLOR")))
            self.buttons.append(Button("TITRES", start_x + spacing*3, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "TITLE" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("TITLE")))
            self.buttons.append(Button("THÈMES", start_x + spacing*4, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "THEME" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("THEME")))
            self.buttons.append(Button("BADGES", start_x + spacing*5, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "BADGE" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("BADGE")))
            self.buttons.append(Button("PACKS", start_x + spacing*6, 140, tab_w, 50, ACCENT_COLOR if self.inventory_tab == "CATEGORY" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_inventory_tab("CATEGORY")))

            self.buttons.append(Button("RETOUR", 40, 40, 120, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")))

        elif self.state == "MENU_FRIENDS":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            
            # Configuration Grille Amis
            card_w, card_h = 500, 140
            gap_x, gap_y = 40, 30
            
            # Calcul dynamique des colonnes (Adaptive)
            available_w = SCREEN_WIDTH - 100
            cols = max(1, available_w // (card_w + gap_x))
            cols = min(2, cols) # Max 2 colonnes pour l'esthétique
            
            start_y = 200
            start_x = cx - ((cols * card_w + (cols - 1) * gap_x) // 2)
            
            # Récupérer l'IP si pas encore fait
            if self.public_ip is None:
                threading.Thread(target=self.get_public_ip, daemon=True).start()
                
            for i, friend in enumerate(self.friends):
                row = i // cols
                col = i % cols
                x = start_x + col * (card_w + gap_x)
                y = start_y + row * (card_h + gap_y)
                
                # Actions dans la carte
                btn_y = y + 90
                can_invite = self.friends_menu_from_lobby and self.is_host
                
                # Bouton Rejoindre/Inviter
                if can_invite:
                    self.buttons.append(Button("INVITER", x + 100, btn_y, 180, 45, (50, 200, 50), HOVER_COLOR, lambda ip=friend['ip']: self.send_game_invite(ip), font=self.small_bold_font))
                else:
                    self.buttons.append(Button("REJOINDRE", x + 100, btn_y, 180, 45, ACCENT_COLOR, HOVER_COLOR, lambda ip=friend['ip']: self.join_friend(ip), font=self.small_bold_font))
                
                # Bouton Échanger
                self.buttons.append(Button("TRADE", x + 290, btn_y, 110, 45, (255, 200, 0), (255, 220, 50), lambda ip=friend['ip']: self.request_trade(ip), font=self.small_bold_font, text_color=(50, 40, 0)))
                
                # Bouton Supprimer (X en haut à droite de la carte)
                self.buttons.append(Button("X", x + card_w - 40, y + 10, 30, 30, ALERT_COLOR, (255, 100, 100), lambda idx=i: self.delete_friend(idx), font=self.small_bold_font))
            
            # Footer
            self.buttons.append(Button("COPIER CODE AMI", cx - 250, 800, 200, 40, ACCENT_COLOR, HOVER_COLOR, self.copy_ip, font=pygame.font.SysFont("Arial", 16, bold=True)))
            self.buttons.append(Button("AJOUTER UN AMI", cx + 50, 800, 200, 40, PANEL_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_ADD_FRIEND"), font=pygame.font.SysFont("Arial", 16, bold=True)))
            
            self.buttons.append(Button("RETOUR", 60, 40, 140, 60, ALERT_COLOR, (255, 100, 120), self.close_friends_menu))
        elif self.state == "MENU_ADD_FRIEND":
            port_txt = "PORT: MANUEL" if self.friend_custom_port else "PORT: AUTO"
            port_col = ACCENT_COLOR if self.friend_custom_port else PANEL_COLOR
            
            self.buttons = [
                Button("ENVOYER LA DEMANDE", cx - 200, 520, 400, 60, ACCENT_COLOR, HOVER_COLOR, self.request_friend),
                Button(port_txt, cx + 130, 320, 140, 40, port_col, HOVER_COLOR, self.toggle_friend_port, font=pygame.font.SysFont("Arial", 18, bold=True)),
                Button("ANNULER", cx - 200, 600, 400, 60, ALERT_COLOR, (255, 100, 120), lambda: self.open_friends_menu(from_lobby=self.friends_menu_from_lobby))
            ]
        elif self.state == "MENU_GIFT_CODE":
            self.buttons = [
                Button("VALIDER", cx - 200, 520, 400, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_gift_code),
                Button("ANNULER", cx - 200, 600, 400, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETTINGS"))
            ]
        elif self.state == "SNAKE_GAME":
            self.buttons = [
                Button("QUITTER", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETTINGS"))
            ]
        elif self.state == "COLOR_PICKER":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("VALIDER", cx - 160, 700, 150, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_color_picker),
                Button("ANNULER", cx + 10, 700, 150, 60, ALERT_COLOR, (255, 100, 100), lambda: self.set_state("MENU_CUSTOMIZE_LIST"))
            ]
        elif self.state == "MENU_HISTORY":
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("INPUT_NAME"))
            ]
        elif self.state == "MENU_ACHIEVEMENTS":
            cx = SCREEN_WIDTH // 2
            btn_w = 180
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN")),
                Button("TOUS", cx - btn_w - 10, 190, btn_w, 50, ACCENT_COLOR if self.achievements_filter == "ALL" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_achievements_filter("ALL")),
                Button("DÉBLOQUÉS", cx, 190, btn_w, 50, ACCENT_COLOR if self.achievements_filter == "UNLOCKED" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_achievements_filter("UNLOCKED")),
                Button("VERROUILLÉS", cx + btn_w + 10, 190, btn_w, 50, ACCENT_COLOR if self.achievements_filter == "LOCKED" else PANEL_COLOR, HOVER_COLOR, lambda: self.set_achievements_filter("LOCKED"))
            ]
        elif self.state == "TRADE_LOBBY":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            panel_w, panel_h = 500, 600
            gap = 100
            left_x = cx - panel_w - gap//2
            left_bottom = cy + panel_h//2
            
            lock_txt = "VERROUILLER" if not self.trade_lobby_data["me"]["locked"] else "DÉVERROUILLER"
            lock_col = ACCENT_COLOR if not self.trade_lobby_data["me"]["locked"] else (100, 100, 100)
            
            # Boutons sous le panneau "MOI"
            self.buttons = [
                Button("+10", left_x + 50, left_bottom - 160, 100, 50, (255, 215, 0), HOVER_COLOR, lambda: self.add_trade_coin(10), text_color=(0,0,0)),
                Button("+50", left_x + 160, left_bottom - 160, 100, 50, (255, 215, 0), HOVER_COLOR, lambda: self.add_trade_coin(50), text_color=(0,0,0)),
                Button("-10", left_x + 270, left_bottom - 160, 100, 50, (200, 150, 0), HOVER_COLOR, lambda: self.add_trade_coin(-10), text_color=(0,0,0)),
                
                Button(lock_txt, left_x + panel_w//2 - 100, left_bottom + 20, 200, 60, lock_col, HOVER_COLOR, self.update_trade_lock),
                Button("QUITTER", cx - 100, cy + panel_h//2 + 20, 200, 60, ALERT_COLOR, (255, 100, 120), self.reset_network)
            ]
        elif self.state == "MENU_CUSTOM_CATS":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            
            # Panel config
            panel_w = 900
            panel_h = 700
            panel_y = cy - panel_h // 2
            
            # Footer buttons (Déplacés en bas pour ne pas cacher le titre)
            self.buttons.append(Button("RETOUR", cx - panel_w//2 + 40, panel_y + panel_h - 80, 140, 50, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETTINGS")))
            self.buttons.append(Button("+ CRÉER", cx + panel_w//2 - 180, panel_y + panel_h - 80, 140, 50, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("EDIT_CAT_NAME")))
            
            # List config
            list_y = panel_y + 120
            list_h = panel_h - 160
            item_h = 90
            gap = 15
            
            cats = list(self.custom_categories.keys())
            total_h = len(cats) * (item_h + gap)
            max_scroll = max(0, total_h - list_h)
            if self.custom_cats_scroll > max_scroll: self.custom_cats_scroll = max_scroll
            if self.custom_cats_scroll < 0: self.custom_cats_scroll = 0
            
            # List items
            for i, cat in enumerate(cats):
                y = list_y + i * (item_h + gap) - self.custom_cats_scroll
                # Clipping
                if y + item_h > list_y and y < list_y + list_h:
                    # Delete button (Trash icon style)
                    btn_x = cx + panel_w//2 - 100
                    self.buttons.append(Button("🗑️", btn_x, y + 20, 50, 50, (40, 45, 55), (255, 80, 80), lambda c=cat: self.delete_custom_category(c), font=self.ui_emoji_font))

        elif self.state == "EDIT_CAT_NAME":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("SUIVANT", cx - 150, 550, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("EDIT_CAT_WORDS") if self.cat_name_input else None),
                Button("ANNULER", cx - 150, 630, 300, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_CUSTOM_CATS"))
            ]
        elif self.state == "MENU_SPIN":
            self.buttons.append(Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_SHOP")))
        elif self.state == "MENU_STATS":
            self.buttons.append(Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("INPUT_NAME")))
        elif self.state == "EDIT_CAT_WORDS":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("SAUVEGARDER", cx - 150, 650, 300, 60, ACCENT_COLOR, HOVER_COLOR, self.save_custom_category),
                Button("RETOUR", cx - 150, 730, 300, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("EDIT_CAT_NAME"))
            ]
        elif self.state == "MENU_BATTLEPASS":
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_MAIN"))
            ]
            
            list_y = 260
            list_h = 600
            item_h = 100
            gap = 15
            cx = SCREEN_WIDTH // 2
            s_level = self.stats["season"]["level"]
            
            for i, lvl in enumerate(range(5, 101, 5)):
                y = list_y + i * (item_h + gap) - self.season_scroll
                if y + item_h < list_y or y > list_y + list_h: continue
                
                unlocked = lvl <= s_level
                claimed = lvl in self.stats["season"]["claimed"]
                
                if unlocked and not claimed:
                    btn_x = cx + 400 - 260
                    btn_y = y + 20
                    self.buttons.append(Button("RÉCUPÉRER", btn_x, btn_y, 240, 60, (0, 200, 150), HOVER_COLOR, lambda l=lvl: self.claim_season_reward(l), font=self.small_bold_font))
        elif self.state == "CONTROLS":
            cx = SCREEN_WIDTH // 2
            # Simple toggle pour l'exemple, ou juste affichage
            contest_key = "MAJ GAUCHE" if self.keys["CONTEST"] == pygame.K_LSHIFT else "TAB"
            validate_key = "ENTRÉE"
            self.buttons = [
                Button(f"CONTESTER : {contest_key}", cx - 200, 350, 400, 60, PANEL_COLOR, HOVER_COLOR, self.toggle_contest_key),
                Button(f"VALIDER : {validate_key}", cx - 200, 450, 400, 60, PANEL_COLOR, PANEL_COLOR, None), # Informatif
                Button("RETOUR", cx - 200, 600, 400, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("SETTINGS"))
            ]
        elif self.state == "MENU_CREDITS":
            self.buttons = [
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETTINGS"))
            ]
        elif self.state == "OPPONENT_LEFT":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("MENU PRINCIPAL (AUTO)", cx - 150, 500, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))
            ]
        elif self.state == "MENU_JOIN":
            cx = SCREEN_WIDTH // 2
            
            port_txt = "PORT: MANUEL" if self.join_custom_port else "PORT: AUTO"
            port_col = ACCENT_COLOR if self.join_custom_port else PANEL_COLOR
            
            self.buttons = [
                Button("CONNEXION", cx - 150, 530, 300, 70, ACCENT_COLOR, HOVER_COLOR, self.connect_to_host),
                Button(port_txt, cx + 180, 320, 140, 40, port_col, HOVER_COLOR, self.toggle_join_port, font=pygame.font.SysFont("Arial", 18, bold=True)),
                Button("MES AMIS", cx - 150, 620, 300, 60, PANEL_COLOR, HOVER_COLOR, lambda: self.open_friends_menu(from_lobby=False)),
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("MENU_ONLINE"))
            ]
        elif self.state == "GAME_OVER":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            base_y = cy + 300 # Remonté pour éviter le débordement et laisser place au texte
            
            if not self.is_local_game:
                # Layout 3 colonnes avec GG au milieu
                self.buttons = [
                    Button("RECOMMENCER" if not self.rematch_ready[self.my_id] else "EN ATTENTE...", 
                           cx - 450, base_y, 280, 60, 
                           ACCENT_COLOR if not self.rematch_ready[self.my_id] else (100, 100, 100), 
                           HOVER_COLOR, self.request_rematch),
                    Button("GG !", cx - 100, base_y, 200, 60, (255, 200, 0), HOVER_COLOR, self.send_gg),
                    Button("MENU PRINCIPAL", cx + 170, base_y, 280, 60, PANEL_COLOR, HOVER_COLOR, self.reset_network),
                    Button("QUITTER", cx - 100, base_y + 80, 200, 60, ALERT_COLOR, (255, 100, 120), self.ask_quit)
                ]
            else:
                # Layout standard
                self.buttons = [
                    Button("RECOMMENCER" if not self.rematch_ready[self.my_id] else "EN ATTENTE...", 
                           cx - 300, base_y, 250, 60, 
                           ACCENT_COLOR if not self.rematch_ready[self.my_id] else (100, 100, 100), 
                           HOVER_COLOR, self.request_rematch),
                    Button("MENU PRINCIPAL", cx + 50, base_y, 250, 60, PANEL_COLOR, HOVER_COLOR, self.reset_network),
                    Button("QUITTER", cx - 100, base_y + 80, 200, 60, ALERT_COLOR, (255, 100, 120), self.ask_quit)
                ]
        elif self.state == "CONFIRM_QUIT":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            self.buttons = [
                Button("OUI, QUITTER", cx - 220, cy + 50, 200, 70, ALERT_COLOR, (255, 100, 100), self.force_quit),
                Button("NON, RETOUR", cx + 20, cy + 50, 200, 70, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state(self.prev_state))
            ]
        elif self.state == "CONFIRM_LEAVE":
            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2
            self.buttons = [
                Button("OUI, QUITTER", cx - 220, cy + 50, 200, 70, ALERT_COLOR, (255, 100, 100), self.reset_network),
                Button("NON, RESTER", cx + 20, cy + 50, 200, 70, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("LOBBY"))
            ]
        elif self.state == "LOCAL_NAMES":
            cx = SCREEN_WIDTH // 2
            self.buttons = [
                Button("LANCER", cx - 150, 600, 300, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_local_names),
                Button("RETOUR", 50, 50, 150, 60, ALERT_COLOR, (255, 100, 120), lambda: self.set_state("SETUP"))
            ]
        elif self.state == "LOBBY":
            self.update_lobby_buttons()

    def set_state(self, new_state):
        if new_state == self.state: return
        self.next_state = new_state
        self.transition_state = "OUT"

    def _apply_state_change(self):
        self.buttons = []
        if self.state == "MENU_MAIN" and not self.daily_reward_claimed:
            self.check_daily_login()
            self.daily_reward_claimed = True
        self.avatar_grid_buttons = []
        if self.state == "INPUT_NAME":
            self.selected_lobby_player_id = None
            self.lobby_player_rects.clear()
            self.avatar_scroll = 0
            self.active_input_field = "USERNAME"
        if self.state == "MENU_GIFT_CODE":
            self.gift_code_input = ""
        if self.state == "MENU_FRIENDS":
            self.connect_status = "" # Reset copy feedback
        if self.state == "MENU_SHOP":
            self.shop_scroll = 0
            self.shop_tab = "ALL"
        if self.state == "MENU_INVENTORY":
            self.inventory_scroll = 0
            self.inventory_tab = "ALL"
        if self.state == "MENU_ACHIEVEMENTS":
            self.achievements_scroll = 0
            self.achievements_filter = "ALL"
        if self.state == "MENU_CUSTOM_CATS":
            self.custom_cats_scroll = 0
        if self.state == "MENU_JOIN":
            self.active_input_field = "JOIN_IP"
        if self.state == "MENU_ADD_FRIEND":
            self.active_input_field = "FRIEND_IP"
        if self.state == "MENU_SPIN":
            self.spin_result = None
            self.popup = None
        
        if self.state in ["MENU_MAIN", "MENU_ONLINE", "SETUP", "INPUT_NAME", "GAME_OVER", "SETTINGS", "CONTROLS", "OPPONENT_LEFT", "MENU_JOIN", "TUTORIAL", "MENU_FRIENDS", "MENU_ADD_FRIEND", "CONFIRM_QUIT", "CONFIRM_LEAVE", "MENU_CUSTOM_CATS", "EDIT_CAT_NAME", "EDIT_CAT_WORDS", "MENU_SHOP", "MENU_INVENTORY", "TRADE_LOBBY", "CROP_AVATAR", "MENU_ACHIEVEMENTS", "MENU_HISTORY", "COLOR_PICKER", "PAUSED", "LOCAL_NAMES", "MENU_BATTLEPASS", "MENU_CREDITS", "MENU_GIFT_CODE", "SNAKE_GAME"]:
            self.create_menu_buttons()
        elif self.state == "HOW_TO":
            self.buttons = [Button("RETOUR", 50, 50, 150, 50, ACCENT_COLOR, HOVER_COLOR, lambda: self.set_state("MENU_MAIN"))]
        elif self.state in ["MENU_SPIN", "MENU_STATS"]:
            self.create_menu_buttons()
        elif self.state == "LOBBY":
            self.update_lobby_buttons()
        elif self.state == "JUDGMENT":
            cx = SCREEN_WIDTH // 2
            if self.is_local_game or self.judge_id == self.my_id:
                # Determine loser (the one who spoke previously)
                loser_id = (self.current_player - 1) % self.settings['players']
                self.buttons = [
                    Button("QUITTER", 20, 20, 120, 40, ALERT_COLOR, (255, 100, 100), self.quit_game),
                    Button("RECOMMENCER (R)", cx - 320, 300, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.send_action("RESTART")),
                    Button("POINT ADVERSE (P)", cx + 20, 300, 300, 60, ACCENT_COLOR, HOVER_COLOR, lambda: self.send_action(f"POINT|JUDGMENT|{loser_id}")),
                    Button("ANNULER (C)", cx - 100, 400, 200, 60, (100, 100, 100), (150, 150, 150), lambda: self.send_action("CONTINUE"))
                ]
            else:
                self.buttons = []
        elif self.state == "CROP_AVATAR":
            self.buttons = [
                Button("VALIDER", SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT - 100, 150, 60, ACCENT_COLOR, HOVER_COLOR, self.validate_crop),
                Button("ANNULER", SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT - 100, 150, 60, ALERT_COLOR, (255, 100, 100), lambda: self.set_state("INPUT_NAME"))
            ]

    def update_lobby_buttons(self):
        cx = SCREEN_WIDTH // 2
        self.buttons = []
        
        # Sécurité: vérifier que ready_status est bien initialisé
        if not self.ready_status or len(self.ready_status) != self.settings['players']:
            self.ready_status = [False] * self.settings['players']
        
        if self.my_id >= len(self.ready_status):
            self.my_id = 0
        
        # Bouton Retour
        self.buttons.append(Button("RETOUR", 50, 50, 150, 50, ALERT_COLOR, (255, 100, 120), self.ask_leave_lobby))
        self.buttons.append(Button("AMIS", 220, 50, 150, 50, PANEL_COLOR, HOVER_COLOR, lambda: self.open_friends_menu(from_lobby=True)))
        
        # Bouton Prêt - Sécurité maximale
        if self.my_id >= len(self.ready_status):
            self.ready_status.extend([False] * (self.my_id - len(self.ready_status) + 1))
        
        ready_col = (100, 200, 100) if self.ready_status[self.my_id] else (200, 100, 100)
        ready_txt = "ANNULER" if self.ready_status[self.my_id] else "PRÊT !"
        # Position sous le panneau joueurs
        self.buttons.append(Button(ready_txt, 350 - 125, 770, 250, 70, ready_col, HOVER_COLOR, self.toggle_ready, font=self.medium_font))

        # --- Player Cards Interaction ---
        panel_x, panel_y = 50, 170 # Décalage pour le nouveau header agrandi
        panel_w = 600
        start_y = panel_y + 20 # Alignement corrigé avec le dessin (120px)
        card_h = 110
        gap = 15

        for i in range(self.settings['players']):
            y_pos = start_y + i * (card_h + gap)
            
            # Identifier le joueur
            p_ip = None
            p_name = ""
            is_me = False
            has_player = False
            
            if self.is_host:
                if i == 0: is_me = True; has_player = True
                elif i - 1 < len(self.clients):
                    p_ip = self.clients[i-1].get('ip')
                    p_name = self.clients[i-1].get('name')
                    has_player = True
                elif self.test_mode and i == 1:
                    p_name = "Bot (Dev)"
                    has_player = True
            else:
                if i == self.my_id: is_me = True; has_player = True
                elif i in self.lobby_cache:
                    p_ip = self.lobby_cache[i].get('ip')
                    p_name = self.lobby_cache[i].get('name')
                    has_player = True
                elif i == 0 and not self.is_local_game: # Host
                    p_ip = self.input_ip
                    p_name = "Hôte" # Nom pas toujours dispo ici si pas dans cache, mais bon
                    has_player = True

            if has_player:
                # Bouton Kick (Host only, not on self)
                if self.is_host and not is_me and i > 0:
                     client_id = self.clients[i-1]['id'] if i-1 < len(self.clients) else -1
                     if client_id != -1:
                        self.buttons.append(Button("X", panel_x + panel_w - 60, y_pos + 10, 40, 40, ALERT_COLOR, (255, 100, 100), lambda cid=client_id: self.kick_client(cid)))

                # Bouton Add Friend (Pas moi, pas déjà ami)
                # Vérification robuste (IP ou Nom) pour éviter les doublons
                is_friend = False
                for f in self.friends:
                    if f['ip'] == p_ip or f['name'] == p_name:
                        is_friend = True
                        break
                
                if not is_me and p_ip and not is_friend:
                     self.buttons.append(Button("+", panel_x + panel_w - 110, y_pos + 10, 40, 40, (50, 200, 50), HOVER_COLOR, lambda ip=p_ip, n=p_name: self.direct_add_friend(ip, n)))

        # Bouton Wizz
        chat_x = 680
        chat_w = SCREEN_WIDTH - chat_x - 50
        chat_bottom = SCREEN_HEIGHT - 50
        
        # Emotes Rapides
        emotes = ["👋", "😂", "😭", "😡", "😱", "👍", "👎", "🔥", "GG", "EZ", "🤔", "👀"]
        emote_size = 45
        emote_gap = 10
        total_emote_w = len(emotes) * (emote_size + emote_gap)
        emote_start_x = chat_x + (chat_w - total_emote_w) // 2
        emote_y = chat_bottom - 110 # Au dessus de l'input
        
        for idx, emo in enumerate(emotes):
            self.buttons.append(Button(emo, emote_start_x + idx*(emote_size+emote_gap), emote_y, emote_size, emote_size, PANEL_COLOR, HOVER_COLOR, lambda e=emo: self.send_chat(e), font=self.ui_emoji_font))

        # Wizz Button (Redesign: Circular Icon)
        def try_wizz():
            now = pygame.time.get_ticks()
            if now - self.last_wizz_time > 5000: # 5 secondes cooldown
                self.last_wizz_time = now
                self.send_action("BUZZ")
            else:
                self.show_notification("Wizz en recharge...", type="error")

        self.buttons.append(Button("⚡", chat_x + chat_w - 60, chat_bottom - 55, 50, 50, (255, 200, 0), (255, 255, 100), try_wizz, font=self.ui_emoji_font, text_color=(0,0,0)))

        # --- Player Profile Popup Buttons ---
        if self.selected_lobby_player_id is not None:
            p_data = self.get_player_data_by_id(self.selected_lobby_player_id)

            if p_data:
                # Popup centered on the left panel
                popup_cx, popup_cy = 350, 400
                
                # Add Friend button
                is_me = (self.selected_lobby_player_id == self.my_id and not self.is_local_game) or (self.is_local_game and self.selected_lobby_player_id == 0)
                is_friend = any(f['ip'] == p_data.get('ip') for f in self.friends)
                if not is_me and not is_friend and p_data.get('ip') and p_data.get('ip') != "local":
                    self.buttons.append(Button("AJOUTER EN AMI", popup_cx - 125, popup_cy + 160, 250, 50, ACCENT_COLOR, HOVER_COLOR, lambda ip=p_data['ip'], n=p_data['name']: self.direct_add_friend(ip, n)))

                # Close button
                popup_w, popup_h = 580, 350
                self.buttons.append(Button("X", popup_cx + popup_w//2 - 25, popup_cy - popup_h//2 + 5, 40, 40, ALERT_COLOR, (255, 100, 100), self.close_lobby_popup))

    def validate_name(self):
        if len(self.username) > 0:
            self.save_settings()
            self.set_state("MENU_MAIN")

    def change_setting(self, key, delta):
        if key == 'players':
            self.settings['players'] = max(2, min(4, self.settings['players'] + delta)) # Max 4 joueurs pour fiabilité
            # Réinitialiser les scores si on change le nombre de joueurs
            self.score = [0] * self.settings['players']
            self.ready_status = [False] * self.settings['players']
            self.rematch_ready = [False] * self.settings['players']
        elif key == 'time':
            limit = 20 if self.settings['mode'] == 'WRITTEN' else 10
            self.settings['time'] = max(3, min(limit, self.settings['time'] + delta))
        elif key == 'win_score':
            self.settings['win_score'] = max(5, min(50, self.settings['win_score'] + delta))
        elif key == 'mode':
            self.settings['mode'] = 'WRITTEN' if self.settings['mode'] == 'VOCAL' else 'VOCAL'
        elif key == 'category':
            cats = list(self.all_categories.keys())
            # Ajouter les catégories non possédées pour les voir (verrouillées)
            for k, v in SHOP_CATALOG.items():
                if v.get('type') == 'category' and v['name'] not in cats:
                    cats.append(v['name'])
            
            if self.settings['category'] not in cats: self.settings['category'] = "GÉNÉRAL"

            current_idx = cats.index(self.settings['category'])
            next_idx = (current_idx + delta) % len(cats)
            if next_idx < 0: # Handle negative modulo result for previous button
                next_idx += len(cats)
            self.settings['category'] = cats[next_idx]
        elif key == 'game_type':
            modes = ['NORMAL', 'SURVIVAL', 'SPEED', 'HARDCORE', 'CHAOS', 'TIME_TRIAL']
            curr = self.settings.get('game_type', 'NORMAL')
            try:
                idx = modes.index(curr)
            except: idx = 0
            self.settings['game_type'] = modes[(idx + 1) % len(modes)]
        elif key == 'bot_difficulty':
            diffs = ["FACILE", "MOYEN", "DIFFICILE", "HARDCORE"]
            try: idx = diffs.index(self.bot_difficulty)
            except: idx = 1
            self.bot_difficulty = diffs[(idx + delta) % len(diffs)]
        
        # Recréer les boutons pour mettre à jour l'affichage (si besoin)
        if self.state == "SETUP":
            self.create_menu_buttons()
        if self.state == "SETUP" or self.state == "LOBBY":
            if self.state == "LOBBY":
                self.update_lobby_buttons()
                if self.is_host:
                    self.broadcast_settings()
            else:
                self.create_menu_buttons()

    def toggle_contest_key(self):
        if self.keys["CONTEST"] == pygame.K_LSHIFT:
            self.keys["CONTEST"] = pygame.K_TAB
        else:
            self.keys["CONTEST"] = pygame.K_LSHIFT
        self.save_settings()
        self.create_menu_buttons()

    def toggle_ready(self):
        # Sécurité: vérifier que les indices sont valides
        if self.my_id >= len(self.ready_status):
            self.ready_status.extend([False] * (self.my_id - len(self.ready_status) + 1))
        if len(self.ready_status) != self.settings['players']:
            self.ready_status = [False] * self.settings['players']
        
        self.ready_status[self.my_id] = not self.ready_status[self.my_id]
        
        if self.ready_status[self.my_id]: self.play_sound("success")
        else: self.play_sound("error")
        
        # En mode test (DEV), le bot se met prêt automatiquement avec nous
        if self.test_mode and self.is_host and len(self.ready_status) > 1:
            self.ready_status[1] = self.ready_status[self.my_id]
            
        status_str = "1" if self.ready_status[self.my_id] else "0"
        if not self.is_local_game:
            if self.is_host:
                self.broadcast_player_list() # Host broadcast tout pour sync parfaite
            else:
                self.send_data(f"READY|{self.my_id}|{status_str}")
        self.update_lobby_buttons() # Refresh color/text
        self.check_start_game()

    def toggle_pause(self):
        if not self.is_local_game:
            self.show_notification("Pause impossible en ligne !", "error")
            return
        
        if self.state == "GAME":
            self.paused_at = pygame.time.get_ticks()
            self.state = "PAUSED"
            self.create_menu_buttons()
        elif self.state == "PAUSED":
            duration = pygame.time.get_ticks() - self.paused_at
            self.start_ticks += duration
            self.freeze_until += duration
            self.state = "GAME"
            self.create_menu_buttons()

    def quit_game(self):
        if not self.is_local_game:
            self.send_data("QUIT")
        self.reset_network()

    def send_gg(self):
        self.send_chat("GG ! Bien joué.")
        self.send_action("GG_EFFECT")

    def handle_opponent_quit(self):
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        self.conn = None
        self.server = None
        self.connected = False
        self.opponent_left_time = pygame.time.get_ticks()
        self.set_state("OPPONENT_LEFT")

    # --- RÉSEAU ---
    def reset_network(self):
        # UPnP reste ouvert tant que l'application est lancée
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        self.conn = None
        self.server = None
        self.connected = False
        self.trade_finalize_at = 0
        self.trade_coin_particles = []
        self.trade_lobby_data["countdown"] = None
        self.selected_lobby_player_id = None
        self.set_state("MENU_MAIN")
        self.chat_messages = []
        self.ready_status = [False] * self.settings['players']
        self.network_queue = [] # Vider la file pour éviter les bugs de retour en jeu

    def setup_local(self):
        self.is_local_game = True
        self.is_training = False
        self.current_player = 0
        self.score = [0] * self.settings['players']
        self.rematch_ready = [False] * self.settings['players']
        self.set_state("SETUP")
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.ready_status = [False] * self.settings['players']
        self.turn_count = 0
        self.rally_combo = 0

    def setup_training(self):
        self.is_local_game = True
        self.is_training = True
        self.current_player = 0
        self.settings['players'] = 2
        self.score = [0, 0]
        self.rematch_ready = [False, False]
        self.ready_status = [True, True]
        self.turn_count = 0
        self.rally_combo = 0
        self.bot_difficulty = "MOYEN"
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.set_state("SETUP")

    def validate_local_names(self):
        self.global_timer_start = 0
        self.start_round()

    def start_local_game(self):
        if self.is_training:
            self.local_player_names = [self.username, "Bot Entraînement"]
            self.validate_local_names()
            return

        self.local_player_names = [f"Joueur {i+1}" for i in range(self.settings['players'])]
        self.local_player_names[0] = self.username
        self.active_local_name_idx = -1
        self.set_state("LOCAL_NAMES")

    def setup_host(self):
        self.is_host = True
        self.is_local_game = False
        self.is_training = False
        self.my_id = 0
        self.current_player = 0
        self.clients = []
        self.settings['players'] = 2
        self.round_num = 1
        self.turn_count = 0
        self.rally_combo = 0
        self.score = [0] * self.settings['players']
        self.last_round_reason = ""
        self.rematch_ready = [False] * self.settings['players']
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.ready_status = [False] * self.settings['players']
        self.set_state("SETUP")
        

    def get_public_ip(self):
        if self.is_fetching_ip: return
        self.is_fetching_ip = True
        try:
            self.public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8')
        except:
            self.public_ip = None
        self.is_fetching_ip = False

    def try_upnp(self):
        if not self.upnp_enabled:
            self.upnp_status = "Désactivé"
            return

        # Tentative d'ouverture de port automatique (UPnP) ULTRA ROBUSTE
        self.upnp_status = "Recherche Box..."
        import xml.etree.ElementTree as ET
        from urllib.parse import urlparse
        import re
        
        # Liste des services cibles (v1 et v2)
        target_services = [
            "urn:schemas-upnp-org:service:WANIPConnection:1",
            "urn:schemas-upnp-org:service:WANIPConnection:2",
            "urn:schemas-upnp-org:service:WANPPPConnection:1"
        ]

        try:
            # 1. Découverte SSDP (Broadcast multiple et écoute prolongée)
            msg = \
                'M-SEARCH * HTTP/1.1\r\n' \
                'HOST:239.255.255.250:1900\r\n' \
                'ST:urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n' \
                'MAN:"ssdp:discover"\r\n' \
                'MX:2\r\n' \
                '\r\n'
            
            locations = set()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.settimeout(2)
            s.sendto(msg.encode(), ('239.255.255.250', 1900))
            
            # On écoute pendant 2.5 secondes pour récupérer TOUTES les réponses
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < 2500:
                try:
                    data, addr = s.recvfrom(1024)
                    resp = data.decode(errors='ignore')
                    loc = re.search(r'LOCATION:\s*(.*)', resp, re.IGNORECASE)
                    if loc:
                        locations.add(loc.group(1).strip())
                except socket.timeout:
                    break
                except:
                    pass
            s.close()

            if not locations:
                self.upnp_status = "Box introuvable (UPnP OFF)"
                return

            # 2. Essayer chaque appareil trouvé
            for location in locations:
                try:
                    # Téléchargement XML
                    xml_raw = urllib.request.urlopen(location, timeout=3).read().decode(errors='ignore')
                    
                    # Nettoyage namespaces pour parsing facile avec ElementTree
                    xml_clean = re.sub(r' xmlns="[^"]+"', '', xml_raw)
                    root = ET.fromstring(xml_clean)
                    
                    control_url = None
                    service_type = None
                    
                    # Recherche du service WAN (IP ou PPP)
                    for service in root.findall(".//service"):
                        stype = service.find("serviceType")
                        if stype is not None and stype.text in target_services:
                            surl = service.find("controlURL")
                            if surl is not None:
                                service_type = stype.text
                                control_url = surl.text
                                break
                    
                    if not control_url: continue

                    # Construction URL absolue
                    parsed = urlparse(location)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    
                    # Check URLBase
                    urlbase = root.find("URLBase")
                    if urlbase is not None and urlbase.text:
                        base_url = urlbase.text.rstrip("/")
                    
                    if not control_url.startswith("http"):
                        if not control_url.startswith("/"):
                            control_url = "/" + control_url
                        control_url = base_url + control_url

                    # 3. Envoi SOAP AddPortMapping
                    # Essayer une plage de ports si le 5000 est pris (conflit même box)
                    for ext_port in range(self.server_port, self.server_port + 6):
                        try:
                            soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body><u:AddPortMapping xmlns:u="{service_type}">
<NewRemoteHost></NewRemoteHost><NewExternalPort>{ext_port}</NewExternalPort><NewProtocol>TCP</NewProtocol>
<NewInternalPort>{self.server_port}</NewInternalPort><NewInternalClient>{self.local_ip}</NewInternalClient>
<NewEnabled>1</NewEnabled><NewPortMappingDescription>WorldRush</NewPortMappingDescription>
<NewLeaseDuration>0</NewLeaseDuration>
</u:AddPortMapping></s:Body></s:Envelope>"""
            
                            headers = {
                                'SOAPAction': f'"{service_type}#AddPortMapping"',
                                'Content-Type': 'text/xml',
                                'Connection': 'Close'
                            }
                            req = urllib.request.Request(control_url, soap_body.encode(), headers)
                            urllib.request.urlopen(req, timeout=3)
                            
                            self.upnp_status = "SUCCÈS (Port Ouvert)"
                            if ext_port != self.server_port:
                                self.upnp_status = f"SUCCÈS (Port {ext_port})"
                            self.upnp_control_url = control_url
                            self.upnp_service_type = service_type
                            self.external_port = ext_port
                            return
                        except:
                            continue
                except:
                    continue
            
            self.upnp_status = "ÉCHEC (Box incompatible)"
        except Exception as e:
            self.upnp_status = "Erreur Réseau"

    def remove_upnp(self):
        if self.upnp_control_url and self.upnp_service_type:
            print("Fermeture UPnP en cours...")
            success = False
            for i in range(2): # 2 tentatives pour être sûr
                try:
                    soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body><u:DeletePortMapping xmlns:u="{self.upnp_service_type}">
<NewRemoteHost></NewRemoteHost><NewExternalPort>{self.external_port}</NewExternalPort><NewProtocol>TCP</NewProtocol>
</u:DeletePortMapping></s:Body></s:Envelope>"""
                    headers = {'SOAPAction': f'"{self.upnp_service_type}#DeletePortMapping"', 'Content-Type': 'text/xml', 'Connection': 'Close'}
                    req = urllib.request.Request(self.upnp_control_url, soap_body.encode(), headers)
                    with urllib.request.urlopen(req, timeout=3) as response:
                        if response.status == 200:
                            print("UPnP: Port fermé avec succès !")
                            success = True
                            break
                except Exception as e:
                    print(f"Tentative {i+1} échouée: {e}")
            
            self.upnp_control_url = None

    def ask_quit(self):
        self.prev_state = self.state
        self.set_state("CONFIRM_QUIT")
        
    def ask_leave_lobby(self):
        self.prev_state = self.state
        self.set_state("CONFIRM_LEAVE")


    def kick_client(self, client_id):
        for c in self.clients:
            if c['id'] == client_id:
                try: c['conn'].close()
                except: pass
                if c in self.clients: self.clients.remove(c)
                msg = f"SYSTEM: {c['name']} a été exclu."
                self.chat_messages.append(msg)
                self.broadcast_player_list()
                self.send_data(f"CHAT|{msg}")
                self.create_menu_buttons()
                break

    def force_quit(self):
        self.state = "EXITING"
        self.draw_background()
        self.draw_text("FERMETURE DES PORTS...", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.draw_text("Nettoyage UPnP et déconnexion...", self.font, TEXT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
        pygame.display.flip()
        
        self.remove_upnp()
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()

    def start_host_lobby(self):
        self.set_state("LOBBY")
        # Le listener global gère maintenant les connexions entrantes

    def host_receive_client_data(self, client):
        buffer = b""
        while True:
            try:
                if len(buffer) > 2000000: buffer = b"" # Sécurité anti-flood (Augmenté pour avatars)
                data = client['conn'].recv(16384)
                if not data: break
                buffer += data
                while b"\n" in buffer:
                    msg_bytes, buffer = buffer.split(b"\n", 1)
                    msg = msg_bytes.decode('utf-8').strip()
                    if msg == "PONG":
                        client['ping'] = pygame.time.get_ticks() - client.get('last_ping_sent', 0)
                        self.broadcast_player_list()
                        continue
                    if msg: self.network_queue.append(f"FROM|{client['id']}|{msg}")
            except Exception: break
        
        with self.clients_lock:
            if client in self.clients:
                self.clients.remove(client)
        msg = f"SYSTEM: {client['name']} est parti."
        self.chat_messages.append(msg)
        self.send_data(f"CHAT|{msg}")
        self.broadcast_player_list()
        self.network_queue.append("REFRESH_LOBBY")

    def kick_client(self, client_id):
        with self.clients_lock:
            for c in self.clients:
                if c['id'] == client_id:
                    try: c['conn'].close()
                    except: pass
                    if c in self.clients: self.clients.remove(c)
                    msg = f"SYSTEM: {c['name']} a été exclu."
                    self.chat_messages.append(msg)
                    self.broadcast_player_list()
                    self.send_data(f"CHAT|{msg}")
                    self.create_menu_buttons()
                    break

    def force_quit(self):
        self.state = "EXITING"
        self.draw_background()
        self.draw_text("FERMETURE DES PORTS...", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.draw_text("Nettoyage UPnP et déconnexion...", self.font, TEXT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
        pygame.display.flip()
        
        self.remove_upnp()
        if self.conn: self.conn.close()
        if self.server: self.server.close()
        pygame.time.delay(800)
        pygame.quit()
        sys.exit()


    def broadcast_player_list(self):
        with self.clients_lock:
            # Sécurité: vérifier que ready_status est initialisé
            if not self.ready_status or len(self.ready_status) == 0:
                self.ready_status = [False] * self.settings['players']
            
            # Envoie la liste des joueurs à tout le monde
            # Format: PLAYERS|id,name,avatar,border,ready,name_color,ip,level,theme,ping;id,name...
            host_ip = self.public_ip if self.public_ip else self.local_ip
            ready_val = int(self.ready_status[0]) if len(self.ready_status) > 0 else 0
            p_list = [f"0,{self.username},{self.avatar},{self.equipped['border']},{ready_val},{self.equipped['name_color']},{host_ip},{self.level},{self.equipped['theme']},0,{self.equipped['badge']},{self.stats.get('win_streak', 0)}"]
            for c in self.clients:
                p_list.append(f"{c['id']},{c['name']},{c['avatar']},{c['border']},{int(c['ready'])},{c.get('name_color', 'name_color_default')},{c.get('ip','')},{c.get('level', 1)},{c.get('theme', 'theme_default')},{c.get('ping', 0)},{c.get('badge', 'badge_default')},{c.get('streak', 0)}")
            
            msg = "PLAYERS|" + ";".join(p_list)
        
        # Envoyer hors du lock pour éviter blocage / deadlock si un client est lent
        self.send_data(msg)

    def setup_join(self):
        self.is_host = False
        self.is_local_game = False
        self.is_training = False
        self.my_id = 1
        self.current_player = 0
        self.settings['players'] = 2
        self.round_num = 1
        self.turn_count = 0
        self.rally_combo = 0
        self.score = [0] * self.settings['players']
        self.last_round_reason = ""
        self.rematch_ready = [False] * self.settings['players']
        self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
        self.opponent_name = "Adversaire"
        self.opponent_avatar = "🙂"
        self.opponent_border = "border_default"
        self.set_state("MENU_JOIN")
        self.chat_messages = []
        self.ready_status = [False] * self.settings['players']
        self.connect_status = ""
        self.is_connecting = False
        self.reset_history()

    def connect_to_host(self):
        if self.is_connecting: return
        self.is_connecting = True
        self.input_ip = self.input_ip.strip() # Nettoyage des espaces
        self.show_notification("Connexion en cours...", type="info")
        self.connect_status = ""
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        self.connect_status = "Connexion..."
        success = False
        
        # Stratégie de connexion "Aggressive & Robuste" (10 tentatives)
        # Rapide au début pour l'instantanéité, puis insistant pour la fiabilité
        delays = [0.1, 0.2, 0.5, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 5.0]
        
        def_port = int(self.input_port_val) if self.join_custom_port else DEFAULT_PORT
        target_ip, target_port = self.parse_address(self.input_ip, def_port)

        for i, delay in enumerate(delays):
            try:
                if i > 0:
                    self.connect_status = f"Connexion... ({i+1}/{len(delays)})"
                    time.sleep(delay)

                if self.conn:
                    try: self.conn.close()
                    except: pass
                
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                
                # Optimisations pour une connexion "Instant" et Robuste
                self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Pas de délai Nagle
                self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) # Garder la ligne active
                
                # Timeout augmenté pour l'établissement TCP (10s) pour réseaux lents
                self.conn.settimeout(10) 
                self.conn.connect((target_ip, target_port))
                
                # Une fois connecté, on laisse plus de temps pour l'échange de données (Handshake)
                # Surtout si l'avatar est lourd
                self.conn.settimeout(20) 
                
                # Envoi données
                payload = f"INTENT_GAME|{self.username}|{self.avatar}|{self.equipped['border']}|{self.equipped['name_color']}|{self.level}|{self.equipped['theme']}|{self.equipped['badge']}|{self.stats.get('win_streak', 0)}\n"
                self.conn.sendall(payload.encode())
                
                # Attente réponse handshake (robuste: peut contenir des messages suivants dans le même paquet)
                resp_buffer = b""
                while b"\n" not in resp_buffer:
                    chunk = self.conn.recv(4096)
                    if not chunk:
                        raise ConnectionError("Connexion fermée pendant le handshake")
                    resp_buffer += chunk
                    if len(resp_buffer) > 2000000:
                        raise ConnectionError("Handshake trop volumineux")

                first_line, leftover = resp_buffer.split(b"\n", 1)
                resp = first_line.decode('utf-8', errors='ignore').strip()
                
                if resp.startswith("ACCEPT"):
                    parts = resp.split("|")
                    my_id = 1 # Fallback
                    if len(parts) > 1:
                        try:
                            my_id = int(parts[1])
                        except ValueError:
                            my_id = 1
                    self.my_id = my_id
                    self.conn.settimeout(None) # Socket bloquant pour le thread de réception
                    self.connected = True
                    self.show_notification("Connecté !", type="success")
                    self.set_state("LOBBY")
                    threading.Thread(target=self.receive_data, args=(leftover,), daemon=True).start()
                    success = True
                    break
                else:
                    self.show_notification("Connexion Refusée / Plein", type="error")
                    self.conn.close()
                    break # Pas la peine de réessayer si refusé explicitement
            except Exception as e:
                # On continue silencieusement (ou log console) tant qu'il reste des essais
                print(f"Erreur connexion tentative {i+1}: {e}")
                if self.conn:
                    try: self.conn.close()
                    except: pass
                self.conn = None
                continue

        if not success:
            self.show_notification("Hôte introuvable ou hors ligne", type="error")
            self.connected = False
        
        self.is_connecting = False

    def receive_data(self, initial_buffer=b""):
        buffer = initial_buffer
        while self.connected:
            try:
                if len(buffer) > 2000000: buffer = b"" # Sécurité anti-flood (Augmenté pour avatars)
                # On lit seulement si le buffer ne contient pas déjà des commandes complètes
                if b"\n" not in buffer:
                    data = self.conn.recv(16384) # Augmenté pour supporter les images (Stabilité)
                    if not data: break
                    buffer += data
                while b"\n" in buffer:
                    msg_bytes, buffer = buffer.split(b"\n", 1)
                    try:
                        msg = msg_bytes.decode('utf-8').strip()
                        if msg == "PING":
                            self.send_data("PONG")
                            continue
                        if msg: self.network_queue.append(msg)
                    except: pass
            except Exception:
                break
        if self.connected:
            self.handle_opponent_quit()
        else:
            self.set_state("MENU_MAIN")

    def send_data(self, data):
        # Cas spécial : Lobby d'échange (Connexion P2P dans self.conn)
        if self.state == "TRADE_LOBBY":
            if self.conn:
                try:
                    self.conn.sendall((data + "\n").encode())
                except (BrokenPipeError, ConnectionResetError, OSError):
                    self.handle_opponent_quit()
            return

        if self.is_host:
            with self.clients_lock:
                clients_snapshot = list(self.clients)
            for c in clients_snapshot:
                try:
                    c['conn'].sendall((data + "\n").encode())
                except (BrokenPipeError, ConnectionResetError, OSError):
                    # Déconnexion propre si erreur d'envoi
                    self.kick_client(c['id'])
        else:
            # Client -> Host
            if self.conn:
                try:
                    self.conn.sendall((data + "\n").encode())
                except (BrokenPipeError, ConnectionResetError, OSError):
                    self.handle_opponent_quit()
    
    def send_name(self):
        # Envoie mon pseudo à l'autre
        self.send_data(f"NAME|{self.username}|{self.avatar}|{self.equipped['border']}|{self.level}|{self.equipped['name_color']}|{self.equipped['badge']}|{self.stats.get('win_streak', 0)}")

    def send_chat(self, text=None):
        if text is None: text = self.chat_input
        if text.strip():
            timestamp = datetime.datetime.now().strftime("[%H:%M]")
            # Commandes Chat
            if text.startswith("/"):
                cmd = text.split(" ")[0].lower()
                if cmd == "/roll":
                    val = random.randint(1, 100)
                    msg = f"{timestamp} SYSTEM: {self.username} a lancé {val} (1-100)"
                    self.chat_messages.append(msg)
                    if not self.is_local_game: self.send_data(f"CHAT|{msg}")
                elif cmd == "/flip":
                    res = random.choice(["PILE", "FACE"])
                    msg = f"{timestamp} SYSTEM: {self.username} a obtenu {res}"
                    self.chat_messages.append(msg)
                    if not self.is_local_game: self.send_data(f"CHAT|{msg}")
                elif cmd == "/clear":
                    self.chat_messages = []
                elif cmd == "/help":
                    self.chat_messages.append("SYSTEM: Commandes disponibles:")
                    self.chat_messages.append("/roll : Lancer un dé (1-100)")
                    self.chat_messages.append("/flip : Pile ou Face")
                    self.chat_messages.append("/clear : Effacer le chat")
                    self.chat_messages.append("/ping : Afficher la latence")
                    self.chat_messages.append("/stats : Voir mes statistiques")
                    self.chat_messages.append("/me <action> : Faire une action")
                elif cmd == "/ping":
                    p = 0
                    if not self.is_local_game and not self.is_host and self.my_id in self.lobby_cache:
                        p = self.lobby_cache[self.my_id].get('ping', 0)
                    self.chat_messages.append(f"{timestamp} SYSTEM: Latence: {p}ms")
                elif cmd == "/stats":
                    self.chat_messages.append(f"{timestamp} SYSTEM: Niv {self.level} ({self.get_player_title(self.level)}) | {self.stats['wins']} Victoires | {self.coins} $")
                elif cmd == "/me":
                    action = text[4:].strip()
                    if action:
                        msg = f"{timestamp} *{self.username} {action}*"
                        self.chat_messages.append(msg)
                        if not self.is_local_game: self.send_data(f"CHAT|{msg}")
                
                if text == self.chat_input: self.chat_input = ""
                return

            msg = f"{timestamp} {self.username}: {text}"
            self.chat_messages.append(msg)
            if not self.is_local_game:
                self.send_data(f"CHAT|{msg}")
            if text == self.chat_input: # Clear input only if it was typed
                self.chat_input = ""

    def send_action(self, action):
        # Envoie une action et l'exécute localement aussi si nécessaire
        if not self.is_local_game:
            self.send_data(f"ACTION|{action}")
        self.process_action(action)

    def request_rematch(self):
        # Action locale et réseau
        if not self.is_local_game:
            self.send_data(f"ACTION|REMATCH|{self.my_id}")
        self.process_action(f"REMATCH|{self.my_id}")

    def get_random_word(self):
        # Assurer que la catégorie existe, sinon fallback
        if not self.all_categories:
            self.all_categories = WORD_CATEGORIES.copy()
        
        if self.settings['category'] not in self.all_categories or not self.all_categories[self.settings['category']]:
            self.settings['category'] = "GÉNÉRAL"
            if "GÉNÉRAL" not in self.all_categories:
                self.all_categories = WORD_CATEGORIES.copy()
        
        words = self.all_categories.get(self.settings['category'], [])
        if not words:
            words = WORD_CATEGORIES.get("GÉNÉRAL", ["Mot"])
        
        return random.choice(words) if words else "Mot"

    def check_start_game(self):
        # Si tout le monde est prêt
        # Sécurité: vérifier que ready_status n'est pas vide et que tout le monde est prêt
        if len(self.ready_status) == self.settings['players'] and all(self.ready_status):
            if self.is_host or self.is_local_game:
                self.send_data(f"START|{self.settings['mode']}|{self.settings['time']}|{self.settings['win_score']}|{self.settings['category']}|{self.settings['game_type']}|{self.settings['players']}")
                if self.is_host: self.send_name() # Envoyer mon nom aux clients
                self.start_round()

    def start_round(self, new_word=True, specific_word=None):
        # Seul l'hôte ou le jeu local décide du mot
        if self.is_host or self.is_local_game:
            if new_word:
                self.current_word = self.get_random_word() if specific_word is None else specific_word
            
            if self.settings.get('game_type') == 'TIME_TRIAL':
                if self.round_num == 1 and self.turn_count == 0:
                    self.global_timer_start = pygame.time.get_ticks()
            
            round_time = self.settings['time']
            if self.settings.get('game_type') == 'SURVIVAL':
                round_time = max(2.0, self.settings['time'] - (self.turn_count * 1.0)) # Réduction par mot dit
            elif self.settings.get('game_type') == 'SPEED':
                round_time = 3.0 # Temps fixe très court
            elif self.settings.get('game_type') == 'HARDCORE':
                round_time = 4.0 # Temps fixe court
            elif self.settings.get('game_type') == 'CHAOS':
                round_time = random.uniform(2.0, 8.0) # Temps aléatoire imprévisible
            elif self.settings.get('game_type') == 'TIME_TRIAL':
                round_time = 10.0 # Temps de réflexion par tour, mais le global prime

            if not self.is_local_game:
                self.send_data(f"NEW_ROUND|{self.current_word}|{round_time}|{self.settings['win_score']}|{self.round_num}")
            self.reset_round_state(round_time)

    def reset_round_state(self, time_val=None):
        self.user_text = ""
        self.opponent_text = ""
        self.start_ticks = pygame.time.get_ticks()
        if time_val is None: time_val = self.settings['time']
        self.round_duration = float(time_val)
        self.time_left = self.round_duration # Initialiser le temps pour éviter le timeout immédiat
        self.state = "GAME"
        self.freeze_until = 0
        self.update_game_buttons()
        self.rematch_ready = [False] * self.settings['players']
        self.particles = []
        self.judge_id = -1
        self.game_emotes = [] # Reset emotes
        self.ready_status = [False] * self.settings['players'] # Reset ready correct pour N joueurs

    def update_game_buttons(self):
        self.buttons = [
            Button("QUITTER", 50, 35, 120, 40, ALERT_COLOR, (255, 100, 100), self.quit_game)
        ]
        if self.state == "GAME" and self.current_freezes > 0:
             self.buttons.append(Button(f"❄️ {self.current_freezes}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 100, 100, 60, (100, 200, 255), HOVER_COLOR, self.use_freeze, font=self.ui_emoji_font, text_color=(255, 255, 255)))

    def use_freeze(self):
        if self.current_freezes > 0 and pygame.time.get_ticks() > self.freeze_until:
            self.current_freezes -= 1
            self.send_action("FREEZE")
            self.update_game_buttons()

    def draw_text(self, text, font, color, x, y, center=True):
        if text is None: return # Sécurité anti-crash
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_text_fit(self, text, font, color, x, y, max_width, center=True):
        if text is None: return
        surface = font.render(text, True, color)
        w = surface.get_width()
        if w > max_width:
            scale = max_width / w
            new_h = int(surface.get_height() * scale)
            surface = pygame.transform.smoothscale(surface, (int(max_width), new_h))
        
        rect = surface.get_rect()
        if center: rect.center = (x, y)
        else: rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def wrap_text_lines(self, text, font, max_width):
        if not text:
            return [""]
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw_text_glitch(self, text, font, color, x, y, center=True):
        # Effet Glitch (Décalage RGB aléatoire)
        off_r = (random.randint(-4, 4), random.randint(-4, 4))
        off_c = (random.randint(-4, 4), random.randint(-4, 4))
        self.draw_text(text, font, (255, 50, 50), x + off_r[0], y + off_r[1], center) # Rouge
        self.draw_text(text, font, (50, 255, 255), x + off_c[0], y + off_c[1], center) # Cyan
        self.draw_text(text, font, color, x, y, center) # Blanc

    def draw_text_shadow(self, text, font, color, x, y, center=True):
        # Ombre
        surface_s = font.render(text, True, (0, 0, 0))
        rect_s = surface_s.get_rect()
        if center: rect_s.center = (x+2, y+2)
        else: rect_s.topleft = (x+2, y+2)
        self.screen.blit(surface_s, rect_s)
        # Texte
        self.draw_text(text, font, color, x, y, center)

    def draw_text_with_emoji(self, text, base_font, emoji_font, color, x, y, center=True):
        # Emojis désactivés: rendu simple
        self.draw_text(text, base_font, color, x, y, center)

    def process_action(self, action):
        # Gestion des arguments dans l'action (ex: REMATCH|0)
        try:
            args = action.split("|")
            action_type = args[0]

            if action_type == "RESTART":
                if self.is_host or self.is_local_game: self.start_round()
            
            elif action_type == "POINT":
                if self.state == "GAME_OVER": return # Empêche le score de dépasser la limite une fois fini
                # Récupérer la raison (TIMEOUT ou NORMAL)
                reason = args[1] if len(args) > 1 else "NORMAL"
                
                loser_id = self.current_player
                if len(args) > 2:
                    try: loser_id = int(args[2])
                    except: pass

                self.last_round_reason = reason
                self.used_words = [] # SUPPRIMER LES MOTS DE LA MANCHE D'AVANT (Reset pour la nouvelle manche)
                
                # Animation de tremblement (Shake) quand un point est marqué (donc perdu par qqn)
                self.shake_timer = 20
                self.play_sound("buzz")
                
                # Le joueur 'loser_id' a perdu le point
                winner_idx = (loser_id + 1) % self.settings['players']
                
                # Sécurité Index
                if 0 <= winner_idx < len(self.score):
                    if self.score[winner_idx] < self.settings['win_score']:
                        self.score[winner_idx] += 1
                self.round_num += 1
                self.turn_count = 0 # Reset du compteur de survie pour la nouvelle manche
                self.rally_combo = 0 # Reset du combo
                self.last_round_winner = winner_idx
                self.add_particles(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, ACCENT_COLOR)
                
                # Effet spécial Hardcore
                if self.settings.get('game_type') == 'HARDCORE':
                    self.generate_hardcore_win_particles()
                
                # Vérification victoire
                if 0 <= winner_idx < len(self.score) and self.score[winner_idx] >= self.settings['win_score']:
                    self.winner_text = f"Joueur {winner_idx + 1}" if self.is_local_game else (self.username if winner_idx == self.my_id else self.opponent_name)
                    
                    # Gain XP fin de partie
                    if self.is_local_game:
                        if self.daily_challenge_active and winner_idx == self.my_id:
                            self.coins += 300
                            self.add_coins(300)
                            self.last_daily_challenge_date = str(datetime.date.today())
                            self.show_notification("DÉFI DU JOUR RÉUSSI !", "success")
                            self.daily_challenge_active = False
                        self.stats["wins"] += 1
                        self.stats['wins_per_mode'][self.settings.get('game_type')] = self.stats['wins_per_mode'].get(self.settings.get('game_type'), 0) + 1
                        self.coins += 50
                        self.spawn_coin_fly(50, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
                        # Historique Local
                        if "history" in self.stats: self.stats["history"].insert(0, {
                            "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
                            "opponent": "Local",
                            "score": f"{self.score[0]}-{self.score[1]}",
                            "winner": self.winner_text,
                            "result": "WIN"
                        })
                        self.prepare_xp_animation(50)
                        # Border XP
                        bid = self.equipped['border']
                        if bid != "border_default":
                             self.stats['border_xp'][bid] = self.stats['border_xp'].get(bid, 0) + 10
                    else:
                        if winner_idx == self.my_id:
                            self.stats["wins"] += 1
                            game_type = self.settings.get('game_type')
                            if winner_idx != self.my_id and self.score[self.my_id] == 0:
                                self.stats['perfect_lose'] = True
                            self.stats['wins_per_mode'][game_type] = self.stats['wins_per_mode'].get(game_type, 0) + 1
                            self.prepare_xp_animation(50)
                            self.coins += 50 # Victoire
                            self.spawn_coin_fly(50, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
                            # Border XP
                            bid = self.equipped['border']
                            if bid != "border_default":
                                 self.stats['border_xp'][bid] = self.stats['border_xp'].get(bid, 0) + 50
                        else:
                            # Reset Win Streak
                            self.stats['win_streak'] = 0
                            
                            self.prepare_xp_animation(0)
                            # self.coins += 0 # Défaite (Rien)
                            # Border XP (Lose)
                            bid = self.equipped['border']
                            if bid != "border_default":
                                 self.stats['border_xp'][bid] = self.stats['border_xp'].get(bid, 0) + 10
                        
                        # Historique En Ligne
                        res_str = "VICTOIRE" if winner_idx == self.my_id else "DÉFAITE"
                        my_score = self.score[self.my_id] if self.my_id < len(self.score) else 0
                        opp_score = self.score[1 if self.my_id == 0 else 0] if len(self.score) > 1 else 0
                        if "history" in self.stats: self.stats["history"].insert(0, {
                            "date": datetime.datetime.now().strftime("%d/%m %H:%M"),
                            "opponent": self.opponent_name,
                            "score": f"{my_score}-{opp_score}",
                            "winner": self.winner_text,
                            "result": res_str
                        })

                    if "history" in self.stats and len(self.stats["history"]) > 20: self.stats["history"].pop()
                    self.stats["games"] += 1
                    self.check_achievements()
                    self.save_settings()
                    self.set_state("GAME_OVER")
                else:
                    self.current_player = winner_idx
                    # Lancer le compte à rebours avant la prochaine manche
                    self.state = "ROUND_COUNTDOWN"
                    self.countdown_start = pygame.time.get_ticks()
                    
                    # Chance de lancer le mini-jeu bonus (20%)
                    if (self.is_host or self.is_local_game) and random.random() < 0.20:
                        self.send_action("BONUS_START")

                    # Réinitialiser les boutons pour éviter de cliquer pendant le compte à rebours
                    self.buttons = []
            
            elif action_type == "CONTINUE":
                self.reset_round_state(self.time_left) # Keep current time
            
            elif action_type == "NEXT_TURN":
                # Récupérer le mot tapé s'il y en a un (Mode écrit)
                next_word = args[1] if len(args) > 1 else None
                
                # Historique
                if next_word:
                    self.used_words.append(next_word.lower().strip())
                    self.save_history()
                
                # --- SYSTÈME DE COMBO ---
                elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                if elapsed < 2.5: # Réponse en moins de 2.5s
                    self.rally_combo += 1
                    if self.rally_combo > 1:
                        self.feedback_msg = f"COMBO x{self.rally_combo} !"
                        self.feedback_timer = pygame.time.get_ticks()
                        self.play_sound("coin")
                        
                        # Bonus pour le joueur actuel (si c'est moi)
                        if self.current_player == self.my_id:
                            bonus = self.rally_combo * 5
                            self.coins += bonus
                            self.add_coins(bonus)
                            # self.show_notification(f"Combo x{self.rally_combo} (+{bonus}$)", type="success") # Remplacé par texte flottant
                        
                        # Texte flottant Combo
                        self.floating_texts.append({
                            'x': SCREEN_WIDTH // 2, 'y': SCREEN_HEIGHT // 2 - 100,
                            'text': f"COMBO x{self.rally_combo} !", 'color': (255, 200, 0),
                            'life': 60, 'speed': 2
                        })
                    
                    # Mise à jour Stats & Succès
                    if self.rally_combo > self.stats.get("max_combo", 0):
                        self.stats["max_combo"] = self.rally_combo
                        self.save_settings()
                    if self.rally_combo >= 10:
                        self.unlock_achievement("SPEEDSTER")
                else:
                    self.rally_combo = 0
                
                self.current_player = (self.current_player + 1) % self.settings['players']
                self.turn_count += 1 # Incrémenter pour le mode Survie
                
                if self.is_host or self.is_local_game:
                    # En mode écrit, le nouveau mot est celui qui vient d'être validé
                    # En mode vocal, on garde le même mot affiché (ou on ne change rien) pour ne pas perturber la chaîne
                    should_change = (self.settings['mode'] == 'WRITTEN')
                    self.start_round(new_word=should_change, specific_word=next_word)
            
            elif action_type == "BUZZ":
                if not self.stats.get("wizz_used", False):
                    self.stats["wizz_used"] = True
                    self.unlock_achievement("SECRET_WIZZ")
                self.shake_timer = 20
                self.play_sound("buzz")
                # Animation Spéciale Wizz (Explosion)
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                for _ in range(80):
                    angle = random.uniform(0, 6.28)
                    speed = random.uniform(5, 30)
                    self.particles.append({
                        'x': cx, 'y': cy,
                        'vx': math.cos(angle) * speed,
                        'vy': math.sin(angle) * speed,
                        'life': random.randint(150, 255),
                        'color': (255, random.randint(200, 255), 0),
                        'size': random.randint(5, 15)
                    })
            
            elif action_type == "EMOTE":
                # ACTION|EMOTE|😂|player_id
                emoji = args[1]
                pid = int(args[2]) if len(args) > 2 else 0
                # Position de départ selon le joueur (Gauche ou Droite)
                start_x = 100 if pid == 0 else SCREEN_WIDTH - 100
                start_y = SCREEN_HEIGHT - 150
                self.game_emotes.append({'emoji': emoji, 'x': start_x, 'y': start_y, 'life': 100, 'speed': 3})
                self.play_sound("chat")
            
            elif action_type == "GG_EFFECT":
                self.play_sound("success")
                self.generate_hardcore_win_particles() # Reuse confetti
                self.show_notification("L'adversaire dit GG !", "success")

            elif action_type == "JUDGE":
                self.judge_id = int(args[1]) if len(args) > 1 else -1
                self.set_state("JUDGMENT")
            
            elif action_type == "REMATCH":
                if len(args) > 1:
                    player_id = int(args[1])
                    if 0 <= player_id < len(self.rematch_ready):
                        self.rematch_ready[player_id] = True
                
                # Si tout le monde est prêt
                if all(self.rematch_ready):
                    self.score = [0] * self.settings['players']
                    self.last_round_reason = ""
                    self.round_num = 1
                    self.turn_count = 0
                    self.rally_combo = 0
                    self.current_freezes = 1 + self.inventory.count("upgrade_freeze")
                    self.reset_history()
                    self.ready_status = [False] * self.settings['players'] # Reset ready
                    if self.is_host or self.is_local_game:
                        self.start_round()
            
            elif action_type == "BONUS_START":
                self.state = "BONUS_GAME"
                self.bonus_end_time = pygame.time.get_ticks() + 5000 # 5 secondes
                self.bonus_targets = []
                self.spawn_bonus_target()
                self.play_sound("start")

            elif action_type == "TRADE_UPDATE":
                if len(args) > 3:
                    self.trade_lobby_data["them"]["coins"] = int(args[1])
                    self.trade_lobby_data["them"]["items"] = args[2].split(',') if args[2] else []
                    self.trade_lobby_data["them"]["locked"] = (args[3] == "1")
                    self.refresh_trade_countdown()
            
            elif action_type == "TRADE_CONFIRM":
                # Echange validé
                my_offer = self.trade_lobby_data["me"]["coins"]
                their_offer = self.trade_lobby_data["them"]["coins"]
                self.coins += (their_offer - my_offer)
                if self.coins < 0:
                    self.coins = 0
                self.spawn_trade_coin_transfer(my_offer, their_offer)
                if their_offer > 0:
                    self.display_coins = self.coins - their_offer
                    self.temp_coin_display_timer = pygame.time.get_ticks() + 1800
                self.check_achievements()
                self.save_settings()
                self.show_notification("Echange réussi !", type="success")
                self.trade_finalize_at = pygame.time.get_ticks() + 1800
            
            elif action_type == "FREEZE":
                self.freeze_until = pygame.time.get_ticks() + 5000
                self.play_sound("start")
                # Particules de glace
                for _ in range(50):
                    self.particles.append({
                        'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(0, SCREEN_HEIGHT),
                        'vx': 0, 'vy': random.uniform(1, 3), 'life': 200, 'color': (200, 240, 255), 'size': random.randint(2, 5)
                    })
                self.show_notification("TEMPS GELÉ (5s) !", type="info")
        except Exception as e:
            print(f"Erreur action: {e}")

    def spawn_bonus_target(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        self.bonus_targets.append(pygame.Rect(x, y, 70, 70))

    def draw_achievement_popup(self):
        if not self.current_achievement and self.achievement_queue:
            self.current_achievement = {
                "data": self.achievement_queue.pop(0),
                "start_time": pygame.time.get_ticks(),
                "y": SCREEN_HEIGHT + 100
            }
        
        if self.current_achievement:
            ach = self.current_achievement
            now = pygame.time.get_ticks()
            elapsed = now - ach["start_time"]
            
            target_y = SCREEN_HEIGHT - 100
            
            if elapsed < 500:
                t = elapsed / 500
                ach["y"] = (SCREEN_HEIGHT + 100) - ((SCREEN_HEIGHT + 100) - target_y) * (1 - (1-t)**3)
            elif elapsed < 4500:
                ach["y"] = target_y
            elif elapsed < 5000:
                t = (elapsed - 4500) / 500
                ach["y"] = target_y + ((SCREEN_HEIGHT + 100) - target_y) * (t**3)
            else:
                self.current_achievement = None
                return

            rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, ach["y"], 400, 80)
            
            s = pygame.Surface((400, 80), pygame.SRCALPHA)
            pygame.draw.rect(s, (30, 35, 45, 240), (0, 0, 400, 80), border_radius=10)
            pygame.draw.rect(s, (50, 55, 65), (0, 0, 400, 80), 2, border_radius=10)
            
            # Icone Trophée
            trophy_surf = self.ui_emoji_font.render("🏆", True, (255, 215, 0))
            trophy_rect = trophy_surf.get_rect(center=(50, 40))
            s.blit(trophy_surf, trophy_rect)
            
            self.screen.blit(s, rect)
            self.draw_text("SUCCÈS DÉBLOQUÉ", self.small_bold_font, (255, 215, 0), rect.centerx + 20, rect.top + 20)
            self.draw_text(ach["data"]["name"], self.font, (255, 255, 255), rect.centerx + 20, rect.top + 50)

    def get_border_level(self, border_id):
        # Niveau 1: 0 XP
        # Niveau 2: 100 XP
        # Niveau 3: 500 XP
        if border_id == "border_default": return 1
        xp = self.stats.get('border_xp', {}).get(border_id, 0)
        if xp >= 500: return 3
        if xp >= 100: return 2
        return 1

    def draw_avatar(self, avatar, x, y, size=30, border_id=None, is_combo=False):
        # Effet de feu si Combo (Visual Feedback)
        if is_combo:
            for _ in range(2):
                angle = random.uniform(0, 6.28)
                dist = random.randint(size, size + 10)
                fx = x + math.cos(angle) * dist
                fy = y + math.sin(angle) * dist
                self.particles.append({
                    'x': fx, 'y': fy,
                    'vx': 0, 'vy': -2,
                    'life': random.randint(20, 50),
                    'color': (255, random.randint(100, 200), 0),
                    'size': random.randint(3, 8)
                })

        # Cercle de fond
        pygame.draw.circle(self.screen, (40, 45, 60), (x, y), size)
        
        # Bordure équipée
        if border_id is None:
            border_id = self.equipped['border']
            
        border_col = ACCENT_COLOR
        level = self.get_border_level(border_id)
        now = pygame.time.get_ticks()

        if border_id == "border_rainbow":
             hue = (now // 5) % 360
             c = pygame.Color(0)
             c.hsla = (hue, 100, 50, 100)
             border_col = (c.r, c.g, c.b)
        elif border_id == "border_fire":
            pulse = (math.sin(now * 0.005) + 1) / 2
            border_col = self.interpolate_color((255, 100, 0), (255, 0, 0), pulse)
        elif border_id == "border_electric":
            if (now // 100) % 2 == 0:
                border_col = (150, 150, 255)
            else:
                border_col = (255, 255, 255)
        elif border_id == "border_glitch":
            # Dessine plusieurs cercles décalés pour un effet de glitch
            for _ in range(3):
                off_x = random.randint(-4, 4)
                off_y = random.randint(-4, 4)
                glitch_col = random.choice([(255, 0, 255, 100), (0, 255, 255, 100), (255, 255, 0, 100)])
                s = pygame.Surface((size*2 + 8, size*2 + 8), pygame.SRCALPHA)
                pygame.draw.circle(s, glitch_col, (s.get_width()//2, s.get_height()//2), size, 3)
                self.screen.blit(s, (x - size - 4 + off_x, y - size - 4 + off_y))
            border_col = (200, 200, 200) # Cercle de base
        elif border_id == "border_double":
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size + 4, 1)
            border_col = (200, 200, 200)
        elif border_id == "border_plasma":
            hue = (now // 2) % 360
            c = pygame.Color(0)
            c.hsla = (hue, 100, 50, 100)
            border_col = (c.r, c.g, c.b)
            # Extra rings
            pygame.draw.circle(self.screen, (border_col[0]//2, border_col[1]//2, border_col[2]//2), (x, y), size + 4, 1)
            pygame.draw.circle(self.screen, border_col, (x, y), size - 2, 1)
        elif border_id == "border_pulse":
            pulse = (math.sin(now * 0.01) + 1) / 2
            width = 2 + int(pulse * 4)
            border_col = SHOP_CATALOG[border_id]['color']
            pygame.draw.circle(self.screen, border_col, (x, y), size, width)
            self._draw_avatar_content(avatar, x, y, size)
            return
        elif border_id == "custom_border_color":
            border_col = self.custom_colors.get('border', (255, 255, 255))
        elif border_id in SHOP_CATALOG:
            border_col = SHOP_CATALOG[border_id]['color']
        
        pygame.draw.circle(self.screen, border_col, (x, y), size, 3)
        # Visuals based on level
        width = 3 + (level - 1) * 2
        
        # Level 3 Glow
        if level >= 3:
             s = pygame.Surface((size*2+20, size*2+20), pygame.SRCALPHA)
             pygame.draw.circle(s, (*border_col, 60), (size+10, size+10), size+8)
             self.screen.blit(s, (x - size - 10, y - size - 10))

        pygame.draw.circle(self.screen, border_col, (x, y), size, width)
        if level >= 2:
             pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size - width, 1)
        
        self._draw_avatar_content(avatar, x, y, size)

    def draw_badge(self, badge_id, x, y):
        if badge_id and badge_id != "badge_default" and badge_id in SHOP_CATALOG:
            icon = SHOP_CATALOG[badge_id].get('icon', '')
            if icon:
                badge_surf = self.ui_emoji_font.render(icon, True, (255, 255, 255))
                badge_rect = badge_surf.get_rect(center=(x, y))
                self.screen.blit(badge_surf, badge_rect)
                return badge_rect
        return None

    def _draw_avatar_content(self, avatar, x, y, size):
        # Gestion Avatar (Image ou Emoji)
        if avatar.startswith("IMG:"):
            # Clé de cache incluant la taille pour gérer les différents affichages
            cache_key = (avatar, size)
            
            # Gestion du cache pour éviter de décoder à chaque frame
            if cache_key not in self.avatar_cache:
                try:
                    img_data = base64.b64decode(avatar[4:])
                    original = pygame.image.load(io.BytesIO(img_data)).convert_alpha()
                    
                    # Création du masque circulaire pour ne pas déborder
                    diameter = size * 2
                    # On redimensionne l'image pour qu'elle couvre le cercle
                    scaled = pygame.transform.smoothscale(original, (diameter, diameter))
                    
                    # Masque : On crée une surface transparente avec un cercle blanc, et on applique BLEND_RGBA_MIN
                    mask = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                    pygame.draw.circle(mask, (255, 255, 255), (size, size), size - 3)
                    scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                    
                    self.avatar_cache[cache_key] = scaled
                except:
                    self.avatar_cache[cache_key] = None
            
            surf = self.avatar_cache.get(cache_key)
            if surf:
                rect = surf.get_rect(center=(x, y))
                self.screen.blit(surf, rect)
            else:
                # Fallback si erreur
                font = self.emoji_font if size > 40 else self.ui_emoji_font
                txt = font.render("⚡", True, (255, 255, 255))
                rect = txt.get_rect(center=(x, y))
                self.screen.blit(txt, rect)
        else:
            # Emoji Classique
            font = self.emoji_font if size > 40 else self.ui_emoji_font
            try:
                txt = font.render(avatar, True, (255, 255, 255))
            except:
                txt = self.big_font.render(avatar, True, (255, 255, 255))
            rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, rect)

    def get_cached_sun(self, radius):
        # Génère ou récupère le soleil mis en cache (Optimisation Fluidité)
        if self.cached_sun_surf is None:
            base_radius = 200 # Taille de base haute qualité
            surf = pygame.Surface((base_radius*2, base_radius*2), pygame.SRCALPHA)
            sun_top = (255, 220, 0)
            sun_bot = (255, 0, 128)
            # Dessin du dégradé
            for i in range(base_radius*2):
                ratio = i / (base_radius*2)
                col = self.interpolate_color(sun_top, sun_bot, ratio)
                dy = i - base_radius
                if abs(dy) < base_radius:
                    dx = math.sqrt(base_radius**2 - dy**2)
                    pygame.draw.line(surf, col, (base_radius - dx, i), (base_radius + dx, i))
            # Bandes "Stores"
            for i in range(base_radius + 10, base_radius*2, 14):
                h = max(2, int((i - base_radius) / 6))
                pygame.draw.rect(surf, BG_COLOR, (0, i, base_radius*2, h))
            self.cached_sun_surf = surf
        
        # Redimensionnement à la taille demandée (Pulsation)
        return pygame.transform.smoothscale(self.cached_sun_surf, (radius*2, radius*2))

    def draw_background(self):
        # Thème équipé
        bg_col = BG_COLOR
        # Couleur dynamique selon la catégorie (si en jeu et thème par défaut)
        if self.state in ["GAME", "ROUND_COUNTDOWN", "JUDGMENT", "GAME_OVER"] and self.equipped['theme'] == "theme_default":
            cat = self.settings['category']
            if cat in CATEGORY_COLORS:
                bg_col = CATEGORY_COLORS[cat]
            else:
                # Fallback généré pour les catégories custom ou inconnues
                h = hash(cat)
                bg_col = (abs(h) % 60, abs(h >> 8) % 60, abs(h >> 16) % 60)

        elif self.equipped['theme'] in SHOP_CATALOG:
            bg_col = SHOP_CATALOG[self.equipped['theme']]['color']
            
        # Urgence Time Trial (10 dernières secondes)
        if self.state == "GAME" and self.settings.get('game_type') == 'TIME_TRIAL' and self.global_timer_start > 0:
            rem_global = max(0, 60 - (pygame.time.get_ticks() - self.global_timer_start) / 1000)
            if rem_global <= 10:
                ratio = (10 - rem_global) / 10.0
                target_col = (80, 0, 0) # Rouge sombre
                bg_col = self.interpolate_color(bg_col, target_col, ratio * 0.8)

        self.screen.fill(bg_col)

        # --- THÈMES ANIMÉS ---
        if self.equipped['theme'] in ["theme_matrix", "theme_hacker"]:
            self.update_draw_matrix_rain()
        elif self.equipped['theme'] == "theme_space":
            self.update_draw_starfield()
        elif self.equipped['theme'] == "theme_retro":
            self.draw_scanlines()

        # Formes flottantes (Amélioration graphique)
        self.update_draw_floating_shapes()

        # Grille mouvante (Effet moderne amélioré)
        t = pygame.time.get_ticks()
        grid_color = (30, 40, 55)
        
        # Perspective Grid (Pseudo-3D floor)
        if self.state == "MENU_MAIN":
            horizon = int(SCREEN_HEIGHT * 0.55)
            cx = SCREEN_WIDTH // 2
            
            # --- SOLEIL CYBERPUNK ---
            # Pulsation rythmique
            pulse = math.sin(t * 0.003) * 0.05 + 1.0
            sun_radius = int(160 * pulse)
            
            # Récupération du soleil optimisé
            sun_surf = self.get_cached_sun(sun_radius)
            
            # Glow (Lueur arrière)
            glow_radius = int(sun_radius * 1.4)
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 50, 100, 40), (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surf, (cx - glow_radius, horizon - sun_radius - 20 - (glow_radius - sun_radius)))

            # Affichage (Posé sur l'horizon)
            self.screen.blit(sun_surf, (cx - sun_radius, horizon - sun_radius - 20))
            # Masque sol (pour couper le bas du soleil proprement)
            pygame.draw.rect(self.screen, BG_COLOR, (0, horizon, SCREEN_WIDTH, SCREEN_HEIGHT - horizon))

            # Lignes Verticales (Fuite)
            for i in range(-20, 21):
                x_top = cx + i * 15
                x_bot = cx + i * 400
                col_v = (25, 30, 40) # Très sombre
                pygame.draw.line(self.screen, col_v, (x_top, horizon), (x_bot, SCREEN_HEIGHT), 2)

            # Lignes Horizontales (Mouvement fluide avec Fade)
            phase = (t * 0.0005) % 1.0
            for i in range(20):
                z = (i + 1) - phase
                if z <= 0.1: continue
                
                projection_scale = 250 
                y = horizon + (projection_scale / z)
                
                if y >= SCREEN_HEIGHT: continue
                
                # Fade in/out selon la distance (z)
                intensity = 1.0 / (z * 0.6)
                intensity = min(1.0, max(0.0, intensity))
                col = self.interpolate_color(BG_COLOR, (0, 200, 255), intensity)
                
                pygame.draw.line(self.screen, col, (0, int(y)), (SCREEN_WIDTH, int(y)), 1 if z > 2 else 2)

            # Brouillard Horizon (Cache la coupure nette)
            if not hasattr(self, 'horizon_fog') or self.horizon_fog.get_width() != SCREEN_WIDTH:
                self.horizon_fog = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
                for y in range(150):
                    alpha = int(255 * (1 - (y / 150)**2)) # Fade quadratique
                    pygame.draw.line(self.horizon_fog, (*BG_COLOR, alpha), (0, y), (SCREEN_WIDTH, y))
            
            self.screen.blit(self.horizon_fog, (0, horizon))
        else:
            # Standard moving grid
            offset = (t // 50) % 50
            for x in range(0, SCREEN_WIDTH, 50): pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
            for y in range(-50, SCREEN_HEIGHT, 50): pygame.draw.line(self.screen, grid_color, (0, y + offset), (SCREEN_WIDTH, y + offset))
            
        # Particules Menu
        if self.state.startswith("MENU") or self.state == "INPUT_NAME":
            self.update_draw_menu_particles()
            
        if self.state == "MENU_MAIN":
            self.draw_news_ticker()
        
        # Vignette v0.2 (Assombrir les coins)
        self.screen.blit(self.vignette_surf, (0, 0))

    def draw_panel(self, x, y, w, h):
        # Caching pour fluidité (Optimisation majeure)
        key = (w, h)
        if key not in self.panel_cache:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((*PANEL_COLOR, 240)) # Couleur sombre avec transparence
            # Glow effect
            pygame.draw.rect(s, (*ACCENT_COLOR, 20), s.get_rect(), border_radius=15)
            # Bordure fine
            pygame.draw.rect(s, (60, 70, 90), s.get_rect(), 1, border_radius=15)
            # Accent border bottom
            pygame.draw.line(s, ACCENT_COLOR, (20, h), (w - 20, h), 2)
            self.panel_cache[key] = s
        
        self.screen.blit(self.panel_cache[key], (x, y))

    def draw_fancy_input_box(self, rect, text, placeholder="", active=False, font=None, center_text=True, text_color=TEXT_COLOR):
        _font = font if font else self.font
        
        # Background with subtle gradient
        bg_start = (30, 35, 45)
        bg_end = (20, 25, 35)
        gradient_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        for i in range(rect.height):
            ratio = i / rect.height
            color = self.interpolate_color(bg_start, bg_end, ratio)
            pygame.draw.line(gradient_surf, color, (0, i), (rect.width, i))

        # Clip to rounded rect
        mask = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=15)
        gradient_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.screen.blit(gradient_surf, rect.topleft)

        # Border
        border_col = ACCENT_COLOR if active else (60, 65, 80)
        pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=15)

        # Inner glow if active
        if active:
            glow_rect = rect.inflate(-4, -4)
            glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*ACCENT_COLOR, 20), glow_surf.get_rect(), border_radius=12)
            self.screen.blit(glow_surf, glow_rect.topleft)

        # Text logic
        display_text = text
        current_text_color = text_color
        if not text and placeholder:
            display_text = placeholder
            current_text_color = (100, 100, 120)

        if active and (pygame.time.get_ticks() // 500) % 2 == 0: display_text += "|"

        font_h = _font.get_height()
        text_y = rect.y + (rect.h - font_h) // 2 - 2
        if center_text:
            self.draw_text_fit(display_text, _font, current_text_color, rect.centerx, text_y + font_h // 2, rect.width - 20)
        else:
            self.draw_text_fit(display_text, _font, current_text_color, rect.x + 15, text_y, rect.width - 30, center=False)

    def run(self):
        running = True
        while running:
          try:
            self.draw_background()
            self.current_frame_card_offsets = {}
            
            # Gestion des événements globaux
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                if event.type == pygame.VIDEORESIZE:
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    self.create_vignette()
                    self.create_menu_buttons()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Effet Ripple / Particules au clic
                    for _ in range(5):
                        # Easter Egg: Titre Interactif (Menu Principal)
                        if self.state == "MENU_MAIN" and 100 < event.pos[1] < 200:
                             self.add_particles(event.pos[0], event.pos[1], random.choice([(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 215, 0)]))
                             if random.random() < 0.3: self.play_sound("coin")

                        self.particles.append({
                            'x': event.pos[0], 'y': event.pos[1],
                            'vx': random.uniform(-3, 3), 'vy': random.uniform(-3, 3),
                            'life': random.randint(10, 30), 'color': (200, 255, 255), 'size': random.randint(2, 5)
                        })

                    # Clics Menu Principal (UPnP)
                    if self.state == "MENU_MAIN":
                        # Rafraîchir IP
                        if self.refresh_btn_rect and self.refresh_btn_rect.collidepoint(event.pos):
                            self.upnp_status = "Rafraîchissement..."
                            self.public_ip = None
                            threading.Thread(target=self.get_public_ip, daemon=True).start()
                            threading.Thread(target=self.try_upnp, daemon=True).start()
                            self.play_sound("click")
                        
                        # Copier IP (Clic sur le point)
                        elif math.hypot(event.pos[0] - 30, event.pos[1] - 130) < 15:
                            if "SUCCÈS" in self.upnp_status:
                                self.copy_ip()
                                self.show_notification("IP Copiée !", "success")

                if event.type == pygame.MOUSEWHEEL:
                    if self.state == "LOBBY":
                        self.chat_scroll += event.y
                        if self.chat_scroll < 0: self.chat_scroll = 0
                    elif self.state == "INPUT_NAME":
                        self.avatar_scroll -= event.y * 50 # Scroll plus rapide
                        self.create_menu_buttons() # Recalculer positions
                    elif self.state == "MENU_SHOP":
                        # Refonte du défilement magasin
                        self.shop_scroll -= event.y * 40
                        if self.shop_scroll < 0: self.shop_scroll = 0
                        
                        # Calcul Max Scroll dynamique (hauteur de carte mise à jour)
                        card_h = 320
                        gap = 30
                        available_w = SCREEN_WIDTH - 100
                        cols = max(1, available_w // (260 + 30))
                        all_items = self.get_sorted_shop_items()
                        if self.shop_tab == "BORDER": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'border']
                        elif self.shop_tab == "THEME": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'theme']
                        elif self.shop_tab == "TITLE": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'title_style']
                        elif self.shop_tab == "CATEGORY": all_items = [k for k in all_items if SHOP_CATALOG[k]['type'] == 'category']
                        count = len(all_items)
                        
                        rows = math.ceil(count / cols)
                        total_h = rows * (card_h + gap)
                        visible_h = SCREEN_HEIGHT - 220
                        max_scroll = max(0, total_h - visible_h + 100)
                        
                        if self.shop_scroll > max_scroll: self.shop_scroll = max_scroll
                        self.create_menu_buttons() # Recalculer positions
                    elif self.state == "MENU_INVENTORY":
                        self.inventory_scroll -= event.y * 40
                        if self.inventory_scroll < 0: self.inventory_scroll = 0
                        
                        # Calcul Max Scroll
                        card_h = 320
                        gap = 30
                        available_w = SCREEN_WIDTH - 100
                        cols = max(1, available_w // (260 + 30))
                        
                        owned_items = [item_id for item_id in self.inventory if item_id in SHOP_CATALOG]
                        filtered_items = []
                        for item_id in owned_items:
                            item = SHOP_CATALOG[item_id]
                            if self.inventory_tab == "ALL": filtered_items.append(item_id)
                            elif self.inventory_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                            elif self.inventory_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                            elif self.inventory_tab == "TITLE" and item['type'] == 'title_style': filtered_items.append(item_id)
                            elif self.inventory_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                            elif self.inventory_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)
                        
                        count = len(filtered_items)
                        rows = math.ceil(count / cols)
                        total_h = rows * (card_h + gap)
                        visible_h = SCREEN_HEIGHT - 220
                        max_scroll = max(0, total_h - visible_h + 100)
                        
                        if self.inventory_scroll > max_scroll: self.inventory_scroll = max_scroll
                    elif self.state == "MENU_ACHIEVEMENTS":
                        self.achievements_scroll -= event.y * 30
                        if self.achievements_scroll < 0: self.achievements_scroll = 0
                        max_scroll = max(0, math.ceil(len(ACHIEVEMENTS) / 2) * 120 - 700)
                        if self.achievements_scroll > max_scroll: self.achievements_scroll = max_scroll
                    elif self.state == "MENU_CUSTOM_CATS":
                        self.custom_cats_scroll -= event.y * 40
                        if self.custom_cats_scroll < 0: self.custom_cats_scroll = 0
                        self.create_menu_buttons()
                    elif self.state == "MENU_BATTLEPASS":
                        self.season_scroll -= event.y * 40
                        if self.season_scroll < 0: self.season_scroll = 0
                        self.create_menu_buttons()

                # --- KONAMI CODE ---
                if event.type == pygame.KEYDOWN:
                    if self.konami_index < len(self.konami_code):
                        if event.key == self.konami_code[self.konami_index]:
                            self.konami_index += 1
                            if self.konami_index == len(self.konami_code):
                                self.coins += 5000
                                self.save_settings()
                                self.play_sound("success")
                                self.show_notification("KONAMI CODE ! (+5000$)", "success")
                                self.unlock_achievement("SECRET_DEV_MODE")
                                self.konami_index = 0
                        else: self.konami_index = 0

                # --- MODE TEST (Touche T x3) ---
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    now = pygame.time.get_ticks()
                    if now - self.last_t_press < 1000: # Délai augmenté pour faciliter l'activation
                        self.t_press_count += 1
                    else:
                        self.t_press_count = 1
                    self.last_t_press = now
                    
                    if self.t_press_count >= 3:
                        self.test_mode = not self.test_mode
                        self.stats['dev_mode'] = True
                        self.t_press_count = 0
                        if "badge_dev" not in self.inventory:
                            self.inventory.append("badge_dev")
                            self.show_notification("BADGE DEV DÉBLOQUÉ !", "success")
                            self.save_settings()

                # --- ACTIONS DEV MODE ---
                if self.test_mode and event.type == pygame.KEYDOWN:
                    # Cheat Code "coins"
                    if event.unicode:
                        self.cheat_buffer += event.unicode.lower()
                        if self.cheat_buffer.endswith("coins"):
                            self.coins += 10000
                            self.add_coins(10000)
                            self.save_settings()
                            self.show_notification("DEV: +10000 Pièces !", type="success")
                            self.play_sound("coin")
                            self.cheat_buffer = ""
                        if len(self.cheat_buffer) > 10: self.cheat_buffer = self.cheat_buffer[-10:]

                    if event.key == pygame.K_x:
                        self.gain_xp(500)
                        self.show_notification("DEV: +500 XP", type="info")
                    elif event.key == pygame.K_u:
                        for ach in ACHIEVEMENTS:
                            if ach not in self.achievements_unlocked:
                                self.unlock_achievement(ach)
                        self.show_notification("DEV: Succès débloqués", type="success")
                    elif event.key == pygame.K_i:
                        for item in SHOP_CATALOG:
                            if item not in self.inventory:
                                self.inventory.append(item)
                        self.save_settings()
                        self.show_notification("DEV: Boutique débloquée", type="success")
                    elif event.key == pygame.K_w and self.state == "GAME":
                        # Victoire instantanée
                        self.score[self.my_id] = self.settings['win_score'] - 1
                        # On fait perdre l'adversaire pour gagner le point final
                        self.current_player = 1 if self.my_id == 0 else 0
                        self.process_action("POINT")

                    if event.unicode == ':' or event.key == pygame.K_COLON:
                        # Faire perdre le bot (donc JE gagne le point)
                        # Pour gagner le point, c'est comme si le joueur précédent (Bot) avait échoué
                        self.current_player = 1 if self.my_id == 0 else 0 # On force le tour du bot
                        self.process_action("POINT")
                    
                    elif event.unicode == '/' or event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                        # Faire gagner le bot (donc JE perds le point)
                        # C'est comme si J'avais échoué
                        self.current_player = self.my_id # On force mon tour
                        self.process_action("POINT")
                    
                    elif event.key == pygame.K_s:
                        self.stats["season"]["level"] = min(100, self.stats["season"]["level"] + 5)
                        self.save_settings()
                        self.show_notification(f"DEV: Saison Niv {self.stats['season']['level']}", "success")
                        if self.state == "MENU_BATTLEPASS": self.create_menu_buttons()

                # Saisie du pseudo
                if self.state == "INPUT_NAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                        elif event.key == pygame.K_RETURN: self.validate_name()
                        elif len(self.username) < 15: self.username += event.unicode

                # Gestion Popup
                if self.popup:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        # Bouton action unique (ex: Récompense)
                        if self.popup.get("action") and self.popup.get("rect_action") and self.popup.get("rect_action").collidepoint(mx, my):
                            self.popup["action"]()
                            continue # Événement géré
                        # Boutons Oui/Non
                        if self.popup.get("yes") and self.popup.get("rect_yes") and self.popup.get("rect_yes").collidepoint(mx, my):
                            self.popup["yes"]()
                            continue # Événement géré
                        elif self.popup.get("no") and self.popup.get("rect_no") and self.popup.get("rect_no").collidepoint(mx, my):
                            self.popup["no"]()
                            continue # Événement géré
                    
                    # Bloquer les autres interactions (clics, clavier) si une pop-up est active
                    if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEWHEEL]:
                        continue

                # --- MINI-JEU BONUS ---
                if self.state == "BONUS_GAME":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        for t in self.bonus_targets[:]:
                            if t.collidepoint(mx, my):
                                self.bonus_targets.remove(t)
                                self.coins += 5
                                self.add_coins(5)
                                self.spawn_bonus_target()
                                self.play_sound("coin")
                                self.add_particles(mx, my, (255, 215, 0))

                # Gestion des boutons
                if self.state == "CROP_AVATAR":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: self.validate_crop()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: self.crop_dragging = True; self.crop_last_mouse = event.pos
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1: self.crop_dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        if self.crop_dragging:
                            dx = event.pos[0] - self.crop_last_mouse[0]
                            dy = event.pos[1] - self.crop_last_mouse[1]
                            self.crop_offset[0] += dx
                            self.crop_offset[1] += dy
                            self.crop_last_mouse = event.pos
                    elif event.type == pygame.MOUSEWHEEL:
                        self.crop_scale += event.y * 0.05
                        if self.crop_scale < 0.1: self.crop_scale = 0.1
                
                if self.state == "COLOR_PICKER":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        for key, rect in self.color_picker_sliders.items():
                            if rect.collidepoint(mx, my):
                                self.active_slider = key
                                ratio = (mx - rect.x) / rect.width
                                self.color_picker_values[key] = int(max(0, min(255, ratio * 255)))
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.active_slider = None
                    elif event.type == pygame.MOUSEMOTION and self.active_slider:
                        mx, my = event.pos
                        rect = self.color_picker_sliders[self.active_slider]
                        ratio = (mx - rect.x) / rect.width
                        self.color_picker_values[self.active_slider] = int(max(0, min(255, ratio * 255)))

                if self.transition_state is None and not self.is_connecting:
                    action_taken = False
                    try:
                        for btn in self.buttons:
                            if btn.check_click(event):
                                self.play_sound("click")
                                action_taken = True
                                break
                        
                        if not action_taken:
                            for btn in self.avatar_grid_buttons:
                                # Vérification de visibilité pour les avatars (Scroll)
                                if self.state == "INPUT_NAME":
                                    cy = SCREEN_HEIGHT // 2
                                    # Zone visible : cy - 245 à cy + 245 (Correspond à la grille réelle)
                                    if btn.rect.top > cy + 245 or btn.rect.bottom < cy - 245:
                                        continue
                                if btn.check_click(event):
                                    self.play_sound("click")
                                    break
                    except Exception as e:
                        print(f"Erreur UI: {e}")
                
                # --- LOGIQUE DU MENU ---
                if self.state == "MENU_JOIN":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos
                        ip_w = 400 if self.join_custom_port else 600
                        ip_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, 380, ip_w, 80)
                        if ip_rect.collidepoint(mx, my): self.active_input_field = "JOIN_IP"
                        
                        if self.join_custom_port:
                            port_rect = pygame.Rect(SCREEN_WIDTH//2 + 120, 380, 180, 80)
                            if port_rect.collidepoint(mx, my): self.active_input_field = "JOIN_PORT"

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            if self.join_custom_port:
                                self.active_input_field = "JOIN_PORT" if self.active_input_field == "JOIN_IP" else "JOIN_IP"

                        if self.active_input_field == "JOIN_PORT" and self.join_custom_port:
                            if event.key == pygame.K_BACKSPACE: self.input_port_val = self.input_port_val[:-1]
                            elif len(self.input_port_val) < 5 and event.unicode.isdigit(): self.input_port_val += event.unicode
                            elif event.key == pygame.K_RETURN: self.connect_to_host()
                        else:
                            if event.key == pygame.K_BACKSPACE:
                                self.input_ip = self.input_ip[:-1]
                            elif event.key == pygame.K_RETURN:
                                self.connect_to_host()
                            else:
                                self.input_ip += event.unicode

                elif self.state == "MENU_ADD_FRIEND":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos
                        ip_w = 300 if self.friend_custom_port else 500
                        ip_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, 400, ip_w, 60)
                        if ip_rect.collidepoint(mx, my): self.active_input_field = "FRIEND_IP"
                        
                        if self.friend_custom_port:
                            port_rect = pygame.Rect(SCREEN_WIDTH//2 + 70, 400, 180, 60)
                            if port_rect.collidepoint(mx, my): self.active_input_field = "FRIEND_PORT"

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            if self.friend_custom_port:
                                self.active_input_field = "FRIEND_PORT" if self.active_input_field == "FRIEND_IP" else "FRIEND_IP"

                        if self.active_input_field == "FRIEND_PORT" and self.friend_custom_port:
                            if event.key == pygame.K_BACKSPACE: self.friend_port_val = self.friend_port_val[:-1]
                            elif len(self.friend_port_val) < 5 and event.unicode.isdigit(): self.friend_port_val += event.unicode
                            elif event.key == pygame.K_RETURN: self.request_friend()
                        else:
                            if event.key == pygame.K_RETURN:
                                self.request_friend()
                            elif event.key == pygame.K_BACKSPACE:
                                self.friend_code_input = self.friend_code_input[:-1]
                            elif len(self.friend_code_input) < 45: # IPV6 can be long
                                self.friend_code_input += event.unicode

                elif self.state == "MENU_GIFT_CODE":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: self.validate_gift_code()
                        elif event.key == pygame.K_BACKSPACE: self.gift_code_input = self.gift_code_input[:-1]
                        elif len(self.gift_code_input) < 20:
                            self.gift_code_input += event.unicode.upper()

                elif self.state == "SNAKE_GAME":
                    if event.type == pygame.KEYDOWN:
                        if self.snake_data.get("dead"):
                            if event.key == pygame.K_RETURN: self.start_snake_game()
                            elif event.key == pygame.K_ESCAPE: self.set_state("SETTINGS")
                        else:
                            if event.key == pygame.K_UP and self.snake_data["dir"] != (0, 1):
                                self.snake_data["next_dir"] = (0, -1)
                            elif event.key == pygame.K_DOWN and self.snake_data["dir"] != (0, -1):
                                self.snake_data["next_dir"] = (0, 1)
                            elif event.key == pygame.K_LEFT and self.snake_data["dir"] != (1, 0):
                                self.snake_data["next_dir"] = (-1, 0)
                            elif event.key == pygame.K_RIGHT and self.snake_data["dir"] != (-1, 0):
                                self.snake_data["next_dir"] = (1, 0)
                            elif event.key == pygame.K_ESCAPE:
                                self.set_state("SETTINGS")

                elif self.state == "MENU_FRIENDS":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            # Lancer échange avec l'ami survolé
                            if 0 <= self.hovered_friend_idx < len(self.friends):
                                self.request_trade(self.friends[self.hovered_friend_idx]['ip'])
                
                elif self.state == "EDIT_CAT_NAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.cat_name_input = self.cat_name_input[:-1]
                        elif event.key == pygame.K_RETURN and self.cat_name_input: self.set_state("EDIT_CAT_WORDS")
                        elif len(self.cat_name_input) < 20: self.cat_name_input += event.unicode.upper()

                elif self.state == "EDIT_CAT_WORDS":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: self.cat_words_input = self.cat_words_input[:-1]
                        elif event.key == pygame.K_RETURN: self.save_custom_category()
                        else: self.cat_words_input += event.unicode

                elif self.state == "LOCAL_NAMES":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos
                        start_y = 250
                        self.active_local_name_idx = -1
                        for i in range(self.settings['players']):
                            y = start_y + i * 90
                            rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y - 20, 300, 50)
                            if rect.collidepoint(mx, my):
                                self.active_local_name_idx = i
                                self.play_sound("click")
                                break
                    
                    if event.type == pygame.KEYDOWN and self.active_local_name_idx != -1:
                        if event.key == pygame.K_BACKSPACE:
                            self.local_player_names[self.active_local_name_idx] = self.local_player_names[self.active_local_name_idx][:-1]
                        elif event.key == pygame.K_RETURN:
                            self.active_local_name_idx = -1
                        elif len(self.local_player_names[self.active_local_name_idx]) < 12:
                            self.local_player_names[self.active_local_name_idx] += event.unicode

                # --- LOGIQUE LOBBY ---
                elif self.state == "LOBBY":
                    # Gestion Clic Cartes Lobby (si pas de popup et pas de bouton cliqué)
                    if not action_taken and self.selected_lobby_player_id is None:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for pid, rect in self.lobby_player_rects.items():
                                if rect.collidepoint(event.pos):
                                    if self.get_player_data_by_id(pid):
                                        self.selected_lobby_player_id = pid
                                        self.update_lobby_buttons()
                                        self.play_sound("click")
                                    break

                    # Gestion Chat
                    if event.type == pygame.KEYDOWN:
                        # Cheat code: 'P' pour forcer le J2 (Bot) prêt en mode Dev
                        if self.test_mode and self.is_host and event.key == pygame.K_p:
                            if len(self.ready_status) > 1:
                                self.ready_status[1] = not self.ready_status[1]
                                self.check_start_game()

                        if event.key == pygame.K_BACKSPACE:
                            self.chat_input = self.chat_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.send_chat()
                        elif event.key == pygame.K_b and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            self.send_action("BUZZ")
                        else:
                            if len(self.chat_input) < 50:
                                self.chat_input += event.unicode
                    
                    # Scroll Chat
                    if event.type == pygame.MOUSEWHEEL:
                        self.chat_scroll -= event.y
                        if self.chat_scroll < 0: self.chat_scroll = 0

                    # Bouton PRET géré par self.buttons

                # --- LOGIQUE DU JEU ---
                elif self.state == "GAME":
                    # Mode ÉCRIT
                    if self.settings['mode'] == 'WRITTEN':
                        if self.is_local_game or self.current_player == self.my_id:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN and len(self.user_text.strip()) > 0:
                                    if self.user_text.lower().strip() in self.used_words:
                                        self.start_ticks -= 3000 # Pénalité de 3 secondes
                                        self.feedback_msg = "DÉJÀ DIT ! (-3s)"
                                        self.feedback_timer = pygame.time.get_ticks()
                                        self.play_sound("buzz")
                                        self.shake_timer = 10
                                    else:
                                        action_str = f"NEXT_TURN|{self.user_text}"
                                        if not self.is_local_game:
                                            self.send_data(f"ACTION|{action_str}")
                                        self.process_action(action_str)
                                elif event.key == pygame.K_ESCAPE:
                                    self.toggle_pause()
                                elif event.key == pygame.K_BACKSPACE:
                                    self.user_text = self.user_text[:-1]
                                elif event.key == self.keys["CONTEST"]:
                                    self.send_action(f"JUDGE|{self.my_id}")
                                elif event.key == pygame.K_F3:
                                    self.user_text = f"Test_{random.randint(100, 999)}"
                                elif event.key == pygame.K_b and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                                    self.send_action("BUZZ")
                                else:
                                    if len(self.user_text) < 20 and event.key != self.keys["CONTEST"]:
                                        self.user_text += event.unicode
                                        self.play_sound("click") # Son de frappe
                                        if not self.is_local_game:
                                            self.send_data(f"TYPE|{self.user_text}")
                        
                        if not self.is_local_game and self.current_player != self.my_id:
                            if event.type == pygame.KEYDOWN and event.key == self.keys["CONTEST"]:
                                self.send_action(f"JUDGE|{self.my_id}")

                    # Mode VOCAL
                    elif self.settings['mode'] == 'VOCAL':
                        if self.is_local_game or self.current_player == self.my_id:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    self.send_action("NEXT_TURN")
                                elif event.key == pygame.K_ESCAPE:
                                    self.toggle_pause()
                                elif event.key == self.keys["CONTEST"] or event.key == pygame.K_a:
                                    self.send_action(f"JUDGE|{self.my_id}")
                                # Emotes Rapides (1-4)
                                elif event.key == pygame.K_1:
                                    self.send_action(f"EMOTE|😂|{self.my_id}")
                                elif event.key == pygame.K_2:
                                    self.send_action(f"EMOTE|😡|{self.my_id}")
                                elif event.key == pygame.K_3:
                                    self.send_action(f"EMOTE|😱|{self.my_id}")
                                elif event.key == pygame.K_4:
                                    self.send_action(f"EMOTE|👍|{self.my_id}")
                        
                        if not self.is_local_game and self.current_player != self.my_id:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                                self.send_action(f"JUDGE|{self.my_id}")

            # --- LOGIQUE CONTINUE (Hors événements) ---
            if self.state == "GAME":
                # Gestion Gel du Temps
                if pygame.time.get_ticks() < self.freeze_until:
                    # On décale le start_ticks pour que le temps écoulé n'augmente pas
                    self.start_ticks += self.clock.get_time()

                # Timer & Timeout
                elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                
                # Effet Flammes Combo
                if self.rally_combo > 5:
                    self.generate_flame_particles()
                
                self.time_left = self.round_duration - elapsed
                
                # Son Battement de coeur (Stress)
                if 0 < self.time_left <= 3.5:
                    now = pygame.time.get_ticks()
                    if now - self.last_heartbeat > 1000: # Toutes les secondes
                        self.play_sound("click") # Son sec
                        self.last_heartbeat = now

                if (self.is_host or self.is_local_game) and self.time_left <= 0:
                    self.send_action(f"POINT|TIMEOUT|{self.current_player}")
                    self.time_left = 100 # Prevent double trigger
            
            elif self.state == "ROUND_COUNTDOWN":
                if pygame.time.get_ticks() - self.countdown_start > 5000: # 5 secondes pour correspondre à l'affichage
                    self.start_round()
            
            elif self.state == "BONUS_GAME":
                if pygame.time.get_ticks() > self.bonus_end_time:
                    self.state = "ROUND_COUNTDOWN"
                    self.countdown_start = pygame.time.get_ticks()
            
            elif self.state == "TRADE_LOBBY":
                if self.trade_lobby_data["countdown"]:
                    if pygame.time.get_ticks() - self.trade_lobby_data["countdown"] > 5000:
                        # Fin du timer
                        self.send_action("TRADE_CONFIRM")
                        self.trade_lobby_data["countdown"] = None
                if self.trade_finalize_at and pygame.time.get_ticks() >= self.trade_finalize_at:
                    self.reset_network()

            # --- LOGIQUE BOT (TRAINING & TEST) ---
            if (self.test_mode or self.is_training) and self.state == "GAME" and self.current_player == 1 and self.current_player != self.my_id:
                if self.bot_next_move_time == 0:
                    # Calculer le délai une seule fois par tour
                    min_delay, max_delay = 1500, 3000 # MOYEN
                    if self.is_training:
                        if self.bot_difficulty == "FACILE": min_delay, max_delay = 3000, 5000
                        elif self.bot_difficulty == "DIFFICILE": min_delay, max_delay = 500, 1500
                        elif self.bot_difficulty == "HARDCORE": min_delay, max_delay = 200, 600
                    if self.test_mode: min_delay, max_delay = 2000, 2000
                    
                    self.bot_next_move_time = pygame.time.get_ticks() + random.randint(min_delay, max_delay)

                if pygame.time.get_ticks() >= self.bot_next_move_time:
                    if self.is_training:
                        # Bot intelligent (un peu)
                        cat = self.settings['category']
                        words = self.all_categories.get(cat, ["Mot"])
                        msg = random.choice(words)
                    else:
                        # Le bot envoie a, b, c... pour tester
                        msg = chr(97 + (self.bot_msg_index % 26))
                        self.bot_msg_index += 1
                    self.process_action(f"NEXT_TURN|{msg}")
                    self.bot_next_move_time = 0
            else:
                self.bot_next_move_time = 0

            # --- PING HOST ---
            if self.is_host:
                now = pygame.time.get_ticks()
                with self.clients_lock:
                    for c in self.clients:
                        if now - c.get('last_ping_sent', 0) > 2000:
                            c['last_ping_sent'] = now
                            try: c['conn'].sendall(b"PING\n")
                            except: pass

            # --- GESTION RÉSEAU ---
            process_count = 0
            while self.network_queue and process_count < 50: # Limite de traitement par frame (Anti-Freeze)
                msg = self.network_queue.pop(0)
                process_count += 1
                parts = msg.split("|")
                cmd = parts[0]
                
                if cmd == "START":
                    self.settings['mode'] = parts[1]
                    self.settings['time'] = int(parts[2])
                    self.settings['win_score'] = int(parts[3])
                    if len(parts) > 4: self.settings['category'] = parts[4]
                    if len(parts) > 5: self.settings['game_type'] = parts[5]
                    if len(parts) > 6: self.settings['players'] = int(parts[6])
                    self.score = [0] * self.settings['players']
                    self.round_num = 1
                    self.turn_count = 0
                    self.rally_combo = 0
                    self.reset_history()
                    self.send_name() # Envoyer mon nom en réponse
                    # Le client attend le mot
                elif cmd == "FROM":
                    # Traitement des messages venant des clients (Host)
                    # On retire le wrapper FROM|id| et on traite le message original
                    client_id = int(parts[1])
                    real_msg = "|".join(parts[2:])
                    
                    # Injection IP/ID pour les requêtes ami In-Game
                    if real_msg.startswith("LOBBY_FRIEND_"):
                         c = next((c for c in self.clients if c['id'] == client_id), None)
                         if c:
                             real_msg += f"|{c['ip']}|{client_id}"
                    
                    self.network_queue.insert(0, real_msg)
                elif cmd == "NEW_ROUND":
                    self.current_word = parts[1]
                    self.reset_round_state(float(parts[2]))
                elif cmd == "ACTION":
                    self.process_action("|".join(parts[1:]))
                elif cmd == "TRADE_UPDATE":
                    self.process_action("|".join(parts))
                elif cmd == "TYPE":
                    self.opponent_text = parts[1]
                elif cmd == "NAME":
                    self.opponent_name = parts[1]
                    if len(parts) > 2: self.opponent_avatar = parts[2]
                    if len(parts) > 3: self.opponent_border = parts[3]
                    if len(parts) > 4: self.opponent_level = int(parts[4])
                    if len(parts) > 5: self.opponent_name_color = parts[5]
                    if len(parts) > 6: self.opponent_badge = parts[6]
                    if len(parts) > 7: self.opponent_win_streak = int(parts[7])
                    self.show_notification(f"{self.opponent_name} connecté !", type="success")
                elif cmd == "READY":
                    try:
                        pid = int(parts[1])
                        is_r = (parts[2] == "1")
                        # Sécurité: vérifier que pid est valide
                        if pid < 0 or pid >= len(self.ready_status):
                            continue
                        if pid != self.my_id: # Sécurité : ne pas modifier mon propre statut via réseau
                            self.ready_status[pid] = is_r
                            if is_r: self.play_sound("info")
                            
                            # Mise à jour explicite du client pour le broadcast
                            if self.is_host:
                                with self.clients_lock:
                                    for c in self.clients:
                                        if c['id'] == pid:
                                            c['ready'] = is_r
                                            break
                            
                            self.check_start_game()
                            # Si je suis l'hôte, je relaie l'info aux autres clients
                            if self.is_host:
                                self.broadcast_player_list() # Sync parfaite au lieu de simple relais
                        if pid in self.lobby_cache:
                            self.lobby_cache[pid]["ready"] = is_r
                    except: pass
                elif cmd == "PLAYERS":
                    try:
                        self.lobby_cache = {}
                        raw_list = parts[1].split(';')
                        for p_str in raw_list:
                            p = p_str.split(',')
                            if len(p) >= 10:
                                pid = int(p[0])
                                self.lobby_cache[pid] = {
                                    "name": p[1], "avatar": p[2], "border": p[3], 
                                    "ready": (p[4] == "1"), 
                                    "name_color": p[5], 
                                    "ip": p[6],
                                    "level": int(p[7]),
                                    "theme": p[8],
                                    "ping": int(p[9]),
                                    "badge": p[10] if len(p) > 10 else "badge_default",
                                    "streak": int(p[11]) if len(p) > 11 else 0
                                }
                                if pid >= len(self.ready_status):
                                    self.ready_status.extend([False] * (pid - len(self.ready_status) + 1))
                                # FIX: Ne pas écraser son propre statut pour éviter le clignotement
                                if pid != self.my_id:
                                    self.ready_status[pid] = (p[4] == "1")
                    except: pass
                elif cmd == "CHAT":
                    self.chat_messages.append("|".join(parts[1:]))
                    self.play_sound("chat")
                elif cmd == "SETTINGS_UPDATE":
                    self.settings['mode'] = parts[1]
                    self.settings['time'] = int(parts[2])
                    self.settings['win_score'] = int(parts[3])
                    self.settings['category'] = parts[4]
                    self.settings['game_type'] = parts[5]
                    if len(parts) > 6:
                        new_players = int(parts[6])
                        if new_players != self.settings['players']:
                            self.settings['players'] = new_players
                            self.score = [0] * new_players
                            self.ready_status = [False] * new_players
                            self.rematch_ready = [False] * new_players
                elif cmd == "REFRESH_LOBBY":
                    self.create_menu_buttons()
                elif cmd == "QUIT":
                    self.handle_opponent_quit()
                
                # --- GESTION AMIS IN-GAME ---
                elif cmd == "LOBBY_FRIEND_REQ":
                    sender_name = parts[1]
                    sender_avatar = parts[2]
                    # Si Host reçoit: parts contient aussi IP et ID à la fin (injectés par FROM)
                    sender_ip = parts[3] if len(parts) > 3 else self.input_ip
                    sender_id = int(parts[4]) if len(parts) > 4 else -1
                    
                    def accept_lobby_friend():
                        if not any(f['ip'] == sender_ip for f in self.friends):
                            self.friends.append({"name": sender_name, "ip": sender_ip})
                            self.save_settings()
                            self.show_notification(f"{sender_name} ajouté !", type="success")
                        
                        # Répondre
                        resp = f"LOBBY_FRIEND_RESP|ACCEPT|{self.username}"
                        if self.is_host and sender_id != -1:
                            # Host répond à un client spécifique
                            c = next((c for c in self.clients if c['id'] == sender_id), None)
                            if c: c['conn'].sendall((resp + "\n").encode())
                        else:
                            # Client répond à l'hôte
                            self.send_data(resp)
                        self.popup = None

                    self.popup = {
                        "title": "DEMANDE D'AMI", "msg": f"{sender_name} veut vous ajouter !", "avatar": sender_avatar,
                        "yes": accept_lobby_friend, "no": lambda: setattr(self, 'popup', None)
                    }

                elif cmd == "LOBBY_FRIEND_RESP":
                    status = parts[1]
                    if status == "ACCEPT":
                        fname = parts[2]
                        fip = parts[3] if len(parts) > 3 else self.input_ip # IP injectée ou Host IP
                        
                        # Vérification par IP ou Nom pour éviter les doublons/boutons persistants
                        if not any(f['ip'] == fip or f['name'] == fname for f in self.friends):
                            self.friends.append({"name": fname, "ip": fip})
                            self.save_settings()
                            self.show_notification(f"{fname} a accepté !", type="success")
                            if self.state == "LOBBY": self.update_lobby_buttons() # Rafraîchir l'interface

                elif cmd == "TRADE_GIVE":
                    self.show_notification(f"Reçu {parts[1]} pièces !", type="success")
                    self.process_action(f"TRADE_GIVE|{parts[1]}")

            if not running:
                break

            # --- AFFICHAGE ---
            # Gestion du tremblement (BUZZ)
            real_screen = self.screen
            using_temp_screen = False
            if self.shake_timer > 0:
                self.shake_timer -= 1
                intensity = 8
                if self.settings.get('game_type') == 'HARDCORE':
                    intensity = 25 # Tremblement beaucoup plus violent
                shake_x = random.randint(-intensity, intensity)
                shake_y = random.randint(-intensity, intensity)
                self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                using_temp_screen = True
            
            if self.state == "STARTUP_ANIM":
                if self.startup_start_time == 0:
                    self.startup_start_time = pygame.time.get_ticks()
                    # Explosion de particules initiale
                    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                    for _ in range(40):
                        angle = random.uniform(0, 6.28)
                        speed = random.uniform(2, 8)
                        self.particles.append({
                            'x': cx, 'y': cy,
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'life': random.randint(50, 120),
                            'color': ACCENT_COLOR,
                            'size': random.randint(2, 5)
                        })

                total_duration = 3200
                elapsed = pygame.time.get_ticks() - self.startup_start_time

                if elapsed > total_duration:
                    # Transition fluide via la couleur de fond (plus joli que le noir)
                    self.transition_color = BG_COLOR
                    self.set_state(self.post_anim_state)
                else:
                    # Centre
                    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                    word = "dodosi"
                    
                    # Calcul largeur totale
                    letter_surfs = []
                    total_w = 0
                    for ch in word:
                        surf = self.anim_font_obj.render(ch, True, (255, 255, 255))
                        letter_surfs.append(surf)
                        total_w += surf.get_width() + 8
                    total_w -= 8
                    
                    start_x = cx - total_w // 2
                    current_x = start_x
                    
                    # Animation
                    for i, surf in enumerate(letter_surfs):
                        # Délai par lettre
                        delay = i * 80
                        t = elapsed - delay
                        
                        if t < 0: 
                            current_x += surf.get_width() + 8
                            continue
                        
                        # Phase 1: Apparition (Elastic)
                        reveal_dur = 800
                        if t < reveal_dur:
                            prog = t / reveal_dur
                            # Elastic Out
                            p = 1 - pow(2, -10 * prog) * math.sin((prog * 10 - 0.75) * (2 * math.pi) / 3)
                            if p > 1: p = 1
                            
                            scale = 0.5 + 0.5 * p
                            alpha = int(255 * min(1.0, prog * 3))
                            offset_y = (1 - p) * 100
                            col = self.interpolate_color(ACCENT_COLOR, (255, 255, 255), min(1.0, p))
                        
                        # Phase 2: Hold & Shine
                        elif elapsed < 2400:
                            scale = 1.0
                            alpha = 255
                            offset_y = 0
                            col = (255, 255, 255)
                            
                            # Shine wave
                            shine_t = (elapsed - 1200) / 800
                            if 0 <= shine_t <= 1:
                                rel_pos = i / len(word)
                                dist = abs(shine_t - rel_pos)
                                if dist < 0.2:
                                    intensity = 1 - (dist / 0.2)
                                    col = self.interpolate_color((255, 255, 255), ACCENT_COLOR, intensity)
                                    scale = 1.0 + 0.1 * intensity

                        # Phase 3: Exit
                        else:
                            exit_t = (elapsed - 2400) / 800
                            exit_t = min(1.0, exit_t)
                            p = exit_t * exit_t * exit_t # Ease In
                            
                            scale = 1.0 - 0.3 * p
                            alpha = int(255 * (1 - p))
                            offset_y = -p * 100 # Move Up and Fade out
                            col = (255, 255, 255)

                        # Rendu
                        if alpha > 5:
                            w = int(surf.get_width() * scale)
                            h = int(surf.get_height() * scale)
                            
                            # Glow (Ombre colorée)
                            if alpha > 100:
                                glow = pygame.transform.smoothscale(surf, (w + 20, h + 20))
                                glow.fill(ACCENT_COLOR, special_flags=pygame.BLEND_RGBA_MULT)
                                glow.set_alpha(50)
                                self.screen.blit(glow, (current_x + (surf.get_width() - w)//2 - 10, cy - h//2 + offset_y - 10))

                            scaled = pygame.transform.smoothscale(surf, (w, h))
                            scaled.fill(col, special_flags=pygame.BLEND_RGBA_MULT)
                            scaled.set_alpha(alpha)
                            
                            draw_x = current_x + (surf.get_width() - w) // 2
                            draw_y = cy - h // 2 + offset_y
                            self.screen.blit(scaled, (draw_x, draw_y))
                        
                        current_x += surf.get_width() + 8
            elif self.state == "TUTORIAL":
                # Fond moderne en dégradé
                for y in range(SCREEN_HEIGHT):
                    t = y / max(1, SCREEN_HEIGHT - 1)
                    col = self.interpolate_color((10, 14, 22), (22, 26, 42), t)
                    pygame.draw.line(self.screen, col, (0, y), (SCREEN_WIDTH, y))

                t_now = pygame.time.get_ticks()
                glow = 0.65 + 0.35 * math.sin(t_now * 0.004)

                # Panneau principal
                main_w = min(1480, SCREEN_WIDTH - 90)
                main_h = min(840, SCREEN_HEIGHT - 90)
                main_x = (SCREEN_WIDTH - main_w) // 2
                main_y = (SCREEN_HEIGHT - main_h) // 2
                main_rect = pygame.Rect(main_x, main_y, main_w, main_h)

                self.draw_panel(main_rect.x, main_rect.y, main_rect.w, main_rect.h)
                pygame.draw.rect(self.screen, (18, 23, 34), main_rect, border_radius=22)
                border_col = (80, int(145 + 45 * glow), int(200 + 30 * glow))
                pygame.draw.rect(self.screen, border_col, main_rect, 2, border_radius=22)

                # Header
                header_h = 145
                header_rect = pygame.Rect(main_rect.x, main_rect.y, main_rect.w, header_h)
                pygame.draw.rect(self.screen, (24, 31, 46), header_rect, border_top_left_radius=22, border_top_right_radius=22)
                pygame.draw.line(self.screen, (70, 85, 110), (header_rect.x + 20, header_rect.bottom), (header_rect.right - 20, header_rect.bottom), 2)

                self.draw_text_shadow("BIENVENUE SUR WORLD RUSH", self.big_font, (190, 235, 255), SCREEN_WIDTH // 2, header_rect.y + 45)
                self.draw_text("Guide rapide pour demarrer efficacement", self.font, (175, 190, 210), SCREEN_WIDTH // 2, header_rect.y + 95)

                # Badge version
                ver_w = min(240, max(180, header_rect.w // 5))
                ver_rect = pygame.Rect(header_rect.right - ver_w - 24, header_rect.y + 24, ver_w, 42)
                pygame.draw.rect(self.screen, (34, 44, 64), ver_rect, border_radius=18)
                pygame.draw.rect(self.screen, (95, 140, 195), ver_rect, 1, border_radius=18)
                self.draw_text_fit(f"VERSION {CURRENT_VERSION}", self.small_bold_font, (175, 210, 255), ver_rect.centerx, ver_rect.centery, ver_rect.w - 18)

                # Zones contenu
                content_top = header_rect.bottom + 16
                content_h = main_rect.bottom - 136 - content_top
                col_gap = 24
                inner_margin = 30
                col_w = (main_rect.w - inner_margin * 2 - col_gap) // 2
                left_rect = pygame.Rect(main_rect.x + inner_margin, content_top, col_w, content_h)
                right_rect = pygame.Rect(left_rect.right + col_gap, content_top, col_w, content_h)

                pygame.draw.rect(self.screen, (20, 27, 40), left_rect, border_radius=16)
                pygame.draw.rect(self.screen, (20, 27, 40), right_rect, border_radius=16)
                pygame.draw.rect(self.screen, (65, 82, 108), left_rect, 1, border_radius=16)
                pygame.draw.rect(self.screen, (65, 82, 108), right_rect, 1, border_radius=16)

                self.draw_text("PLAN DE JEU", self.medium_font, (160, 240, 200), left_rect.centerx, left_rect.y + 26)
                self.draw_text("MODES ET CONSEILS", self.medium_font, (170, 220, 255), right_rect.centerx, right_rect.y + 26)

                # Colonne gauche: étapes
                steps = [
                    ("1", "Trouve un mot lié au précédent", "Vise une réponse claire avant la fin du chrono (5s)."),
                    ("2", "Valide ou conteste au bon moment", "ENTRÉE valide. MAJ/TAB conteste un mot douteux."),
                    ("3", "Contrôle ton rythme", "Les réponses rapides créent des combos utiles."),
                    ("4", "Progression & Bonus", "Battle Pass, Défi du jour, Roue et Échanges.")
                ]
                step_top = left_rect.y + 48
                step_h = max(62, min(92, (left_rect.h - 80) // 4))
                for i, (num, title, desc) in enumerate(steps):
                    y = step_top + i * step_h
                    card = pygame.Rect(left_rect.x + 14, y, left_rect.w - 28, step_h - 10)
                    pygame.draw.rect(self.screen, (30, 38, 54), card, border_radius=12)
                    pygame.draw.rect(self.screen, (78, 96, 125), card, 1, border_radius=12)

                    bubble = pygame.Rect(card.x + 14, card.y + 10, 34, 34)
                    pygame.draw.rect(self.screen, (0, 195, 160), bubble, border_radius=17)
                    self.draw_text(num, self.small_bold_font, (10, 25, 30), bubble.centerx, bubble.centery)
                    self.draw_text(title, self.small_bold_font, (225, 235, 245), card.x + 62, card.y + 14, center=False)
                    desc_lines = self.wrap_text_lines(desc, self.small_bold_font, card.w - 78)
                    for li, line in enumerate(desc_lines[:2]):
                        self.draw_text(line, self.small_bold_font, (150, 170, 192), card.x + 62, card.y + 36 + li * 18, center=False)

                # Colonne droite: cartes modes
                mode_cards = [
                    ("NORMAL / SPEED", "Rythme classique ou ultra-rapide."),
                    ("SURVIE / HARDCORE", "Pression maximale, peu d'erreurs permises."),
                    ("CHAOS / TIME TRIAL", "Patterns imprévisibles et timing strict."),
                    ("MULTI / PROGRESSION", "Amis, lobby, succès, boutique, saison.")
                ]
                grid_gap = 14
                card_w = (right_rect.w - 42 - grid_gap) // 2
                card_h = (right_rect.h - 92 - grid_gap) // 2
                for i, (title, desc) in enumerate(mode_cards):
                    row = i // 2
                    col_i = i % 2
                    x = right_rect.x + 14 + col_i * (card_w + grid_gap)
                    y = right_rect.y + 56 + row * (card_h + grid_gap)
                    card = pygame.Rect(x, y, card_w, card_h)
                    bg = (34, 44, 63) if i % 2 == 0 else (29, 42, 58)
                    pygame.draw.rect(self.screen, bg, card, border_radius=14)
                    pygame.draw.rect(self.screen, (92, 125, 166), card, 1, border_radius=14)
                    self.draw_text(title, self.small_bold_font, (205, 230, 255), card.centerx, card.y + 28)
                    desc_lines = self.wrap_text_lines(desc, self.small_bold_font, card.w - 22)
                    for li, line in enumerate(desc_lines[:3]):
                        self.draw_text(line, self.small_bold_font, (160, 178, 200), card.centerx, card.y + 62 + li * 18)

                # Bandeau tips bas
                tips_rect = pygame.Rect(main_rect.x + 30, main_rect.bottom - 100, main_rect.w - 60, 62)
                pygame.draw.rect(self.screen, (30, 40, 56), tips_rect, border_radius=14)
                pygame.draw.rect(self.screen, (85, 112, 148), tips_rect, 1, border_radius=14)
                tips_text = "ASTUCE: garde toujours une option de mot de secours pour ne jamais perdre un tour."
                tips_lines = self.wrap_text_lines(tips_text, self.small_bold_font, tips_rect.w - 24)
                if len(tips_lines) == 1:
                    self.draw_text(tips_lines[0], self.small_bold_font, (190, 214, 238), tips_rect.centerx, tips_rect.centery)
                else:
                    self.draw_text(tips_lines[0], self.small_bold_font, (190, 214, 238), tips_rect.centerx, tips_rect.y + 22)
                    self.draw_text(tips_lines[1], self.small_bold_font, (190, 214, 238), tips_rect.centerx, tips_rect.y + 42)

            elif self.state == "INPUT_NAME":
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                panel_w, panel_h = 1200, 650
                panel_x, panel_y = cx - panel_w // 2, cy - panel_h // 2

                # Fond Principal
                self.draw_panel(panel_x, panel_y, panel_w, panel_h)
                
                # Séparateur
                left_w = 400
                pygame.draw.line(self.screen, (60, 70, 90), (panel_x + left_w, panel_y + 20), (panel_x + left_w, panel_y + panel_h - 20), 2)

                # --- COLONNE GAUCHE (Preview) ---
                left_cx = panel_x + left_w // 2
                self.draw_text_shadow("MON PROFIL", self.big_font, ACCENT_COLOR, left_cx, panel_y + 60)
                
                # Avatar Preview (Grand)
                self.draw_avatar(self.avatar, left_cx, panel_y + 180, 90, self.equipped['border'])
                # Draw Badge
                if self.equipped['badge'] != "badge_default":
                    self.draw_badge(self.equipped['badge'], left_cx + 60, panel_y + 240)
                
                # Input Pseudo
                input_y = panel_y + 410
                self.draw_text("PSEUDO", self.small_bold_font, (150, 150, 150), left_cx, input_y - 35)
                input_rect = pygame.Rect(left_cx - 140, input_y, 280, 60)
                name_color = self.get_name_color(self.equipped.get('name_color', 'name_color_default'))
                self.draw_fancy_input_box(input_rect, self.username, "...", active=True, font=self.medium_font, text_color=name_color)

                # --- COLONNE DROITE (Grille) ---
                right_x = panel_x + left_w + 20
                right_w = panel_w - left_w - 40
                grid_y = panel_y + 80
                grid_h = panel_h - 160
                
                self.draw_text_shadow("CHOISIR UN AVATAR", self.big_font, (200, 200, 200), right_x + right_w//2, panel_y + 50)
                
                # Fond Grille
                pygame.draw.rect(self.screen, (20, 25, 30), (right_x, grid_y, right_w, grid_h), border_radius=10)
                
                # Clipping et Dessin Boutons
                self.screen.set_clip(pygame.Rect(right_x, grid_y, right_w, grid_h))
                for btn in self.avatar_grid_buttons:
                    btn.draw(self.screen)
                self.screen.set_clip(None)
                
                # Scrollbar visuelle
                total_rows = math.ceil(len(AVATARS) / 8) # 8 cols
                total_h = total_rows * 70 # 60 size + 10 gap
                if total_h > grid_h:
                    sb_h = max(30, (grid_h / total_h) * grid_h)
                    sb_y = grid_y + (self.avatar_scroll / (total_h - grid_h)) * (grid_h - sb_h)
                    pygame.draw.rect(self.screen, (60, 70, 80), (right_x + right_w - 8, sb_y, 6, sb_h), border_radius=3)

            elif self.state == "MENU_HISTORY":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 50, 800, 850)
                self.draw_text_shadow("HISTORIQUE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                start_y = 180
                cx = SCREEN_WIDTH // 2
                
                if not self.stats["history"]:
                    self.draw_text("Aucune partie jouée.", self.font, (150, 150, 150), cx, 300)
                
                for i, game in enumerate(self.stats["history"]):
                    if i > 8: break # Max 9 items visible
                    y = start_y + i * 80
                    rect = pygame.Rect(cx - 350, y, 700, 70)
                    
                    col = (50, 200, 50) if game["result"] == "VICTOIRE" or game["result"] == "WIN" else ((200, 50, 50) if game["result"] == "DÉFAITE" else TEXT_COLOR)
                    
                    pygame.draw.rect(self.screen, (30, 35, 45), rect, border_radius=10)
                    pygame.draw.rect(self.screen, (60, 70, 80), rect, 1, border_radius=10)
                    self.draw_text(f"{game['date']}", self.small_bold_font, (150, 150, 150), rect.left + 80, rect.centery)
                    self.draw_text(f"vs {game['opponent']}", self.font, TEXT_COLOR, rect.centerx, rect.centery)
                    self.draw_text(f"{game['score']}", self.big_font, col, rect.right - 80, rect.centery)

            elif self.state == "CROP_AVATAR":
                self.draw_text_shadow("AJUSTER L'IMAGE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 50)
                self.draw_text("Zoom: Molette | Déplacer: Clic gauche", self.font, (150, 150, 150), SCREEN_WIDTH//2, 100)
                
                if self.crop_image:
                    img_w = int(self.crop_image.get_width() * self.crop_scale)
                    img_h = int(self.crop_image.get_height() * self.crop_scale)
                    scaled = pygame.transform.smoothscale(self.crop_image, (img_w, img_h))
                    rect = scaled.get_rect(center=(self.crop_offset[0], self.crop_offset[1]))
                    self.screen.blit(scaled, rect)
                
                # Masque sombre
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                pygame.draw.circle(overlay, (0, 0, 0, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 150)
                self.screen.blit(overlay, (0, 0))
                
                # Cercle guide
                pygame.draw.circle(self.screen, ACCENT_COLOR, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 150, 3)

            elif self.state == "MENU_JOIN":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 150, 1000, 650) # Agrandissement fenêtre rejoindre
                self.draw_text_shadow("REJOINDRE UNE PARTIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 220)
                self.draw_text("Entrez l'IP de l'hôte :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 320)
                
                # Input Box Moderne
                ip_w = 400 if self.join_custom_port else 600
                input_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, 380, ip_w, 80)
                is_active = (self.active_input_field == "JOIN_IP")
                self.draw_fancy_input_box(input_rect, self.input_ip, "127.0.0.1", active=is_active, font=self.big_font)
                
                if self.join_custom_port:
                    port_rect = pygame.Rect(SCREEN_WIDTH//2 + 120, 380, 180, 80)
                    is_p_active = (self.active_input_field == "JOIN_PORT")
                    self.draw_fancy_input_box(port_rect, self.input_port_val, "PORT", active=is_p_active, font=self.big_font)
                    self.draw_text(":", self.big_font, TEXT_COLOR, SCREEN_WIDTH//2 + 110, 420)
                
                if self.connect_status:
                    col = ACCENT_COLOR if "Connecté" in self.connect_status else ALERT_COLOR
                    self.draw_text(self.connect_status, self.font, col, SCREEN_WIDTH//2, 490)
                
                self.draw_text("Demandez l'IP Internet à l'hôte (ou utilisez Radmin/Hamachi)", self.font, (100, 100, 100), SCREEN_WIDTH//2, 720)

            elif self.state == "MENU_FRIENDS":
                self.draw_panel(SCREEN_WIDTH//2 - 600, 50, 1200, 850)
                self.draw_text_shadow("MES AMIS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                # Affichage IP Publique
                ip_txt = f"Mon IP: {self.public_ip}" if self.public_ip else "Mon IP: Recherche..."
                self.draw_text(ip_txt, self.font, (150, 150, 150), SCREEN_WIDTH//2, 160) # Centré sous le titre
                if self.connect_status == "IP Copiée !":
                    self.draw_text("Copié !", self.font, ACCENT_COLOR, SCREEN_WIDTH//2 + 200, 160)

                cx = SCREEN_WIDTH // 2
                card_w, card_h = 500, 140
                gap_x, gap_y = 40, 30
                
                available_w = SCREEN_WIDTH - 100
                cols = max(1, available_w // (card_w + gap_x))
                cols = min(2, cols)
                
                start_y = 200
                start_x = cx - ((cols * card_w + (cols - 1) * gap_x) // 2)

                if not self.friends:
                    self.draw_text("Aucun ami ajouté.", self.font, (100, 100, 100), cx, 400)

                for i, friend in enumerate(self.friends):
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap_x)
                    y = start_y + row * (card_h + gap_y)
                    
                    # Fond Carte
                    pygame.draw.rect(self.screen, (35, 40, 50), (x, y, card_w, card_h), border_radius=15)
                    pygame.draw.rect(self.screen, (60, 70, 80), (x, y, card_w, card_h), 2, border_radius=15)
                    
                    # Avatar (Placeholder ou Initiale)
                    # pygame.draw.circle(self.screen, (50, 60, 70), (x + 60, y + card_h//2), 40) # Remplacé par draw_avatar générique si possible, sinon simple
                    initial = friend['name'][0].upper() if friend['name'] else "👤"
                    self.draw_text(initial, self.medium_font, ACCENT_COLOR, x + 60, y + card_h//2)
                    
                    # Infos
                    self.draw_text_fit(friend['name'], self.medium_font, TEXT_COLOR, x + 120, y + 5, card_w - 320, center=False)
                    self.draw_text(friend['ip'], self.font, (120, 120, 120), x + 120, y + 55, center=False)
                    
                    # Statut En ligne / Hors ligne
                    status = self.friends_status.get(friend['ip'], "...")
                    stat_col = (120, 120, 120)
                    if status == "En ligne": stat_col = (50, 255, 50)
                    elif status == "Hors ligne": stat_col = (255, 50, 50)
                    
                    pygame.draw.circle(self.screen, stat_col, (x + card_w - 190, y + 30), 6)
                    self.draw_text_fit(status, self.small_bold_font, stat_col, x + card_w - 175, y + 20, 160, center=False)

            elif self.state == "MENU_ADD_FRIEND":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 250, 600, 450)
                self.draw_text_shadow("AJOUTER UN AMI", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 300)
                
                self.draw_text("Entrez le Code Ami :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 370)
                
                ip_w = 300 if self.friend_custom_port else 500
                input_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, 400, ip_w, 60)
                is_active = (self.active_input_field == "FRIEND_IP")
                self.draw_fancy_input_box(input_rect, self.friend_code_input, "IP ou Code Ami", active=is_active, font=self.font)
                
                if self.friend_custom_port:
                    port_rect = pygame.Rect(SCREEN_WIDTH//2 + 70, 400, 180, 60)
                    is_p_active = (self.active_input_field == "FRIEND_PORT")
                    self.draw_fancy_input_box(port_rect, self.friend_port_val, "PORT", active=is_p_active, font=self.font)

                self.draw_text("Le nom de l'ami sera ajouté automatiquement.", self.font, (150, 150, 150), SCREEN_WIDTH//2, 480)

            elif self.state == "COLOR_PICKER":
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                self.draw_panel(cx - 300, cy - 300, 600, 600)
                self.draw_text_shadow("COULEUR PERSONNALISÉE", self.big_font, ACCENT_COLOR, cx, cy - 250)

                # Color Preview
                current_color = (self.color_picker_values['r'], self.color_picker_values['g'], self.color_picker_values['b'])
                pygame.draw.rect(self.screen, current_color, (cx - 100, cy - 180, 200, 100), border_radius=15)
                pygame.draw.rect(self.screen, (255,255,255), (cx - 100, cy - 180, 200, 100), 2, border_radius=15)

                # Sliders
                slider_y = cy - 20
                slider_w = 400
                self.color_picker_sliders = {} # Reset rects
                for color_key, y_offset, color_tuple in [('r', 0, (255, 0, 0)), ('g', 80, (0, 255, 0)), ('b', 160, (0, 0, 255))]:
                    y = slider_y + y_offset
                    slider_rect = pygame.Rect(cx - slider_w//2, y, slider_w, 40)
                    pygame.draw.rect(self.screen, (30, 35, 45), slider_rect, border_radius=10)
                    value = self.color_picker_values[color_key]
                    ratio = value / 255.0
                    pygame.draw.rect(self.screen, color_tuple, (slider_rect.x, y, slider_w * ratio, 40), border_radius=10)
                    self.draw_text(f"{color_key.upper()}: {value}", self.font, TEXT_COLOR, cx, y + 20)
                    self.color_picker_sliders[color_key] = slider_rect

            elif self.state == "MENU_ACHIEVEMENTS":
                self.draw_panel(SCREEN_WIDTH//2 - 600, 50, 1200, 850)
                self.draw_text_shadow("SUCCÈS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 100)
                
                # Filter buttons (already created, just for positioning)
                cx = SCREEN_WIDTH // 2
                btn_w = 180
                if len(self.buttons) > 3:
                    self.buttons[1].rect.center = (cx - btn_w - 10, 215)
                    self.buttons[2].rect.center = (cx, 215)
                    self.buttons[3].rect.center = (cx + btn_w + 10, 215)

                # Filter achievements
                all_ach_ids = list(ACHIEVEMENTS.keys())
                if self.achievements_filter == "UNLOCKED":
                    filtered_achievements = [aid for aid in all_ach_ids if aid in self.achievements_unlocked]
                elif self.achievements_filter == "LOCKED":
                    filtered_achievements = [aid for aid in all_ach_ids if aid not in self.achievements_unlocked]
                else: # ALL
                    filtered_achievements = sorted(all_ach_ids, key=lambda x: (x in self.achievements_unlocked, x))

                total_ach = len(ACHIEVEMENTS)
                unlocked_count = len(self.achievements_unlocked)
                pct = int((unlocked_count / total_ach) * 100) if total_ach > 0 else 0
                self.draw_text(f"Progression: {unlocked_count}/{total_ach} ({pct}%)", self.font, (200, 200, 200), SCREEN_WIDTH//2, 150)

                # Zone de clipping pour le défilement
                clip_rect = pygame.Rect(SCREEN_WIDTH//2 - 600, 250, 1200, 640)
                self.screen.set_clip(clip_rect)
                
                cols = 2
                card_w, card_h = 550, 120 # Hauteur augmentée pour la barre de progression
                gap_x, gap_y = 40, 20
                start_x = SCREEN_WIDTH // 2 - (card_w * cols + gap_x * (cols - 1)) // 2
                start_y = 260 - self.achievements_scroll

                for i, aid in enumerate(filtered_achievements):
                    data = ACHIEVEMENTS[aid]
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap_x)
                    y = start_y + row * (card_h + gap_y)
                    unlocked = aid in self.achievements_unlocked
                    
                    # Card background with gradient for unlocked
                    bg_col = (30, 30, 35)
                    if unlocked:
                        s = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                        pygame.draw.rect(s, (40, 60, 40), (0, 0, card_w, card_h), border_radius=15)
                        pygame.draw.rect(s, (50, 80, 50, 100), (0, 0, card_w, card_h // 2), border_top_left_radius=15, border_top_right_radius=15)
                        self.screen.blit(s, (x, y))
                    else:
                        pygame.draw.rect(self.screen, bg_col, (x, y, card_w, card_h), border_radius=15)

                    border_col = (255, 215, 0) if unlocked else (50, 55, 65)
                    pygame.draw.rect(self.screen, bg_col, (x, y, card_w, card_h), border_radius=15)
                    pygame.draw.rect(self.screen, border_col, (x, y, card_w, card_h), 2, border_radius=15)
                    
                    # Trophy icon
                    trophy_col = (255, 215, 0) if unlocked else (80, 80, 80)
                    self.draw_text("🏆", self.ui_emoji_font, trophy_col, x + 40, y + 40)
                    
                    # Text
                    name_col = (255, 255, 255) if unlocked else (150, 150, 150)
                    self.draw_text(data["name"], self.small_bold_font, name_col, x + 80, y + 25, center=False)
                    self.draw_text(data["desc"], self.font, (180, 180, 180), x + 80, y + 50, center=False)
                    
                    # Reward
                    self.draw_coin_ui(x + card_w - 100, y + 40, data['reward'])

                    # Progress Bar
                    stat_key = data.get("stat")
                    if stat_key and not unlocked:
                        current_val = self.get_stat_value(stat_key)
                        target_val = data.get("target", 1)
                        # Special handling for shop_king target
                        if stat_key == "shop_king":
                            target_val = len([k for k in SHOP_CATALOG.keys() if k != "gift_daily"])

                        progress = min(1.0, current_val / target_val) if target_val > 0 else 1.0
                        
                        progress_text = f"{int(current_val)} / {target_val}"
                        txt_surf = self.small_bold_font.render(progress_text, True, (180, 180, 180))
                        
                        bar_h_inner = 12
                        bar_y = y + card_h - 30
                        bar_x = x + 80
                        
                        # Texte à droite
                        txt_x = x + card_w - 40 - txt_surf.get_width()
                        self.screen.blit(txt_surf, (txt_x, bar_y - 8))
                        
                        # Barre à gauche du texte (remplit l'espace restant)
                        bar_w = txt_x - bar_x - 15
                        
                        pygame.draw.rect(self.screen, (20, 25, 30), (bar_x, bar_y, bar_w, bar_h_inner), border_radius=6)
                        if progress > 0:
                            pygame.draw.rect(self.screen, ACCENT_COLOR, (bar_x, bar_y, bar_w * progress, bar_h_inner), border_radius=6)
                        pygame.draw.rect(self.screen, (60, 60, 70), (bar_x, bar_y, bar_w, bar_h_inner), 1, border_radius=6)
                
                self.screen.set_clip(None)

            elif self.state == "MENU_BATTLEPASS":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 50, 1000, 850)
                self.draw_text_shadow("BATTLE PASS - SAISON 1", self.big_font, (0, 255, 128), SCREEN_WIDTH//2, 90)
                
                if self.test_mode:
                    self.draw_text("DEV: Appuyez sur 'S' pour +5 Niveaux", self.small_bold_font, (255, 100, 100), SCREEN_WIDTH//2, 130)
                
                # Info Saison
                s_level = self.stats["season"]["level"]
                s_xp = self.stats["season"]["xp"]
                
                if s_level >= 100:
                    # Animation Niveau 100
                    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
                    col = self.interpolate_color((255, 215, 0), (255, 255, 255), pulse)
                    self.draw_text_shadow("NIVEAU MAX ATTEINT ! 👑", self.medium_font, col, SCREEN_WIDTH//2, 160)
                    
                    # Particules dorées
                    if random.random() < 0.1:
                        self.particles.append({
                            'x': random.randint(SCREEN_WIDTH//2 - 300, SCREEN_WIDTH//2 + 300), 'y': 200,
                            'vx': random.uniform(-2, 2), 'vy': random.uniform(-2, 2), 'life': random.randint(50, 150), 'color': (255, 215, 0), 'size': random.randint(3, 8)
                        })
                else:
                    self.draw_text(f"Niveau Actuel : {s_level}", self.medium_font, TEXT_COLOR, SCREEN_WIDTH//2, 160)
                
                # Barre XP Saison
                bar_w, bar_h = 600, 20
                bx, by = SCREEN_WIDTH//2 - bar_w//2, 190
                ratio = min(1.0, s_xp / 200)
                
                # Fond barre
                pygame.draw.rect(self.screen, (30, 35, 45), (bx, by, bar_w, bar_h), border_radius=10)
                
                # Remplissage dégradé
                if ratio > 0:
                    fill_w = int(bar_w * ratio)
                    fill_rect = pygame.Rect(bx, by, fill_w, bar_h)
                    pygame.draw.rect(self.screen, (0, 255, 128), fill_rect, border_radius=10)
                    
                    # Glow effect at tip
                    if fill_w > 10:
                        pygame.draw.circle(self.screen, (200, 255, 200), (bx + fill_w - 5, by + bar_h//2), 8)

                self.draw_text(f"{s_xp} / 200 XP", self.small_bold_font, (200, 200, 200), SCREEN_WIDTH//2, by + 35)

                # Liste des niveaux
                list_y = 260
                list_h = 600
                item_h = 100
                gap = 15
                cx = SCREEN_WIDTH // 2
                
                clip_rect = pygame.Rect(cx - 450, list_y, 900, list_h)
                self.screen.set_clip(clip_rect)
                
                # Ligne de temps centrale (Fond)
                total_items = len(range(5, 101, 5))
                total_h = total_items * (item_h + gap)
                line_start_y = list_y - self.season_scroll + item_h // 2
                line_end_y = line_start_y + total_h - item_h - gap
                
                # Draw full line background
                pygame.draw.line(self.screen, (40, 50, 60), (cx, line_start_y), (cx, line_end_y), 6)
                
                # Draw unlocked line (Progressive)
                if s_level >= 5:
                    step = item_h + gap
                    progress_h = (s_level - 5) * (step / 5)
                    
                    # Add sub-level progress (XP)
                    if s_level < 100:
                        xp_frac = self.stats["season"]["xp"] / 200.0
                        progress_h += xp_frac * (step / 5)
                        
                    max_h = line_end_y - line_start_y
                    if progress_h > max_h: progress_h = max_h
                    pygame.draw.line(self.screen, (0, 255, 128), (cx, line_start_y), (cx, line_start_y + progress_h), 6)
                
                for i, lvl in enumerate(range(5, 101, 5)):
                    y = list_y + i * (item_h + gap) - self.season_scroll
                    if y + item_h < list_y or y > list_y + list_h: continue
                    
                    reward = self.get_season_reward(lvl)
                    unlocked = lvl <= s_level
                    claimed = lvl in self.stats["season"]["claimed"]
                    
                    # Fond Carte
                    bg_col = (35, 45, 40) if unlocked else (30, 30, 35)
                    rect = pygame.Rect(cx - 400, y, 800, item_h)
                    
                    # Effet Glow si débloqué
                    if unlocked and not claimed:
                        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
                        glow_alpha = int(20 + 30 * pulse)
                        s_glow = pygame.Surface((rect.w + 20, rect.h + 20), pygame.SRCALPHA)
                        pygame.draw.rect(s_glow, (0, 255, 128, glow_alpha), s_glow.get_rect(), border_radius=25)
                        self.screen.blit(s_glow, (rect.x - 10, rect.y - 10))

                    pygame.draw.rect(self.screen, bg_col, rect, border_radius=15)
                    border_col = (0, 255, 128) if unlocked else (60, 60, 70)
                    pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=15)
                    
                    # Cercle Niveau (Sur la ligne centrale)
                    circle_col = (0, 255, 128) if unlocked else (40, 45, 55)
                    pygame.draw.circle(self.screen, (20, 23, 28), (cx, rect.centery), 30) # Cache ligne
                    pygame.draw.circle(self.screen, circle_col, (cx, rect.centery), 25)
                    pygame.draw.circle(self.screen, (20, 20, 25), (cx, rect.centery), 20)
                    
                    lvl_col = (255, 255, 255) if unlocked else (150, 150, 150)
                    self.draw_text(str(lvl), self.small_bold_font, lvl_col, cx, rect.centery)
                    
                    # Récompense
                    # Icone
                    icon = "🎁"
                    if reward['type'] == 'coins': icon = "💰"
                    elif reward['type'] == 'item':
                        if 'border' in reward['id']: icon = "🖼️"
                        elif 'theme' in reward['id']: icon = "🎨"
                        elif 'badge' in reward['id']: icon = "📛"
                        elif 'name_color' in reward['id']: icon = "✍️"
                    
                    self.draw_text(icon, self.ui_emoji_font, (255, 255, 255), rect.left + 50, rect.centery)
                    self.draw_text(reward["name"], self.medium_font, TEXT_COLOR, rect.left + 100, rect.centery, center=False)
                    
                    # Droite : Statut
                    if claimed:
                        self.draw_text("✔", self.ui_emoji_font, (100, 255, 100), rect.right - 150, rect.centery)
                        self.draw_text("REÇU", self.small_bold_font, (100, 255, 100), rect.right - 90, rect.centery)
                    elif not unlocked:
                        self.draw_text("🔒", self.ui_emoji_font, (100, 100, 100), rect.right - 100, rect.centery)
                    # Si unlocked et pas claimed, le bouton est géré par create_menu_buttons
                
                self.screen.set_clip(None)

            elif self.state == "MENU_CREDITS":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 700)
                self.draw_text_shadow("CRÉDITS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                
                credits = [
                    ("Développeur Principal", "dodosiiii"),
                    ("Design & UI", "dodosiiii"),
                    ("Correction de Bugs", "Gemini"),
                    ("Moteur de Jeu", "Pygame"),
                    ("Inspiration", "Word Games"),
                    ("Remerciements", "Tous les testeurs")
                ]
                
                start_y = 250
                for i, (role, name) in enumerate(credits):
                    self.draw_text(role, self.small_bold_font, (150, 150, 150), SCREEN_WIDTH//2, start_y + i * 80)
                    self.draw_text(name, self.medium_font, TEXT_COLOR, SCREEN_WIDTH//2, start_y + i * 80 + 30)

            elif self.state == "MENU_GIFT_CODE":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 250, 600, 450)
                self.draw_text_shadow("CODE CADEAU", self.big_font, (255, 200, 0), SCREEN_WIDTH//2, 300)
                self.draw_text("Entrez votre code bonus :", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 370)
                input_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, 400, 500, 60)
                self.draw_fancy_input_box(input_rect, self.gift_code_input, "Ex: RUSH2024", active=True, font=self.font)

            elif self.state == "SNAKE_GAME":
                self.update_snake_game()
                self.draw_snake_game()

            elif self.state == "MENU_CUSTOM_CATS":
                cx = SCREEN_WIDTH // 2
                cy = SCREEN_HEIGHT // 2
                panel_w = 900
                panel_h = 700
                panel_y = cy - panel_h // 2
                
                self.draw_panel(cx - panel_w//2, panel_y, panel_w, panel_h)
                
                # Header
                self.draw_text_shadow("CATÉGORIES PERSO", self.big_font, ACCENT_COLOR, cx, panel_y + 65)
                
                # List Area
                list_y = panel_y + 120
                list_h = panel_h - 160
                item_h = 90
                gap = 15
                
                cats = list(self.custom_categories.keys())
                
                if not cats:
                    self.draw_text("Aucune catégorie.", self.medium_font, (100, 100, 120), cx, cy - 20)
                    self.draw_text("Créez-en une pour jouer avec vos mots !", self.font, (80, 80, 100), cx, cy + 20)
                
                # Clipping
                clip_rect = pygame.Rect(cx - panel_w//2 + 40, list_y, panel_w - 80, list_h)
                self.screen.set_clip(clip_rect)
                
                for i, cat in enumerate(cats):
                    y = list_y + i * (item_h + gap) - self.custom_cats_scroll
                    if y + item_h < list_y or y > list_y + list_h: continue
                    
                    # Card background
                    rect = pygame.Rect(cx - panel_w//2 + 50, y, panel_w - 100, item_h)
                    
                    # Hover effect (simple mouse check)
                    mx, my = pygame.mouse.get_pos()
                    is_hover = rect.collidepoint(mx, my)
                    bg_col = (40, 45, 55) if not is_hover else (50, 55, 65)
                    border_col = (60, 70, 80) if not is_hover else ACCENT_COLOR
                    
                    pygame.draw.rect(self.screen, bg_col, rect, border_radius=12)
                    pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=12)
                    
                    # Icon / Letter
                    letter = cat[0].upper()
                    pygame.draw.circle(self.screen, (30, 35, 40), (rect.x + 45, rect.centery), 25)
                    self.draw_text(letter, self.medium_font, ACCENT_COLOR, rect.x + 45, rect.centery)
                    
                    # Title
                    self.draw_text_fit(cat, self.medium_font, TEXT_COLOR, rect.x + 90, rect.centery - 12, 500, center=False)
                    
                    # Word count
                    word_count = len(self.custom_categories[cat])
                    self.draw_text(f"{word_count} mots", self.font, (150, 150, 160), rect.x + 90, rect.centery + 18, center=False)
                
                self.screen.set_clip(None)
                
                # Scrollbar if needed
                total_h = len(cats) * (item_h + gap)
                if total_h > list_h:
                    sb_h = max(30, (list_h / total_h) * list_h)
                    sb_y = list_y + (self.custom_cats_scroll / (total_h - list_h)) * (list_h - sb_h)
                    pygame.draw.rect(self.screen, (60, 70, 80), (cx + panel_w//2 - 30, sb_y, 6, sb_h), border_radius=3)

            elif self.state == "EDIT_CAT_NAME":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 200, 600, 500)
                self.draw_text_shadow("NOM DE LA CATÉGORIE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 250)
                input_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 350, 400, 60)
                self.draw_fancy_input_box(input_rect, self.cat_name_input, "Ex: MARQUES DE VOITURE", active=True, font=self.font)

            elif self.state == "EDIT_CAT_WORDS":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 700)
                self.draw_text_shadow("AJOUTER DES MOTS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                self.draw_text("Séparez les mots par des virgules (,)", self.font, (150, 150, 150), SCREEN_WIDTH//2, 220)
                
                # Zone de texte large
                rect_w = min(900, SCREEN_WIDTH - 200)
                rect = pygame.Rect(SCREEN_WIDTH//2 - rect_w//2, 250, rect_w, 320)
                pygame.draw.rect(self.screen, (20, 25, 30), rect, border_radius=10)
                pygame.draw.rect(self.screen, ACCENT_COLOR, rect, 2, border_radius=10)
                
                # Affichage multiline basique
                words_text = self.cat_words_input + ("|" if (pygame.time.get_ticks() // 500) % 2 == 0 else "")
                
                # Word wrapping
                words = words_text.split(' ')
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + word + " "
                    if self.font.size(test_line)[0] < rect.width - 40:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)

                for i, line in enumerate(lines):
                    if rect.y + 20 + i * 30 > rect.bottom - 30: break # Don't draw outside the box
                    self.draw_text_fit(line, self.font, TEXT_COLOR, rect.x + 20, rect.y + 20 + i * 30, rect.width - 40, center=False)

            elif self.state == "TRADE_LOBBY":
                # --- REDESIGN TRADE LOBBY ---
                # Fond sombre
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((10, 12, 15, 240))
                self.screen.blit(s, (0, 0))
                
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                
                # Titre
                self.draw_text_shadow("ÉCHANGE", self.big_font, (255, 200, 0), cx, 80)
                
                # Zone d'échange (2 panneaux face à face)
                panel_w, panel_h = 500, 600
                gap = 100
                
                # Panneau Gauche (MOI)
                left_rect = pygame.Rect(cx - panel_w - gap//2, cy - panel_h//2, panel_w, panel_h)
                # Couleur de fond change si verrouillé
                bg_col_me = (30, 50, 30) if self.trade_lobby_data["me"]["locked"] else (30, 35, 45)
                border_col_me = (50, 200, 50) if self.trade_lobby_data["me"]["locked"] else (60, 70, 80)
                
                pygame.draw.rect(self.screen, bg_col_me, left_rect, border_radius=20)
                pygame.draw.rect(self.screen, border_col_me, left_rect, 3, border_radius=20)
                
                # Header Moi
                self.draw_avatar(self.avatar, left_rect.centerx, left_rect.y + 60, 40, self.equipped['border'])
                self.draw_text("MOI", self.medium_font, ACCENT_COLOR, left_rect.centerx, left_rect.y + 120)
                
                # Contenu Moi
                self.draw_text("OFFRE :", self.small_bold_font, (150, 150, 150), left_rect.centerx, left_rect.y + 180)
                self.draw_coin_ui(left_rect.centerx, left_rect.y + 240, self.trade_lobby_data["me"]["coins"])
                
                if self.trade_lobby_data["me"]["locked"]:
                    self.draw_text("PRÊT", self.big_font, (100, 255, 100), left_rect.centerx, left_rect.bottom - 80)
                else:
                    self.draw_text("En attente...", self.font, (100, 100, 100), left_rect.centerx, left_rect.bottom - 80)

                # Panneau Droite (EUX)
                right_rect = pygame.Rect(cx + gap//2, cy - panel_h//2, panel_w, panel_h)
                bg_col_them = (30, 50, 30) if self.trade_lobby_data["them"]["locked"] else (30, 35, 45)
                border_col_them = (50, 200, 50) if self.trade_lobby_data["them"]["locked"] else (60, 70, 80)
                
                pygame.draw.rect(self.screen, bg_col_them, right_rect, border_radius=20)
                pygame.draw.rect(self.screen, border_col_them, right_rect, 3, border_radius=20)
                
                # Header Eux
                self.draw_avatar(self.opponent_avatar, right_rect.centerx, right_rect.y + 60, 40)
                self.draw_text(self.opponent_name, self.medium_font, ALERT_COLOR, right_rect.centerx, right_rect.y + 120)
                
                # Contenu Eux
                self.draw_text("OFFRE :", self.small_bold_font, (150, 150, 150), right_rect.centerx, right_rect.y + 180)
                self.draw_coin_ui(right_rect.centerx, right_rect.y + 240, self.trade_lobby_data["them"]["coins"])
                
                if self.trade_lobby_data["them"]["locked"]:
                    self.draw_text("PRÊT", self.big_font, (100, 255, 100), right_rect.centerx, right_rect.bottom - 80)
                else:
                    self.draw_text("En attente...", self.font, (100, 100, 100), right_rect.centerx, right_rect.bottom - 80)

                # Icone Centrale
                self.draw_text("⇄", self.ui_emoji_font, (255, 255, 255), cx, cy)
                self.update_draw_trade_coin_transfer()

                # Timer Confirmation
                if self.trade_lobby_data["countdown"]:
                    rem = 5 - (pygame.time.get_ticks() - self.trade_lobby_data["countdown"]) / 1000
                    # Overlay countdown
                    s_count = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
                    s_count.fill((0, 0, 0, 150))
                    self.screen.blit(s_count, (0, cy - 50))
                    self.draw_text_shadow(f"ECHANGE DANS {int(rem)+1}...", self.big_font, (255, 255, 255), cx, cy)
                elif self.trade_finalize_at:
                    rem = max(0.0, (self.trade_finalize_at - pygame.time.get_ticks()) / 1000.0)
                    self.draw_text_shadow(f"Validation... {rem:.1f}s", self.font, (220, 220, 220), cx, cy + 120)

            elif self.state == "MENU_SHOP":
                self.draw_text_shadow("MAGASIN", self.big_font, (255, 200, 0), SCREEN_WIDTH//2, 80)
                self.draw_coin_ui(SCREEN_WIDTH - 150, 80, self.coins)
                
                # Grid Config
                cx = SCREEN_WIDTH // 2
                card_w, card_h = 260, 320
                gap = 30
                available_w = SCREEN_WIDTH - 100
                cols = max(1, available_w // (card_w + gap))
                start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
                start_y = 220 - self.shop_scroll
                
                all_items = self.get_sorted_shop_items()
                
                # Filtrage
                filtered_items = []
                for item_id in all_items:
                    item = SHOP_CATALOG[item_id]
                    if self.shop_tab == "ALL": filtered_items.append(item_id)
                    elif self.shop_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                    elif self.shop_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                    elif self.shop_tab == "TITLE" and item['type'] == 'title_style': filtered_items.append(item_id)
                    elif self.shop_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                    elif self.shop_tab == "BADGE" and item['type'] == 'badge': filtered_items.append(item_id)
                    elif self.shop_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)

                for i, item_id in enumerate(filtered_items):
                    item = SHOP_CATALOG[item_id]
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap)
                    y = start_y + row * (card_h + gap)
                    
                    # Clipping
                    if y + card_h < 100 or y > SCREEN_HEIGHT: continue
                    
                    # Animation Hover
                    card_rect = pygame.Rect(x, y, card_w, card_h)
                    mx, my = pygame.mouse.get_pos()
                    target = 1.0 if card_rect.collidepoint(mx, my) else 0.0
                    current = self.card_hover_anims.get(item_id, 0.0)
                    new_val = current + (target - current) * 0.2
                    self.card_hover_anims[item_id] = new_val
                    offset = -10 * new_val
                    self.current_frame_card_offsets[item_id] = offset
                    
                    self.draw_shop_card(x, y + offset, card_w, card_h, item_id, item)

            elif self.state == "MENU_INVENTORY":
                self.draw_text_shadow("INVENTAIRE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 80)
                self.draw_coin_ui(SCREEN_WIDTH - 150, 80, self.coins)
                
                # Grid Config
                cx = SCREEN_WIDTH // 2
                card_w, card_h = 260, 320
                gap = 30
                available_w = SCREEN_WIDTH - 100
                cols = max(1, available_w // (card_w + gap))
                start_x = cx - ((cols * card_w + (cols - 1) * gap) // 2)
                start_y = 220 - self.inventory_scroll
                
                # Filtrage
                owned_items = [item_id for item_id in self.inventory if item_id in SHOP_CATALOG]
                
                filtered_items = []
                for item_id in owned_items:
                    item = SHOP_CATALOG[item_id]
                    if self.inventory_tab == "ALL": filtered_items.append(item_id)
                    elif self.inventory_tab == "BORDER" and item['type'] == 'border': filtered_items.append(item_id)
                    elif self.inventory_tab == "COLOR" and item['type'] == 'name_color': filtered_items.append(item_id)
                    elif self.inventory_tab == "TITLE" and item['type'] == 'title_style': filtered_items.append(item_id)
                    elif self.inventory_tab == "THEME" and item['type'] == 'theme': filtered_items.append(item_id)
                    elif self.inventory_tab == "BADGE" and item['type'] == 'badge': filtered_items.append(item_id)
                    elif self.inventory_tab == "CATEGORY" and item['type'] == 'category': filtered_items.append(item_id)

                if not filtered_items:
                    self.draw_text("Inventaire vide pour cette catégorie.", self.font, (150, 150, 150), cx, 400)
                    self.draw_text("Visitez le magasin !", self.font, (150, 150, 150), cx, 440)

                for i, item_id in enumerate(filtered_items):
                    item = SHOP_CATALOG[item_id]
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_w + gap)
                    y = start_y + row * (card_h + gap)
                    
                    if y + card_h < 100 or y > SCREEN_HEIGHT: continue
                    
                    # Animation Hover (Ajouté pour Inventaire)
                    card_rect = pygame.Rect(x, y, card_w, card_h)
                    mx, my = pygame.mouse.get_pos()
                    target = 1.0 if card_rect.collidepoint(mx, my) else 0.0
                    current = self.card_hover_anims.get(item_id, 0.0)
                    new_val = current + (target - current) * 0.2
                    self.card_hover_anims[item_id] = new_val
                    offset = -10 * new_val
                    
                    self.draw_shop_card(x, y + offset, card_w, card_h, item_id, item)

            elif self.state == "SETUP":
                # Fond du panneau principal
                self.draw_panel(SCREEN_WIDTH//2 - 700, SCREEN_HEIGHT//2 - 420, 1400, 840)
                self.draw_text_shadow("CONFIGURATION", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 350)
                
                cx = SCREEN_WIDTH // 2
                cy = SCREEN_HEIGHT // 2
                card_w, card_h = 400, 180
                gap_x, gap_y = 40, 40
                
                def draw_setup_card(x, y, w, h, title, value, icon=None, subtext=None, color=TEXT_COLOR):
                    rect = pygame.Rect(x - w//2, y - h//2, w, h)
                    pygame.draw.rect(self.screen, (35, 40, 50), rect, border_radius=15)
                    pygame.draw.rect(self.screen, (60, 70, 80), rect, 2, border_radius=15)
                    self.draw_text(title, self.small_bold_font, (150, 150, 160), x, y - h//2 + 25)
                    if icon:
                        self.draw_text(icon, self.ui_emoji_font, color, x, y - 25)
                        self.draw_text_fit(str(value), self.medium_font, color, x, y + 15, w - 140)
                    else:
                        self.draw_text_fit(str(value), self.medium_font, color, x, y + 10, w - 140)
                    if subtext:
                        self.draw_text(subtext, self.font, (100, 100, 100), x, y + h//2 - 25)

                # Row Y positions (reorganized)
                r1_y = cy - 220
                r2_y = cy + 20
                r3_y = cy + 240

                # 1. JOUEURS
                c1_x = cx - card_w // 2 - gap_x // 2
                if self.is_training:
                    icon_diff = "🤖"
                    col_diff = TEXT_COLOR
                    if self.bot_difficulty == "FACILE": col_diff = (100, 255, 100)
                    elif self.bot_difficulty == "DIFFICILE": col_diff = (255, 100, 100)
                    elif self.bot_difficulty == "HARDCORE": col_diff = (255, 0, 0); icon_diff = "☠️"
                    draw_setup_card(c1_x, r1_y, card_w, card_h, "DIFFICULTÉ BOT", self.bot_difficulty, icon=icon_diff, color=col_diff)
                else:
                    p_txt = f"{self.settings['players']}"
                    if not (self.is_local_game or self.is_host): p_txt += " (Hôte)"
                    draw_setup_card(c1_x, r1_y, card_w, card_h, "JOUEURS", p_txt, icon="👥")

                # 2. MODE
                c2_x = cx + card_w // 2 + gap_x // 2
                mode_icon = "🎤" if self.settings['mode'] == 'VOCAL' else "⌨️"
                mode_val = "VOCAL" if self.settings['mode'] == 'VOCAL' else "ÉCRIT"
                draw_setup_card(c2_x, r1_y, card_w, card_h, "MODE DE JEU", mode_val, icon=mode_icon)

                # 3. TEMPS
                c3_x = cx - card_w // 2 - gap_x // 2
                draw_setup_card(c3_x, r2_y, card_w, card_h, "TEMPS / TOUR", f"{self.settings['time']}s", icon="TIME")
                draw_setup_card(c3_x, r2_y, card_w, card_h, "TEMPS / TOUR", f"{self.settings['time']}s", icon="⏱️")

                # 4. TYPE DE JEU
                c4_x = cx + card_w // 2 + gap_x // 2
                gtype = self.settings.get('game_type', 'NORMAL')
                type_info = {
                    'NORMAL': ("🙂", "Classique", TEXT_COLOR),
                    'SURVIVAL': ("⏳", "Temps réduit", ALERT_COLOR),
                    'SPEED': ("⚡", "3 secondes !", (255, 255, 0)),
                    'HARDCORE': ("☠️", "4s + Danger", (255, 50, 50)),
                    'CHAOS': ("🎲", "Temps aléatoire", (200, 50, 255)),
                    'TIME_TRIAL': ("⏱️", "60s Global", (0, 255, 255))
                }
                icon, sub, col = type_info.get(gtype, ("WIZZ", "", TEXT_COLOR))
                icon, sub, col = type_info.get(gtype, ("❓", "", TEXT_COLOR))
                draw_setup_card(c4_x, r2_y, card_w, card_h, "TYPE DE PARTIE", gtype, icon=icon, subtext=sub, color=col)

                # 5. CATÉGORIE (Large)
                cat_rect = pygame.Rect(cx - 420, r3_y - 65, 840, 130)
                pygame.draw.rect(self.screen, (35, 40, 50), cat_rect, border_radius=15)
                pygame.draw.rect(self.screen, ACCENT_COLOR, cat_rect, 2, border_radius=15)
                self.draw_text("CATÉGORIE", self.small_bold_font, (150, 150, 160), cx, r3_y - 40)
                
                # Affichage Verrouillé si non possédé
                is_locked = self.settings['category'] not in self.all_categories
                if is_locked:
                    self.draw_text(self.settings['category'], self.big_font, (120, 120, 130), cx, r3_y + 10)
                    
                    # Fix: Affichage séparé du cadenas (Emoji) pour éviter le carré blanc
                    lock_surf = self.ui_emoji_font.render("🔒", True, (200, 100, 100))
                    text_surf = self.small_bold_font.render("ACHETER DANS LE MAGASIN", True, (200, 100, 100))
                    total_w = lock_surf.get_width() + 10 + text_surf.get_width()
                    start_x = cx - total_w // 2
                    self.screen.blit(lock_surf, lock_surf.get_rect(midleft=(start_x, r3_y + 50)))
                    self.screen.blit(text_surf, text_surf.get_rect(midleft=(start_x + lock_surf.get_width() + 10, r3_y + 50)))
                else:
                    self.draw_text(self.settings['category'], self.big_font, ACCENT_COLOR, cx, r3_y + 18)

            elif self.state == "CONFIRM_QUIT":
                # Fond sombre
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 200))
                self.screen.blit(s, (0, 0))
                
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                w, h = 600, 300
                self.draw_panel(cx - w//2, cy - h//2, w, h)
                
                self.draw_text_shadow("CONFIRMATION", self.big_font, ALERT_COLOR, cx, cy - 80)
                self.draw_text("Voulez-vous vraiment quitter ?", self.font, TEXT_COLOR, cx, cy - 10)

            elif self.state == "PAUSED":
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                self.draw_panel(cx - 200, cy - 150, 400, 300)
                self.draw_text_shadow("PAUSE", self.big_font, ACCENT_COLOR, cx, cy - 80)

            elif self.state == "CONFIRM_LEAVE":
                # Fond sombre
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 200))
                self.screen.blit(s, (0, 0))
                
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                w, h = 600, 300
                self.draw_panel(cx - w//2, cy - h//2, w, h)
                
                self.draw_text_shadow("QUITTER LA PARTIE", self.big_font, ALERT_COLOR, cx, cy - 80)
                self.draw_text("Voulez-vous vraiment quitter la partie ?", self.font, TEXT_COLOR, cx, cy - 10)

            elif self.state == "SETTINGS" or self.state == "CONTROLS":
                self.draw_panel(SCREEN_WIDTH//2 - 550, SCREEN_HEIGHT//2 - 350, 1100, 750)
                title = "PARAMÈTRES" if self.state == "SETTINGS" else "TOUCHES"
                self.draw_text_shadow(title, self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 290)
                
                if self.state == "SETTINGS":
                    # Headers de colonnes
                    cx = SCREEN_WIDTH // 2
                    cy = SCREEN_HEIGHT // 2
                    col_w = 400
                    gap = 40
                    total_w = col_w * 2 + gap
                    start_x = cx - total_w // 2
                    c1_x = start_x + col_w // 2
                    c2_x = start_x + col_w + gap + col_w // 2
                    start_y = cy - 150
                    
                    self.draw_text("PRÉFÉRENCES", self.small_bold_font, (150, 150, 150), c1_x, start_y - 40)
                    self.draw_text("DONNÉES", self.small_bold_font, (150, 150, 150), c2_x, start_y - 40)

                if self.state == "CONTROLS":
                    self.draw_text("Cliquez pour changer", self.font, (150, 150, 150), SCREEN_WIDTH//2, 300)

                # Feedback Import/Export
                if self.feedback_msg and pygame.time.get_ticks() - self.feedback_timer < 3000:
                    self.draw_text_shadow(self.feedback_msg, self.font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)
                else:
                    if self.state != "GAME": self.feedback_msg = ""

            elif self.state == "HOW_TO":
                self.draw_panel(SCREEN_WIDTH//2 - 500, 100, 1000, 700)
                self.draw_text_shadow("COMMENT JOUER", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                
                # --- NOUVEAU DESIGN HOW TO ---
                cx = SCREEN_WIDTH // 2
                start_y = 220
                
                # Carte 1: But du jeu
                self.draw_text("🎯", self.ui_emoji_font, ACCENT_COLOR, cx - 250 - 160, start_y - 5)
                self.draw_text("BUT DU JEU", self.medium_font, ACCENT_COLOR, cx - 250, start_y)
                self.draw_text("Trouvez un mot en lien avec le précédent", self.font, TEXT_COLOR, cx - 250, start_y + 40)
                self.draw_text("avant la fin du chrono !", self.font, TEXT_COLOR, cx - 250, start_y + 70)
                
                # Carte 2: Contrôles
                self.draw_text("⌨️", self.ui_emoji_font, ACCENT_COLOR, cx + 250 - 160, start_y - 5)
                self.draw_text("CONTRÔLES", self.medium_font, ACCENT_COLOR, cx + 250, start_y)
                self.draw_text("ENTRÉE : Valider le mot", self.font, TEXT_COLOR, cx + 250, start_y + 40)
                self.draw_text("MAJ / TAB : Contester un mot", self.font, TEXT_COLOR, cx + 250, start_y + 70)
                self.draw_text("CTRL + B : Wizz (Secousse)", self.font, TEXT_COLOR, cx + 250, start_y + 100)
                
                # Carte 3: Modes
                self.draw_text("🎮", self.ui_emoji_font, ACCENT_COLOR, cx - 250 - 180, start_y + 180 - 5)
                self.draw_text("MODES DE JEU", self.medium_font, ACCENT_COLOR, cx - 250, start_y + 180)
                self.draw_text("• NORMAL / SPEED : Classique ou 3s", self.font, TEXT_COLOR, cx - 250, start_y + 220)
                self.draw_text("• SURVIE / HARDCORE : Pression max", self.font, TEXT_COLOR, cx - 250, start_y + 250)
                self.draw_text("• TIME TRIAL / CHAOS : 60s ou Aléatoire", self.font, TEXT_COLOR, cx - 250, start_y + 280)
                
                # Carte 4: Astuces
                self.draw_text("💡", self.ui_emoji_font, ACCENT_COLOR, cx + 250 - 140, start_y + 180 - 5)
                self.draw_text("ASTUCES", self.medium_font, ACCENT_COLOR, cx + 250, start_y + 180)
                self.draw_text("• COMBO : Répondez vite (<2.5s)", self.font, TEXT_COLOR, cx + 250, start_y + 220)
                
                # Fix Gel Square (Affichage composite)
                gel_y = start_y + 250
                start_gel_x = cx + 250 - 130
                self.draw_text("• GEL (", self.font, TEXT_COLOR, start_gel_x, gel_y, center=False)
                self.draw_text("❄️", self.ui_emoji_font, TEXT_COLOR, start_gel_x + 95, gel_y - 2, center=False)
                self.draw_text(") : Fige le temps 5s", self.font, TEXT_COLOR, start_gel_x + 135, gel_y, center=False)
                
                self.draw_text("• SAISON 1 : Montez les niveaux !", self.font, TEXT_COLOR, start_gel_x, start_y + 285, center=False)
                self.draw_text("• DÉFI : +300$ chaque jour !", self.font, TEXT_COLOR, start_gel_x, start_y + 315, center=False)
            
            elif self.state.startswith("MENU"):
                # Titre stylisé pour les menus principaux
                # Animation Vague (Lettre par lettre)
                title_text = "WORLD RUSH"
                total_w = 0
                surfs = []
                
                # Style de titre équipé
                t_style = self.equipped.get('title_style', 'title_default')
                
                for i, ch in enumerate(title_text):
                    c = ACCENT_COLOR
                    if t_style == "title_rainbow":
                        hue = (pygame.time.get_ticks() // 10 + i * 20) % 360
                        c = pygame.Color(0); c.hsla = (hue, 100, 50, 100)
                    elif t_style == "title_gold":
                        c = (255, 215, 0)
                    elif t_style == "title_fire":
                        c = (255, random.randint(50, 150), 0)
                    elif t_style == "title_neon":
                        c = (0, 255, 255)
                    elif t_style == "title_matrix":
                        c = (0, 255, 0) if random.random() > 0.1 else (200, 255, 200)
                    elif t_style == "title_ice":
                        c = (150, 220, 255)
                    elif t_style == "title_void":
                        c = (50, 0, 100)

                    s = self.title_font.render(ch, True, c)
                    surfs.append(s)
                    total_w += s.get_width() + 5
                
                start_x = (SCREEN_WIDTH - total_w) // 2
                curr_x = start_x
                t = pygame.time.get_ticks()
                
                for i, s in enumerate(surfs):
                    offset_y = math.sin((t * 0.005) + (i * 0.5)) * 10
                    
                    # Effet Glitch aléatoire sur le titre (Plus fréquent si style Matrix/Glitch)
                    draw_pos = (curr_x, 120 + offset_y)
                    glitch_chance = 50 if t_style == "title_matrix" else 200
                    if random.randint(0, glitch_chance) == 0:
                        glitch_off = random.randint(-5, 5)
                        self.screen.blit(s, (curr_x + glitch_off, 120 + offset_y))
                    else:
                        self.screen.blit(s, draw_pos)
                        
                    curr_x += s.get_width() + 5

                self.draw_text("Association d'idées rapide", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 260)
                
                # Barre d'XP (Menu Principal)
                if self.state == "MENU_MAIN":
                    xp_x, xp_y = 20, 20
                    xp_w, xp_h = 200, 20
                    # Affichage Pièces Menu Principal (Déplacé pour éviter le carré/chevauchement)
                    self.draw_coin_ui(SCREEN_WIDTH - 150, 30, self.coins)
                    
                    self.draw_text(f"Niveau {self.level}", self.font, ACCENT_COLOR, xp_x + xp_w//2, xp_y + 30)
                    threshold = self.get_xp_threshold(self.level)
                    ratio = min(1.0, self.xp / threshold)
                    pygame.draw.rect(self.screen, (30, 35, 45), (xp_x, xp_y, xp_w, xp_h), border_radius=10)
                    pygame.draw.rect(self.screen, (0, 200, 150), (xp_x, xp_y, int(xp_w * ratio), xp_h), border_radius=10)
                    pygame.draw.rect(self.screen, (100, 100, 100), (xp_x, xp_y, xp_w, xp_h), 2, border_radius=10)
                    
                    # (Supprimé) Affichage Victoires/Parties
                    
                    # Indicateur UPnP (Sous la barre d'XP)
                    upnp_col = (255, 50, 50) # Rouge (Échec/Erreur)
                    is_success = "SUCCÈS" in self.upnp_status
                    is_searching = "Recherche" in self.upnp_status or "Tentative" in self.upnp_status
                    
                    if is_success: upnp_col = (50, 255, 50) # Vert
                    elif is_searching: upnp_col = (255, 200, 0) # Orange
                    
                    cx, cy = 30, 130
                    
                    # Clignotement si recherche
                    alpha_mult = 1.0
                    if is_searching:
                        alpha_mult = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2 * 0.6 + 0.4

                    # Lueur (Glow)
                    s_glow = pygame.Surface((40, 40), pygame.SRCALPHA)
                    glow_alpha = int(80 * alpha_mult)
                    pygame.draw.circle(s_glow, (*upnp_col, glow_alpha), (20, 20), 12)
                    self.screen.blit(s_glow, (cx - 20, cy - 20))
                    
                    # Point principal + Reflet
                    draw_col = upnp_col
                    if is_searching:
                         draw_col = (int(upnp_col[0]*alpha_mult), int(upnp_col[1]*alpha_mult), int(upnp_col[2]*alpha_mult))
                    
                    pygame.draw.circle(self.screen, draw_col, (cx, cy), 6)
                    pygame.draw.circle(self.screen, (255, 255, 255), (cx - 2, cy - 2), 2)
                    
                    # Texte seulement si pas succès (Orange/Rouge/Désactivé)
                    if not is_success:
                        self.draw_text(f"Réseau: {self.upnp_status}", self.small_bold_font, (150, 150, 150), cx + 20, cy, center=False)
                    
                    # Tooltip au survol (Vert)
                    mx, my = pygame.mouse.get_pos()
                    
                    # Maintien du tooltip si survol du point ou de l'info-bulle entière
                    is_hovering_tooltip = self.tooltip_rect and self.tooltip_rect.collidepoint(mx, my)
                    should_show = is_success and (math.hypot(mx - cx, my - cy) < 25 or is_hovering_tooltip)
                    
                    self.refresh_btn_rect = None # Reset zone clic
                    self.tooltip_rect = None

                    if should_show:
                        ip_txt = self.public_ip if self.public_ip else "IP Inconnue"
                        if self.external_port != DEFAULT_PORT:
                            ip_txt += f":{self.external_port}"
                        
                        # Surfaces
                        tip_surf = self.small_bold_font.render(f"IP Publique: {ip_txt}", True, (235, 235, 235))
                        ref_surf = self.ui_emoji_font.render("↻", True, (200, 200, 200))
                        
                        pad = 10
                        w = tip_surf.get_width() + ref_surf.get_width() + pad * 3
                        h = max(tip_surf.get_height(), ref_surf.get_height()) + pad
                        
                        tip_x = cx + 20
                        tip_y = cy - 15
                        
                        # Fond tooltip
                        bg_rect = pygame.Rect(tip_x, tip_y, w, h)
                        self.tooltip_rect = bg_rect.inflate(20, 20) # Zone de maintien agrandie
                        pygame.draw.rect(self.screen, (25, 30, 40), bg_rect, border_radius=8)
                        pygame.draw.rect(self.screen, (90, 110, 130), bg_rect, 1, border_radius=8)
                        
                        self.screen.blit(tip_surf, (tip_x + pad, tip_y + pad//2))
                        ref_rect = ref_surf.get_rect(topleft=(tip_x + pad + tip_surf.get_width() + pad, tip_y + pad//2 - 2))
                        self.screen.blit(ref_surf, ref_rect)
                        self.refresh_btn_rect = ref_rect.inflate(10, 10)

            elif self.state == "LOBBY":
                # --- INTERFACE LOBBY ---
                # Fond global unifié
                lobby_bg = pygame.Rect(30, 30, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60)
                self.draw_panel(lobby_bg.x, lobby_bg.y, lobby_bg.w, lobby_bg.h)
                
                # Header
                header_h = 130
                header_rect = pygame.Rect(lobby_bg.x, lobby_bg.y, lobby_bg.w, header_h)
                pygame.draw.rect(self.screen, (20, 23, 30), header_rect, border_top_left_radius=15, border_top_right_radius=15)
                pygame.draw.line(self.screen, (50, 60, 70), (header_rect.left, header_rect.bottom), (header_rect.right, header_rect.bottom), 2)
                
                self.draw_text_shadow("SALON D'ATTENTE", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, header_rect.y + 45)
                
                # Affichage de l'IP de l'hôte pour la partager
                if self.is_host:
                    # IP Locale
                    local_txt = f"Local: {self.local_ip}"
                    if self.server_port != DEFAULT_PORT:
                        local_txt += f":{self.server_port}"
                    
                    # IP Publique
                    public_txt = f"Online: {self.public_ip}" if self.public_ip else "Online: ..."
                    if self.public_ip and self.external_port != DEFAULT_PORT:
                        public_txt += f":{self.external_port}"

                    ip_txt = f"{local_txt}   |   {public_txt}"
                    
                    # Style "Pilule" pour l'IP
                    ip_surf = self.small_bold_font.render(ip_txt, True, (200, 200, 200))
                    pill_rect = pygame.Rect(0, 0, ip_surf.get_width() + 40, 34)
                    pill_rect.center = (SCREEN_WIDTH // 2, header_rect.y + 95)
                    pygame.draw.rect(self.screen, (40, 45, 55), pill_rect, border_radius=17)
                    pygame.draw.rect(self.screen, (80, 90, 100), pill_rect, 1, border_radius=17)
                    self.screen.blit(ip_surf, ip_surf.get_rect(center=pill_rect.center))
                
                # Zone Gauche : Joueurs
                left_panel = pygame.Rect(50, 170, 600, 650)
                self.lobby_player_rects.clear()
                start_y = left_panel.y + 20
                card_h = 110
                gap = 15
                mx, my = pygame.mouse.get_pos()
                hover_badge_name = None

                for i in range(self.settings['players']):
                    y_pos = start_y + i * (card_h + gap)
                    card_rect = pygame.Rect(left_panel.x + 20, y_pos, left_panel.w - 40, card_h)
                    self.lobby_player_rects[i] = card_rect

                    # Highlight on hover or if selected
                    is_hover = card_rect.collidepoint(mx, my) or self.selected_lobby_player_id == i

                    # Données par défaut
                    p_name = None
                    p_status = "..."
                    p_col = (150, 150, 150)
                    p_av = "⚡"
                    p_border = "border_default"
                    p_level = 1
                    p_ping = 0
                    p_ip = None
                    p_badge = "badge_default"
                    p_streak = 0
                    
                    # Remplissage données réelles
                    if self.is_local_game:
                        p_name = f"Joueur {i+1}"
                        p_name_color = "name_color_default"
                        if i == 0:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']; p_level = self.level; p_badge = self.equipped['badge']
                        else:
                            p_av = AVATARS[i % len(AVATARS)]
                        
                        if i < len(self.ready_status):
                            p_status = "PRÊT" if self.ready_status[i] else "PAS PRÊT"
                            p_col = (100, 255, 100) if self.ready_status[i] else (255, 100, 100)

                    elif self.is_host:
                        if i == 0:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']; p_level = self.level; p_badge = self.equipped['badge']; p_streak = self.stats.get('win_streak', 0)
                            ready_val = self.ready_status[0] if len(self.ready_status) > 0 else False
                            p_status = "PRÊT" if ready_val else "PAS PRÊT"
                            p_col = (100, 255, 100) if ready_val else (255, 100, 100)
                        elif i - 1 < len(self.clients):
                            c = self.clients[i - 1]
                            p_name = c['name']; p_av = c['avatar']; p_border = c['border']; p_name_color = c.get('name_color', 'name_color_default'); p_level = c.get('level', 1); p_ping = c.get('ping', 0); p_badge = c.get('badge', 'badge_default'); p_streak = c.get('streak', 0)
                            p_ip = c.get('ip')
                            p_status = "PRÊT" if c['ready'] else "PAS PRÊT"
                            p_col = (100, 255, 100) if c['ready'] else (255, 100, 100)
                        elif self.test_mode and i == 1:
                            p_name = "Bot (Dev)"; p_av = "🤖"; p_border = "border_neon"; p_level = 99; p_badge = "badge_dev"; p_streak = 99
                            ready_val = self.ready_status[1] if len(self.ready_status) > 1 else False
                            p_status = "PRÊT" if ready_val else "PAS PRÊT"
                            p_col = (100, 255, 100) if ready_val else (255, 100, 100)
                            
                    else: # Client
                        if i in self.lobby_cache:
                            d = self.lobby_cache[i]
                            p_name = d['name']; p_av = d['avatar']; p_border = d['border']; p_name_color = d.get('name_color', 'name_color_default'); p_level = d.get('level', 1); p_ping = d.get('ping', 0); p_badge = d.get('badge', 'badge_default'); p_streak = d.get('streak', 0)
                            p_status = "PRÊT" if d['ready'] else "PAS PRÊT"
                            p_col = (100, 255, 100) if d['ready'] else (255, 100, 100)
                        elif i == self.my_id:
                            p_name = self.username; p_av = self.avatar; p_border = self.equipped['border']; p_name_color = self.equipped['name_color']; p_level = self.level; p_badge = self.equipped['badge']; p_streak = self.stats.get('win_streak', 0)
                            ready_status_i = self.ready_status[i] if i < len(self.ready_status) else False
                            p_status = "PRÊT" if ready_status_i else "PAS PRÊT"
                            p_col = (100, 255, 100) if ready_status_i else (255, 100, 100)
                    
                    # Si emplacement vide
                    if p_name is None:
                        pygame.draw.rect(self.screen, (30, 30, 35), card_rect, border_radius=15)
                        # Effet pointillés
                        pygame.draw.rect(self.screen, (60, 60, 70), card_rect, 2, border_radius=15)
                        self.draw_text("En attente...", self.font, (100, 100, 100), card_rect.centerx, card_rect.centery)
                        continue

                    # Si joueur présent
                    # Couleur de fond par défaut
                    bg_col = (35, 40, 45)
                    
                    # Animation de pulsation (Couleur + Taille)
                    pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1) * 0.5
                    
                    # Couleur bordure dynamique
                    r = int(50 + (100 * pulse))
                    g = int(200 + (55 * pulse))
                    b = int(50 + (100 * pulse))
                    border_col = (r, g, b)
                    
                    # Légère inflation
                    inflation = int(3 * pulse)
                    draw_rect = card_rect.inflate(inflation, inflation)
                    
                    if is_hover:
                        bg_col = tuple(min(255, c + 20) for c in bg_col)
                    
                    pygame.draw.rect(self.screen, bg_col, draw_rect, border_radius=15)
                    pygame.draw.rect(self.screen, border_col, draw_rect, 2, border_radius=15)
                    
                    # Avatar
                    # Vérifier si ce joueur est en combo (pour l'effet de feu dans le lobby, optionnel, ici désactivé)
                    # Mais on utilise draw_avatar pour la cohérence
                    self.draw_avatar(p_av, draw_rect.x + 60, draw_rect.centery, 35, p_border, is_combo=False)

                    # Animation de chargement circulaire si pas prêt
                    if p_status != "PRÊT":
                        spin_angle = (pygame.time.get_ticks() // 3) % 360
                        arc_rect = pygame.Rect(0, 0, 80, 80)
                        arc_rect.center = (draw_rect.x + 60, draw_rect.centery)
                        # Dessiner 2 arcs pour l'effet
                        pygame.draw.arc(self.screen, (255, 200, 0), arc_rect, math.radians(spin_angle), math.radians(spin_angle + 90), 3)
                        pygame.draw.arc(self.screen, (255, 200, 0), arc_rect, math.radians(spin_angle + 180), math.radians(spin_angle + 270), 3)
                    
                    # Name & Level
                    name_col = self.get_name_color(p_name_color)
                    self.draw_text(p_name, self.medium_font, name_col, draw_rect.x + 120, draw_rect.centery - 20, center=False)
                    
                    # Badge (A côté du nom)
                    if p_badge != "badge_default":
                        name_w = self.medium_font.size(p_name)[0]
                        badge_rect = self.draw_badge(p_badge, draw_rect.x + 120 + name_w + 25, draw_rect.centery - 20)
                        if badge_rect and badge_rect.collidepoint(mx, my):
                            hover_badge_name = SHOP_CATALOG.get(p_badge, {}).get("name", "Badge")

                    level_txt = f"Niveau {p_level}"
                    if self.is_host and p_ip and p_ip != "local":
                        level_txt += f" | IP: {p_ip}"
                    self.draw_text(level_txt, self.small_bold_font, (150, 150, 150), draw_rect.x + 120, draw_rect.centery + 20, center=False)
                    
                    # Host Badge
                    if i == 0:
                        self.draw_text("👑", self.ui_emoji_font, (255, 215, 0), draw_rect.right - 30, draw_rect.top + 15)
                    
                    # Ping (si en ligne)
                    if not self.is_local_game and i > 0:
                        ping_col = (0, 255, 0) if p_ping < 100 else ((255, 255, 0) if p_ping < 200 else (255, 0, 0))
                        ping_txt = f"{p_ping}ms"
                        # Dessiner des barres de signal
                        self.draw_text(ping_txt, self.small_bold_font, ping_col, draw_rect.right - 30, draw_rect.bottom - 20)

                    # Ready Status Text
                    stat_col = (100, 255, 100) if p_status == "PRÊT" else (100, 100, 100)
                    if p_status == "PRÊT":
                         self.draw_text_shadow(p_status, self.small_bold_font, stat_col, draw_rect.right - 160, draw_rect.centery)
                    else:
                         self.draw_text(p_status, self.small_bold_font, stat_col, draw_rect.right - 160, draw_rect.centery)
                
                # VS Logo (Si 2 joueurs)
                if self.settings['players'] == 2:
                    vs_y = start_y + card_h + gap // 2
                    cx = left_panel.centerx
                    
                    # Ligne de connexion arrière
                    pygame.draw.line(self.screen, (60, 70, 80), (cx, start_y + card_h), (cx, start_y + card_h + gap), 4)
                    
                    # Losange stylisé Pro
                    sz = 40
                    pts = [(cx, vs_y - sz), (cx + sz + 10, vs_y), (cx, vs_y + sz), (cx - sz - 10, vs_y)]
                    
                    # Ombre portée
                    shadow_pts = [(p[0]+4, p[1]+4) for p in pts]
                    pygame.draw.polygon(self.screen, (0, 0, 0, 100), shadow_pts)
                    
                    pygame.draw.polygon(self.screen, (30, 35, 45), pts) # Fond sombre
                    pygame.draw.polygon(self.screen, (255, 60, 60), pts, 3) # Bordure rouge vif
                    self.draw_text("VS", self.big_font, (255, 255, 255), cx, vs_y + 2)

                # Zone Droite : Chat
                chat_x = 680 # Décalage suite agrandissement gauche
                chat_y = 170
                chat_w = SCREEN_WIDTH - chat_x - 50
                chat_h = SCREEN_HEIGHT - chat_y - 50
                chat_panel = pygame.Rect(chat_x, chat_y, chat_w, chat_h)
                pygame.draw.rect(self.screen, (25, 30, 40, 100), chat_panel, border_radius=15)
                pygame.draw.rect(self.screen, (60, 70, 90), chat_panel, 1, border_radius=15)
                self.draw_text("CHAT", self.font, ACCENT_COLOR, chat_panel.centerx, chat_panel.y + 30)

                # --- Player Profile Popup ---
                if self.selected_lobby_player_id is not None:
                    p_data = self.get_player_data_by_id(self.selected_lobby_player_id)
                    if p_data:
                        # Darken background (only over the left panel)
                        s = pygame.Surface((left_panel.w, left_panel.h), pygame.SRCALPHA)
                        s.fill((0, 0, 0, 180))
                        self.screen.blit(s, (left_panel.x, left_panel.y))

                        popup_cx, popup_cy = left_panel.centerx, 400
                        popup_w, popup_h = 580, 350
                        self.draw_panel(popup_cx - popup_w//2, popup_cy - popup_h//2, popup_w, popup_h)

                        # Player info
                        self.draw_avatar(p_data.get('avatar', '⚡'), popup_cx, popup_cy - 110, 50, p_data.get('border', 'border_default'))
                        
                        name = p_data.get('name', '...')
                        name_col = self.get_name_color(p_data.get('name_color', 'name_color_default'))
                        self.draw_text(name, self.medium_font, name_col, popup_cx, popup_cy - 40)
                        badge_id = p_data.get('badge', 'badge_default')
                        if badge_id != 'badge_default':
                            name_w = self.medium_font.size(name)[0]
                            popup_badge_rect = self.draw_badge(badge_id, popup_cx + name_w // 2 + 30, popup_cy - 40)
                            if popup_badge_rect and popup_badge_rect.collidepoint(mx, my):
                                hover_badge_name = SHOP_CATALOG.get(badge_id, {}).get("name", "Badge")
                            
                        self.draw_text(f"Niveau {p_data.get('level', 1)}", self.font, ACCENT_COLOR, popup_cx, popup_cy - 5)
                        
                        # Affichage du Titre
                        p_title = self.get_player_title(p_data.get('level', 1))
                        self.draw_text(p_title, self.small_bold_font, (255, 215, 0), popup_cx, popup_cy + 20)

                        # Equipped items
                        self.draw_text("Équipement", self.small_bold_font, (150, 150, 150), popup_cx, popup_cy + 55)
                        
                        # Border
                        border_id = p_data.get('border', 'border_default')
                        border_item = SHOP_CATALOG.get(border_id, {"name": "Défaut"})
                        self.draw_text(f"Bordure: {border_item.get('name', 'Défaut')}", self.font, TEXT_COLOR, popup_cx - 150, popup_cy + 85, center=False)
                        
                        # Theme
                        theme_id = p_data.get('theme', 'theme_default')
                        theme_item = SHOP_CATALOG.get(theme_id, {"name": "Défaut"})
                        self.draw_text(f"Thème: {theme_item.get('name', 'Défaut')}", self.font, TEXT_COLOR, popup_cx - 150, popup_cy + 110, center=False)
                    else:
                        self.selected_lobby_player_id = None

                if hover_badge_name:
                    tip_surf = self.small_bold_font.render(hover_badge_name, True, (235, 235, 235))
                    tip_rect = tip_surf.get_rect()
                    tip_rect.width += 24
                    tip_rect.height += 12
                    tip_rect.midbottom = (mx, my - 10)
                    tip_rect.x = max(38, min(tip_rect.x, SCREEN_WIDTH - tip_rect.width - 38))
                    tip_rect.y = max(38, min(tip_rect.y, SCREEN_HEIGHT - tip_rect.height - 38))
                    pygame.draw.rect(self.screen, (25, 30, 40), tip_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (90, 110, 130), tip_rect, 1, border_radius=10)
                    self.screen.blit(tip_surf, tip_surf.get_rect(center=tip_rect.center))

                
                # Messages (avec Scroll)
                input_h = 60
                header_h = 60
                msg_area_y = chat_panel.y + header_h
                msg_area_h = chat_panel.h - header_h - input_h - 60 # Espace pour emotes
                line_h = 40
                max_lines = msg_area_h // line_h
                
                total_msgs = len(self.chat_messages)
                if total_msgs <= max_lines:
                    self.chat_scroll = 0
                    visible_msgs = self.chat_messages
                else:
                    max_scroll = total_msgs - max_lines
                    if self.chat_scroll > max_scroll: self.chat_scroll = max_scroll
                    start = total_msgs - max_lines - self.chat_scroll
                    end = total_msgs - self.chat_scroll
                    visible_msgs = self.chat_messages[start:end]

                # Clipping for chat messages
                chat_clip_rect = pygame.Rect(chat_panel.x, msg_area_y, chat_panel.w, msg_area_h)
                self.screen.set_clip(chat_clip_rect)

                for i, msg in enumerate(visible_msgs):
                    col = (255, 200, 0) if msg.startswith("SYSTEM") else TEXT_COLOR
                    self.draw_text(msg, self.ui_emoji_font, col, chat_panel.x + 20, msg_area_y + i * line_h, center=False)
                
                self.screen.set_clip(None) # Reset clipping

                # Input Chat
                input_rect = pygame.Rect(chat_panel.x + 20, chat_panel.bottom - 60, chat_panel.w - 90, 50)
                self.draw_fancy_input_box(input_rect, self.chat_input, "Écrivez ici...", active=True, font=self.font, center_text=False)

                # Visualisation Cooldown Wizz
                now = pygame.time.get_ticks()
                if now - self.last_wizz_time < 5000:
                    # Position du bouton Wizz (calculée comme dans update_lobby_buttons)
                    wizz_x = chat_x + chat_w - 60
                    wizz_y = SCREEN_HEIGHT - 50 - 55
                    
                    # Overlay sombre
                    s_cd = pygame.Surface((50, 50), pygame.SRCALPHA)
                    pygame.draw.circle(s_cd, (0, 0, 0, 150), (25, 25), 25)
                    self.screen.blit(s_cd, (wizz_x, wizz_y))
                    
                    rem = math.ceil((5000 - (now - self.last_wizz_time)) / 1000)
                    self.draw_text(str(rem), self.small_bold_font, (255, 255, 255), wizz_x + 25, wizz_y + 25)

            elif self.state == "LOCAL_NAMES":
                self.draw_panel(SCREEN_WIDTH//2 - 400, 100, 800, 600)
                self.draw_text_shadow("NOMS DES JOUEURS", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, 150)
                
                start_y = 250
                for i in range(self.settings['players']):
                    y = start_y + i * 90
                    self.draw_text(f"Joueur {i+1}", self.small_bold_font, (150, 150, 150), SCREEN_WIDTH//2 - 200, y)
                    
                    # Input Box simulée (juste affichage pour l'instant, on pourrait rendre éditable)
                    rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y - 20, 300, 50)
                    name = self.local_player_names[i]
                    is_active = (i == self.active_local_name_idx)
                    
                    # Highlight active input (simple logic for now: all active or specific one)
                    # Pour simplifier, on affiche juste les noms générés/édités
                    self.draw_fancy_input_box(rect, name, "", active=is_active, font=self.font)
                
                self.draw_text("Cliquez pour modifier les noms.", self.font, (100, 100, 100), SCREEN_WIDTH//2, 550)

            elif self.state == "MENU_SPIN":
                # Nouveau design complet de la roue de la chance
                for y in range(SCREEN_HEIGHT):
                    t = y / max(1, SCREEN_HEIGHT - 1)
                    c = self.interpolate_color((8, 14, 28), (24, 16, 42), t)
                    pygame.draw.line(self.screen, c, (0, y), (SCREEN_WIDTH, y))

                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20
                radius = min(250, SCREEN_WIDTH // 3, max(140, SCREEN_HEIGHT // 2 - 190))

                # Ambiance lumineuse
                aura = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(aura, (255, 160, 60, 35), (radius * 2, radius * 2), int(radius * 1.6))
                pygame.draw.circle(aura, (80, 190, 255, 25), (radius * 2, radius * 2), int(radius * 1.2))
                self.screen.blit(aura, (cx - radius * 2, cy - radius * 2))

                # Carte titre
                title_rect = pygame.Rect(cx - 430, 30, 860, 120)
                pygame.draw.rect(self.screen, (20, 26, 44), title_rect, border_radius=18)
                pygame.draw.rect(self.screen, (255, 150, 55), title_rect, 2, border_radius=18)
                self.draw_text_shadow("ROUE DE LA CHANCE", self.title_font, (255, 214, 120), cx, 72)
                self.draw_text("1 tirage gratuit par jour - gains instantanes", self.font, (190, 205, 225), cx, 118)

                if not hasattr(self, 'wheel_segments') or not self.wheel_segments:
                    self.wheel_segments = ["50", "100", "200", "500", "1000", "JACKPOT", "ITEM", "25"]
                if not hasattr(self, 'wheel_colors') or not self.wheel_colors:
                    self.wheel_colors = [(220, 60, 60), (70, 180, 80), (65, 110, 220), (230, 180, 60), (190, 70, 190), (255, 210, 70), (40, 190, 200), (130, 130, 130)]

                # Logique rotation
                if self.wheel_spinning:
                    self.wheel_angle += self.wheel_velocity
                    self.wheel_velocity *= 0.988
                    if self.wheel_velocity < 0.11:
                        self.wheel_velocity = 0
                        self.wheel_spinning = False
                        seg_angle = 360 / len(self.wheel_segments)
                        norm_angle = (self.wheel_angle + 90) % 360
                        idx = int(((360 - norm_angle) % 360) / seg_angle)
                        self.spin_result = self.wheel_segments[idx]
                        self.claim_spin_reward(self.spin_result)
                        self.play_sound("success")
                        for _ in range(65):
                            self.add_particles(cx, cy - radius, (255, 190, 90))

                # Anneaux extérieurs
                pygame.draw.circle(self.screen, (255, 175, 70), (cx, cy), radius + 30)
                pygame.draw.circle(self.screen, (26, 30, 44), (cx, cy), radius + 22)
                pygame.draw.circle(self.screen, (255, 220, 120), (cx, cy), radius + 18, 2)
                pygame.draw.circle(self.screen, (38, 44, 60), (cx, cy), radius + 8)

                # Segments
                num_seg = len(self.wheel_segments)
                seg_angle = 360 / num_seg
                for i in range(num_seg):
                    start_a = self.wheel_angle + i * seg_angle
                    end_a = start_a + seg_angle
                    rad_start = math.radians(start_a)
                    rad_end = math.radians(end_a)

                    p1 = (cx, cy)
                    p2 = (cx + math.cos(rad_start) * radius, cy + math.sin(rad_start) * radius)
                    p3 = (cx + math.cos(rad_end) * radius, cy + math.sin(rad_end) * radius)
                    col = self.wheel_colors[i % len(self.wheel_colors)]
                    pygame.draw.polygon(self.screen, col, [p1, p2, p3])
                    pygame.draw.line(self.screen, (255, 245, 220), p1, p2, 2)

                    # Texte horizontal, plus lisible que la version tournée
                    mid_a = math.radians(start_a + seg_angle / 2)
                    tx = cx + math.cos(mid_a) * (radius * 0.70)
                    ty = cy + math.sin(mid_a) * (radius * 0.70)
                    txt = self.small_bold_font.render(self.wheel_segments[i], True, (255, 255, 255))
                    txt_bg = txt.get_rect(center=(tx, ty)).inflate(16, 8)
                    pygame.draw.rect(self.screen, (0, 0, 0, 120), txt_bg, border_radius=8)
                    self.screen.blit(txt, txt.get_rect(center=(tx, ty)))

                # Centre premium
                pygame.draw.circle(self.screen, (255, 245, 220), (cx, cy), 42)
                pygame.draw.circle(self.screen, (255, 170, 60), (cx, cy), 34)
                pygame.draw.circle(self.screen, (255, 235, 175), (cx, cy), 20)
                self.draw_text("WR", self.small_bold_font, (105, 50, 10), cx, cy + 2)

                # Flèche néon
                pointer_y = cy - radius - 28
                pulse = 0.65 + 0.35 * math.sin(pygame.time.get_ticks() * 0.008)
                glow_col = (255, int(150 + 70 * pulse), int(80 + 40 * pulse))
                pygame.draw.polygon(self.screen, glow_col, [(cx, pointer_y + 52), (cx - 22, pointer_y + 8), (cx + 22, pointer_y + 8)])
                pygame.draw.polygon(self.screen, (255, 245, 225), [(cx, pointer_y + 42), (cx - 16, pointer_y + 12), (cx + 16, pointer_y + 12)])
                pygame.draw.circle(self.screen, (255, 180, 80), (cx, pointer_y + 58), 9)

                # Panneau d'etat / resultat
                card_w, card_h = 560, 120
                card_rect = pygame.Rect(cx - card_w // 2, min(SCREEN_HEIGHT - 170, cy + radius + 20), card_w, card_h)
                pygame.draw.rect(self.screen, (18, 23, 36), card_rect, border_radius=16)
                pygame.draw.rect(self.screen, (95, 120, 165), card_rect, 2, border_radius=16)

                if self.wheel_spinning:
                    self.draw_text("Rotation en cours...", self.medium_font, (255, 220, 150), card_rect.centerx, card_rect.y + 38)
                    speed_txt = f"Vitesse: {self.wheel_velocity:04.1f}"
                    self.draw_text(speed_txt, self.small_bold_font, (170, 190, 220), card_rect.centerx, card_rect.y + 84)
                elif self.spin_result is not None:
                    self.draw_text("GAIN OBTENU", self.small_bold_font, (165, 190, 230), card_rect.centerx, card_rect.y + 28)
                    self.draw_text_shadow(str(self.spin_result), self.big_font, (255, 215, 100), card_rect.centerx, card_rect.y + 78)
                else:
                    spin_avail = self.last_spin_date != str(datetime.date.today())
                    if spin_avail:
                        self.draw_text("Pret pour un tirage gratuit.", self.medium_font, (165, 255, 185), card_rect.centerx, card_rect.y + 40)
                        self.draw_text("Cliquez sur LANCER LA ROUE", self.small_bold_font, (180, 210, 235), card_rect.centerx, card_rect.y + 84)
                    else:
                        self.draw_text("Tirage deja utilise aujourd'hui.", self.medium_font, (255, 180, 180), card_rect.centerx, card_rect.y + 40)
                        self.draw_text("Revenez demain pour un nouveau spin.", self.small_bold_font, (185, 205, 235), card_rect.centerx, card_rect.y + 84)

            elif self.state == "MENU_STATS":
                # --- REDESIGN COMPLET STATS ---
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                panel_w, panel_h = 1100, 800
                self.draw_panel(cx - panel_w//2, cy - panel_h//2, panel_w, panel_h)
                
                self.draw_text_shadow("STATISTIQUES DU JOUEUR", self.big_font, ACCENT_COLOR, cx, cy - 350)
                
                # Sécurité : Initialisation si données corrompues
                if self.stats is None: self.stats = {}
                if "wins" not in self.stats: self.stats["wins"] = 0
                if "games" not in self.stats: self.stats["games"] = 0
                if "wins_per_mode" not in self.stats or not isinstance(self.stats["wins_per_mode"], dict): self.stats["wins_per_mode"] = {}

                # 1. Carte Profil (Haut Gauche)
                prof_rect = pygame.Rect(int(cx - 500), int(cy - 280), 400, 200)
                pygame.draw.rect(self.screen, (30, 35, 45), prof_rect, border_radius=15)
                pygame.draw.rect(self.screen, (60, 70, 80), prof_rect, 2, border_radius=15)
                
                border_id = self.equipped.get('border', 'border_default')
                name_color_id = self.equipped.get('name_color', 'name_color_default')
                
                self.draw_avatar(self.avatar, int(prof_rect.x + 60), int(prof_rect.centery), 45, border_id)
                self.draw_text(self.username, self.medium_font, self.get_name_color(name_color_id), int(prof_rect.x + 130), int(prof_rect.y + 50), center=False)
                self.draw_text(self.get_player_title(self.level), self.small_bold_font, (255, 215, 0), int(prof_rect.x + 130), int(prof_rect.y + 85), center=False)
                self.draw_text(f"Niveau {self.level}", self.font, (200, 200, 200), int(prof_rect.x + 130), int(prof_rect.y + 120), center=False)
                
                # 2. Stats Globales (Haut Droite)
                glob_rect = pygame.Rect(int(cx - 60), int(cy - 280), 560, 200)
                pygame.draw.rect(self.screen, (30, 35, 45), glob_rect, border_radius=15)
                pygame.draw.rect(self.screen, (60, 70, 80), glob_rect, 2, border_radius=15)
                
                total_games = self.stats.get("games", 0)
                total_wins = self.stats.get("wins", 0)
                win_rate = int((total_wins / total_games) * 100) if total_games > 0 else 0
                
                # Grille 2x2
                def draw_stat_cell(x, y, label, val, col):
                    self.draw_text(label, self.small_bold_font, (150, 150, 160), int(x), int(y - 15))
                    self.draw_text(str(val), self.medium_font, col, int(x), int(y + 15))

                c1 = glob_rect.x + glob_rect.w // 4
                c2 = glob_rect.x + 3 * glob_rect.w // 4
                r1 = glob_rect.y + 50
                r2 = glob_rect.y + 140
                
                draw_stat_cell(c1, r1, "PARTIES JOUÉES", total_games, TEXT_COLOR)
                draw_stat_cell(c2, r1, "VICTOIRES", total_wins, ACCENT_COLOR)
                draw_stat_cell(c1, r2, "TAUX DE VICTOIRE", f"{win_rate}%", (100, 255, 100) if win_rate > 50 else (255, 200, 100))
                draw_stat_cell(c2, r2, "MEILLEUR COMBO", self.stats.get("max_combo", 0), (255, 215, 0))

                # 3. Détails par Mode (Bas)
                modes_rect = pygame.Rect(int(cx - 500), int(cy - 50), 1000, 350)
                pygame.draw.rect(self.screen, (25, 30, 40), modes_rect, border_radius=15)
                pygame.draw.rect(self.screen, (50, 60, 70), modes_rect, 2, border_radius=15)
                
                self.draw_text("VICTOIRES PAR MODE", self.small_bold_font, (180, 180, 190), cx, int(modes_rect.y + 30))

                modes = ['NORMAL', 'SURVIVAL', 'SPEED', 'HARDCORE', 'CHAOS', 'TIME_TRIAL']
                wins_map = self.stats.get('wins_per_mode', {})
                if not isinstance(wins_map, dict): wins_map = {}
                wins = [wins_map.get(m, 0) for m in modes]

                max_win = max(wins) if wins and max(wins) > 0 else 1
                
                bar_w = 100
                gap = 50
                start_x = cx - (len(modes) * (bar_w + gap)) // 2 + gap//2
                base_y = modes_rect.bottom - 60
                max_h = 200
                
                for i, mode in enumerate(modes):
                    h = (wins[i] / max_win) * max_h
                    x = start_x + i * (bar_w + gap)
                    rect = pygame.Rect(int(x), int(base_y - h), int(bar_w), int(h))
                    
                    col = ACCENT_COLOR
                    if mode == "HARDCORE": col = ALERT_COLOR
                    elif mode == "SPEED": col = (255, 255, 0)
                    elif mode == "SURVIVAL": col = (255, 150, 50)
                    elif mode == "TIME_TRIAL": col = (0, 200, 255)
                    
                    # Barre
                    pygame.draw.rect(self.screen, (40, 45, 55), (int(x), int(base_y - max_h), int(bar_w), int(max_h)), border_radius=8) # Fond gris
                    if h > 0:
                        pygame.draw.rect(self.screen, col, rect, border_radius=8)
                    
                    # Valeur
                    self.draw_text(str(wins[i]), self.small_bold_font, (255, 255, 255), rect.centerx, int(rect.top - 15 if h > 0 else base_y - 15))
                    
                    # Nom du mode (Vertical ou petit)
                    lbl = self.small_bold_font.render(mode[:3], True, (150, 150, 150))
                    self.screen.blit(lbl, lbl.get_rect(center=(rect.centerx, int(base_y + 20))))

            elif self.state == "JUDGMENT":
                if self.is_local_game or self.judge_id == self.my_id:
                    self.draw_text_shadow("CONTESTATION !", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 100)
                    self.draw_text("Le dernier mot est-il valide ?", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 200)
                else:
                    self.draw_text_shadow("CONTESTATION EN COURS...", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 100)
                    self.draw_text("Attente du jugement...", self.font, TEXT_COLOR, SCREEN_WIDTH//2, 200)

            elif self.state == "ROUND_COUNTDOWN":
                remaining = 5 - (pygame.time.get_ticks() - self.countdown_start) / 1000
                if remaining < 0: remaining = 0
                
                # Fond sombre
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                self.screen.blit(s, (0, 0))

                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                self.draw_panel(cx - 400, cy - 200, 800, 400)
                
                # Header
                self.draw_text_shadow(f"FIN DE LA MANCHE {self.round_num - 1}", self.big_font, (200, 200, 200), cx, cy - 140)
                
                # Message de résultat
                msg_color = TEXT_COLOR
                msg_text = "Point attribué !"
                icon = "😐"
                
                if self.last_round_reason == "TIMEOUT":
                    if self.last_round_winner == self.my_id:
                        msg_text = "L'adversaire a été trop lent !"
                        msg_color = ACCENT_COLOR
                        icon = "😎"
                    else:
                        msg_text = "Temps écoulé !"
                        msg_color = ALERT_COLOR
                        icon = "⏰"
                elif self.last_round_winner == self.my_id:
                    msg_text = "Tu marques le point !"
                    msg_color = ACCENT_COLOR
                    icon = "🔥"
                else:
                    msg_text = "L'adversaire marque le point."
                    msg_color = ALERT_COLOR
                    icon = "💀"

                self.draw_text(icon, self.emoji_font, (255, 255, 255), cx, cy - 60)
                self.draw_text(msg_text, self.medium_font, msg_color, cx, cy + 10)
                
                # Next Round Countdown
                self.draw_text("PROCHAINE MANCHE DANS", self.small_bold_font, (150, 150, 150), cx, cy + 80)
                self.draw_text(f"{int(remaining) + 1}", self.title_font, (255, 255, 255), cx, cy + 140)

            elif self.state == "BONUS_GAME":
                self.draw_text_shadow("BONUS : ATTRAPEZ LES PIÈCES !", self.big_font, (255, 215, 0), SCREEN_WIDTH//2, 50)
                rem = (self.bonus_end_time - pygame.time.get_ticks()) / 1000
                self.draw_text(f"{rem:.1f}s", self.big_font, (255, 255, 255), SCREEN_WIDTH//2, 100)
                
                for t in self.bonus_targets:
                    # Dessin pièce
                    pygame.draw.circle(self.screen, (255, 215, 0), t.center, 35)
                    pygame.draw.circle(self.screen, (255, 255, 200), (t.centerx - 10, t.centery - 10), 10)
                    self.draw_text("$", self.medium_font, (200, 150, 0), t.centerx, t.centery)

            elif self.state == "OPPONENT_LEFT":
                self.draw_panel(SCREEN_WIDTH//2 - 300, 200, 600, 400)
                title = "L'HÔTE A QUITTÉ" if not self.is_host else "ADVERSAIRE PARTI"
                self.draw_text_shadow(title, self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 250)
                msg = "L'hôte a fermé la partie." if not self.is_host else "Votre adversaire a quitté."
                self.draw_text(msg, self.font, TEXT_COLOR, SCREEN_WIDTH//2, 350)
                
                # Auto-redirect
                rem = 4 - (pygame.time.get_ticks() - self.opponent_left_time) / 1000
                self.draw_text(f"Retour au menu dans {int(rem)}...", self.font, (150, 150, 150), SCREEN_WIDTH//2, 450)
                if rem <= 0:
                    self.set_state("MENU_MAIN")

            elif self.state == "GAME_OVER":
                # --- REDESIGN GAME OVER ---
                # Fond sombre global
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((10, 12, 15, 240))
                self.screen.blit(s, (0, 0))
                
                title = "VICTOIRE !" if self.winner_text == self.username else "DÉFAITE..."
                if self.is_local_game: title = "FIN DE PARTIE"
                
                is_win = (title == "VICTOIRE !")
                main_col = ACCENT_COLOR if is_win else ALERT_COLOR
                if self.is_local_game: main_col = (255, 215, 0)
                
                # Bannière Résultat
                banner_h = 150
                pygame.draw.rect(self.screen, (*main_col, 50), (0, 100, SCREEN_WIDTH, banner_h))
                pygame.draw.line(self.screen, main_col, (0, 100), (SCREEN_WIDTH, 100), 3)
                pygame.draw.line(self.screen, main_col, (0, 100 + banner_h), (SCREEN_WIDTH, 100 + banner_h), 3)
                
                self.draw_text_shadow(title, self.title_font, main_col, SCREEN_WIDTH//2, 100 + banner_h//2)
                
                # Affichage VS (Avatars)
                cx = SCREEN_WIDTH // 2
                cy = SCREEN_HEIGHT // 2
                
                # Joueur 1 (Moi / J1)
                p1_name = self.username
                p1_av = self.avatar
                p1_border = self.equipped['border']
                
                # Joueur 2 (Adversaire / J2)
                p2_name = self.opponent_name
                p2_av = self.opponent_avatar
                p2_border = self.opponent_border
                
                if self.is_local_game:
                    p1_name = self.local_player_names[0]
                    p2_name = self.local_player_names[1]
                    p2_av = AVATARS[1]
                    p2_border = "border_default"

                # P1 (Gauche)
                self.draw_avatar(p1_av, cx - 300, cy - 50, 80, p1_border)
                self.draw_text(p1_name, self.medium_font, TEXT_COLOR, cx - 300, cy + 60)
                
                # Score P1 (Moi / J1)
                s1 = self.score[self.my_id]
                self.draw_text(str(s1), self.title_font, ACCENT_COLOR, cx - 150, cy - 50)
                
                # VS
                self.draw_text("VS", self.big_font, (100, 100, 100), cx, cy - 50)
                
                # P2 (Droite)
                # Score P2 (Adversaire / J2)
                opp_idx = 1 if self.is_local_game else (1 - self.my_id)
                s2 = self.score[opp_idx] if opp_idx < len(self.score) else 0
                self.draw_text(str(s2), self.title_font, ALERT_COLOR, cx + 150, cy - 50)
                
                self.draw_avatar(p2_av, cx + 300, cy - 50, 80, p2_border)
                self.draw_text(p2_name, self.medium_font, TEXT_COLOR, cx + 300, cy + 60)
                
                # Animation XP
                if self.xp_animating:
                    self._update_xp_anim()

                # Barre XP
                bar_w, bar_h = 600, 30
                bx, by = cx - bar_w//2, cy + 130 # Remonté de 150 à 130
                
                self.draw_text(f"Niveau {self.anim_level_val}", self.medium_font, ACCENT_COLOR, SCREEN_WIDTH//2, by - 30)
                pygame.draw.rect(self.screen, (30, 35, 45), (bx, by, bar_w, bar_h), border_radius=10)
                pygame.draw.rect(self.screen, (0, 200, 150), (bx, by, int(bar_w * ratio), bar_h), border_radius=10)
                pygame.draw.rect(self.screen, (100, 100, 100), (bx, by, bar_w, bar_h), 2, border_radius=10)
                
                gain = 50 if is_win else 10
                self.draw_text(f"+{gain} Pièces", self.medium_font, (255, 215, 0), SCREEN_WIDTH//2, by + 50)
                
                # Status rematch
                rematch_count = sum(self.rematch_ready)
                self.draw_text(f"Rejouer : {rematch_count}/{self.settings['players']}", self.font, (150, 150, 150), SCREEN_WIDTH//2, by + 90)
                if self.rematch_ready[self.my_id]: 
                    self.draw_text("En attente de l'adversaire...", self.small_bold_font, ACCENT_COLOR, SCREEN_WIDTH//2, by + 120)
                
                # Confetti si victoire
                if self.winner_text == self.username or (self.is_local_game and "Joueur" in self.winner_text):
                    if random.random() < 0.3:
                        self.add_particles(random.randint(0, SCREEN_WIDTH), -10, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))

            elif self.state == "GAME":
                # Amélioration Graphique : Ambiance
                if self.settings.get('game_type') != 'TIME_TRIAL':
                    pulse_bg = (math.sin(pygame.time.get_ticks() * 0.001) + 1) * 0.5
                    s_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    s_bg.fill((0, 0, 0, int(30 * pulse_bg)))
                    self.screen.blit(s_bg, (0, 0))

                # HUD modernisé
                hud_h = 90
                hud_rect = pygame.Rect(40, 20, SCREEN_WIDTH - 80, hud_h)
                self.draw_panel(hud_rect.x, hud_rect.y, hud_rect.w, hud_rect.h)

                # Scores
                if self.is_local_game:
                    # Highlight active player score
                    score_parts = []
                    for i, s in enumerate(self.score):
                        prefix = "> " if i == self.current_player else ""
                        name = self.local_player_names[i] if i < len(self.local_player_names) else f"J{i+1}"
                        score_parts.append(f"{prefix}{name}: {s}")
                    score_text = "   ".join(score_parts)
                    self.draw_text(score_text, self.font, ACCENT_COLOR, hud_rect.centerx, hud_rect.y + 28)
                else:
                    p1 = self.username if self.my_id == 0 else self.opponent_name
                    p2 = self.opponent_name if self.my_id == 0 else self.username
                    c1 = self.get_name_color(self.equipped['name_color']) if self.my_id == 0 else self.get_name_color(self.opponent_name_color)
                    c2 = self.get_name_color(self.opponent_name_color) if self.my_id == 0 else self.get_name_color(self.equipped['name_color'])
                    txt1 = f"{p1}: {self.score[0]}"
                    txt2 = f"{p2}: {self.score[1]}"
                    
                    sep = "   |   "
                    surf1 = self.font.render(txt1, True, c1)
                    surf2 = self.font.render(txt2, True, c2)
                    surf_sep = self.font.render(sep, True, TEXT_COLOR)
                    total_w = surf1.get_width() + surf_sep.get_width() + surf2.get_width()
                    start_x = hud_rect.centerx - total_w // 2
                    self.screen.blit(surf1, (start_x, hud_rect.y + 20))
                    self.screen.blit(surf_sep, (start_x + surf1.get_width(), hud_rect.y + 20))
                    self.screen.blit(surf2, (start_x + surf1.get_width() + surf_sep.get_width(), hud_rect.y + 20))

                    # Indicateur visuel (Flèche dessinée)
                    arrow_y = hud_rect.y + 35
                    if self.current_player == 0:
                        # Flèche vers P1 (Gauche) : > P1
                        ax = start_x - 25
                        pygame.draw.polygon(self.screen, ACCENT_COLOR, [(ax, arrow_y - 8), (ax + 15, arrow_y), (ax, arrow_y + 8)])
                    elif self.current_player == 1:
                        # Flèche vers P2 (Droite) : P2 <
                        ax = start_x + total_w + 10
                        pygame.draw.polygon(self.screen, ACCENT_COLOR, [(ax + 15, arrow_y - 8), (ax, arrow_y), (ax + 15, arrow_y + 8)])

                # Tour + mot précédent
                local_name = self.local_player_names[self.current_player] if self.is_local_game and self.current_player < len(self.local_player_names) else f"Joueur {self.current_player + 1}"
                turn_msg = f"Tour de {local_name}" if self.is_local_game else ("C'est votre tour !" if self.current_player == self.my_id else "Tour de l'adversaire...")
                self.draw_text(turn_msg, self.font, ACCENT_COLOR, hud_rect.centerx, hud_rect.y + 60)
                self.draw_text("MOT PRÉCÉDENT", self.small_bold_font, (150, 150, 150), hud_rect.right - 170, hud_rect.y + 26)
                self.draw_text_shadow(f"{self.current_word}", self.medium_font, ACCENT_COLOR, hud_rect.right - 170, hud_rect.y + 60)
                
                # Mot précédent (Design amélioré)
                prev_word_rect = pygame.Rect(hud_rect.right - 320, hud_rect.y + 10, 300, 70)
                pygame.draw.rect(self.screen, (20, 25, 30), prev_word_rect, border_radius=10)
                pygame.draw.rect(self.screen, (50, 60, 70), prev_word_rect, 1, border_radius=10)
                self.draw_text("MOT PRÉCÉDENT", self.small_bold_font, (150, 150, 150), prev_word_rect.centerx, prev_word_rect.y + 20)
                self.draw_text(f"{self.current_word}", self.medium_font, ACCENT_COLOR, prev_word_rect.centerx, prev_word_rect.y + 50)
                
                # Affichage Timer
                timer_panel = pygame.Rect(SCREEN_WIDTH//2 - 350, 140, 700, 200)
                self.draw_panel(timer_panel.x, timer_panel.y, timer_panel.w, timer_panel.h)
                timer_color = ALERT_COLOR if self.time_left < 2 else TEXT_COLOR
                if self.time_left <= 3 and self.time_left > 0:
                    self.draw_text_glitch(f"{max(0, self.time_left):05.2f}", self.timer_font, timer_color, SCREEN_WIDTH//2, 220)
                else:
                    self.draw_text(f"{max(0, self.time_left):05.2f}", self.timer_font, timer_color, SCREEN_WIDTH//2, 220)
                
                # Barre de temps
                bar_width = 600
                bar_height = 25
                bar_rect = pygame.Rect(SCREEN_WIDTH//2 - bar_width//2, 280, bar_width, bar_height)
                fill_width = max(0, (self.time_left / self.round_duration) * bar_width)
                fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_width, bar_height)

                # Background
                pygame.draw.rect(self.screen, (30, 35, 45), bar_rect, border_radius=12)
                
                # Glow effect behind bar
                if fill_width > 0:
                    glow_rect = bar_rect.copy()
                    glow_rect.width = fill_width
                    pygame.draw.rect(self.screen, (*timer_color, 50), glow_rect.inflate(10, 10), border_radius=15)

                # Gradient Fill
                if fill_width > 0:
                    start_color = (0, 220, 150)
                    end_color = (0, 180, 120)
                    if self.time_left < self.round_duration * 0.3: # Last 30%
                        ratio = self.time_left / (self.round_duration * 0.3)
                        start_color = self.interpolate_color(ALERT_COLOR, (255, 165, 0), ratio) # Red to Orange
                        end_color = self.interpolate_color((150, 0, 0), (200, 100, 0), ratio) # Dark Red to Dark Orange
                    
                    gradient_surf = pygame.Surface((fill_width, bar_height), pygame.SRCALPHA)
                    for i in range(int(fill_width)):
                        color = self.interpolate_color(start_color, end_color, i / fill_width)
                        pygame.draw.line(gradient_surf, color, (i, 0), (i, bar_height))
                    self.screen.blit(gradient_surf, fill_rect.topleft)

                pygame.draw.rect(self.screen, (80, 80, 90), bar_rect, 2, border_radius=12)

                # Flash rouge si temps < 2s
                if 0 < self.time_left <= 2:
                    flash_s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    flash_s.fill(ALERT_COLOR)
                    alpha = int(40 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
                    flash_s.set_alpha(alpha)
                    self.screen.blit(flash_s, (0, 0))
                
                # Effet Visuel Gel du Temps
                if pygame.time.get_ticks() < self.freeze_until:
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    overlay.fill((100, 200, 255, 30))
                    self.screen.blit(overlay, (0, 0))
                    self.draw_text("TEMPS GELÉ", self.big_font, (100, 200, 255), SCREEN_WIDTH//2, 180)

                # Affichage Global Timer (Time Trial)
                if self.settings.get('game_type') == 'TIME_TRIAL' and self.global_timer_start > 0:
                    rem_global = max(0, 60 - (pygame.time.get_ticks() - self.global_timer_start) / 1000)
                    self.draw_text_shadow(f"CHRONO GLOBAL: {rem_global:.1f}s", self.big_font, (255, 50, 50), SCREEN_WIDTH//2, 120)
                    if rem_global <= 0 and (self.is_host or self.is_local_game):
                        self.end_game_time_trial()

                # Mort Subite (Sudden Death)
                if self.settings['win_score'] > 1:
                    if self.score[0] == self.settings['win_score'] - 1 and self.score[1] == self.settings['win_score'] - 1:
                        alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
                        txt_surf = self.big_font.render("MORT SUBITE !", True, (255, 50, 50))
                        txt_surf.set_alpha(alpha)
                        self.screen.blit(txt_surf, txt_surf.get_rect(center=(SCREEN_WIDTH//2, 150)))

                if self.time_left <= 0:
                    self.draw_text_shadow("TEMPS ÉCOULÉ !", self.big_font, ALERT_COLOR, SCREEN_WIDTH//2, 450)
                    # Ici on pourrait forcer la fin du tour ou attendre une action

                # Spécifique Mode Écrit
                if self.settings['mode'] == "WRITTEN":
                    # Zone de texte centrée
                    input_w = 500
                    input_rect = pygame.Rect(SCREEN_WIDTH//2 - input_w//2, 380, input_w, 70)
                    
                    is_active = self.is_local_game or self.current_player == self.my_id
                    # Afficher le texte de l'utilisateur ou de l'adversaire
                    if self.current_player == self.my_id:
                        display_text = self.user_text
                    else:
                        display_text = self.opponent_text if self.opponent_text else "L'adversaire réfléchit..."
                    
                    self.draw_fancy_input_box(input_rect, display_text, "", active=is_active, font=self.font)
                    self.draw_text("Écrivez et appuyez sur ENTRÉE.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 500)
                    
                # Spécifique Mode Vocal
                if self.settings['mode'] == "VOCAL":
                    if self.is_local_game or self.current_player == self.my_id:
                        self.draw_text_shadow("Parlez maintenant !", self.font, ACCENT_COLOR, SCREEN_WIDTH//2, 400)
                        self.draw_text("ESPACE quand fini. 'A' pour contester.", self.font, (100, 100, 120), SCREEN_WIDTH//2, 550)
                    else:
                        self.draw_text_shadow("Tour de l'adversaire...", self.font, (150, 150, 150), SCREEN_WIDTH//2, 400)

            # Dessin des particules et animations au premier plan
            self.update_draw_particles()
            self.update_draw_coin_particles()
            self.update_draw_coin_fly()
            self.update_draw_game_emotes()
            self.update_draw_floating_texts()

            # Notifications (Dessinées avant la pop-up pour être en arrière-plan)
            self.draw_notifications()

            # Affichage des boutons (en dernier pour être au-dessus des panneaux)
            for btn in self.buttons:
                offset = self.current_frame_card_offsets.get(btn.tag, 0)
                btn.draw(self.screen, offset_y=offset)
            
            # Affichage Popup
            if self.popup:
                cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                mx, my = pygame.mouse.get_pos()

                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 185))
                self.screen.blit(s, (0, 0))

                if self.popup.get("type") == "DAILY_CHALLENGE":
                    w, h = 700, 500

                    glow_surf = pygame.Surface((w + 60, h + 60), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 100, 50, 50), glow_surf.get_rect(), border_radius=40)
                    self.screen.blit(glow_surf, (cx - w//2 - 30, cy - h//2 - 30))

                    self.draw_panel(cx - w//2, cy - h//2, w, h)
                    pygame.draw.rect(self.screen, PANEL_COLOR, (cx - w//2, cy - h//2, w, h), border_radius=15)

                    pygame.draw.rect(self.screen, (255, 80, 40), (cx - w//2, cy - h//2, w, 100), border_top_left_radius=15, border_top_right_radius=15)
                    self.draw_text_shadow("DÉFI DU JOUR", self.big_font, (255, 255, 255), cx, cy - h//2 + 50)

                    self.draw_text("OBJECTIF", self.small_bold_font, (150, 150, 150), cx, cy - 80)
                    self.draw_text(f"Gagner en mode {self.popup['mode']}", self.medium_font, TEXT_COLOR, cx, cy - 40)
                    self.draw_text("CATÉGORIE", self.small_bold_font, (150, 150, 150), cx, cy + 20)
                    self.draw_text(self.popup['category'], self.medium_font, ACCENT_COLOR, cx, cy + 60)
                    self.draw_coin_ui(cx, cy + 130, self.popup['reward'])

                    btn_w, btn_h = 250, 70
                    yes_rect = pygame.Rect(cx - btn_w - 20, cy + h//2 - 100, btn_w, btn_h)
                    no_rect = pygame.Rect(cx + 20, cy + h//2 - 100, btn_w, btn_h)
                    self.popup["rect_yes"], self.popup["rect_no"] = yes_rect, no_rect

                    col_yes = (255, 120, 60) if yes_rect.collidepoint(mx, my) else (200, 80, 40)
                    col_no = (80, 80, 90) if no_rect.collidepoint(mx, my) else (60, 60, 70)
                    pygame.draw.rect(self.screen, col_yes, yes_rect, border_radius=15)
                    pygame.draw.rect(self.screen, col_no, no_rect, border_radius=15)
                    self.draw_text("ACCEPTER", self.medium_font, (255, 255, 255), yes_rect.centerx, yes_rect.centery)
                    self.draw_text("REFUSER", self.medium_font, (200, 200, 200), no_rect.centerx, no_rect.centery)

                elif self.popup.get("type") == "RESET_CONFIRM":
                    w, h = 780, 500
                    panel_rect = pygame.Rect(cx - w//2, cy - h//2, w, h)

                    # Glow + panel principal
                    glow_surf = pygame.Surface((w + 80, h + 80), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 60, 60, 65), glow_surf.get_rect(), border_radius=45)
                    self.screen.blit(glow_surf, (panel_rect.x - 40, panel_rect.y - 40))
                    self.draw_panel(panel_rect.x, panel_rect.y, panel_rect.w, panel_rect.h)
                    pygame.draw.rect(self.screen, (22, 24, 32), panel_rect, border_radius=18)
                    pygame.draw.rect(self.screen, (170, 55, 60), panel_rect, 2, border_radius=18)

                    # Bandeau d'alerte
                    header_rect = pygame.Rect(panel_rect.x, panel_rect.y, panel_rect.w, 110)
                    pygame.draw.rect(self.screen, (185, 55, 58), header_rect, border_top_left_radius=18, border_top_right_radius=18)
                    self.draw_text_shadow("⚠ CONFIRMATION FINALE", self.big_font, (255, 255, 255), cx, header_rect.y + 48)

                    # Message principal (2 lignes pour éviter tout débordement)
                    self.draw_text("Cette action va supprimer", self.medium_font, (230, 230, 230), cx, panel_rect.y + 158)
                    self.draw_text("definitivement vos donnees locales.", self.medium_font, (230, 230, 230), cx, panel_rect.y + 190)

                    bullet_color = (255, 180, 180)
                    self.draw_text("• Progression et niveau", self.font, bullet_color, cx, panel_rect.y + 215)
                    self.draw_text("• Inventaire, thèmes et badges", self.font, bullet_color, cx, panel_rect.y + 248)
                    self.draw_text("• Historique et liste d'amis", self.font, bullet_color, cx, panel_rect.y + 281)

                    # Ligne info basse
                    info_rect = pygame.Rect(panel_rect.x + 40, panel_rect.y + 315, panel_rect.w - 80, 62)
                    pygame.draw.rect(self.screen, (45, 28, 33), info_rect, border_radius=12)
                    pygame.draw.rect(self.screen, (120, 55, 65), info_rect, 1, border_radius=12)
                    self.draw_text("Aucune récupération possible après validation.", self.small_bold_font, (255, 200, 200), info_rect.centerx, info_rect.centery)

                    # Boutons
                    btn_w, btn_h = 300, 72
                    yes_rect = pygame.Rect(cx - btn_w - 16, panel_rect.bottom - 95, btn_w, btn_h)
                    no_rect = pygame.Rect(cx + 16, panel_rect.bottom - 95, btn_w, btn_h)
                    self.popup["rect_yes"], self.popup["rect_no"] = yes_rect, no_rect

                    yes_col = (220, 65, 70) if not yes_rect.collidepoint(mx, my) else (245, 88, 95)
                    no_col = (70, 80, 92) if not no_rect.collidepoint(mx, my) else (90, 102, 118)

                    pygame.draw.rect(self.screen, yes_col, yes_rect, border_radius=14)
                    pygame.draw.rect(self.screen, (130, 35, 45), yes_rect, 2, border_radius=14)
                    pygame.draw.rect(self.screen, no_col, no_rect, border_radius=14)
                    pygame.draw.rect(self.screen, (95, 110, 130), no_rect, 2, border_radius=14)

                    self.draw_text(self.popup.get("yes_text", "ACCEPTER"), self.small_bold_font, (255, 245, 245), yes_rect.centerx, yes_rect.centery)
                    self.draw_text(self.popup.get("no_text", "ANNULER"), self.small_bold_font, (225, 235, 245), no_rect.centerx, no_rect.centery)

                else:
                    w, h = 600, 400
                    self.draw_panel(cx - w//2, cy - h//2, w, h)

                    self.draw_text_shadow(self.popup["title"], self.big_font, ACCENT_COLOR, cx, cy - 120)
                    lines = self.popup["msg"].split('\n')
                    for i, line in enumerate(lines):
                        self.draw_text(line, self.font, TEXT_COLOR, cx, cy - 50 + i * 35)

                    if "avatar" in self.popup:
                        self.draw_avatar(self.popup["avatar"], cx, cy + 20, 40)

                    btn_w, btn_h = 200, 60
                    if self.popup.get("single_button_text"):
                        btn_rect = pygame.Rect(cx - 150, cy + 100, 300, 60)
                        self.popup["rect_action"] = btn_rect
                        col = HOVER_COLOR if btn_rect.collidepoint(mx, my) else ACCENT_COLOR
                        pygame.draw.rect(self.screen, col, btn_rect, border_radius=15)
                        self.draw_text(self.popup["single_button_text"], self.small_bold_font, (20, 25, 35), btn_rect.centerx, btn_rect.centery)
                    else:
                        yes_rect = pygame.Rect(cx - btn_w - 20, cy + 100, btn_w, btn_h)
                        no_rect = pygame.Rect(cx + 20, cy + 100, btn_w, btn_h)
                        self.popup["rect_yes"], self.popup["rect_no"] = yes_rect, no_rect

                        col_yes = HOVER_COLOR if yes_rect.collidepoint(mx, my) else ACCENT_COLOR
                        col_no = (255, 100, 100) if no_rect.collidepoint(mx, my) else ALERT_COLOR
                        pygame.draw.rect(self.screen, col_yes, yes_rect, border_radius=15)
                        pygame.draw.rect(self.screen, col_no, no_rect, border_radius=15)
                        self.draw_text("ACCEPTER", self.small_bold_font, (20, 25, 35), yes_rect.centerx, yes_rect.centery)
                        self.draw_text("REFUSER", self.small_bold_font, (255, 255, 255), no_rect.centerx, no_rect.centery)

            # Popup Succès (Steam style)
            self.draw_achievement_popup()

            if using_temp_screen:
                real_screen.blit(self.screen, (shake_x, shake_y))
                self.screen = real_screen

            # Copyright & Version
            if self.state != "STARTUP_ANIM":
                self.draw_text("© dodosi", self.font, (80, 80, 90), SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30)
            self.draw_text(CURRENT_VERSION, self.font, (80, 80, 90), 40, SCREEN_HEIGHT - 30)
            
            # Indicateur Mode Développeur
            if self.test_mode:
                banner_w, banner_h = 900, 80
                bx = SCREEN_WIDTH // 2 - banner_w // 2
                by = 6
                s = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
                pygame.draw.rect(s, (30, 35, 45, 220), (0, 0, banner_w, banner_h), border_radius=16)
                pygame.draw.rect(s, (255, 120, 120), (0, 0, banner_w, banner_h), 2, border_radius=16)
                self.screen.blit(s, (bx, by))
                self.draw_text("DEV MODE ACTIF", self.small_bold_font, (255, 150, 150), SCREEN_WIDTH//2, by + 22)
                self.draw_text("X: XP | U: Succès | I: Items | W: Win | coins: $$$ | /: Lose | : : Win Pt", self.small_bold_font, (220, 180, 180), SCREEN_WIDTH//2, by + 52)

            # Overlay de connexion (Global - Visible quel que soit l'état si connexion en cours)
            if self.is_connecting:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, 200))
                self.screen.blit(s, (0, 0))
                
                # Animation de chargement
                spin_angle = (pygame.time.get_ticks() // 2) % 360
                center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                pygame.draw.arc(self.screen, ACCENT_COLOR, (center[0]-40, center[1]-40, 80, 80), math.radians(spin_angle), math.radians(spin_angle + 270), 5)
                
                self.draw_text_shadow(self.connect_status if self.connect_status else "Connexion en cours...", self.big_font, ACCENT_COLOR, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)
                self.draw_text("Veuillez patienter jusqu'à 10 secondes...", self.font, (150, 150, 150), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)

            # --- TRANSITION ---
            if self.transition_state == "OUT":
                self.transition_alpha += 15
                if self.transition_alpha >= 255:
                    self.transition_alpha = 255
                    self.state = self.next_state
                    self._apply_state_change()
                    self.transition_state = "IN"
            elif self.transition_state == "IN":
                self.transition_alpha -= 15
                if self.transition_alpha <= 0:
                    self.transition_alpha = 0
                    self.transition_state = None
                    self.transition_color = (0, 0, 0) # Reset couleur par défaut
            
            if self.transition_alpha > 0:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                s.set_alpha(self.transition_alpha)
                s.fill(self.transition_color)
                self.screen.blit(s, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)
          except Exception as e:
            print(f"Erreur récupérée (Stabilité): {e}")
            # On continue la boucle au lieu de crasher

        self.remove_upnp()
        pygame.quit()

    def _update_xp_anim(self):
        threshold = self.get_xp_threshold(self.anim_level_val)
        self.anim_xp_val += max(0.5, threshold / 60.0) # Vitesse animation (approx 1 sec)
        if self.anim_xp_val >= threshold:
            self.anim_xp_val = 0
            self.anim_level_val += 1
            self.play_sound("start")
        
        # Fin animation
        if self.anim_level_val > self.target_level_val or (self.anim_level_val == self.target_level_val and self.anim_xp_val >= self.target_xp_val):
            self.anim_xp_val = self.target_xp_val
            self.anim_level_val = self.target_level_val
            self.xp_animating = False

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        game.remove_upnp()
        pygame.quit()
