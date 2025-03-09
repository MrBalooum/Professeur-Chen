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

# 📥 Charger la liste des Pokémon pour l'auto-complétion
POKEMON_LIST_FILE = "pokemon_names.json"

def load_pokemon_list():
    if not os.path.exists(POKEMON_LIST_FILE):
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
        if response.status_code == 200:
            data = response.json()
            pokemon_list = [p["name"] for p in data["results"]]
            with open(POKEMON_LIST_FILE, "w", encoding="utf-8") as f:
                json.dump(pokemon_list, f, ensure_ascii=False, indent=4)
            return pokemon_list
    else:
        with open(POKEMON_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

POKEMON_LIST = load_pokemon_list()

# 📌 Commande /pokemon améliorée
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
        generation = species_data["generation"]["name"].replace("generation-", "").upper()
        description = next((entry["flavor_text"] for entry in species_data["flavor_text_entries"] if entry["language"]["name"] == "fr"), "Pas de description trouvée.")

        # 📌 Statistiques de base
        stats = "\n".join([f"**{s['stat']['name'].capitalize()}** : {s['base_stat']}" for s in data["stats"]])

        # 📌 Talents spéciaux
        abilities = ", ".join([a["ability"]["name"].replace("-", " ").capitalize() for a in data["abilities"]])

        # 📌 Ratio de genre
        gender_ratio = species_data["gender_rate"]
        if gender_ratio == -1:
            gender_text = "Asexué"
        else:
            male_chance = round((8 - gender_ratio) / 8 * 100)
            female_chance = 100 - male_chance
            gender_text = f"♂️ {male_chance}% / ♀️ {female_chance}%"

        # 📌 Groupes d'œufs
        egg_groups = ", ".join([egg["name"].capitalize() for egg in species_data["egg_groups"]])

        # 📌 Taux de capture et bonheur
        capture_rate = species_data["capture_rate"]
        base_happiness = species_data["base_happiness"]

        # 📌 Évolutions
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url)
        evolution_data = evolution_response.json()
        evolution_chain = []
        evo_stage = evolution_data["chain"]

        while evo_stage:
            evolution_chain.append(evo_stage["species"]["name"].capitalize())
            evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

        evolution_text = " ➡️ ".join(evolution_chain)

        # 📌 Création de l'embed
        embed = discord.Embed(title=f"📜 {name} (Génération {generation})", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)
        embed.add_field(name="🌟 Type(s)", value=types, inline=True)
        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=True)
        embed.add_field(name="📖 Pokédex", value=description, inline=False)
        embed.add_field(name="⭐ Talents", value=abilities, inline=True)
        embed.add_field(name="♂️♀️ Ratio de genre", value=gender_text, inline=True)
        embed.add_field(name="🍃 Groupes d'œufs", value=egg_groups, inline=True)
        embed.add_field(name="🎯 Taux de capture", value=f"{capture_rate}/255", inline=True)
        embed.add_field(name="💖 Bonheur initial", value=f"{base_happiness}", inline=True)
        embed.add_field(name="🌀 Évolutions", value=evolution_text, inline=False)
        embed.add_field(name="📊 Statistiques", value=stats, inline=False)

        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    except requests.exceptions.HTTPError as http_err:
        await interaction.response.send_message("❌ Erreur lors de la récupération des données.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

# 📌 Auto-complétion des noms de Pokémon
@pokemon.autocomplete("nom")
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [p for p in POKEMON_LIST if current.lower() in p.lower()]
    return [discord.app_commands.Choice(name=p.capitalize(), value=p.lower()) for p in suggestions[:10]]

# 📌 Événement de connexion du bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
