import discord
from discord.ext import commands
import asyncio
import os
import json
import requests

# 🔧 Configuration du bot
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1347496375390048349  # ID du salon autorisé
DELETE_DELAY = 60  # Suppression après 60 secondes

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 📥 Vérification et téléchargement de la liste des Pokémon
POKEMON_LIST_FILE = "pokemon_names.json"

def load_pokemon_list():
    if not os.path.exists(POKEMON_LIST_FILE):
        print("📥 Téléchargement de la liste des Pokémon...")
        try:
            response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
            response.raise_for_status()
            data = response.json()
            pokemon_list = [p["name"] for p in data["results"]]
            with open(POKEMON_LIST_FILE, "w", encoding="utf-8") as f:
                json.dump(pokemon_list, f, ensure_ascii=False, indent=4)
            print("✅ Liste des Pokémon téléchargée avec succès !")
            return pokemon_list
        except Exception as e:
            print(f"❌ Erreur de récupération de la liste des Pokémon : {e}")
            return []
    else:
        with open(POKEMON_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

POKEMON_LIST = load_pokemon_list()

# 📌 Commande /pokemon
@bot.tree.command(name="pokemon", description="Obtiens toutes les infos sur un Pokémon")
async def pokemon(interaction: discord.Interaction, nom: str):
    if interaction.channel_id != CHANNEL_ID:
        await interaction.response.send_message("❌ Commande interdite ici !", ephemeral=True)
        return

    pokemon_name = nom.lower()
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

        # 📌 Envoi et suppression après 60s
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erreur HTTP : {http_err}")
        await interaction.response.send_message("❌ Erreur lors de la récupération des données.", ephemeral=True)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

# 📌 Auto-complétion des noms de Pokémon
@pokemon.autocomplete("nom")
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [p for p in POKEMON_LIST if current.lower() in p.lower()]
    return [discord.app_commands.Choice(name=p.capitalize(), value=p.lower()) for p in suggestions[:10]]

# 📌 Événement de connexion du bot + Changer son statut
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))  # 🔥 Le bot affiche "Joue à Pokémon Jaune"
        print(f'✅ Connecté en tant que {bot.user} et commandes synchronisées !')
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes : {e}")

# 📌 Démarrer le bot
if __name__ == "__main__":
    bot.run(TOKEN)
