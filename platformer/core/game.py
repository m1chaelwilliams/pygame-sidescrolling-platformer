import pygame
from pygame import Surface, Rect
from pygame.time import Clock
from .tilemap import *
from .camera import Camera
from ..sprites import *
from ..utils.constants import *

def load_img_scaled(path: str, scale: float) -> Surface:
	return pygame.transform.scale_by(
		pygame.image.load(path).convert_alpha(),
		scale
	)

class Game:
	def __init__(self) -> None:
		pygame.init()
		self.screen: Surface = pygame.display.set_mode((600, 400))
		self.clock: Clock = Clock()
		self.running = True
		self.tilemap = None
		self.camera: Camera = Camera(Vec2.ZERO)
		self.player = None
	def run(self) -> None:
		self.setup()
		while self.running:
			dt = self.clock.tick(120) / 1000
			
			self.update(dt)
			self.draw()

			pygame.display.update()
		self.close()

	def setup(self) -> None:
		keymap = {
			1: Vec2(0,0),
			2: Vec2(1,0)
		}

		self.tilemap = TilemapBuilder()\
			.load_from_csv("data/map.csv")\
			.load_spritesheet("assets/spritesheet.png", 4)\
			.set_tilekeymap(keymap)\
			.build()
		
		self.player = Player(
			[],
			load_img_scaled("assets/player_static.png", 4),
			Vec2(0, -3),
			self.tilemap
		)
			
	def update(self, dt: float) -> None:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				self.running = False
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_q:
					self.running = False
					return
		
		# getting key held events
		held = pygame.key.get_pressed()
		# updating the player
		self.player.update(events, held, dt)

		# updating the camera offset
		self.camera.follow(self.player.rect, Vec2(*self.screen.get_size()))

	def draw(self) -> None:
		self.screen.fill('lightblue')

		# loop over tiles
		for pos, tile in self.tilemap.tiles.items():
			# if tile value is > 0 (0 being air)
			if tile > 0:
				# get the pixel destination pos
				dest_pos = Vec2(pos.x * TILESIZE, pos.y * TILESIZE)
				# adjust the position with the camera offset
				dest_pos += self.camera.offset

				# get texture coordinate of item
				spritesheet_pos = Vec2(*self.tilemap.keymap.get(tile, (0,0)))
				# convert texture coordinate to rect area
				rect_area = Rect(
					spritesheet_pos.x * TILESIZE,
					spritesheet_pos.y * TILESIZE,
					TILESIZE,
					TILESIZE
				)
				# draw the tile
				self.screen.blit(
					self.tilemap.spritesheet,
					dest_pos.as_tupi(),
					rect_area
				)

		
		self.player.draw(self.screen, self.camera.offset)

		# pygame.draw.rect(
		# 	self.screen,
		# 	'green',
		# 	Rect(
		# 		self.player.rect.x + self.camera.offset.x,
		# 		self.player.rect.y + self.camera.offset.y,
		# 		self.player.rect.width,
		# 		self.player.rect.height
		# 	),
		# 	2
		# )

		# for pos in self.player.intersecting_blocks:
		# 	rect = Rect(
		# 		pos.x * TILESIZE + self.camera.offset.x,
		# 		pos.y * TILESIZE + self.camera.offset.y,
		# 		TILESIZE,
		# 		TILESIZE
		# 	)

		# 	pygame.draw.rect(
		# 		self.screen,
		# 		'red',
		# 		rect,
		# 		2
		# 	)
	def close(self) -> None:
		pygame.quit()