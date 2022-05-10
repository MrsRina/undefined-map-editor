from .lib import pygame, GL11, math, os, Flag, json, threading, time;
from .    import util;

# Up == Pular
class InputManager:
	def __init__(self, master):
		self.master = master;
		self.entity_in = None;

		self.motion = 0;
		self.left = False;
		self.right = False;
		self.up = False;
		self.down = False;

		self.synced_keybind_left = -1;
		self.synced_keybind_right = -1;
		self.synced_keybind_up = -1;
		self.synced_keybind_down = -1;

		self.synced = False;

	def on_mouse_event(self, mx, my, button, state):
		pass;

	def on_key_event(self, key, state):
		if key == self.synced_keybind_left and state == Flag.KEYDOWN:
			self.left = True;

		if key == self.synced_keybind_left and state == Flag.KEYUP:
			self.left = False;

		if key == self.synced_keybind_right and state == Flag.KEYDOWN:
			self.right = True;

		if key == self.synced_keybind_right and state == Flag.KEYUP:
			self.right = False;

		if key == self.synced_keybind_up and state == Flag.KEYDOWN:
			self.up = True;

		if key == self.synced_keybind_up and state == Flag.KEYUP:
			self.up = False;

		if key == self.synced_keybind_down and state == Flag.KEYDOWN:
			self.down = True;

		if key == self.synced_keybind_down and state == Flag.KEYUP:
			self.down = False;

	def update(self):
		if self.synced is False:
			self.motion = self.master.game_settings.setting_keybind.value("mouse-motion");

			self.synced_keybind_left = self.master.game_settings.setting_keybind.value("left");
			self.synced_keybind_right = self.master.game_settings.setting_keybind.value("right");
			self.synced_keybind_up = self.master.game_settings.setting_keybind.value("up");
			self.synced_keybind_down = self.master.game_settings.setting_keybind.value("down");

			self.synced = True;

		if self.entity_in is not None:
			if self.motion == 0 or motion == 3:
				self.entity_in.motion_x = 0;

				self.entity_in.motion_x = -1 if self.left else self.entity_in.motion_x;
				self.entity_in.motion_x = 1 if self.right else self.entity_in.motion_x;

			if self.motion >= 1:
				x, y = pygame.mouse.get_rel();

				self.entity_in.left = -util.lerp(self.entity_in.left, 1 if x < 0 else 0, self.master.partial_ticks);
				self.entity_in.right = util.lerp(self.entity_in.right, 1 if x > 0 else 0, self.master.partial_ticks);
				self.entity_in.up = util.lerp(self.entity_in.up, 1 if y > 0 else 0, self.master.partial_ticks);
				self.entity_in.down = -util.lerp(self.entity_in.down, 1 if y < 0 else 0, self.master.partial_ticks);

			if self.up:
				self.entity_in.jump();

	def render(self):
		pass;

