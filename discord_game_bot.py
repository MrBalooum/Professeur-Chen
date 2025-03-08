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

if __name__ == "__main__":
    bot.run(TOKEN)
