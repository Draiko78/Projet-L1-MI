from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import os
import signal
import time

app = Flask(__name__)

game_process = None

@app.route('/')
def index():
    """Afficher la page index.html avec les bouton jouer, arre^ter et supprimer la sauvegarde"""
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Lancement du jeu dans un Subprocess"""
    global game_process
    
    if game_process and game_process.poll() is None:
        return jsonify({'status': 'error', 'message': 'Le jeu est déjà lancé'})
    
    try:
        env = os.environ.copy()
        env['DISPLAY'] = ':0'  
        env['FLASK_LAUNCH'] = '1'  
        
        
        game_path = os.path.join(os.path.dirname(__file__), 'game', 'main.py')
        
        
        cmd = ['python3', game_path]
        
        game_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            env=env  
        )
        
     
        def log_output(pipe, prefix):
            for line in iter(pipe.readline, b''):
                if line:
                    print(f"{prefix}: {line.decode().strip()}")
        
        # Start threads to read output (so buffer doesn't fill up)
        threading.Thread(target=log_output, args=(game_process.stdout, "STDOUT"), daemon=True).start()
        threading.Thread(target=log_output, args=(game_process.stderr, "STDERR"), daemon=True).start()
        
        return jsonify({'status': 'success', 'message': 'Jeu lancé!'})
        
    except Exception as e:
        print(f"Error starting game: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_game', methods=['POST'])
def stop_game():
    """Arrêter le jeu"""
    global game_process
    
    if game_process and game_process.poll() is None:        
        game_process.terminate()
        try:           
            game_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            
            game_process.kill()
        
        return jsonify({'status': 'success', 'message': 'Jeu arrêté.'})
    
    return jsonify({'status': 'error', 'message': 'Aucun jeu lancé'})

@app.route('/game_status', methods=['GET'])
def game_status():
    """Vérifie si le jeu est bien lancé"""
    global game_process
    
    if game_process and game_process.poll() is None:
        return jsonify({'status': 'running'})
    else:
        return jsonify({'status': 'stopped'})
        
@app.route('/delete_save', methods=['POST'])
def delete_save():
    """Supprimer le fichier de sauvegarde"""
    try:
        save_path = 'game/Database/Save.db'
        
        if os.path.exists(save_path):
            os.remove(save_path)
            return jsonify({'status': 'success', 'message': 'Sauvegarde supprimée avec succès'})
        else:
            return jsonify({'status': 'error', 'message': 'Fichier de sauvegarde non trouvé'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
