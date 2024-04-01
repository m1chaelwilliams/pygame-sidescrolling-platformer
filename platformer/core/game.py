import pygame
from pygame import Surface, Rect
from pygame.time import Clock
from .tilemap import *

class Game:
	def __init__(self) -> None:
		pygame.init()
		self.screen: Surface = pygame.display.set_mode((600, 400))
		self.clock: Clock = Clock()
		self.running = True
		self.tilemap = None
	def run(self) -> None:
		self.setup()
		while self.running:
			self.update()
			self.draw()

			pygame.display.update()
			self.clock.tick(60)
		self.close()

	def setup(self) -> None:
		keymap = {
			1: Vec2(0,0),
			2: Vec2(1,0)
		}

		self.tilemap = TilemapBuilder()\
			.load_from_csv("data/map.csv")\
			.load_spritesheet("assets/spritesheet.png", 4)\
			.set_tilesize(Vec2(32, 32))\
			.set_tilekeymap(keymap)\
			.build()
			
	def update(self) -> None:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				self.running = False
	def draw(self) -> None:
		self.screen.fill('lightblue')

		# loop over rows
		for y_index, row in enumerate(self.tilemap.tiles):
			# loop over cells in current row
			for x_index, item in enumerate(row):
				# if not air
				if item > 0:
					# get pixel destinate x and y
					x = x_index * self.tilemap.tilesize.x
					y = y_index * self.tilemap.tilesize.y
					# get texture coordinate of item
					spritesheet_pos = Vec2(*self.tilemap.keymap.get(item, (0,0)))
					# convert texture coordinate to rect area
					rect_area = Rect(
						spritesheet_pos.x * self.tilemap.tilesize.x,
						spritesheet_pos.y * self.tilemap.tilesize.y,
						self.tilemap.tilesize.x,
						self.tilemap.tilesize.y
					)
					# draw the tile
					self.screen.blit(
						self.tilemap.spritesheet, 
						(x, y), 
						rect_area
					)
	def close(self) -> None:
		pygame.quit()