import discord
from discord.ext import commands
import asyncio
import os
import json
import requests
import random
import sqlite3

# 🔧 Configuration du bot
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1347496375390048349  # ID du salon autorisé pour /pokemon
DELETE_DELAY = 60  # Suppression après 60 secondes
POKEMON_LIST_FILE = "pokemon_names_fr.json"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Connexion à la base de données SQLite
conn = sqlite3.connect('pokemon_collections.db')
cursor = conn.cursor()

# Créer la table user_collections
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_collections (
    user_id INTEGER,
    card_name TEXT,
    PRIMARY KEY (user_id, card_name)
)
''')
conn.commit()


# 📌 Table des boosters et des cartes disponibles
BOOSTERS = {
    "Pikachu": {
        "6": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/6.png",
            "allowed_positions" : [1, 2, 3, 4]  
        },
         "5": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/5.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "14": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/14.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
        "27": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/27.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
        "29": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/29.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "39": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/39.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "42": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/42.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "48": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/48.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "51": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/51.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "53": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/53.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "57": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/57.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "64": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/64.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "70": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/70.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "72": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/72.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "77": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/77.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "92": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/92.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "94": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/94.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "97": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/97.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "99": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/99.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "101": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/101.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "105": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/105.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "110": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/110.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "111": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/111.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "113": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/113.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "118": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/118.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "124": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/124.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "133": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/133.png",
            "allowed_positions" : [1, 2, 3, 4] 
        }, 
         "134": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/134.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "135": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/135.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "137": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/137.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "139": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/139.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "147": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/147.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "160": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/160.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "162": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/162.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "164": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/164.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "166": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/166.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "169": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/169.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "179": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/179.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "189": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/189.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "190": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/190.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "193": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/193.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "194": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/194.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "199": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/199.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "208": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/208.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "212": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/212.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "214": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/214.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "215": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/215.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "216": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/216.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },

        ############################################
        
        "15": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/15.png",
            "allowed_positions" : [5, 6]
        },
        "26": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/26.png",
            "allowed_positions" : [5, 6]
        },
        "28": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/28.png",
            "allowed_positions" : [5, 6]
        },
        "30": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/30.png",
            "allowed_positions" : [5, 6]
        },
         "43": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/43.png",
            "allowed_positions" : [5, 6]
        },
         "52": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/52.png",
            "allowed_positions" : [5, 6]
        },
         "54": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/54.png",
            "allowed_positions" : [5, 6]
        },
         "58": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/58.png",
            "allowed_positions" : [5, 6]
        },
         "65": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/65.png",
            "allowed_positions" : [5, 6]
        },
         "71": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/71.png",
            "allowed_positions" : [5, 6]
        },
         "73": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/73.png",
            "allowed_positions" : [5, 6]
        },
         "81": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/81.png",
            "allowed_positions" : [5, 6]
        },
         "91": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/91.png",
            "allowed_positions" : [5, 6]
        },
         "93": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/93.png",
            "allowed_positions" : [5, 6]
        },
         "100": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/100.png",
            "allowed_positions" : [5, 6]
        },
         "106": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/106.png",
            "allowed_positions" : [5, 6]
        },
         "112": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/112.png",
            "allowed_positions" : [5, 6]
        },
         "114": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/114.png",
            "allowed_positions" : [5, 6]
        },
         "119": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/119.png",
            "allowed_positions" : [5, 6]
        },
         "136": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/136.png",
            "allowed_positions" : [5, 6]
        },
         "138": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/138.png",
            "allowed_positions" : [5, 6]
        },
         "140": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/140.png",
            "allowed_positions" : [5, 6]
        },
         "148": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/148.png",
            "allowed_positions" : [5, 6]
        },
         "150": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/150.png",
            "allowed_positions" : [5, 6]
        },
         "161": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/161.png",
            "allowed_positions" : [5, 6]
        },
         "163": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/163.png",
            "allowed_positions" : [5, 6]
        },
         "165": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/165.png",
            "allowed_positions" : [5, 6]
        },
         "167": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/167.png",
            "allowed_positions" : [5, 6]
        },
         "170": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/170.png",
            "allowed_positions" : [5, 6]
        },
         "180": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/180.png",
            "allowed_positions" : [5, 6]
        },
         "200": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/200.png",
            "allowed_positions" : [5, 6]
        },
         "202": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/202.png",
            "allowed_positions" : [5, 6]
        },
         "213": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/213.png",
            "allowed_positions" : [5, 6]
        },
         "220": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/220.png",
            "allowed_positions" : [5, 6]
        },
         "224": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/224.png",
            "allowed_positions" : [5, 6]
        },
         "226": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/226.png",
            "allowed_positions" : [5, 6]
        },
        ############################################
        "7": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/7.png",
            "allowed_positions" : [5, 6]
        },    
         "40": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/40.png",
            "allowed_positions" : [5, 6]
        },
         "55": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/55.png",
            "allowed_positions" : [5, 6]
        },
         "82": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/82.png",
            "allowed_positions" : [5, 6]
        },
         "95": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/95.png",
            "allowed_positions" : [5, 6]
        },
         "98": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/98.png",
            "allowed_positions" : [5, 6]
        },
         "102": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/102.png",
            "allowed_positions" : [5, 6]
        },
         "149": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/149.png",
            "allowed_positions" : [5, 6]
        },
         "169": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/169.png",
            "allowed_positions" : [5, 6]
        },
         "171": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/171.png",
            "allowed_positions" : [5, 6]
        },
        
        ############################################
         "41": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/41.png",
            "allowed_positions" : [5, 6]
        }, 
         "56": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/56.png",
            "allowed_positions" : [5, 6]
        },
         "96": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/96.png",
            "allowed_positions" : [5, 6]
        },
        "195": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/195.png",
            "allowed_positions" : [5, 6]
        },
        ############################################
        
        "232": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/232.png",
            "allowed_positions" : [5, 6]
        },  
         "233": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/233.png",
            "allowed_positions" : [5, 6]
        }, 
         "235": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/235.png",
            "allowed_positions" : [5, 6]
        }, 
         "238": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/238.png",
            "allowed_positions" : [5, 6]
        },
         "240": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/240.png",
            "allowed_positions" : [5, 6]
        }, 
         "241": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/241.png",
            "allowed_positions" : [5, 6]
        }, 
         "248": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/248.png",
            "allowed_positions" : [5, 6]
        },  
        ############################################
         "254": {
            "drop_rate": 0.0005,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/254.png",
            "allowed_positions" : [6]
        },  
         "260": {
            "drop_rate": 0.0005,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/260.png",
            "allowed_positions" : [6]
        } 
       }
    "MewTwo": {
        "1": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/1.png",
            "allowed_positions" : [1, 2, 3, 4]  
        },
         "8": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/8.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "9": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/9.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
        "16": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/16.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
        "25": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/25.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "27": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/27.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "29": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/29.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "42": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/42.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "48": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/48.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "49": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/49.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "50": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/50.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "51": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/51.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "57": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/57.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "62": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/62.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "66": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/66.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "68": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/68.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "92": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/92.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "105": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/105.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "107": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/107.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "110": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/110.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "111": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/111.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "118": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/118.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "120": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/120.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "127": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/127.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "130": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/130.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "133": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/133.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "134": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/134.png",
            "allowed_positions" : [1, 2, 3, 4] 
        }, 
         "135": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/135.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "137": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/137.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "151": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/151.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "154": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/154.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "156": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/156.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "162": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/162.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "164": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/164.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "172": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/172.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "174": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/174.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "176": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/176.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "179": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/179.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "187": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/187.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "189": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/189.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "190": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/190.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "199": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/199.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "207": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/207.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "212": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/212.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "214": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/214.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "215": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/215.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "218": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/218.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },
         "185": {
            "drop_rate": 0.02083,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/185.png",
            "allowed_positions" : [1, 2, 3, 4] 
        },

        ############################################
        
        "198": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/198.png",
            "allowed_positions" : [5, 6]
        },
         "2": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/2.png",
            "allowed_positions" : [5, 6]
        },
         "17": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/17.png",
            "allowed_positions" : [5, 6]
        },
        "26": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/26.png",
            "allowed_positions" : [5, 6]
        },
        "28": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/28.png",
            "allowed_positions" : [5, 6]
        },
        "30": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/30.png",
            "allowed_positions" : [5, 6]
        },
         "43": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/43.png",
            "allowed_positions" : [5, 6]
        },
         "52": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/52.png",
            "allowed_positions" : [5, 6]
        },
         "58": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/58.png",
            "allowed_positions" : [5, 6]
        },
         "63": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/63.png",
            "allowed_positions" : [5, 6]
        },
         "67": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/67.png",
            "allowed_positions" : [5, 6]
        },
         "69": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/69.png",
            "allowed_positions" : [5, 6]
        },
         "91": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/91.png",
            "allowed_positions" : [5, 6]
        },
         "93": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/93.png",
            "allowed_positions" : [5, 6]
        },
         "106": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/106.png",
            "allowed_positions" : [5, 6]
        },
         "108": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/108.png",
            "allowed_positions" : [5, 6]
        },
         "112": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/112.png",
            "allowed_positions" : [5, 6]
        },
         "119": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/119.png",
            "allowed_positions" : [5, 6]
        },
        "121": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/121.png",
            "allowed_positions" : [5, 6]
        },
         "126": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/126.png",
            "allowed_positions" : [5, 6]
        },
         "131": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/131.png",
            "allowed_positions" : [5, 6]
        },
         "136": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/136.png",
            "allowed_positions" : [5, 6]
        },
         "138": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/138.png",
            "allowed_positions" : [5, 6]
        },
         "152": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/152.png",
            "allowed_positions" : [5, 6]
        },
         "157": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/157.png",
            "allowed_positions" : [5, 6]
        },
         "150": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/150.png",
            "allowed_positions" : [5, 6]
        },
         "163": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/163.png",
            "allowed_positions" : [5, 6]
        },
         "165": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/165.png",
            "allowed_positions" : [5, 6]
        },
         "167": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/167.png",
            "allowed_positions" : [5, 6]
        },
         "173": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/173.png",
            "allowed_positions" : [5, 6]
        },
         "180": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/180.png",
            "allowed_positions" : [5, 6]
        },
         "200": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/200.png",
            "allowed_positions" : [5, 6]
        },
         "201": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/201.png",
            "allowed_positions" : [5, 6]
        },
         "209": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/209.png",
            "allowed_positions" : [5, 6]
        },
         "213": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/213.png",
            "allowed_positions" : [5, 6]
        },
         "222": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/222.png",
            "allowed_positions" : [5, 6]
        },
         "223": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/223.png",
            "allowed_positions" : [5, 6]
        },
        ############################################
        "3": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/3.png",
            "allowed_positions" : [5, 6]
        },    
         "10": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/10.png",
            "allowed_positions" : [5, 6]
        },
         "80": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/80.png",
            "allowed_positions" : [5, 6]
        },
         "83": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/83.png",
            "allowed_positions" : [5, 6]
        },
         "109": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/109.png",
            "allowed_positions" : [5, 6]
        },
         "122": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/122.png",
            "allowed_positions" : [5, 6]
        },
         "132": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/132.png",
            "allowed_positions" : [5, 6]
        },
         "175": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/175.png",
            "allowed_positions" : [5, 6]
        },
         "177": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/177.png",
            "allowed_positions" : [5, 6]
        },
         "186": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/186.png",
            "allowed_positions" : [5, 6]
        },
         "188": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/188.png",
            "allowed_positions" : [5, 6]
        },
         "210": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/210.png",
            "allowed_positions" : [5, 6]
        },
        ############################################
         "84": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/84.png",
            "allowed_positions" : [5, 6]
        }, 
         "129": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/129.png",
            "allowed_positions" : [5, 6]
        },
         "153": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/153.png",
            "allowed_positions" : [5, 6]
        },
        ############################################
        
        "239": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/239.png",
            "allowed_positions" : [5, 6]
        },  
         "242": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/242.png",
            "allowed_positions" : [5, 6]
        }, 
         "245": {
            "drop_rate": 0.00321,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/245.png",
            "allowed_positions" : [5, 6]
        }, 
        ############################################
         "251": {
            "drop_rate": 0.0005,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/251.png",
            "allowed_positions" : [6]
        },  
        ############################################
         "282": {
            "drop_rate": 0.000222,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/282.png",
            "allowed_positions" : [6]
        } 
    },
    # Ajouter d'autres boosters ici (Mewtwo, Palkia, Dialga, Mew)
}

# 📥 Charger la liste des Pokémon en français
def load_pokemon_list(): 
    if os.path.exists(POKEMON_LIST_FILE):
        with open(POKEMON_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    pokemon_list = {}
    response = requests.get("https://pokeapi.co/api/v2/pokemon-species?limit=1000")
    if response.status_code == 200:
        data = response.json()
        for species in data["results"]:
            name_en = species["name"]
            species_data = requests.get(species["url"]).json()
            name_fr = next((entry["name"] for entry in species_data["names"] if entry["language"]["name"] == "fr"), name_en)
            pokemon_list[name_fr] = name_en

    with open(POKEMON_LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(pokemon_list, f, ensure_ascii=False, indent=4)

    return pokemon_list

POKEMON_LIST = load_pokemon_list()

# 📌 Traduction des types en français
TYPES_FR = {
    "normal": "Normal", "fire": "Feu", "water": "Eau", "electric": "Électrik", "grass": "Plante", "ice": "Glace",
    "fighting": "Combat", "poison": "Poison", "ground": "Sol", "flying": "Vol", "psychic": "Psy", "bug": "Insecte",
    "rock": "Roche", "ghost": "Spectre", "dragon": "Dragon", "dark": "Ténèbres", "steel": "Acier", "fairy": "Fée"
}

# 📌 Déterminer les forces et faiblesses d’un type
def get_type_relations(types):
    damage_url = "https://pokeapi.co/api/v2/type/"

    strong_against = set()
    weak_against = set()

    for t in types:
        type_data = requests.get(f"{damage_url}{t}").json()
        
        for double_damage in type_data["damage_relations"]["double_damage_to"]:
            strong_against.add(TYPES_FR.get(double_damage["name"], double_damage["name"]))
        
        for double_damage_from in type_data["damage_relations"]["double_damage_from"]:
            weak_against.add(TYPES_FR.get(double_damage_from["name"], double_damage_from["name"]))

    return ", ".join(strong_against) if strong_against else "Aucune", ", ".join(weak_against) if weak_against else "Aucune"

# 📌 Récupérer la chaîne d'évolution avec niveaux
def get_evolution_chain(evolution_url):
    evolution_response = requests.get(evolution_url)
    evolution_data = evolution_response.json()
    evolution_chain = []
    evo_stage = evolution_data["chain"]

    while evo_stage:
        species_name = evo_stage["species"]["name"]
        species_data = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{species_name}").json()
        name_fr = next((entry["name"] for entry in species_data["names"] if entry["language"]["name"] == "fr"), species_name)

        level_up = ""
        if evo_stage["evolves_to"]:
            for evo in evo_stage["evolves_to"]:
                for condition in evo["evolution_details"]:
                    if "min_level" in condition and condition["min_level"]:
                        level_up = f" ({condition['min_level']})"
                        break

        evolution_chain.append(f"- {name_fr}{level_up}")
        evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

    return "\n".join(evolution_chain)

# 📌 Commande /pokemon
@bot.tree.command(name="pokemon", description="Obtiens toutes les infos sur un Pokémon")
async def pokemon(interaction: discord.Interaction, nom: str):
    if interaction.channel_id != CHANNEL_ID:
        await interaction.response.send_message("❌ Commande interdite ici !", ephemeral=True)
        return

    pokemon_name = POKEMON_LIST.get(nom)
    if not pokemon_name:
        await interaction.response.send_message("❌ Pokémon introuvable.", ephemeral=True)
        return

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"

    try:
        response = requests.get(url)
        species_response = requests.get(species_url)

        response.raise_for_status()
        species_response.raise_for_status()

        data = response.json()
        species_data = species_response.json()

        # 📌 Infos générales
        sprite = data["sprites"]["front_default"]
        official_art = data["sprites"]["other"]["official-artwork"]["front_default"]
        types = [t["type"]["name"] for t in data["types"]]
        translated_types = ", ".join([TYPES_FR.get(t, t) for t in types])
        weight = data["weight"] / 10  # kg
        height = data["height"] / 10  # mètres
        generation = species_data["generation"]["name"].replace("generation-", "").upper()

        # 📌 Talents avec description et type (Normal / Caché)
        abilities = []
        for a in data["abilities"]:
            ability_url = a["ability"]["url"]
            ability_data = requests.get(ability_url).json()
            ability_fr = next((entry["name"] for entry in ability_data["names"] if entry["language"]["name"] == "fr"), a["ability"]["name"])
            description_fr = next((entry["flavor_text"] for entry in ability_data["flavor_text_entries"] if entry["language"]["name"] == "fr"), "Aucune description.")
            is_hidden = "(Caché)" if a["is_hidden"] else "(Normal)"
            abilities.append(f"▫️ **{ability_fr}** {is_hidden} : {description_fr}")
        abilities_text = "\n".join(abilities)

        # 📌 Forces et faiblesses
        strong_against, weak_against = get_type_relations(types)

        # 📌 Évolutions avec niveaux
        evolution_text = get_evolution_chain(species_data["evolution_chain"]["url"])

        # 📌 Création de l'embed avec mise en page demandée
        embed = discord.Embed(title=f"📜 {nom.capitalize()} (Génération {generation})", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)

        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=False)
        embed.add_field(name="🌟 Type", value=translated_types, inline=False)
        embed.add_field(name="💪 Fort contre", value=strong_against, inline=False)
        embed.add_field(name="⚠️ Faible contre", value=weak_against, inline=False)
        embed.add_field(name="⭐ Talents", value=abilities_text, inline=False)
        embed.add_field(name="🌀 Évolutions", value=evolution_text, inline=False)

        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    except requests.exceptions.HTTPError:
        await interaction.response.send_message("❌ Erreur lors de la récupération des données.", ephemeral=True)
    except Exception:
        await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

# 📌 Auto-complétion pour la commande /pokemon
@pokemon.autocomplete("nom")
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [name for name in POKEMON_LIST.keys() if current.lower() in name.lower()]
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]

# 📌 Classe pour gérer les boutons de navigation
class BoosterView(discord.ui.View):
    def __init__(self, cards, current_index=0):
        super().__init__()
        self.cards = cards
        self.current_index = current_index

    @discord.ui.button(label="Précédent", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index - 1) % len(self.cards)
        await self.update_embed(interaction)

    @discord.ui.button(label="Suivant", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index + 1) % len(self.cards)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        card_name = self.cards[self.current_index]
        card_data = BOOSTERS["Pikachu"][card_name]  # Remplacez "Pikachu" par le booster sélectionné
        embed = discord.Embed(title=f"🎴 Carte {self.current_index + 1}/{len(self.cards)}", color=0xFFD700)
        embed.set_image(url=card_data["image_url"])
        await interaction.response.edit_message(embed=embed, view=self)

def sync_cards():
    # Charger les cartes actuelles depuis le fichier JSON ou l'API
    with open(POKEMON_LIST_FILE, "r", encoding="utf-8") as f:
        pokemon_list = json.load(f)

    # Mettre à jour les cartes dans la base de données
    cursor.execute('DELETE FROM user_collections')  # Supprimer toutes les cartes existantes
    conn.commit()

    for user_id, card_name in pokemon_list.items():
        cursor.execute('INSERT OR IGNORE INTO user_collections (user_id, card_name) VALUES (?, ?)', (user_id, card_name))
    conn.commit()

# Commande /booster modifiée
@bot.tree.command(name="booster", description="Ouvre un booster de cartes Pokémon")
async def booster(interaction: discord.Interaction, nom: str):
    if nom not in BOOSTERS:
        await interaction.response.send_message("❌ Booster introuvable.", ephemeral=True)
        return

    # Ouvrir 6 cartes aléatoires en fonction des taux de drop et des positions autorisées
    cards = BOOSTERS[nom]
    selected_cards = []

    for position in range(1, 7):  # Positions de 1 à 6
        eligible_cards = [card for card, data in cards.items() if position in data["allowed_positions"]]
        if eligible_cards:
            selected_card = random.choices(eligible_cards, weights=[cards[card]["drop_rate"] for card in eligible_cards])[0]
            selected_cards.append(selected_card)
        else:
            # Si aucune carte n'est éligible pour cette position, sélectionner une carte aléatoire parmi toutes les cartes
            selected_card = random.choices(list(cards.keys()), weights=[card["drop_rate"] for card in cards.values()])[0]
            selected_cards.append(selected_card)

    # Enregistrer les cartes obtenues dans la table user_collections
    user_id = interaction.user.id
    for card_name in selected_cards:
        cursor.execute('INSERT OR IGNORE INTO user_collections (user_id, card_name) VALUES (?, ?)', (user_id, card_name))
    conn.commit()

    # URL de l'image du booster en fonction du nom du booster
    if nom == "Pikachu":
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/pikachu.png"
    elif nom == "Dialga":
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/dialga.png"

    # Création de l'embed initial avec l'image du booster
    embed = discord.Embed(title="🎁 Booster Fermé", color=0xFFD700)
    embed.set_image(url=booster_image_url)

    # Ajouter le bouton "Ouvrir"
    view = BoosterView(selected_cards, booster_image_url)
    await interaction.response.send_message(embed=embed, view=view)
    
# Auto-complétion pour la commande /booster
@booster.autocomplete("nom")
async def booster_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [name for name in BOOSTERS.keys() if current.lower() in name.lower()]
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]

# Classe pour gérer l'affichage du booster et des cartes
class BoosterView(discord.ui.View):
    def __init__(self, cards, booster_image_url):
        super().__init__()
        self.cards = cards
        self.current_index = 0
        self.booster_image_url = booster_image_url
        self.opened = False

        # Ajouter le bouton "Ouvrir"
        self.open_button = discord.ui.Button(label="Ouvrir", style=discord.ButtonStyle.success)
        self.open_button.callback = self.open_booster
        self.add_item(self.open_button)

        # Ajouter les boutons de navigation
        self.previous_button = discord.ui.Button(label="Précédent", style=discord.ButtonStyle.primary)
        self.next_button = discord.ui.Button(label="Suivant", style=discord.ButtonStyle.primary)
        self.previous_button.callback = self.previous
        self.next_button.callback = self.next

    async def open_booster(self, interaction: discord.Interaction):
        # Remplacer l'image du booster par la première carte
        self.opened = True
        self.remove_item(self.open_button)  # Retirer le bouton "Ouvrir"
        self.add_item(self.previous_button)  # Ajouter les boutons de navigation
        self.add_item(self.next_button)
        await self.update_embed(interaction)

    async def previous(self, interaction: discord.Interaction):
        self.current_index = (self.current_index - 1) % len(self.cards)
        self.update_buttons()
        await self.update_embed(interaction)

    async def next(self, interaction: discord.Interaction):
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.update_buttons()
        await self.update_embed(interaction)

    def update_buttons(self):
        # Désactiver les boutons "Précédent" et "Suivant" si nécessaire
        self.previous_button.disabled = (self.current_index == 0)
        self.next_button.disabled = (self.current_index == len(self.cards) - 1)

    async def update_embed(self, interaction: discord.Interaction):
        if not self.opened:
            # Afficher l'image du booster
            embed = discord.Embed(title="🎁 Booster Fermé", color=0xFFD700)
            embed.set_image(url=self.booster_image_url)
        else:
            # Afficher la carte actuelle
            card_name = self.cards[self.current_index]
            card_data = BOOSTERS["Pikachu"][card_name]  # Remplacez "Pikachu" par le booster sélectionné
            embed = discord.Embed(title=f"🎴 Carte {self.current_index + 1}/{len(self.cards)}", color=0xFFD700)
            embed.set_image(url=card_data["image_url"])

        await interaction.response.edit_message(embed=embed, view=self)


# Classe pour gérer l'affichage des cartes de la collection avec un select menu
class CollectionView(discord.ui.View):
    def __init__(self, cards):
        super().__init__()
        self.cards = sorted(cards, key=lambda x: int(x.split()[0]))  # Trier les cartes par numéro

        # Créer un select menu pour naviguer entre les cartes
        self.select_menu = discord.ui.Select(
            placeholder="Sélectionnez une carte...",
            options=[discord.SelectOption(label=card.capitalize(), value=card) for card in self.cards]
        )
        self.select_menu.callback = self.select_card
        self.add_item(self.select_menu)

    async def select_card(self, interaction: discord.Interaction):
        selected_card = self.select_menu.values[0]
        card_data = BOOSTERS["Pikachu"][selected_card]  # Remplacez "Pikachu" par le booster sélectionné
        embed = discord.Embed(title=f"🎴 {selected_card.capitalize()}", color=0xFFD700)
        embed.set_image(url=card_data["image_url"])
        await interaction.response.edit_message(embed=embed, view=self)

# Commande /collect modifiée pour utiliser un select menu
@bot.tree.command(name="collect", description="Voir votre collection de cartes Pokémon")
async def collect(interaction: discord.Interaction):
    user_id = interaction.user.id
    cursor.execute('SELECT card_name FROM user_collections WHERE user_id = ?', (user_id,))
    cards = [row[0] for row in cursor.fetchall()]

    if not cards:
        await interaction.response.send_message("Vous n'avez pas encore de cartes dans votre collection.", ephemeral=True)
        return

    # Création de l'embed initial avec le select menu
    view = CollectionView(cards)
    initial_card = cards[0]
    card_data = BOOSTERS["Pikachu"][initial_card]  # Remplacez "Pikachu" par le booster sélectionné
    embed = discord.Embed(title=f"🎴 {initial_card.capitalize()}", color=0xFFD700)
    embed.set_image(url=card_data["image_url"])
    await interaction.response.send_message(embed=embed, view=view)

# 📌 Événement de connexion du bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
