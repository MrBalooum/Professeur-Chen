import logging
import sqlite3
import discord
from discord.ext import commands
import asyncio
import os
import json
import requests
import random

# 🔧 Configuration du bot
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1347496375390048349  # ID du salon autorisé pour /pokemon
DELETE_DELAY = 60  # Suppression après 60 secondes
POKEMON_LIST_FILE = "pokemon_names_fr.json"

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True  # Activer l'intent message_content
bot = commands.Bot(command_prefix="!", intents=intents)

# Connexion à la base de données SQLite
conn = sqlite3.connect('pokemon_collections.db')
cursor = conn.cursor()

# Créer la table user_collections si elle n'existe pas
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
    "PGO - Pokemon Go": {
        "PGO-064 - Capitaine Blanche": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-064-epee-et-bouclier-pokemon-go-capitaine-dequipe-blanche.webp",
            "allowed_positions" : [1]  
        },
         "PGO-065 - Capitaine Candale": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-065-epee-et-bouclier-pokemon-go-capitaine-dequipe-candela.webp",
            "allowed_positions" : [1] 
        },
         "PGO-066 - Incubateur D'oeufs": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-066-epee-et-bouclier-pokemon-go-incubateur-doeufs.webp",
            "allowed_positions" : [1] 
        },
        "PGO-067 - Module Leurre": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-067-epee-et-bouclier-pokemon-go-module-leurre.webp",
            "allowed_positions" : [1] 
        },
        "PGO-068 - Pokestop": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-068-epee-et-bouclier-pokemon-go-pokestop.webp",
            "allowed_positions" : [1] 
        },
         "PGO-069 - Super bonbon": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-069-epee-et-bouclier-pokemon-go-super-bonbon.webp",
            "allowed_positions" : [1] 
        },
         "PGO-070 Capitaine Spark": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-070-epee-et-bouclier-pokemon-go-capitaine-dequipe-spark.webp",
            "allowed_positions" : [1] 
        },
         "PGO-078 - Recherches professorales": {
            "drop_rate": 11,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-078-epee-et-bouclier-pokemon-go-recherches-professorales.webp",
            "allowed_positions" : [1] 
        },
         "PGO-082 - Capitaine Blanche Rare": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-082-epee-et-bouclier-pokemon-go-capitaine-dequipe-blanche.webp",
            "allowed_positions" : [1] 
        },
         "PGO-083 - Capitaine Candela Rare": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-083-epee-et-bouclier-pokemon-go-capitaine-dequipe-candela.webp",
            "allowed_positions" : [1] 
        },
         "PGO-084 - Recherches professorales Rare": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-084-epee-et-bouclier-pokemon-go-recherches-professorales.webp",
            "allowed_positions" : [1] 
        },
         "PGO-085 - Capitaine Spark Rare": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-085-epee-et-bouclier-pokemon-go-capitaine-dequipe-spark.webp",
            "allowed_positions" : [1] 
        },
