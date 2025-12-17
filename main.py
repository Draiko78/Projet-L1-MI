import asyncio
import pygame
from screen import Screen

pygame.init()
async def main():
  game = Screen()
  game.start()

  pygame.quit()

asyncio.run(main())