class FontRenderer:
	def __init__(self, master, font = "Arial", size = 16):
		self.master = master;

		self.path = font;
		self.size = size;
		self.font = font;

		self.cfont = None;

		try:
			self.cfont = pygame.font.SysFont(font, self.size);
		except:
			self.cfont = pygame.font.Font(self.path, self.size);

		self.font

		self.texture = GL11.glGenTextures(1);

	def get_width(self, string):
		surface_text = self.cfont.render(string, 1, (255, 255, 255), False);

		width, height = surface_text.get_size();

		return width;

	def get_height(self):
		surface_text = self.cfont.render("", 1, (255, 255, 255), False);

		width, height = surface_text.get_size();

		return height;

	def render(self, text, x, y, color):
		surface = self.cfont.render(text, 1, (util.clamp(color[0], 0, 255), util.clamp(color[1], 0, 255), util.clamp(color[2], 0, 255), util.clamp(color[3], 0, 255))).convert_alpha()
		data = pygame.image.tostring(surface, "RGBA", False);

		GL11.glPushMatrix();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.texture);

		GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_LINEAR);
		GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_LINEAR);

		GL11.glTexImage2D(GL11.GL_TEXTURE_2D, 0, GL11.GL_RGBA, surface.get_width(), surface.get_height(), 0, GL11.GL_RGBA, GL11.GL_UNSIGNED_BYTE, data);		

		GL11.glEnable(GL11.GL_BLEND);
		GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);

		width = surface.get_width();
		height = surface.get_height();

		GL11.glColor(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord(0, 0); GL11.glVertex(x, y, 0);
		GL11.glTexCoord(0, 1); GL11.glVertex(x, y + height, 0);
		GL11.glTexCoord(1, 1); GL11.glVertex(x + width, y + height, 0);
		GL11.glTexCoord(1, 0); GL11.glVertex(x + width, y, 0);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glPopMatrix();

class OpenGL:
	def matrix():
		GL11.glPushMatrix();

	def refresh():
		GL11.glPopMatrix();

	def set(state):
		GL11.glEnable(state);

	def unset(state):
		GL11.glDisable(state);

	def cut(x, y, w, h, rect):
		factored_w = int(x + w);
		factored_h = int(y + h);

		try:
			GL11.glScissor(int(x), int(rect.h - (factored_h)), int(factored_w - x), int(factored_h - y));
		except:
			pass

	def blend():
		GL11.glEnable(GL11.GL_BLEND);
		GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);

	def set_mask():
		util.log("Invalid GL context: set_mask", "GL11");

	def unset_mask():
		util.log("Invalid GL context: unset_mask", "GL11");

	def set_culling():
		GL11.glCullFace(GL11.GL_FRONT);

	def unset_culling():
		GL11.glCullFace(GL11.GL_BACK);

	def color(r, g, b, a):
		GL11.glColor(r / 255.0, g / 255.0, b / 255.0, a / 255.0);

	def color(color):
		GL11.glColor(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0);

	def rotate(amount, x, y, z):
		GL11.glRotate(amount, x, y, z);

	def move(x, y, z):
		GL11.glTranslate(x, y, z);

	def fill_line_point(point_1, point_2, c, size):
		GL11.glPushMatrix();
		GL11.glEnable(GL11.GL_LINE_SMOOTH);
		GL11.glHint(GL11.GL_LINE_SMOOTH_HINT, GL11.GL_NICEST);

		OpenGL.blend();

		GL11.glLineWidth(size);

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);

		GL11.glBegin(GL11.GL_LINES);
		GL11.glVertex(point_1[0], point_1[1]);
		GL11.glVertex(point_2[0], point_2[1]);
		GL11.glEnd();

		GL11.glDisable(GL11.GL_LINE_SMOOTH);
		GL11.glPopMatrix();

	def fill_texture(x, y, w, h, id, c, uuv = None):
		GL11.glPushMatrix();
		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, id);

		GL11.glEnable(GL11.GL_BLEND);
		GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)]

		GL11.glColor(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0);
		GL11.glBegin(GL11.GL_QUADS);

		i = 1;
		k = 1;

		rw = 1;
		rh = 1;

		if uuv is not None and w is not 0 and h is not 0 and uuv[0] is not 0 and uuv[1] is not 0:
			i = 1 + (w - uuv[0]) / uuv[0];
			k = 1 + (h - uuv[1]) / uuv[1];

		GL11.glTexCoord(0, 0); GL11.glVertex(x, y);
		GL11.glTexCoord(i, 0); GL11.glVertex(x + w, y);

		GL11.glTexCoord(i, k); GL11.glVertex(x + w, y + h);
		GL11.glTexCoord(0, k); GL11.glVertex(x, y + h);

		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glPopMatrix();

	def fill_line_rect(rect, c, line, side):
		GL11.glPushMatrix();

		OpenGL.unset(GL11.GL_TEXTURE_2D);
		OpenGL.blend();

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);
	
		GL11.glLineWidth(line);

		if side is "all":
			GL11.glBegin(GL11.GL_LINE_LOOP);
		else:
			GL11.glBegin(GL11.GL_LINES);
		
		if "min_x" in side or side is "all":
			GL11.glVertex(rect.x, rect.y);

		if "min_y" in side or side is "all":
			GL11.glVertex(rect.x, rect.y + rect.h);

		if side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(rect.x, rect.y + rect.h);

		if "max_x" in side or side is "all":
			GL11.glVertex(rect.x + rect.w, rect.y + rect.h);

		if side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(rect.x + rect.w, rect.y + rect.h);

		if "max_y" in side or side is "all":
			GL11.glVertex(rect.x + rect.w, rect.y);

		if "max_y" in side and side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(rect.x + rect.w, rect.y);
			GL11.glVertex(rect.x, rect.y);
		
		GL11.glEnd();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glPopMatrix();

	def fill_line_shape(x, y, w, h, c, line, side):
		GL11.glPushMatrix();

		OpenGL.unset(GL11.GL_TEXTURE_2D);
		OpenGL.blend();

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);
	
		GL11.glLineWidth(line);

		if side is "all":
			GL11.glBegin(GL11.GL_LINE_LOOP);
		else:
			GL11.glBegin(GL11.GL_LINES);
		
		if "min_x" in side or side is "all":
			GL11.glVertex(x, y);

		if "min_y" in side or side is "all":
			GL11.glVertex(x, y + h);

		if side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(x, y + h);

		if "max_x" in side or side is "all":
			GL11.glVertex(x + w, y + h);

		if side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(x + w, y + h);

		if "max_y" in side or side is "all":
			GL11.glVertex(x + w, y);

		if "max_y" in side and side is not "all":
			GL11.glEnd();
			GL11.glBegin(GL11.GL_LINES);
			GL11.glVertex(x + w, y);
			GL11.glVertex(x, y);
		
		GL11.glEnd();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glPopMatrix();

	def fill_shape_rect(rect, c):
		GL11.glPushMatrix();

		OpenGL.unset(GL11.GL_TEXTURE_2D);
		OpenGL.blend();

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);

		GL11.glBegin(GL11.GL_QUADS);
		
		GL11.glVertex(rect.x, rect.y);
		GL11.glVertex(rect.x + rect.w, rect.y);

		GL11.glVertex(rect.x + rect.w, rect.y + rect.h);
		GL11.glVertex(rect.x, rect.y + rect.h);
		
		GL11.glEnd();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glPopMatrix();

	def fill_shape(x, y, w, h, c):
		GL11.glPushMatrix();

		OpenGL.unset(GL11.GL_TEXTURE_2D);
		OpenGL.blend();

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);

		GL11.glBegin(GL11.GL_QUADS);
		
		GL11.glVertex(x, y);
		GL11.glVertex(x + w, y);

		GL11.glVertex(x + w, y + h);
		GL11.glVertex(x, y + h);
		
		GL11.glEnd();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glPopMatrix();

	def fill(rect, c):
		GL11.glPushMatrix();

		OpenGL.unset(GL11.GL_TEXTURE_2D);
		OpenGL.blend();

		color = [util.clamp(c[0], 0, 255), util.clamp(c[1], 0, 255), util.clamp(c[2], 0, 255), util.clamp(c[3], 0, 255)];

		OpenGL.color(color);

		GL11.glBegin(GL11.GL_QUADS);
		
		GL11.glVertex(rect.min_x.x, rect.min_x.y);
		GL11.glVertex(rect.min_y.x, rect.min_y.y);

		GL11.glVertex(rect.max_y.x, rect.max_y.y);
		GL11.glVertex(rect.max_x.x, rect.max_x.y);
		
		GL11.glEnd();

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glPopMatrix();

