from dataclasses import dataclass
from ..utils.math import *
import csv
from pygame.surface import Surface
import pygame

def csv_to_2dlist(filename: str) -> list[list[int]]:
	try:
		data = []

		with open(filename, 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				row = [int(cell) for cell in row]
				data.append(row)
		return data
	
	except ValueError:
		print(f"TILEMAP ERROR: File data is invalid, failed to parse: {filename}")
	except FileNotFoundError:
		print(f"TILEMAP ERROR: File does not exist: {filename}")
	except:
		print(f"TILEMAP ERROR: Failed to open file: {filename}")
	return [[]]

@dataclass
class Tilemap:
	tiles: list[list[int]] = None
	tilesize: Vec2 = None
	spritesheet: Surface = None
	keymap: dict[int, Vec2] = None

class TilemapBuilder:
	def __init__(self) -> None:
		self._tilemap = Tilemap()
	def load_from_csv(self, filepath: str) -> 'TilemapBuilder':
		self._tilemap.tiles = csv_to_2dlist(filepath)
		return self
	def load_spritesheet(self, filepath: str, scale: float) -> 'TilemapBuilder':
		self._tilemap.spritesheet = pygame.transform.scale_by(
			pygame.image.load(filepath).convert_alpha(),
			scale
		)
		return self
	def set_tilesize(self, tilesize: Vec2) -> 'TilemapBuilder':
		self._tilemap.tilesize = tilesize
		return self
	def set_tilekeymap(self, tilekeymap: dict[int, Vec2]) -> 'TilemapBuilder':
		self._tilemap.keymap = tilekeymap
		return self	
	def build(self) -> Tilemap:
		return self._tilemap