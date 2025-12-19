import pygame
import asyncio
import signal
import sys
import os
from screen import Screen
from sqlDB import save_game_data
from map_grid import extract_plants_from_map

async def main(pseudo):
    """Lancement de la boucle de gameplay"""
    pygame.init()
    
    flask_launch = os.environ.get('FLASK_LAUNCH', '0') == '1'
    game = Screen(pseudo, fullscreen=not flask_launch)
    
    game_task = asyncio.create_task(game.start())
    
    loop = asyncio.get_running_loop()
    
    def shutdown():
        print("🛑 Shutdown signal received")
        game.run = False 
        game_task.cancel() 
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)
    
    try:
        await game_task
    except asyncio.CancelledError:
        print("Game task cancelled")
    finally:
        plants_dict = extract_plants_from_map(game.lose)
        save_game_data(game.pseudo, plants_dict, [0])
        pygame.quit()

if __name__ == "__main__":
    asyncio.run(main('P1'))
