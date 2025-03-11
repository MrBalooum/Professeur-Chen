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
         "52": {
            "drop_rate": 0.02432,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/52.png",
            "allowed_positions" : [5, 6]
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
         "40": {
            "drop_rate": 0.00357,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/40.png",
            "allowed_positions" : [5, 6]
        },
         "41": {
            "drop_rate": 0.00333,
            "image_url": "https://raw.githubusercontent.com/MrBalooum/Professeur-Chen/refs/heads/Pokemon-Card/41.png",
            "allowed_positions" : [5, 6]
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

    # Création de l'embed pour afficher la première carte
    card_name = selected_cards[0]
    card_data = cards[card_name]  # Récupérer les données de la carte
    embed = discord.Embed(title=f"🎴 Carte 1/6", color=0xFFD700)
    embed.set_image(url=card_data["image_url"])  # Afficher l'image de la carte
    embed.add_field(name="Nom", value=card_name.capitalize(), inline=False)

    # Ajouter les boutons de navigation
    view = BoosterView(selected_cards)
    await interaction.response.send_message(embed=embed, view=view)

class BoosterView(discord.ui.View):
    def __init__(self, cards):
        super().__init__()
        self.cards = cards
        self.current_index = 0
        self.previous_button = discord.ui.Button(label="Précédent", style=discord.ButtonStyle.primary)
        self.next_button = discord.ui.Button(label="Suivant", style=discord.ButtonStyle.primary)
        self.previous_button.callback = self.previous
        self.next_button.callback = self.next
        self.add_item(self.previous_button)
        self.add_item(self.next_button)
        self.update_buttons()

    def update_buttons(self):
        # Désactiver les boutons "Précédent" et "Suivant" si nécessaire
        self.previous_button.disabled = (self.current_index == 0)
        self.next_button.disabled = (self.current_index == len(self.cards) - 1)

    async def previous(self, interaction: discord.Interaction):
        self.current_index -= 1
        await self.update_embed(interaction)

    async def next(self, interaction: discord.Interaction):
        self.current_index += 1
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        card_name = self.cards[self.current_index]
        card_data = BOOSTERS["Pikachu"][card_name]  # Remplacez "Pikachu" par le booster sélectionné
        embed = discord.Embed(title=f"🎴 Carte {self.current_index + 1}/{len(self.cards)}", color=0xFFD700)
        embed.set_image(url=card_data["image_url"])
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)


# 📌 Auto-complétion pour la commande /booster
@booster.autocomplete("nom")
async def booster_autocomplete(interaction: discord.Interaction, current: str):
    suggestions = [name for name in BOOSTERS.keys() if current.lower() in name.lower()]
    return [discord.app_commands.Choice(name=p, value=p) for p in suggestions[:10]]

class CollectionView(discord.ui.View):
    def __init__(self, cards, current_page=0, cards_per_page=6):
        super().__init__()
        self.cards = sorted(cards, key=lambda x: int(x.split()[0]))  # Trier les cartes par numéro
        self.current_page = current_page
        self.cards_per_page = cards_per_page
        self.total_pages = (len(self.cards) + cards_per_page - 1) // cards_per_page
        self.previous_button = discord.ui.Button(label="Page Précédente", style=discord.ButtonStyle.primary)
        self.next_button = discord.ui.Button(label="Page Suivante", style=discord.ButtonStyle.primary)
        self.previous_button.callback = self.previous_page
        self.next_button.callback = self.next_page
        self.add_item(self.previous_button)
        self.add_item(self.next_button)
        self.update_buttons()

    def update_buttons(self):
        # Désactiver les boutons "Page Précédente" et "Page Suivante" si nécessaire
        self.previous_button.disabled = (self.current_page == 0)
        self.next_button.disabled = (self.current_page == self.total_pages - 1)

    async def previous_page(self, interaction: discord.Interaction):
        self.current_page -= 1
        await self.update_embed(interaction)

    async def next_page(self, interaction: discord.Interaction):
        self.current_page += 1
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        start_index = self.current_page * self.cards_per_page
        end_index = start_index + self.cards_per_page
        cards_on_page = self.cards[start_index:end_index]

        embed = discord.Embed(title=f"🎴 Collection de Cartes (Page {self.current_page + 1}/{self.total_pages})", color=0xFFD700)
        for card_name in cards_on_page:
            card_data = BOOSTERS["Pikachu"][card_name]  # Remplacez "Pikachu" par le booster sélectionné
            embed.add_field(name=card_name.capitalize(), value=f"[Voir la Carte]({card_data['image_url']})", inline=False)

        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(name="collect", description="Voir votre collection de cartes Pokémon")
async def collect(interaction: discord.Interaction):
    user_id = interaction.user.id
    cursor.execute('SELECT card_name FROM user_collections WHERE user_id = ?', (user_id,))
    cards = [row[0] for row in cursor.fetchall()]

    if not cards:
        await interaction.response.send_message("Vous n'avez pas encore de cartes dans votre collection.", ephemeral=True)
        return

    # Création de l'embed pour afficher la première page de cartes
    view = CollectionView(cards)
    await view.update_embed(interaction)

@bot.tree.command(name="search", description="Rechercher une carte spécifique dans votre collection")
async def search(interaction: discord.Interaction, card_name: str):
    user_id = interaction.user.id
    cursor.execute('SELECT card_name FROM user_collections WHERE user_id = ? AND card_name LIKE ?', (user_id, f"%{card_name}%"))
    cards = [row[0] for row in cursor.fetchall()]

    if not cards:
        await interaction.response.send_message("Aucune carte trouvée dans votre collection.", ephemeral=True)
        return

    # Création de l'embed pour afficher les cartes trouvées
    embed = discord.Embed(title=f"🎴 Résultats de Recherche pour '{card_name}'", color=0xFFD700)
    for card in cards:
        card_data = BOOSTERS["Pikachu"][card]  # Remplacez "Pikachu" par le booster sélectionné
        embed.add_field(name=card.capitalize(), value=f"[Voir la Carte]({card_data['image_url']})", inline=False)

    await interaction.response.send_message(embed=embed)

# 📌 Événement de connexion du bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Pokémon Jaune"))
    await bot.tree.sync()
    print(f'✅ Connecté en tant que {bot.user}')

bot.run(TOKEN)
