import discord
from discord.ext import commands
import psycopg2
import asyncio
import os
import json
import requests

# 🔧 Configuration du bot
TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
CHANNEL_ID = 1347496375390048349  # ID du salon autorisé
DELETE_DELAY = 60  # Suppression après 60 secondes

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 📌 Connexion à PostgreSQL
if DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require", client_encoding="UTF8")
    cursor = conn.cursor()
    conn.commit()
    print("✅ Connexion à la base de données réussie.")
else:
    print("❌ Erreur: Variable d'environnement `DATABASE_URL` introuvable.")

# 📥 Vérification et téléchargement de la liste des Pokémon
if not os.path.exists("pokemon_names.json"):
    print("📥 Téléchargement de la liste des Pokémon...")
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    if response.status_code == 200:
        data = response.json()
        POKEMON_LIST = [p["name"] for p in data["results"]]
        with open("pokemon_names.json", "w", encoding="utf-8") as f:
            json.dump(POKEMON_LIST, f, ensure_ascii=False, indent=4)
        print("✅ Liste des Pokémon téléchargée avec succès !")
    else:
        print("❌ Impossible de récupérer la liste des Pokémon.")
        POKEMON_LIST = []
else:
    with open("pokemon_names.json", "r", encoding="utf-8") as f:
        POKEMON_LIST = json.load(f)

# 📌 Commande /pokemon améliorée
@bot.tree.command(name="pokemon", description="Obtiens toutes les infos sur un Pokémon")
async def pokemon(interaction: discord.Interaction, nom: str):
    if interaction.channel_id != CHANNEL_ID:
        await interaction.response.send_message("❌ Commande interdite ici !", ephemeral=True)
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
        generation = species_data["generation"]["name"].replace("generation-", "").upper()

        # 📌 Statistiques de base
        stats = "\n".join([f"**{s['stat']['name'].capitalize()}** : {s['base_stat']}" for s in data["stats"]])

        # 📌 Talents spéciaux
        abilities = ", ".join([a["ability"]["name"].replace("-", " ").capitalize() for a in data["abilities"]])

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

        # 📌 Attaques (triées par catégorie)
        moves = {
            "Physique": [],
            "Spéciale": [],
            "Statut": []
        }
        
        for move in data["moves"]:
            move_name = move["move"]["name"].replace("-", " ").capitalize()
            move_url = move["move"]["url"]
            move_response = requests.get(move_url)
            
            if move_response.status_code == 200:
                move_data = move_response.json()
                category = move_data["damage_class"]["name"]
                if category == "physical":
                    moves["Physique"].append(move_name)
                elif category == "special":
                    moves["Spéciale"].append(move_name)
                else:
                    moves["Statut"].append(move_name)

        # 📌 Création de l'embed
        embed = discord.Embed(title=f"📜 {name} (Génération {generation})", color=0xFFD700)
        embed.set_thumbnail(url=sprite)
        embed.set_image(url=official_art)
        embed.add_field(name="🌟 Type(s)", value=types, inline=True)
        embed.add_field(name="⚖️ Taille & Poids", value=f"{height}m / {weight}kg", inline=True)
        embed.add_field(name="📖 Pokédex", value=description, inline=False)
        embed.add_field(name="⭐ Talents", value=abilities, inline=True)
        embed.add_field(name="🌀 Évolutions", value=evolution_text, inline=False)
        embed.add_field(name="📊 Statistiques", value=stats, inline=False)
        embed.add_field(name="⚔️ Attaques Physiques", value="\n".join(moves["Physique"][:5]) + "\n...", inline=False)
        embed.add_field(name="💥 Attaques Spéciales", value="\n".join(moves["Spéciale"][:5]) + "\n...", inline=False)
        embed.add_field(name="🛡️ Attaques Statut", value="\n".join(moves["Statut"][:5]) + "\n...", inline=False)

        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(DELETE_DELAY)
        await interaction.delete_original_response()

    else:
        await interaction.response.send_message("❌ Pokémon non trouvé !", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
