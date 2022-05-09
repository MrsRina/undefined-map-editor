from .lib import math, pygame;
from .    import api, util, universe;

class Physic:
	def __init__(self, master):
		self.gravity = 0.9;

	def apply_rect_clamp_collision(self, x, y, w, h, rect, diff):
		if x <= diff:
			x = diff;

		if y <= diff:
			y = diff;

		if x + w >= rect.x + rect.w - diff:
			x = rect.x + rect.w - w - diff;

		if y + h >= rect.y + rect.h - diff:
			y = rect.y + rect.h - h - diff;

	def check(self, tile):
		return tile.get_name() != "player_spawn" and tile.get_name() != "mob_spawn" and tile.get_name() != "passive_spawn";