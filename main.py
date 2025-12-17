import asyncio
import pygame
from screen import Screen

pygame.init()
async def main():
  game = Screen()
  game.start()
  await asyncio.sleep(0)
  pygame.quit()

asyncio.run(main())
