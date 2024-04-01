from pygame import Rect
from ..utils import Vec2

class Camera:
	'''
	A class for managing the position of our camera in game.
	'''
	def __init__(self, init_pos: Vec2) -> None:
		self.offset = init_pos
	def follow(self, target: Rect, screen_size: Vec2) -> None:
		'''
		Follows the target rect (centered for now)
		'''
		self.offset = Vec2(
			-target.x + (screen_size.x / 2 - target.width / 2),
			-target.y + (screen_size.y / 2 - target.height / 2),
		)

	# convenience methods since we'll be applying the offset frequently
	def add_offset_coord(self, coord: Vec2) -> Vec2:
		return self.offset + coord
	def add_offset_rect(self, rect: Rect) -> Rect:
		return Rect(
			rect.x + self.offset.x,
			rect.y + self.offset.y,
			rect.width,
			rect.height
		)