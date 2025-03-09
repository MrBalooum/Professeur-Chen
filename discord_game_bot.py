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
        types = ", ".join([TYPES_FR.get(t["type"]["name"], t["type"]["name"]) for t in data["types"]])
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
            abilities.append(f"▫️ {ability_fr}")
        abilities_text = "\n".join(abilities)

        # 📌 Évolutions avec niveaux en français
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url)
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
            evolution_chain.append(f"{name_fr}{level_up}")
            evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

        evolution_text = " ➡️ ".join(evolution_chain)

        # 📌 Création de l'embed
        embed = discord.Embed(title=f"📜 {nom.capitalize()} (Génération {generation})", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)
        embed.add_field(name="🌟 Type(s)", value=types, inline=True)
        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=True)
        embed.add_field(name="📖 Pokédex", value=description, inline=False)
        embed.add_field(name="⭐ Talents", value=abilities_text, inline=False)
        embed.add_field(name="🌀 Évolutions", value=evolution_text, inline=False)

        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    except requests.exceptions.HTTPError:
        await interaction.response.send_message("❌ Erreur lors de la récupération des données.", ephemeral=True)
    except Exception:
        await interaction.response.send_message("❌ Une erreur est survenue.", ephemeral=True)

# 📌 Auto-complétion
@pokemon.autocomplete("nom")
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [name for name in POKEMON_LIST.keys() if current.lower() in name.lower()]
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]

# 📌 Événement de connexion du bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
