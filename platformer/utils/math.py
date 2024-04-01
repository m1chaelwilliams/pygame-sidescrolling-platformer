# Math utils that make life easier in the long run

from pygame.math import Vector2

class Vec2:
	'''
	Class for handling 2D vectors. In pygame, there are many instances where you need both
	a 2D vector of floats and a 2D vector of ints. This class alleviates the issue, by providing
	convenience conversions.

	- `.x` and `.y` for int representations
	- `.xf` and `.yf` for float representations
	- `.as_pgvec2`, `.as_tupi`, and `.as_tupf` for easy conversions
	- Operator overloads for comparisons
	- Bracket indexing: `[0]`, `[1]`
	'''
	def __init__(self, x: float, y: float) -> None:
		self._x = x
		self._y = y
	
	@property
	def x(self) -> int:
		return int(self._x)
	@x.setter
	def x(self, new_x: int):
		self._x = float(new_x)

	@property
	def y(self) -> int:
		return int(self._y)
	@y.setter
	def y(self, new_y: int):
		self._y = float(new_y)
	
	@property
	def xf(self) -> float:
		return self._x
	@xf.setter
	def xf(self, new_x: float):
		self._x = new_x

	@property
	def yf(self) -> float:
		return self._y
	@yf.setter
	def yf(self, new_y: float):
		self._y = new_y

	def __add__(self, other: 'Vec2') -> 'Vec2':
		return Vec2(
			self._x + other._x,
			self._y + other._y
		)
	def __sub__(self, other: 'Vec2') -> 'Vec2':
		return Vec2(
			self._x - other._x,
			self._y - other._y
		)
	def __eq__(self, other: 'Vec2') -> bool:
		return self._x == other._x and self._y == other._y
	def __ne__(self, other: 'Vec2') -> bool:
		return not self == other
	
	def __str__(self) -> str:
		f"x: {self._x}, y: {self._y}"

	def __getitem__(self, index) -> float:
		return self.as_tupf()[index]
	def __setitem__(self, index, val: float) -> None:
		if val == 0:
			self._x = val
		elif val == 1:
			self._y = val

	def __hash__(self) -> int:
		return hash((self._x, self._y))

	def as_pgvec2(self) -> Vector2:
		'''
		Converts `Vec2` to `pygame.math.Vector2`
		'''

		return Vector2(self._x, self._y)
	def as_tupi(self) -> tuple[int, int]:
		'''
		Returns int values for `x` and `y` in a tuple
		'''

		return (self.x, self.y)
	def as_tupf(self) -> tuple[float, float]:
		'''
		Returns float values for `x` and `y` in a tuple
		'''

		return (self._x, self._y)