class Data:
	def __init__(self, context):
		self.context = context;
		self.data = {};

	def registry(self, name, value):
		self.data[name] = value;

	def set(self, name, value):
		if self.data.__contains__(name):
			self.data[name] = value;

	def get(self, name):
		if self.data.__contains__(name):
			return self.data[name];

	def remove(self, value_name):
		if self.data.__contains__(value_name):
			self.data.pop(value_name);

class Setting:
	def __init__(self, name):
		self.name = name;
		self.data = {};

	def value(self, value_name, value = None):
		if value is not None:
			self.data[value_name] = value;
		else:
			if self.data.__contains__(value_name):
				return self.data[value_name];

	def remove(self, value_name):
		if self.data.__contains__(value_name):
			self.data.pop(value_name);

class GameSetting:
	def __init__(self, master):
		self.master = master;
		self.settings = {};

		# Todas as settings do jogo.
		self.setting_fullscreen = Setting("fullscreen");
		self.setting_framerate = Setting("framerate");
		self.setting_keybind = Setting("keybind");

	def init(self):
		# Algumas settings mais basicas.
		self.setting_fullscreen.value("active", False);
		self.setting_fullscreen.value("width", 1280);
		self.setting_fullscreen.value("height", 720);

		self.setting_framerate.value("vsync", False);
		self.setting_framerate.value("value", 60);

		# Todas as keybinds do jogo!
		self.setting_keybind.value("mouse-motion", Flag.DISABLED);

		self.setting_keybind.value("left", pygame.K_LEFT);
		self.setting_keybind.value("right", pygame.K_RIGHT);
		self.setting_keybind.value("up", pygame.K_UP);
		self.setting_keybind.value("down", pygame.K_DOWN);

		self.setting_keybind.value("attack", pygame.K_SPACE);
		self.setting_keybind.value("interact", pygame.K_h);
		self.setting_keybind.value("inventory", pygame.K_e);
		self.setting_keybind.value("hook", pygame.K_f);

		# Registramos tudinho!
		self.registry(self.setting_fullscreen);
		self.registry(self.setting_framerate);
		self.registry(self.setting_keybind);

	def registry(self, setting):
		self.settings[setting.name] = setting;

	def on_save(self):
		erase = open("settings.dat", 'w').close();
		data = {};

		for names in self.settings:
			setting = self.settings[names];

			data[setting.name] = setting.data;

		with open("settings.dat", 'w', encoding = 'utf-8') as file:
			json.dump(data, file, ensure_ascii = 0, indent = 4);

			util.log("Main settings saved!", "MAIN");
			file.close();

	def on_load(self):
		data = {};

		if os.path.exists("settings.dat") is False:
			return;

		try:
			with open("settings.dat", 'r') as file:
				data = json.load(file);
				file.close();
		except:
			pass

		for name in self.settings:
			setting = self.settings[name];

			if data.__contains__(setting.name):
				setting.data = data[setting.name];

