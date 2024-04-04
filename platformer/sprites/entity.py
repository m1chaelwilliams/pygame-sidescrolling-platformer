from pygame import Surface, Rect
from pygame.sprite import Sprite, Group
from pygame.event import Event
import pygame
from ..utils import Vec2
from ..core.tilemap import Tilemap
from ..utils.constants import *
from dataclasses import dataclass

@dataclass
class PhysicsSettings:
	friction_divisor: float = 1.2
	gravity_constant: float = 5000
	terminal_velocity: float = 10000

class Entity(Sprite):
	'''
	Base class for all non-static sprites in-game.
	'''
	def __init__(
			self, 
			groups: list[Group],
			image: Surface,
			position: Vec2
		) -> None:
		super().__init__(groups)
		self.image = image
		self.rect = self.image.get_rect(topleft = position.as_tupi())
	def update(self, events: list[Event], held: dict, dt: float) -> None:
		pass
	def draw(self, screen: Surface, offset: Vec2) -> None:
		temp_rect = self.rect.copy()
		temp_rect.x += offset.x
		temp_rect.y += offset.y

		screen.blit(self.image, temp_rect)

class PhysicsEntity(Entity):
	def __init__(
			self, 
			groups: list[Group], 
			image: Surface, 
			position: Vec2,
			tilemap: Tilemap,
			velocity: Vec2,
			physics_settings: PhysicsSettings
		) -> None:
		super().__init__(groups, image, position)
		self.velocity: Vec2 = velocity
		self.physics_settings = physics_settings

		self.grounded: bool = False
		self.air_dt: float = 0
	def step_x(self, dt: float) -> None:
		self.rect.x += self.velocity.x * dt
	def step_y(self, dt: float) -> None:
		self.rect.y += self.velocity.y * dt
	def update_physics_state(self, dt: float) -> None:
		self.velocity.x /= self.physics_settings.friction_divisor
		if abs(self.velocity.x) < 100:
			self.velocity.x = 0

		self.v_acceleration = self.physics_settings.gravity_constant * self.air_dt
		self.velocity.y += self.v_acceleration * dt

		if not self.grounded:
			self.air_dt += dt
	def check_collisions_horizontal(self) -> list[Vec2]:
		if abs(self.velocity.x) < 0.01:
			return []

		intersecting_tiles: list[Vec2] = []
		# get intersection block positions... (could be turned into an algorithm, not necessary)
		for x in range(self.rect.width // TILESIZE + 1):
			for y in range(self.rect.height // TILESIZE + 1):					
				intersecting_tiles.append(Vec2(
					(self.rect.x + x*TILESIZE) // TILESIZE,
					(self.rect.y + y*(TILESIZE-1)) // TILESIZE,
				))
		# loop over intersecting blocks
		for pos in intersecting_tiles:
			# if tile exists
			if self.tilemap.tiles.get(pos, 0) > 0:
				# collision resolution
				if self.velocity.x > 0:
					self.rect.x = pos.x * TILESIZE - self.rect.width
				else:
					self.rect.x = pos.x * TILESIZE + TILESIZE
				self.velocity.x = 0
				return intersecting_tiles
		return intersecting_tiles
			
	def check_collisions_vertical(self) -> list[Vec2]:
		if abs(self.velocity.y) < 0.01:
			return []

		intersecting_tiles: list[Vec2] = []
		# get intersection block positions... (could be turned into an algorithm, not necessary)
		for x in range(self.rect.width // TILESIZE + 1):
			for y in range(self.rect.height // TILESIZE + 1):					
				intersecting_tiles.append(Vec2(
					(self.rect.x + x*(TILESIZE-1)) // TILESIZE,
					(self.rect.y + y*TILESIZE) // TILESIZE,
				))
		# loop over intersecting blocks
		collision = False
		for pos in intersecting_tiles:
			if self.tilemap.tiles.get(pos, 0) > 0:
				if self.velocity.y > 0:
					self.rect.y = pos.y * TILESIZE - self.rect.height
					collision = True
				else:
					self.rect.y = pos.y * TILESIZE + TILESIZE
				self.velocity.y = 0
				break
		self.grounded = collision
		return intersecting_tiles		

class Player(PhysicsEntity):
	'''
	Class that the user controls.
	'''
	def __init__(
			self, 
			groups: list[Group], 
			image: Surface, 
			position: Vec2,
			tilemap: Tilemap
		) -> None:
		super().__init__(groups, image, position, tilemap, Vec2.ZERO, PhysicsSettings())
		self.tilemap = tilemap
		self.velocity: Vec2 = Vec2.ZERO

		# state vars
		self.grounded = False
		self.time_since_grounded = 0
		# holds our intersecting blocks | could be local, but used for debugging
		self.intersecting_blocks: list[Vec2] = []
	def update(self, events: list[Event], held: dict, dt: float) -> None:
		space = False
		for e in events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					space = True
		
		if held[pygame.K_RIGHT]:
			self.velocity.x = 300
		if held[pygame.K_LEFT]:
			self.velocity.x = -300
		if space and self.grounded:
			self.air_dt = 0
			self.velocity.y = -500

		if not self.grounded:
			self.air_dt += dt

		self.update_physics_state(dt)

		self.step_x(dt)
		# check x collisions
		self.intersecting_blocks = self.check_collisions_horizontal()

		self.step_y(dt)
		# check y collisions
		self.intersecting_blocks = self.check_collisions_vertical()