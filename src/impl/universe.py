from .lib import pygame, Flag, RANGE, json, math, GL11, messagebox;
from .    import util, api;

#
# IMPORTANTE:
# Eu tinha visto um tutorial como fazer um tile game,
# descobri que não é dificil, mas o código dele é horrível.
# Nisso eu vou reescrever todo o sistema pra deixar muito mais
# rápido, ou seja, vou ter que tirar um suor pra fazer algo in
# sanamente mais rapido!
# -
# Bjinhos dá Rina.
#
# CHEGA DE TILE, SEM TILE HUHUH!
#
# NAO HEGA CHEGA
#
TILE_SIZE = 32;

# Eventos!!
EVENT_REFRESH = 0;
EVENT_ADD_IMAGE = [0, 0];

# IDs dos sprites.
PHASE  = 0;
SOLID  = 1;
LIQUID = 2;

# Flags.
ID   = 0;
TAG  = 1;
NAME = 2;
MODE = 3;

class Object:
	def __init__(self, tag, x, y):
		self.prev_x = x;
		self.prev_y = y;

		self.x = x;
		self.y = y;

		self.rect = api.Rect(0, 0, 0, 0);

		self.w = 30;
		self.h = 30;

		self.found_texture = None;
		self.color = [255, 255, 255];
		self.superior = False;

		self.alpha = 255;
		self.static = False;
		self.tile = True;
		self.visibility = 0;

		self.database = [PHASE, tag, tag, "scaled"];
		self.texture_id = 0;

	def set_id(self, id):
		self.database[ID] = id;

	def get_id(self):
		return self.database[ID];

	def set_tag(self, tag):
		self.database[TAG] = tag;

	def get_tag(self):
		return self.database[TAG];

	def set_name(self, name):
		self.database[NAME] = name;

	def get_name(self):
		return self.database[NAME];

	def set_mode(self, mode):
		self.database[MODE] = mode;

	def get_mode(self):
		return self.database[MODE];

	def update(self, partial_ticks, texture_manager, camera):
		self.prev_x = self.x + (camera.x if self.static is False else 0);
		self.prev_y = self.y + (camera.y if self.static is False else 0);

		if self.found_texture is None or self.found_texture.tag is not self.get_name():
			if (self.texture_id == 0):
				self.texture_id = GL11.glGenTextures(1);

			self.found_texture = texture_manager.get(self.get_name());

			if self.found_texture is None or self.found_texture.image is None:
				return;

			data = pygame.image.tostring(self.found_texture.image, "RGBA");

			GL11.glEnable(GL11.GL_TEXTURE_2D);
			GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.texture_id);

			GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_NEAREST);
			GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_NEAREST);

			param = util.convert_mode_to_byte(self.get_mode());

			GL11.glTexParameteriv(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_S, param);
			GL11.glTexParameteriv(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_WRAP_T, param);

			GL11.glTexImage2D(GL11.GL_TEXTURE_2D, 0, GL11.GL_RGBA, self.found_texture.image.get_width(), self.found_texture.image.get_height(), 0, GL11.GL_RGBA, GL11.GL_UNSIGNED_BYTE, data);
		
			GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
			GL11.glDisable(GL11.GL_TEXTURE_2D);

	def collide_with_mouse(self, mouse):
		return mouse[0] >= self.prev_x and mouse[1] >= self.prev_y and mouse[0] <= self.prev_x + self.w and mouse[1] <= self.prev_y + self.h;

	def collide_with_rect(self, rect):
		return self.prev_x <= (rect.x + rect.w) and (self.prev_x + self.w) >= rect.x and self.prev_y <= (rect.y + rect.h) and (self.prev_y + self.h) >= rect.y;

	def get_rect(self):
		self.rect.x = self.prev_x;
		self.rect.y = self.prev_y;
		self.rect.w = self.w;
		self.rect.h = self.h;

		return self.rect;

	def render(self):
		if self.found_texture is not None:
			if self.superior:
				api.OpenGL.fill_shape(self.prev_x, self.prev_y, self.w, self.h, [self.color[0], self.color[1], self.color[2], 100]);

			api.OpenGL.fill_texture(self.prev_x, self.prev_y, self.w, self.h, self.texture_id, [self.color[1], self.color[2], self.color[2], self.alpha], None if self.get_mode() == "scaled" else [self.found_texture.image.get_width(), self.found_texture.image.get_height()]);

