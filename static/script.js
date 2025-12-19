let gameStatusInterval;

function updateGameStatus() {
    fetch('/game_status')
        .then(response => response.json())
        .then(data => {
            const statusDiv = document.getElementById('status');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            
            if (data.status === 'running') {
                statusDiv.textContent = 'Etat du jeu : Lancé';
                statusDiv.className = 'status running';
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                statusDiv.textContent = 'Etat du jeu : Arrêté';
                statusDiv.className = 'status stopped';
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        })
        .catch(error => {
            console.error('Error checking game status:', error);
        });
}

function startGame() {
    document.getElementById('message').textContent = 'Lancement du jeu...';
    
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
        updateGameStatus();
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
    });
}

function stopGame() {
    document.getElementById('message').textContent = 'Arrêt du jeu...';
    
    fetch('/stop_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
        updateGameStatus();
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
    });
}

function deleteSave() {
    if (!confirm('Êtes-vous sûr de vouloir supprimer la sauvegarde ? Cette action est irréversible.')) {
        return;
    }
    
    document.getElementById('message').textContent = 'Suppression de la sauvegarde...';
    
    fetch('/delete_save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
    });
}

gameStatusInterval = setInterval(updateGameStatus, 2000);

updateGameStatus();

window.addEventListener('beforeunload', () => {
    clearInterval(gameStatusInterval);
});
