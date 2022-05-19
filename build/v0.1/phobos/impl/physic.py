from .lib import math, pygame;
from .    import api, util, universe;

"""
	This class contains static methods to manipule vectors.
"""
class Math:
	def vec2(x, y):
		return [x, y];

	def project(vertices, axis):
		dots = [Math.dot(vertex, axis) for vertex in vertices];
		return Math.vec2(min(dots), max(dots));

	def overlap(proj1, proj2):
		return min(proj1) <= max(proj2) and min(proj2) <= max(proj1);

	def add(vec1, vec2):
		return Math.vec2(vec1[0] + vec2[0], vec1[1] + vec2[1]);

	def subtract(vec1, vec2):
		return Math.vec2(vec1[0] - vec2[0], vec1[1] - vec2[1]);

	def square(n):
		return n * n;

	def dot(vec1, vec2):
		return (vec1[0] * vec2[0] + vec1[1] * vec2[1]);

	def cross(vec1, vec2):
		return (vec1[0] * vec2[1] - vec1[1] * vec2[0]);

	def length(vec):
		return math.sqrt(Math.square(vec[0]) + Math.square(vec[1]));

	def rotate(vec, vec_center, angle):
		x = vec[0] - vec_center[0];
		y = vec[1] - vec_center[1];

		matrix_rotation = [
			x * math.sin(a) - y * math.cos(a),
			x * math.cos(a) + y * math.cos(a)
		];

		return Math.add(matrix_rotation, vec_center);

	def normalize(vec):
		l = Math.length(vec);

		if l > 0:
			l = 1 / l;

		return Math.vec2(vec[0] * l, vec[1] * l);

	def distance(vec1, vec2):
		x = vec1[0] - vec2[0];
		y = vec1[1] - vec2[1]; 

		return math.sqrt(Math.square(x), Math.square(y));

class RigidShape:
	def __init__(self, center):
		self.center = center;
		self.angle = 0;
		self.gravity = False;
		self.type = "empty";
		self.collided = 0;

	def push(self, physic_manager):
		physic_manager.add(self);

	def update(self):
		self.collided = 0;

class Rectangle(RigidShape):
	def __init__(self, center, w, h):
		super().__init__(center);

		self.type = "rectangle";
		self.gravity = 0;
		self.spd = 0;
		self.sp = None;
		self.bound_radius = math.sqrt(w * w + h * h) / 2;

		self.w = w;
		self.h = h;

		self.vertex = [0, 0, 0, 0];
		self.face_normals = [0, 0, 0, 0];

		self.vertex[0] = Math.vec2(center[0] - w / 2, center[1] - h / 2);
		self.vertex[1] = Math.vec2(center[0] + w / 2, center[1] - h / 2);
		self.vertex[2] = Math.vec2(center[0] + w / 2, center[1] + h / 2);
		self.vertex[3] = Math.vec2(center[0] - w / 2, center[1] + h / 2);

		self.face_normals[0] = Math.normalize(Math.subtract(self.vertex[1], self.vertex[2]));
		self.face_normals[1] = Math.normalize(Math.subtract(self.vertex[2], self.vertex[3]));
		self.face_normals[2] = Math.normalize(Math.subtract(self.vertex[3], self.vertex[0]));
		self.face_normals[3] = Math.normalize(Math.subtract(self.vertex[0], self.vertex[1]));

	def move(self, vec):
		for i in range(0, 4):
			self.vertex[i] = Math.add(self.vertex[i], vec);

		self.center = Math.add(self.center, vec);
		return self;

	def rotate(self, angle):
		self.angle += angle;

		for i in range(0, 4):
			self.vertex[i] = Math.rotate(self.vertex[i], self.center, angle);

		self.face_normals[0] = Math.normalize(Math.subtract(self.vertex[1], self.vertex[2]));
		self.face_normals[1] = Math.normalize(Math.subtract(self.vertex[2], self.vertex[3]));
		self.face_normals[2] = Math.normalize(Math.subtract(self.vertex[3], self.vertex[0]));
		self.face_normals[3] = Math.normalize(Math.subtract(self.vertex[0], self.vertex[1]));

		return self;

	def collide_with_rect(self, rigid_shape_1):
		axes = self.face_normals + rigid_shape_1.face_normals;

		for axis in axes:
			proj1 = Math.project(self.vertex, axis);
			proj2 = Math.project(rigid_shape_1.vertex, axis);

			overlaping = Math.overlap(proj1, proj2);

			if not overlaping:
				return 0;

		return 1;

class Physic:
	def __init__(self, master):
		self.gravity = 0.9;
		self.shape_list = [];
		self.master = master;
		self.offset_ticks = 0;

	def add(self, rigidshape):
		self.shape_list.append(rigidshape);

	def apply_rect_clamp_collision(self, x, y, w, h, rect, diff):
		pass

	def update(self):
		for segment_shapes_1 in self.shape_list:
			segment_shapes_1.update();

			for segment_shapes_2 in self.shape_list:
				if segment_shapes_2 == segment_shapes_1:
					continue;

				if segment_shapes_1.type == "rectangle" and segment_shapes_2.type == "rectangle" and segment_shapes_1.collide_with_rect(segment_shapes_2):
					segment_shapes_1.collided = 1;

	def render(self, partial_ticks):
		key = pygame.key.get_pressed();

		if key[pygame.K_SPACE] and self.offset_ticks > 80:
			rect = Rectangle(Math.vec2(self.master.player.rect.x, self.master.player.rect.y), 200, 200);
			rect.push(self);
			self.offset_ticks = 0;

		self.offset_ticks += 1;

		for shapes in self.shape_list:
			if shapes.type == "rectangle":
				api.OpenGL.fill_rectangle(shapes, self.master.camera, (255, 255, 0 if shapes.collided else 255, 200));
			elif shapes.type == "circle":
				api.OpenGL.fill_arc(shapes, self.master.camera, (255, 255, 255, 200));

	def check(self, tile):
		return tile.get_name() != "player_spawn" and tile.get_name() != "mob_spawn" and tile.get_name() != "passive_spawn";