class RenderManager:
	def __init__(self, master):
		self.master = master;
		self.range = 100;

		self.batch_object = [];
		self.batch_entity = [];

	def refresh(self):
		if not self.master.current_map.loaded:
			return;

		self.batch_object.clear();
		self.batch_entity.clear();

		for i, tags in enumerate(self.master.current_map.loaded_image_list):
			images = self.master.current_map.loaded_image_list[tags];

			if images.visibility:
				self.batch_object.append(images);

		for ids in self.master.current_map.loaded_entity_list:
			entity = self.master.current_map.loaded_entity_list[ids];

			if entity.visibility:
				self.batch_entity.append(entity);

	def render(self, partial_ticks):
		if self.master.current_map is not None:
			api.OpenGL.fill_shape(self.master.current_map.rect.x, self.master.current_map.rect.y, self.master.current_map.rect.w, self.master.current_map.rect.h, self.master.current_map.background_color);

			api.OpenGL.set(GL11.GL_SCISSOR_TEST);
			api.OpenGL.cut(self.master.current_map.rect.x, self.master.current_map.rect.y, self.master.current_map.rect.w, self.master.current_map.rect.h, self.master.screen_rect);

			for images in self.batch_object:
				images.render();

			for entities in self.batch_entity:
				entities.render(partial_ticks);

			api.OpenGL.unset(GL11.GL_SCISSOR_TEST);