class Gui:
	def __init__(self, tag):
		self.tag = tag;
		self.active = False;

		self.tick_alpha_255 = 0;
		self.last_tick_alpha_255 = 0;

	def update_alpha_255(self, partial_ticks):
		self.last_tick_alpha_255 = util.lerp(self.last_tick_alpha_255, self.tick_alpha_255, partial_ticks);

		if self.tick_alpha_255 <= 10:
			self.do_close();

	def close(self):
		self.tick_alpha_255 = 0;

	def do_close(self):
		if self.active:
			self.tick_alpha_255 = 0;

			self.on_close();
			self.active = False;

	def do_open(self):
		if self.active is not True:
			self.tick_alpha_255 = 255;

			self.on_open();
			self.active = True;

	def on_close(self):
		pass

	def on_open(self):
		pass

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		pass

	def on_render(self, mx, my, partial_ticks):
		pass

class GameGui:
	def __init__(self, master):
		self.master = master;
		self.current_gui = None;

	def init(self):
		self.current_gui = None;

	def open(self, gui):
		if gui is not None:
			if self.current_gui is not None:
				self.current_gui.do_close();

			self.current_gui = gui;
			self.current_gui.do_open();

	def close(self):
		if self.current_gui is not None:
			self.current_gui.close();

	def process_key_event(self, key, state):
		if self.current_gui is not None:
			self.current_gui.on_key_event(key, state);

	def process_mouse_event(self, mx, my, button, state):
		if self.current_gui is not None:
			self.current_gui.on_mouse_event(mx, my, button, state);

	def process_render(self, mx, my, partial_ticks):
		if self.current_gui is not None:
			self.current_gui.update_alpha_255(partial_ticks);
			self.current_gui.on_render(mx, my, partial_ticks);