############################################
         "PGO-001 - Bulbizarre": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-001-epee-et-bouclier-pokemon-go-bulbizarre.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-002 - Herbizarre": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-002-epee-et-bouclier-pokemon-go-herbizarre.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-006 - Mimigal": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-006-epee-et-bouclier-pokemon-go-mimigal.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-007 - Migalos": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-007-epee-et-bouclier-pokemon-go-migalos.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-008 - Salameche": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-008-epee-et-bouclier-pokemon-go-salameche.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-009 - Reptincel": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-009-epee-et-bouclier-pokemon-go-reptincel.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-013 - Chamallot": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-013-epee-et-bouclier-pokemon-go-chamallot.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-014 - Camerupt": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-014-epee-et-bouclier-pokemon-go-camerupt.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-015 - Carapuce": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-015-epee-et-bouclier-pokemon-go-carapuce.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-016 - Carabaffe": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-016-epee-et-bouclier-pokemon-go-carabaffe.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-019 - Ramoloss": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-019-epee-et-bouclier-pokemon-go-ramoloss.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-020 - Flagadoss": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-020-epee-et-bouclier-pokemon-go-flagadoss.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-021 - Magicarpe": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-021-epee-et-bouclier-pokemon-go-magicarpe.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-025 - Sovkipou": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-025-epee-et-bouclier-pokemon-go-sovkipou.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-027 - Pikachu": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-027-epee-et-bouclier-pokemon-go-pikachu.webp",
            "allowed_positions" : [2, 3, 4] 
        }, 
         "PGO-032 - Natu": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-032-epee-et-bouclier-pokemon-go-natu.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-033 - Xatu": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-033-epee-et-bouclier-pokemon-go-xatu.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-034 - Seleroc": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-034-epee-et-bouclier-pokemon-go-seleroc.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-036 - Onix": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-036-epee-et-bouclier-pokemon-go-onix.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-037 - Embrylex": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-037-epee-et-bouclier-pokemon-go-embrylex.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-038 - Ymphect": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-038-epee-et-bouclier-pokemon-go-ymphect.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-039 - Solaroc": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-039-epee-et-bouclier-pokemon-go-solaroc.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-041 - Rattata d'Alola": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-041-epee-et-bouclier-pokemon-go-rattata-dalola.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-042 - Rattatac d'Alola": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-042-epee-et-bouclier-pokemon-go-rattatac-dalola.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-044 - Steelix": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-044-epee-et-bouclier-pokemon-go-steelix.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-045 - Meltan": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-045-epee-et-bouclier-pokemon-go-meltan.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-051 - Leveinard": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-051-epee-et-bouclier-pokemon-go-leveinard.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-054 - Evoli": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-054-epee-et-bouclier-pokemon-go-evoli.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-056 - Capumain": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-056-epee-et-bouclier-pokemon-go-capumain.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-057 - Capidextre": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-057-epee-et-bouclier-pokemon-go-capidextre.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-059 - Keunotor": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-059-epee-et-bouclier-pokemon-go-keunotor.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-060 - Castorno": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-060-epee-et-bouclier-pokemon-go-castorno.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-061 - Poichigeon": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-061-epee-et-bouclier-pokemon-go-poichigeon.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-062 - Colombeau": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-062-epee-et-bouclier-pokemon-go-colombeau.webp",
            "allowed_positions" : [2, 3, 4] 
        },
         "PGO-063 - Deflaisan": {
            "drop_rate": 2.857,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-063-epee-et-bouclier-pokemon-go-deflaisan.webp",
            "allowed_positions" : [2, 3, 4] 
        },
############################################
        
        "PGO-003 - Florizarre": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-003-epee-et-bouclier-pokemon-go-florizarre.webp",
            "allowed_positions" : [5, 6]
        },
        "PGO-005 - Noadkoko D'Alola V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-005-epee-et-bouclier-pokemon-go-noadkoko-dalola-v.webp",
            "allowed_positions" : [5, 6]
        },
        "PGO-010 - Dracaufeu": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-010-epee-et-bouclier-pokemon-go-dracaufeu.webp",
            "allowed_positions" : [5, 6]
        },
        "PGO-012 - Sulfura": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-012-epee-et-bouclier-pokemon-go-sulfura.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-017 - Tortank": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-017-epee-et-bouclier-pokemon-go-tortank.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-022 - Leviator": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-022-epee-et-bouclier-pokemon-go-leviator.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-023 - Lokhlass": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-023-epee-et-bouclier-pokemon-go-lokhlass.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-024 - Artikodin": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-024-epee-et-bouclier-pokemon-go-artikodin.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-026 - Sarmurai": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-026-epee-et-bouclier-pokemon-go-sarmurai.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-028 - Pikachu": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-028-epee-et-bouclier-pokemon-go-pikachu.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-029 - Electhor": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-029-epee-et-bouclier-pokemon-go-electhor.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-030 - Mewtwo": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-030-epee-et-bouclier-pokemon-go-mewtwo-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-035 - Nymphali": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-035-epee-et-bouclier-pokemon-go-nymphali.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-040 - Betochef": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-040-epee-et-bouclier-pokemon-go-betochef-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-043 - Tyranocif": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-043-epee-et-bouclier-pokemon-go-tyranocif.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-046 - Melmetal": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-046-epee-et-bouclier-pokemon-go-melmetal.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-047 - Melmetal V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-047-epee-et-bouclier-pokemon-go-melmetal-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-049 - Dracolosse V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-049-epee-et-bouclier-pokemon-go-dracolosse-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-052 - Leuphorie": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-052-epee-et-bouclier-pokemon-go-leuphorie.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-053 - Metamorph": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-053-epee-et-bouclier-pokemon-go-metamorph.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-055 - Ronflex": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-055-epee-et-bouclier-pokemon-go-ronflex.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-058 - Monaflemit V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-058-epee-et-bouclier-pokemon-go-monaflemit-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-071 - Noardkoko d'Alola V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-071-epee-et-bouclier-pokemon-go-noadkoko-dalola-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-072 - Mewtwo V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-072-epee-et-bouclier-pokemon-go-mewtwo-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-073 - Betochef V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-073-epee-et-bouclier-pokemon-go-betochef-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-074 - Betochef V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-074-epee-et-bouclier-pokemon-go-betochef-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-075 - Melmetal V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-075-epee-et-bouclier-pokemon-go-melmetal-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-076 - Dracolosse V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-076-epee-et-bouclier-pokemon-go-dracolosse-v.webp",
            "allowed_positions" : [5, 6]
        },
         "PGO-077 - Monaflemit V": {
            "drop_rate": 3,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-077-epee-et-bouclier-pokemon-go-monaflemit-v.webp",
            "allowed_positions" : [5, 6]
        },
        
