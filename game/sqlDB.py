import sqlite3
import json
import os

def init_db():
    """Créer la BDD si elle n'existe pas"""
    connection = sqlite3.connect("game/Database/Save.db")
    cursor = connection.cursor()
    requete = """CREATE TABLE IF NOT EXISTS Sauvegarde(
                    pseudo TEXT PRIMARY KEY,
                    plantes_positions TEXT,
                    recent_temperatures TEXT
                    )"""
    cursor.execute(requete)
    connection.commit()
    connection.close()

def save_game_data(pseudo, plants_dict, temperatures):
    """Sauvegarder les données"""
    connection = sqlite3.connect("game/Database/Save.db")
    cursor = connection.cursor()
    
    plants_json = json.dumps(plants_dict)
    temps_json = json.dumps(temperatures)
    
    cursor.execute("""
        INSERT OR REPLACE INTO Sauvegarde 
        VALUES (?, ?, ?)
    """, (pseudo, plants_json, temps_json))
    
    connection.commit()
    connection.close()

def get_plants_dict(pseudo):
    """Récupère les données"""
    connection = sqlite3.connect("game/Database/Save.db")
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT plantes_positions 
        FROM Sauvegarde 
        WHERE pseudo = ?
    """, (pseudo,))
    
    result = cursor.fetchone()
    connection.close()
    
    if result and result[0]:
        plants_dict_str_keys = json.loads(result[0])
        
        plants_dict = {}
        for key_str, positions in plants_dict_str_keys.items():
            plants_dict[int(key_str)] = positions
        
        return plants_dict 
    
    return {}