class Vec:
	def __init__(self, x, y, z):
		self.x = x;
		self.y = y;
		self.z = z;

	def get_x(self):
		return self.x;

	def get_y(self):
		return self.y;

	def get_z(self):
		return self.z;

	def get(self):
		return [self.x, self.y, self.z];

	def length(self):
		return sqrt(self.x * self.x + self.y * self.y + self.z * self.z);

	def __add__(self, num):
		if type(num) is Vec:
			return Vec(self.x + num.x, self.y + num.y, self.z + num.z);

		return Vec(self.x + num, self.y + num, self.z + num);

	def __sub__(self, num):
		if type(num) is Vec:
			return Vec(self.x - num.x, self.y - num.y, self.z - num.z);

		return Vec(self.x - num, self.y - num, self.z - num);

	def __mul__(self, num):
		if type(num) is Vec:
			return Vec(self.x * num.x, self.y * num.y, self.z * num.z);

		return Vec(self.x * num, self.y * num, self.z * num);

	def __div__(self, num):
		return Vec(self.x / num, self.vec.y / num, self.z / num);

	def __neg__(self):
		return Vec(-self.x, -self.y, -self.z);

class Point:
	def __init__(self, x, y, z_lolololol_zzzkkkkue):
		self.x = x;
		self.y = y;

	def set(self, x, y, angle):
		sin = math.sin(math.radians(angle));
		cos = math.cos(math.radians(angle));

		self.x -= x;
		self.y -= y;

		ultra_giga_sync_x = (self.x * cos) - (self.y * sin);
		ultra_giga_sync_y = (self.x * sin) + (self.y * cos);

		self.x = ultra_giga_sync_x + x;
		self.y = ultra_giga_sync_y + y;

class Rect(pygame.Rect):
	def __init__(self, x, y, w, h):
		super().__init__([x, y], [w, h]);

		self.angle = 0;

		self.min_x = Point(x, y, self.angle);
		self.min_y = Point(x, y + h, self.angle);

		self.max_x = Point(x + w, y, self.angle);
		self.max_y = Point(x + w, y + h, self.angle);

		self.set_position(x, y);
		self.set_size(w, h);

	def set_position(self, x, y):
		if self.x == x and self.y == y:
			return;

		self.x = x;
		self.y = y;

		self.min_x.x = self.x;
		self.min_x.y = self.y;

		self.min_y.x = self.x;
		self.min_y.y = self.y + self.h;

		self.min_x.set(self.x + (self.w / 2), self.y + (self.h / 2), self.angle);
		self.min_y.set(self.x + (self.w / 2), self.y + (self.h / 2), self.angle);

	def set_size(self, w, h):
		if self.w == w and self.h == h:
			return;

		self.w = w;
		self.h = h;

		self.max_x.x = self.x + self.w;
		self.max_x.y = self.y;

		self.max_y.x = self.x + self.w;
		self.max_y.y = self.y + self.h;

		self.max_x.set(self.x + (self.w / 2), self.y + (self.h / 2), self.angle);
		self.max_y.set(self.x + (self.w / 2), self.y + (self.h / 2), self.angle);

	def add(self, x, y):
		rect = Rect(self.x, self.y, self.w, self.h);

		rect.set_position(self.x + x, self.y + y);
		rect.set_size(self.w, self.h);

		return rect;

	def collide_with_mouse(self, mouse):
		return mouse[0] >= self.min_x.x and mouse[1] >= self.min_x.y and \
		       mouse[0] >= self.min_y.x and mouse[1] <= self.min_y.y and \
		       mouse[0] <= self.max_x.x and mouse[1] >= self.max_x.y and \
		       mouse[0] <= self.max_y.x and mouse[1] <= self.max_y.y;

	def collide_with_mouse_shape(self, mouse):
		return mouse[0] >= self.x and mouse[1] >= self.y and mouse[0] <= self.x + self.w and mouse[1] <= self.y + self.h;

	def collide_with_rect_shape(self, rect):
		return self.x <= (rect.x + rect.w) and (self.x + self.w) >= rect.x and self.y <= (rect.y + rect.h) and (self.y + self.h) >= rect.y;

