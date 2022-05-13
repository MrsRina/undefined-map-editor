from .lib import math, pygame;
from .    import util, api;

# EU SOu GOSTOSA/
TAG = 0;
HEALTH = 1;
ID = 2;

# Modos do spawn point.
RESPAWN = 0;
MOB = 1;
PASSIVE = 2;

class Entity:
	def __init__(self, tag, id):
		self.prev_x = 0;
		self.prev_y = 0;

		self.last_tick_x = 0;
		self.last_tick_y = 0;

		self.rect = pygame.Rect(0, 0, 16, 30);

		self.visibility = True;
		self.alive = True;
		self.on_ground = False;
		self.collide_vertical = False;
		self.collide_horizontal = False;
		self.flying = False;
		self.air = False;
		self.phase = False;
		self.gravity = False;
		self.just_jump = False;

		self.motion_x = 0;
		self.motion_y = 0;

		self.angle = 0;
		self.ampl = 0.999;

		self.left = 0;
		self.right = 0;
		self.up = 0;
		self.down = 0;
		self.speed = 8;
		self.air_speed = 1;

		self.database = [tag, 20, id];
		self.animation = 0;

	def set_tag(self, tag):
		self.database[TAG] = tag;

	def get_tag(self):
		return self.database[TAG];

	def set_health(self, value):
		self.database[HEALTH] = util.clamp(value, 0, 20);

	def get_health(self):
		return self.database[HEALTH];

	def get_id(self):
		return self.database[ID];

	def set_size(self, w, h):
		self.w = w;
		self.h = h;

	def kill(self):
		self.set_health(0);
		self.alive = False;
		self.visibility = False;

	def set_velocity(self, left, right):
		self.left = left;
		self.right = right;

	def set_position(self, x, y):
		self.rect.x = x;
		self.rect.y = y;

	def respawn(self, default_position = None):
		self.set_health(20);
		self.alive = True;
		self.visibility = True;

	def collide(self, physic, objects, frustum):
		x = self.rect.x;
		y = self.rect.y;

	def jump(self):
		if self.on_ground:
			self.just_jump = True;
			self.on_ground = False;

	def update(self, objects, physic, partial_ticks, frustum):
		if not self.on_ground:
		 	self.angle, self.motion_y = util.add_angle_length(self.angle, self.motion_y, math.pi, physic.gravity);
		 	self.motion_y *= self.ampl;

		self.rect.x += self.motion_x * self.speed * physic.gravity * partial_ticks;
		self.rect.y += -math.cos(self.angle) * self.motion_y;

		self.prev_x = self.rect.x - frustum.x;
		self.prev_y = self.rect.y - frustum.y;

		self.on_ground = False;
		self.collide(physic, objects, frustum);

		self.motion_x = self.motion_x * 0.1;
		self.motion_y = self.motion_y * 0.1;

	def render(self, partial_ticks):
		if self.alive:
			api.OpenGL.fill_shape(self.prev_x, self.prev_y, self.rect.w, self.rect.h, [255, 0, 255, 100]);

class EntityPlayer(Entity):
	def __init__(self, tag, id):
		super().__init__(tag, id);

class SpawnPoint(Entity):
	def __init__(self, id):
		super().__init__("sp", id);

		self.mode = PASSIVE;
		self.stamp = api.TimerStamp();

	def read_context(self, player, history, current_map):
		if self.visibility and self.current_map is not None:
			if self.mode == PASSIVE:
				pass
