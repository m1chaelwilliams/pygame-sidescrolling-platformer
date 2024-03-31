import pygame
from pygame import Surface, Rect
from pygame.time import Clock

class Game:
	def __init__(self) -> None:
		self.screen: Surface = pygame.display.set_mode((600, 400))
		self.clock: Clock = Clock()
		self.running = True
	def run(self) -> None:
		while self.running:
			self.update()
			self.draw()

			pygame.display.update()
			self.clock.tick(60)
		self.close()
	def update(self) -> None:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				self.running = False
	def draw(self) -> None:
		self.screen.fill('lightblue')
	def close(self) -> None:
		pygame.quit()