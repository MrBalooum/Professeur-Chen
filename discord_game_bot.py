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
POKEMON_LIST_FILE = "pokemon_names_fr.json"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 📥 Charger la liste des Pokémon en français avec debug
def load_pokemon_list():
    """ Charge les noms de Pokémon en français et vérifie s'ils existent. """
    if os.path.exists(POKEMON_LIST_FILE):
        print("✅ Chargement du fichier des noms de Pokémon en français...")
        with open(POKEMON_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    print("🔄 Génération du fichier des noms de Pokémon en français...")
    pokemon_list = {}

    response = requests.get("https://pokeapi.co/api/v2/pokemon-species?limit=1000")
    print(f"📡 Requête API PokeAPI status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        for species in data["results"]:
            name_en = species["name"]
            species_data = requests.get(species["url"]).json()
            name_fr = next((entry["name"] for entry in species_data["names"] if entry["language"]["name"] == "fr"), name_en)
            pokemon_list[name_fr] = name_en  # Stocke le FR -> EN

    # Sauvegarde en fichier JSON pour éviter de recharger
    with open(POKEMON_LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(pokemon_list, f, ensure_ascii=False, indent=4)

    print(f"✅ Fichier {POKEMON_LIST_FILE} généré avec {len(pokemon_list)} Pokémon en français.")
    return pokemon_list

POKEMON_LIST = load_pokemon_list()
print(f"📜 Liste chargée: {len(POKEMON_LIST)} Pokémon trouvés.")

# 📌 Auto-complétion des noms de Pokémon en français avec debug
@bot.tree.command(name="pokemon", description="Obtiens toutes les infos sur un Pokémon")
async def pokemon(interaction: discord.Interaction, nom: str):
    print(f"🔍 Recherche de {nom}...")
    
    if interaction.channel_id != CHANNEL_ID:
        print(f"❌ Commande refusée : Mauvais salon ({interaction.channel_id})")
        await interaction.response.send_message("❌ Commande interdite ici !", ephemeral=True)
        return

    # Trouver le nom anglais correspondant
    pokemon_name = POKEMON_LIST.get(nom)
    if not pokemon_name:
        print(f"❌ {nom} introuvable dans la liste !")
        await interaction.response.send_message("❌ Pokémon introuvable.", ephemeral=True)
        return

    print(f"✅ Pokémon trouvé : {nom} -> {pokemon_name}")

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"

    try:
        response = requests.get(url)
        species_response = requests.get(species_url)
        print(f"📡 API PokeAPI (Données Pokémon) status: {response.status_code}")
        print(f"📡 API PokeAPI (Espèce) status: {species_response.status_code}")

        response.raise_for_status()
        species_response.raise_for_status()

        data = response.json()
        species_data = species_response.json()

        # 📌 Infos générales
        sprite = data["sprites"]["front_default"]
        official_art = data["sprites"]["other"]["official-artwork"]["front_default"]
        types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
        weight = data["weight"] / 10  # kg
        height = data["height"] / 10  # mètres
        generation = species_data["generation"]["name"].replace("generation-", "").upper()
        description = next((entry["flavor_text"] for entry in species_data["flavor_text_entries"] if entry["language"]["name"] == "fr"), "Pas de description trouvée.")

        # 📌 Talents en français
        abilities = []
        for a in data["abilities"]:
            ability_url = a["ability"]["url"]
            ability_data = requests.get(ability_url).json()
            ability_fr = next((entry["name"] for entry in ability_data["names"] if entry["language"]["name"] == "fr"), a["ability"]["name"])
            abilities.append(ability_fr)
        abilities_text = ", ".join(abilities)

        # 📌 Création de l'embed
        embed = discord.Embed(title=f"📜 {nom.capitalize()} (Génération {generation})", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)
        embed.add_field(name="🌟 Type(s)", value=types, inline=True)
        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=True)
        embed.add_field(name="📖 Pokédex", value=description, inline=False)
        embed.add_field(name="⭐ Talents", value=abilities_text, inline=True)

        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erreur HTTP: {http_err}")
        await interaction.response.send_message("❌ Erreur lors de la récupération des données.", ephemeral=True)
    except Exception as e:
        print(f"❌ Erreur inconnue: {e}")
        await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

# 📌 Auto-complétion des noms de Pokémon en français avec debug
@pokemon.autocomplete("nom")
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    """ Renvoie une liste de suggestions de Pokémon en français. """
    print(f"🔍 Auto-complétion pour: {current}")
    suggestions = [name for name in POKEMON_LIST.keys() if current.lower() in name.lower()]
    print(f"📋 {len(suggestions)} suggestions trouvées.")
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]

# 📌 Événement de connexion du bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