############################################
        "PGO-004 - Florizarre Radieux": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-004-epee-et-bouclier-pokemon-go-florizarre-radieux.webp",
            "allowed_positions" : [6]
        },    
         "PGO-011 - Dracaufeu Radieux": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-011-epee-et-bouclier-pokemon-go-dracaufeu-radieux.webp",
            "allowed_positions" : [6]
        },
         "PGO-018 - Tortank Radieux": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-018-epee-et-bouclier-pokemon-go-tortank-radieux.webp",
            "allowed_positions" : [6]
        },
         "PGO-031 - Mewtwo VStar": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-031-epee-et-bouclier-pokemon-go-mewtwo-vstar.webp",
            "allowed_positions" : [6]
        },
         "PGO-048 - Melmetal VMax": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-048-epee-et-bouclier-pokemon-go-melmetal-vmax.webp",
            "allowed_positions" : [6]
        },
         "PGO-050 - Dracolosse VStar": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-050-epee-et-bouclier-pokemon-go-dracolosse-vstar.webp",
            "allowed_positions" : [6]
        },
         "PGO-079 - Mewtwo VStar": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-079-epee-et-bouclier-pokemon-go-mewtwo-vstar.webp",
            "allowed_positions" : [6]
        },
         "PGO-080 - Melmetal VMax ": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-080-epee-et-bouclier-pokemon-go-melmetal-vmax.webp",
            "allowed_positions" : [6]
        },
         "PGO-081 - Dracolosse VStar": {
            "drop_rate": 1.15,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-081-epee-et-bouclier-pokemon-go-dracolosse-vstar.webp",
            "allowed_positions" : [6]
        },   
############################################
         "PGO-086 - Unique Mewtwo VStar": {
            "drop_rate": 0.8833,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-086-epee-et-bouclier-pokemon-go-mewtwo-vstar.webp",
            "allowed_positions" : [6]
        }, 
         "PGO-087 - Unique Incubateur d'oeufs": {
            "drop_rate": 0.8833,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-087-epee-et-bouclier-pokemon-go-incubateur-doeufs.webp",
            "allowed_positions" : [6]
        },
         "PGO-088 - Unique Module leurre": {
            "drop_rate": 0.8833,
            "image_url": "https://static.pkmcards.fr/cards/fr/pgo/image-cartes-a-collectionner-pokemon-card-game-tcg-pkmcards-pgo-fr-088-epee-et-bouclier-pokemon-go-module-leurre.webp",
            "allowed_positions" : [6]
        },
 ############################################=
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

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# Commande /booster pour ouvrir un booster de cartes Pokémon
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
            weights = [cards[card]["drop_rate"] for card in eligible_cards]
            selected_card = random.choices(eligible_cards, weights=weights)[0]
            selected_cards.append(selected_card)
        else:
            selected_card = random.choices(list(cards.keys()), weights=[data["drop_rate"] for data in cards.values()])[0]
            selected_cards.append(selected_card)

    # Insérer les cartes sélectionnées dans la collection de l'utilisateur
    user_id = interaction.user.id
    for card_name in selected_cards:
        cursor.execute('INSERT OR IGNORE INTO user_collections (user_id, card_name) VALUES (?, ?)', (user_id, card_name))
        print(f"Inserted card: {card_name} for user: {user_id}")  # Ajout du print statement
    conn.commit()

    # URL de l'image du booster en fonction du nom du booster
    if nom == "PGO - Pokemon Go":
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/Pokemon_go.png"
    elif nom == "Dialga":
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/dialga.png"
    elif nom == "Mewtwo":
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/mewtwo.png"
    else:
        booster_image_url = "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/default.png"

    # Création de l'embed initial avec l'image du booster
    embed = discord.Embed(title="🎁 Booster Fermé", color=0xFFD700)
    embed.set_image(url=booster_image_url)

    # Ajouter le bouton "Ouvrir"
    view = BoosterView(selected_cards, booster_image_url, nom)
    await interaction.response.send_message(embed=embed, view=view)

