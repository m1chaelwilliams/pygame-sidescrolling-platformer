from pygame import Surface, Rect
from pygame.sprite import Sprite, Group
from pygame.event import Event
import pygame
from ..utils import Vec2

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
	def update(self, events: list[Event], held: dict) -> None:
		pass
	def draw(self, screen: Surface, offset: Vec2) -> None:
		temp_rect = self.rect.copy()
		temp_rect.x += offset.x
		temp_rect.y += offset.y

		screen.blit(self.image, temp_rect)

class Player(Entity):
	'''
	Class that the user controls.
	'''
	def __init__(
			self, 
			groups: list[Group], 
			image: Surface, 
			position: Vec2
		) -> None:
		super().__init__(groups, image, position)
	def update(self, events: list[Event], held: dict) -> None:
		if held[pygame.K_RIGHT]:
			self.rect.x += 5
		if held[pygame.K_LEFT]:
			self.rect.x -= 5