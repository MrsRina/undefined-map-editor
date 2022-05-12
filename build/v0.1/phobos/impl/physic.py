from .lib import math, pygame;
from .    import api, util, universe;

class Vec2:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def set(self, x, y):
		self.x = x;
		self.y = y;

	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y);

	def add(self, vec):
		return Vec2(vec.x + self.x, vec.y + self.y);

	def subtract(self, vec):
		return Vec2(self.x - vec.x, self.y - vec.y);

	def scale(self, n):
		return Vec2(self.x * n, self.y * n);

	def dot(self, vec):
		return (self.x * vec.x + self.y * vec.y);

	def cross(self, vec):
		return (self.x * vec.y - self.y * vec.x);

	def rotate(self, center, angle):
		x = self.x - center.x;
		y = self.y - center.y;

		matrix_rotation = [0, 0];
		matrix_rotation[0] = x * math.cos(angle) - y * math.sin(angle);
		matrix_rotation[1] = x * math.sin(angle) + y * math.cos(angle);

		matrix_rotation[0] += center.x;
		matrix_rotation[1] += center.y;

		return Vec2(matrix_rotation[0], matrix_rotation[1]);

	def normalize(self):
		length = self.length();

		if length > 0:
			length = 1 / length;

		return self.scale(length);

	def distance(self, vec):
		x = self.x - vec.x;
		y = self.y - vec.y;

		return math.sqrt(self.x * self.x + self.y * self.y);

class RigidShape:
	def __init__(self, center):
		self.center = center;
		self.angle = 0;
		self.gravity = False;

	def push(self, physic_manager):
		physic_manager.add(self);

	def update(self):
		pass

class Rectangle(RigidShape):
	def __init__(self, center, w, h):
		super().__init__(center);

		self.type = "rectangle";
		self.gravity = 0;

		self.w = w;
		self.h = h;

		self.vertex = [0, 0, 0, 0];
		self.faceNormal = [0, 0, 0, 0];

		self.vertex[0] = Vec2(center.x - w / 2, center.y - h / 2);
		self.vertex[1] = Vec2(center.x + w / 2, center.y - h / 2);
		self.vertex[2] = Vec2(center.x + w / 2, center.y + h / 2);
		self.vertex[3] = Vec2(center.x - w / 2, center.y + h / 2);

		self.faceNormal[0] = self.vertex[1].subtract(self.vertex[2]);
		self.faceNormal[0] = self.faceNormal[0].normalize();
		self.faceNormal[1] = self.vertex[2].subtract(self.vertex[3]);
		self.faceNormal[1] = self.faceNormal[1].normalize();
		self.faceNormal[2] = self.vertex[3].subtract(self.vertex[0]);
		self.faceNormal[2] = self.faceNormal[2].normalize();
		self.faceNormal[3] = self.vertex[0].subtract(self.vertex[1]);
		self.faceNormal[3] = self.faceNormal[3].normalize();

	def move(self, vec):
		for i in range(0, 4):
			self.vertex[i] = self.vertex[i].add(vec);

		self.center.add(vec);
		return self;

	def rotate(self, angle):
		self.angle += angle;

		for i in range(0, 4):
			self.vertex[i] = self.vertex[i].rotate(self.center, angle);

		self.faceNormal[0] = self.vertex[1].subtract(self.vertex[2]);
		self.faceNormal[0] = self.faceNormal[0].normalize();
		self.faceNormal[1] = self.vertex[2].subtract(self.vertex[3]);
		self.faceNormal[1] = self.faceNormal[1].normalize();
		self.faceNormal[2] = self.vertex[3].subtract(self.vertex[0]);
		self.faceNormal[2] = self.faceNormal[2].normalize();
		self.faceNormal[3] = self.vertex[0].subtract(self.vertex[1]);
		self.faceNormal[3] = self.faceNormal[3].normalize();

		return self;

class Circle(RigidShape):
	def __init__(self, center, radius):
		super().__init__(center);

		self.type = "circle";
		self.gravity = 0;

		self.radius = radius;
		self.startpoint = Vec2(center.x, center.y - radius);

	def move(self, vec):
		self.startpoint = self.startpoint.add(vec);
		self.center = self.center.add(vec);
		return self;

	def rotate(self, angle):
		self.angle += angle;
		self.startpoint = self.startpoint.rotate(self.center, self.angle);
		return self;

class Physic:
	def __init__(self, master):
		self.gravity = 0.9;
		self.shape_list = [];
		self.master = master;

	def add(self, rigidShape):
		self.shape_list.append(rigidShape);

	def apply_rect_clamp_collision(self, x, y, w, h, rect, diff):
		if x <= diff:
			x = diff;

		if y <= diff:
			y = diff;

		if x + w >= rect.x + rect.w - diff:
			x = rect.x + rect.w - w - diff;

		if y + h >= rect.y + rect.h - diff:
			y = rect.y + rect.h - h - diff;

	def update(self):
		for shapes in self.shape_list:
			shapes.update();

	def render(self, partial_ticks):
		key = pygame.key.get_pressed();

		if key[pygame.K_SPACE]:
			rect = Rectangle(Vec2(self.master.player.rect.x, self.master.player.rect.y), 200, 200);
			rect.rotate(90);
			rect.push(self);

		for shapes in self.shape_list:
			if shapes.type == "rectangle":
				api.OpenGL.fill_rectangle(shapes, self.master.camera, (255, 255, 255, 200));
			elif shapes.type == "circle":
				api.OpenGL.fill_arc(shapes, self.master.camera, (255, 255, 255, 200));

	def check(self, tile):
		return tile.get_name() != "player_spawn" and tile.get_name() != "mob_spawn" and tile.get_name() != "passive_spawn";