# Auto-complétion pour la commande /booster
@booster.autocomplete("nom")
async def booster_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [name for name in BOOSTERS.keys() if current.lower() in name.lower()]
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]
    
class BoosterView(discord.ui.View):
    def __init__(self, cards, booster_image_url, booster_name):
        super().__init__()
        self.cards = cards
        self.booster_image_url = booster_image_url
        self.booster_name = booster_name
        self.current_index = 0
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
            card_data = BOOSTERS[self.booster_name][card_name]
            embed = discord.Embed(title=f" Carte {self.current_index + 1}/{len(self.cards)}", color=0xFFD700)
            embed.set_image(url=card_data["image_url"])

            # Vérifier si la carte est déjà dans la collection de l'utilisateur
            user_id = interaction.user.id
            cursor.execute('SELECT 1 FROM user_collections WHERE user_id = ? AND card_name = ?', (user_id, card_name))
            result = cursor.fetchone()
            print(f"Checking card {card_name} for user {user_id}: {result}")  # Ajout du print statement
            if result:
                embed.set_footer(text="Déjà possédée ❌", icon_url="https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/pokeball.png")
            else:
                embed.set_footer(text="✅ New !")

        await interaction.response.edit_message(embed=embed, view=self)

# Configurer le logging
logging.basicConfig(level=logging.INFO)

class CollectionView(discord.ui.View):
    def __init__(self, cards):
        super().__init__()
        self.cards = sorted(cards, key=lambda x: self.extract_number(x))  # Trier les cartes par numéro si possible

        # Créer un select menu pour naviguer entre les cartes
        self.select_menu = discord.ui.Select(
            placeholder="Sélectionnez une carte...",
            options=[discord.SelectOption(label=card[:25].capitalize(), value=card) for card in self.cards]
        )
        self.select_menu.callback = self.select_card
        self.add_item(self.select_menu)

    def extract_number(self, card_name):
        # Extraire le numéro de la carte si possible
        parts = card_name.split('-')
        if len(parts) > 1:
            try:
                return int(parts[1].split('/')[0])
            except ValueError:
                return float('inf')  # Retourner l'infini si la conversion échoue
        return float('inf')  # Retourner l'infini si aucun numéro n'est trouvé

    async def select_card(self, interaction: discord.Interaction):
        selected_card = self.select_menu.values[0]
        # Vérifiez si la carte existe dans le booster
        if selected_card in BOOSTERS["PGO - Pokemon Go"]:
            card_data = BOOSTERS["PGO - Pokemon Go"][selected_card]
            embed = discord.Embed(title=f" {selected_card.capitalize()}", color=0xFFD700)
            embed.set_image(url=card_data["image_url"])

            # Vérifier si la carte est déjà dans la collection de l'utilisateur
            user_id = interaction.user.id
            cursor.execute('SELECT 1 FROM user_collections WHERE user_id = ? AND card_name = ?', (user_id, selected_card))
            result = cursor.fetchone()
            print(f"Checking card {selected_card} for user {user_id}: {result}")  # Ajout du print statement
            if result:
                embed.set_footer(text="Déjà possédée ❌", icon_url="https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/pokeball.png")
            else:
                embed.set_footer(text="✅ New !")

            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Carte introuvable dans le booster.", ephemeral=True)
            
# Commande /collect pour voir la collection de cartes Pokémon de l'utilisateur
@bot.tree.command(name="collect", description="Voir votre collection de cartes Pokémon")
async def collect(interaction: discord.Interaction):
    user_id = interaction.user.id
    cursor.execute('SELECT card_name FROM user_collections WHERE user_id = ?', (user_id,))
    cards = [row[0] for row in cursor.fetchall()]
    print(f"Cards retrieved for user {user_id}: {cards}")  # Ajout du print statement

    if not cards:
        await interaction.response.send_message("Vous n'avez pas encore de cartes dans votre collection.", ephemeral=True)
        return

    # Création de l'embed initial avec le select menu
    view = CollectionView(cards)
    initial_card = cards[0]
    card_data = BOOSTERS["PGO - Pokemon Go"][initial_card]  # Remplacez "PGO - Pokemon Go" par le booster sélectionné
    embed = discord.Embed(title=f" {initial_card.capitalize()}", color=0xFFD700)
    embed.set_image(url=card_data["image_url"])
    await interaction.response.send_message(embed=embed, view=view)
        
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
