import json
from collections import defaultdict

# Pfad zur JSON-Datei
daten_pfad = 'C:/Users/A200274497/OneDrive - Deutsche Telekom AG/Desktop/source/lena geburtstag/wab programm/sv3pt5.json'

# JSON-Datei lesen
with open(daten_pfad, 'r') as file:
    daten = json.load(file)

result = []
for pokemon in daten:
    # Stelle sicher, dass jedes Pokémon das Feld 'types' hat
    types = pokemon.get("types", [])
    
    # Füge das Pokémon zur Ergebnisliste hinzu
    entry = {
        "name": pokemon.get("name"),
        "hp": int(pokemon.get("hp", "0")),  # HP als int konvertieren für die Sortierung
        "pokedex": pokemon.get("nationalPokedexNumbers", []),
        "types": types,  # 'types' hinzufügen oder leere Liste verwenden
        "card_rarity": pokemon.get("rarity", "Unknown"),
        "nummer": pokemon.get("number"),
        "id_number": pokemon.get("id"),
        "evolve_state": pokemon.get("subtypes", [])
    }
    result.append(entry)

def bucket_sort_pokemon_by_type(pokemons):
    # Dictionary von Listen für die Buckets erstellen
    buckets = defaultdict(list)

    # Pokémon in die entsprechenden Buckets einfügen
    for pokemon in pokemons:
        for type_ in pokemon["types"]:
            buckets[type_].append(pokemon)
    
    # Sortieren der Pokémon innerhalb der Buckets nach Pokédex-Nummer und HP
    for key in buckets.keys():
        buckets[key] = bucket_sort_by_pokedex_hp(buckets[key])
    
    # Sammeln der sortierten Pokémon aus allen Buckets
    sorted_pokemons = []
    for key in sorted(buckets.keys()):  # Sortieren der Typen alphabetisch
        sorted_pokemons.extend(buckets[key])
    
    return sorted_pokemons

def bucket_sort_by_pokedex_hp(pokemons):
    # Finden der maximalen Pokédex-Nummer
    max_pokedex_num = 0
    for pokemon in pokemons:
        if pokemon["pokedex"]:
            max_pokedex_num = max(max_pokedex_num, pokemon["pokedex"][0])
    
    # Erstellen der Buckets
    buckets = [[] for _ in range(max_pokedex_num + 2)]  # +2, um Platz für die Pokédex-Nummern und -1 zu haben
    
    # Verteilen der Pokémon in die Buckets basierend auf der Pokédex-Nummer
    for pokemon in pokemons:
        if pokemon["pokedex"]:
            pokedex_num = pokemon["pokedex"][0]
        else:
            pokedex_num = max_pokedex_num + 1  # Keine Pokédex-Nummer -> in den letzten Bucket
        
        buckets[pokedex_num].append(pokemon)
    
    # Sortieren der Pokémon innerhalb der Buckets nach HP
    for bucket in buckets:
        if bucket:
            bucket_sort_by_hp(bucket)
    
    # Sammeln der sortierten Pokémon aus allen Buckets
    sorted_pokemons = []
    for bucket in buckets:
        sorted_pokemons.extend(bucket)
    
    return sorted_pokemons

def bucket_sort_by_hp(pokemons):
    # Einfaches Sortierverfahren für die HP
    n = len(pokemons)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if pokemons[j]["hp"] < pokemons[min_idx]["hp"]:
                min_idx = j
        pokemons[i], pokemons[min_idx] = pokemons[min_idx], pokemons[i]

# Pokémon nach Typen sortieren und nach Pokédex-Nummer und HP innerhalb jedes Typs sortieren
nachTypsortiert = bucket_sort_pokemon_by_type(result)

# Ergebnis ausgeben
for pokemon in nachTypsortiert:
    print(f"{pokemon['name']} - Types: {pokemon['types']} - {pokemon['hp']} - {pokemon['pokedex']} - {pokemon['evolve_state']}")

#- {pokemon['card_rarity']} - {pokemon['nummer']} - {pokemon['id_number']}