class TimerStamp:
	def __init__(self):
		self.ms = -1;

	def reset(self):
		self.ms = pygame.time.get_ticks();

	def current_ms(self):
		return pygame.time.get_ticks() - self.ms;

	def is_passed(self, ms):
		return pygame.time.get_ticks() - self.ms >= ms;

	def count(self, ms_div):
		return (pygame.time.get_ticks() - self.ms) / ms_div;

class Task(threading.Thread):
	def set_task_tag(self, tag, task, args):
		self.task = task;
		self.tag = tag;
		self.done = False;
		self.args = args;

	def run(self):
		while (not self.done):
			self.done = self.task(self.args);

		time.sleep(1.5);

class TaskManager:
	def __init__(self):
		self.task_done_queue = {};

	def task(self, tag, task, args):
		if (self.contains_task(tag)):
			print("oi");
			return;

		thread_task = Task();
		thread_task.set_task_tag(tag, task, args);

		self.task_done_queue[tag] = (thread_task);
		thread_task.start();

	def is_task_done(self, tag):
		flag = self.task_done_queue.__contains__(tag);

		if (flag and not self.task_done_queue[tag].is_alive()):
			del self.task_done_queue[tag];
		else:
			flag = False;

		return flag;	

	def contains_task(self, tag):
		return self.task_done_queue.__contains__(tag);

class Texture:
	def __init__(self, tag, author, path, sheet = False):
		self.author = author;
		self.tag = tag;
		self.path = path;
		self.sheet = sheet;

		self.image = None;
		self.operable = True;

	def read_author(self):
		return "§Texure: " + self.tag + " &Author: " + self.author + "$";

	def reload(self):
		if self.image is None and self.operable is True:
			try:
				self.image = pygame.image.load(self.path).convert_alpha();
				self.operable = True;

				util.log(self.read_author(), "INFO-TEXTURE");
			except IOError as exc:
				self.image = None;
				self.operable = False;

				util.log("IOException texture load: " + str(exc), "INFO-TEXTURE");

	def get_size(self):
		if self.operable:
			return [self.image.get_height(), self.image.get_width()];

		return [None, None];

class TextureManager:
	def __init__(self, master):
		self.master = master;
		self.textures = {};

		self.loaded_count = 0;
		self.unloaded_count = 0;

		self.initialized = False;

	def set_initialized(self):
		self.initialized = True;

	def unset_initialized(self):
		self.initialized = False;

	def init(self):
		self.load(Texture("player_spawn", "rina", "data/player_spawn.png"));
		self.load(Texture("mob_spawn", "rina", "data/mob_spawn.png"));
		self.load(Texture("passive_spawn", "rina", "data/passive_spawn.png"));
		self.load(Texture("tile_terrain_border_left", "werneck", "data/tile_terrain_border_left.png"));
		self.load(Texture("tile_terrain_center", "werneck", "data/tile_terrain_center.png"));
		self.load(Texture("tile_terrain_border_right", "werneck", "data/tile_terrain_border_right.png"));

		if self.unloaded_count != 0 and self.unloaded_count == self.loaded_count:
			util.log("Reloaded " + str(self.loaded_count) + " textures", "INFO-TEXTURE");
		else:
			util.log("Loaded " + str(self.loaded_count) + " textures", "INFO-TEXTURE");

	def load(self, texture, instant = False):
		if instant:
			if self.textures.__contains__(texture.tag) is False:
				self.textures[texture.tag] = texture;
				self.textures[texture.tag].reload();
		else:
			if self.textures.__contains__(texture.tag) is False:
				self.textures[texture.tag] = texture;
	
				self.loaded_count += 1;
			else:
				self.textures[texture.tag].reload();
				self.unloaded_count += 1;

	def get(self, tag):
		if self.textures.__contains__(tag):
			return self.textures[tag];

		return None;