class Map:
	def __init__(self, master):
		self.master = master;

	def start(self, tag, id):
		self.tag = tag;
		self.id = id;

		self.rect = api.Rect(0, 0, 0, 0);
		self.size = 200;

		self.loaded_entity_list = {};
		self.loaded_image_list = {};

		self.spawn_needed = True;
		self.spawn_id = 0;

		self.background_color = [0, 0, 0, 255];
		self.event_list = {};

		self.current_image = None;
		self.initialized = False;

		self.mouse_over_something = False;
		self.mouse_over = False;

		self.op = True;

		self.drag_x = 0;
		self.drag_y = 0;

		self.resize_x = 0;
		self.resize_y = 0;

		self.dragging_image = False;
		self.resizing_image = False;

		self.edit_mode = False;
		self.grid = False;

		self.image_keybind_flag = False;
		self.double_click_timing = api.TimerStamp();
		self.loaded = False;

		return self;

	def end(self):
		self.current_image = None;
		self.loaded_entity_list.clear();
		self.loaded_image_list.clear();

	def init(self):
		pass

	def save(self, path):
		self.tag = util.path_split(path)[0];

		data = util.create_data_map(self);
		erase = open(str(path), 'w').close();

		with open(str(path), 'w', encoding = 'utf-8') as file:
			json.dump(data, file, ensure_ascii = 0, indent = 4);

			util.log("Saved " + self.tag + " as " + self.tag + ".json" + " successfully!", "INFO-MAP");
			file.close();

	def read(self, path):
		with open(path, 'r') as file:
			data = json.load(file);

			util.read_data_map(self, data);
			file.close();

			data.clear();

	def load(self, path):
		self.loaded_image_list.clear();
		self.loaded_entity_list.clear();

		with open(path, 'r') as file:
			data = json.load(file);

			util.load_data_map(self, data);
			file.close();

			data.clear();

		self.loaded = True;

	def set_initialized(self):
		self.initialized = True;

	def unset_initialized(sef):
		self.initialized = False;

	def on_mouse_event(self, mx, my, button, state):
		boolean = False;

		if self.edit_mode:
			if state == Flag.KEYDOWN and self.mouse_over_something is False:
				if button is 1 and self.current_image is not None and self.current_image.collide_with_mouse([mx, my]):
					rect_image = api.Rect(self.current_image.prev_x, self.current_image.prev_y, self.current_image.w, self.current_image.h);

					rect = api.Rect(rect_image.x, rect_image.y, rect_image.w, rect_image.h);
					rect.set_position(rect_image.x + rect_image.w - 4, rect_image.y + rect_image.h - 4);
					rect.set_size(4, 4);

					if rect.collide_with_mouse(self.master.mouse_position):
						self.resize_x = mx - (self.current_image.prev_x + self.current_image.w);
						self.resize_y = my - (self.current_image.prev_y + self.current_image.h);

						self.dragging_image = False;
						self.resizing_image = True;
					else:
						self.drag_x = mx - self.current_image.prev_x;
						self.drag_y = my - self.current_image.prev_y;
	
						self.dragging_image = True;
						self.resizing_image = False;

				image_over = None;

				for images in self.loaded_image_list:
					if self.loaded_image_list[images].collide_with_mouse([mx, my]):
						image_over = self.loaded_image_list[images];

						break;

				if image_over is not None and button == 1 and state == Flag.KEYDOWN:
					if self.double_click_timing.is_passed(750) is False or self.image_keybind_flag:
						self.current_image = image_over;

						boolean = True;
					else:
						self.double_click_timing.reset();

				if self.current_image is not None and self.current_image.collide_with_mouse(self.master.mouse_position):
					boolean = True;

				if boolean is False:
					self.current_image = None;

			if state is Flag.KEYUP:
				self.dragging_image = False;
				self.resizing_image = False;

	def on_key_event(self, key, state):
		if self.edit_mode:
			if state is Flag.KEYDOWN and key == pygame.K_DELETE and self.current_image is not None:
				self.delete_current_image();

			if key == pygame.K_LCTRL or key == pygame.K_RCTRL:
				if state is Flag.KEYDOWN:
					self.image_keybind_flag = True;
				else:
					self.image_keybind_flag = False;

	def add_image(self, texture, custom_init_position = None):
		if custom_init_position is not None and self.image_collide_with_point(custom_init_position):
			return;

		size = [0, 0];
		tag = "";

		if type(texture) is api.Texture:
			size = texture.get_size();
			tag = texture.tag;
		elif type(texture) is Object:
			size = [texture.w, texture.h];
			tag = texture.get_name();
		else:
			size = self.master.texture_manager.get(texture.tag).get_size();
			tag = texture.tag;

		name = tag;
		tag = str("." + str(len(self.loaded_image_list)) + str(1));

		object_ = Object(tag, self.rect.x, self.rect.y);
		object_.set_name(name);

		if type(texture) is Object:
			object_.alpha = texture.alpha;
			object_.tile = texture.tile;
			object_.static = texture.static;
			object_.set_mode(texture.get_mode());

		object_.w = size[0];
		object_.h = size[1];

		if custom_init_position is not None:
			object_.x = custom_init_position[0];
			object_.y = custom_init_position[1];

			if len(custom_init_position) > 1:
				object_.w = custom_init_position[2];
				object_.h = custom_init_position[3];

		if self.loaded_image_list.__contains__(tag) is False:
			self.loaded_image_list[tag] = object_;

		return self.loaded_image_list[tag];

	def get_image(self, position, tile = True):
		found_image = None;

		for i, tags in enumerate(self.loaded_image_list):
			image = self.loaded_image_list[tags];

			if image.tile is False and tile is True:
				continue;

			flag = image.collide_with_mouse(position);

			if flag:
				found_image = image;

				break;

		return found_image;

	def image_collide_with_mouse(self, position):
		return self.image_collide_with_point(position);

	def image_collide_with_point(self, position):
		flag = False;

		if len(self.loaded_image_list) is 0:
			return flag;

		for i, tags in enumerate(self.loaded_image_list):
			image = self.loaded_image_list[tags];

			rect = api.Rect(image.x - 1, image.y - 1, image.w - 2, image.h - 2);

			if rect.collide_with_mouse(position):
				return True;

		return False;

	def delete_current_image(self):
		if self.current_image is None:
			return;

		del self.loaded_image_list[self.current_image.get_tag()];

		self.current_image = None;

	def get_entity(self, id):
		if (self.loaded_entity_list.__contains__(id)):
			return self.loaded_entity_list[id];

		return None;

	def add_entity(self, entity):
		if self.loaded_entity_list.__contains__(entity.get_id()) is False:
			self.loaded_entity_list[entity.get_id()] = entity;

	def remove_entity(self, id):
		if self.get_entity(id) is not None:
			del self.loaded_entity_list[id];

	def get_size(self):
		return [self.rect.w, self.rect.h];

	def get_relative_mouse_position(self):
		mx = (self.master.mouse_position[0] - self.master.camera.x) // TILE_SIZE;
		my = (self.master.mouse_position[1] - self.master.camera.y) // TILE_SIZE;

		return [math.floor(mx) * TILE_SIZE, math.floor(my) * TILE_SIZE];

	def update(self, partial_ticks):
		if not self.loaded:
			return;

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

		if self.event_list.__contains__(EVENT_REFRESH):
			self.event_list.remove(EVENT_REFRESH);

		if self.edit_mode is False:
			self.rect.x = -200;
			self.rect.y = -200;

			self.rect.w = self.master.screen_rect.w + 400;
			self.rect.h = self.master.screen_rect.h + 400;

			for ids in set(self.loaded_entity_list):
				entity = self.loaded_entity_list[ids];
				entity.update(self.loaded_image_list, self.master.physic, partial_ticks, self.master.camera);

				if entity.rect.colliderect(self.rect) and entity.alive:
					entity.visibility = True;
				else:
					entity.visibility = False;

				if entity.alive is False:
					del self.loaded_entity_list[entity.get_id()];

			self.master.camera.x = self.master.player.rect.x - (self.rect.w / 2);
			self.master.camera.y = 0;

			self.master.camera.last_tick_x = self.master.camera.x;
			self.master.camera.last_tick_y = self.master.camera.y;

			print(self.master.player.rect.x);

		for images in self.loaded_image_list:
			image = self.loaded_image_list[images];
			image.update(partial_ticks, self.master.texture_manager, self.master.camera);

			if self.edit_mode:
				image.color = util.check_if_is_superior(image.get_name());

				util.apply_superior(image.get_name(), image);

			if image.collide_with_rect(self.rect):
				image.visibility = 1;
			else:
				image.visibility = 0;

			if self.spawn_needed and self.edit_mode is False:
				if image.get_name() == "player_spawn":
					self.master.player.set_position(image.x, image.y);

					self.master.stage_input = 1;
					self.master.input_manager.entity_in = self.master.player;

					self.spawn_needed = False;

		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

		if self.dragging_image and self.edit_mode and self.current_image is not None:
			the_x = self.master.mouse_position[0] - self.drag_x;
			the_y = self.master.mouse_position[1] - self.drag_y;

			x = the_x;
			y = the_y;

			if self.current_image.tile:
				mx = ((self.master.mouse_position[0] if self.current_image.w == TILE_SIZE else the_x) - self.master.camera.x) // TILE_SIZE;
				my = ((self.master.mouse_position[1] if self.current_image.h == TILE_SIZE else the_y) - self.master.camera.y) // TILE_SIZE;

				x = math.floor(mx) * TILE_SIZE;
				y = math.floor(my) * TILE_SIZE;

			self.current_image.x = x;
			self.current_image.y = y;

		if self.resizing_image and self.edit_mode and self.current_image is not None:
			the_x = self.master.mouse_position[0] - (self.current_image.prev_x + self.resize_x);
			the_y = self.master.mouse_position[1] - (self.current_image.prev_y + self.resize_y);

			x = the_x;
			y = the_y;

			if x <= 10:
				x = 10;

			if y <= 10:
				y = 10;

			if self.current_image.tile:
				# Posição relativa.
				rx = the_x // TILE_SIZE;
				ry = the_y // TILE_SIZE;

				x = TILE_SIZE + (math.floor(rx) * TILE_SIZE);
				y = TILE_SIZE + (math.floor(ry) * TILE_SIZE);

				if x <= TILE_SIZE:
					x = TILE_SIZE;

				if y <= TILE_SIZE:
					y = TILE_SIZE;

			self.current_image.w = x;
			self.current_image.h = y;

	def render(self, partial_ticks):
		pass;

class Camera:
	def __init__(self, master, initial_x, initial_y):
		self.master = master;

		self.x = initial_x;
		self.y = initial_y;

		self.last_tick_x = self.x;
		self.last_tick_y = self.x;

	def set_position(self, x, y):
		self.x = self.x;
		self.y = self.y;

	def get_position(self):
		return [self.last_tick_x, self.last_tick_y];

	def update(self, partial_ticks):
		if self.master.stage_input == 1:
			self.x = util.lerp(self.x, self.last_tick_x, partial_ticks);
			self.y = util.lerp(self.y, self.last_tick_y, partial_ticks);