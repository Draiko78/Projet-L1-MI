import sqlite3
import json

def init_db():
    connection = sqlite3.connect("Save.db")
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
    """Save game data with plants as dict {growth_state: positions_list}"""
    connection = sqlite3.connect("Save.db")
    cursor = connection.cursor()
    
    # Convert dict to JSON string
    plants_json = json.dumps(plants_dict)
    temps_json = json.dumps(temperatures)
    
    cursor.execute("""
        INSERT OR REPLACE INTO Sauvegarde 
        VALUES (?, ?, ?)
    """, (pseudo, plants_json, temps_json))
    
    connection.commit()
    connection.close()

def get_plants_dict(pseudo):
    """Get plants dict for a player"""
    connection = sqlite3.connect("Save.db")
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT plantes_positions 
        FROM Sauvegarde 
        WHERE pseudo = ?
    """, (pseudo,))
    
    result = cursor.fetchone()
    connection.close()
    
    if result and result[0]:
        # Load JSON (keys will be strings like '3', '4', '5')
        plants_dict_str_keys = json.loads(result[0])
        
        # Convert string keys back to integers
        plants_dict = {}
        for key_str, positions in plants_dict_str_keys.items():
            plants_dict[int(key_str)] = positions
        
        return plants_dict  # Returns dict with int keys: {3: [...], 4: [...], 5: [...]}
    
    return {}