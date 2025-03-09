import discord
from discord.ext import commands
import psycopg2
import asyncio
import os
import random
import re
from discord import app_commands
from discord.ext import tasks
import datetime

# Vérification et installation de requests si manquant
try:
    import requests
except ModuleNotFoundError:
    import subprocess
    subprocess.run(["pip", "install", "requests"])
    import requests

# Configuration du bot
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Connexion à PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode="require", client_encoding="UTF8")
cursor = conn.cursor()

conn.commit()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Erreur: La variable d'environnement TOKEN est introuvable ou vide.")
    exit(1)

print(f"✅ [DEBUG] TOKEN chargé correctement : {TOKEN[:5]}... (Masqué)")

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Pokemon Jaune"))

    if bot.user.name != "Professeur Chen":
        try:
            await bot.user.edit(username="Professeur Chen")
            print("✅ Nom du bot mis à jour !")
        except discord.errors.Forbidden:
            print("❌ Permission insuffisante pour changer le nom.")
        except discord.errors.HTTPException as e:
            print(f"❌ Impossible de changer le nom : {e}")

def save_database():
    """Sauvegarde immédiate des changements dans PostgreSQL."""
    conn.commit()
    print("📂 Base de données sauvegardée avec succès.")

print(f"[DEBUG] Token récupéré : {TOKEN is not None}")

import discord
import requests
import json
from discord import app_commands
import asyncio  # Ajout pour la suppression après un délai

TOKEN = "TON_TOKEN_ICI"
CHANNEL_ID = 1347496375390048349  # ID du salon autorisé
DELETE_DELAY = 60  # Temps en secondes avant suppression du message

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Charger la liste des Pokémon pour l'auto-complétion
with open("pokemon_names.json", "r", encoding="utf-8") as f:
    POKEMON_LIST = json.load(f)

# 📌 Commande avec auto-complétion et suppression automatique
@tree.command(name="pokemon", description="Obtiens toutes les infos sur un Pokémon")
async def pokemon(interaction: discord.Interaction, nom: str):
    if interaction.channel_id != CHANNEL_ID:
        await interaction.response.send_message("❌ Cette commande n'est pas autorisée ici !", ephemeral=True)
        return

    pokemon_name = nom.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"

    response = requests.get(url)
    species_response = requests.get(species_url)

    if response.status_code == 200 and species_response.status_code == 200:
        data = response.json()
        species_data = species_response.json()

        # 📌 Infos générales
        name = data["name"].capitalize()
        sprite = data["sprites"]["front_default"]
        official_art = data["sprites"]["other"]["official-artwork"]["front_default"]
        types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
        weight = data["weight"] / 10  # kg
        height = data["height"] / 10  # mètres
        description = next((entry["flavor_text"] for entry in species_data["flavor_text_entries"] if entry["language"]["name"] == "fr"), "Pas de description trouvée.")

        # 📌 Création de l'embed
        embed = discord.Embed(title=f"📜 {name}", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)
        embed.add_field(name="🌟 Type(s)", value=types, inline=True)
        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=True)
        embed.add_field(name="📖 Pokédex", value=description, inline=False)

        # 📌 Envoi du message et suppression après 60s
        message = await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    else:
        await interaction.response.send_message("❌ Pokémon non trouvé ! Vérifie l'orthographe.", ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()  # Synchroniser les commandes slash
    print(f'✅ Connecté en tant que {bot.user}')

if __name__ == "__main__":
    bot.run(TOKEN)
