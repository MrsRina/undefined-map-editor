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
		self.render_x = x;
		self.render_y = y;

		self.rect = api.Rect(x, y, 30, 30);

		self.found_texture = None;
		self.color = [255, 255, 255];
		self.superior = False;

		self.alpha = 255;
		self.static = False;
		self.tile = True;
		self.visibility = 0;

		self.database = [PHASE, tag, tag, "scaled"];
		self.texture_id = 0;
		self.internal_texture_refresh = True;

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

	def set_mode(self, mode, texture_manager):
		if self.database[MODE] != mode:
			self.database[MODE] = mode;
			self.internal_texture_refresh = True;

	def get_mode(self):
		return self.database[MODE];

	def update(self, partial_ticks, texture_manager, camera):
		self.render_x = self.rect.x - (camera.x if self.static is False else 0);
		self.render_y = self.rect.y - (camera.y if self.static is False else 0);

		if self.found_texture is None or self.found_texture.image is None:
			self.found_texture = texture_manager.get(self.get_name());

		if self.internal_texture_refresh and self.found_texture != None and self.found_texture.image != None:
			self.internal_texture_refresh = False;
			self.texture_id = texture_manager.find_in_cache(self.get_name() + "-" + self.get_mode());

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
		x = self.render_x;
		y = self.render_y;
		w = self.rect.w;
		h = self.rect.h;

		return mouse[0] >= x and mouse[1] >= y and mouse[0] <= x + w and mouse[1] <= y + h;

	def collide_with_rect(self, rect):
		x = self.rect.x;
		y = self.rect.y;
		w = self.rect.w;
		h = self.rect.h;

		return x <= (rect.x + rect.w) and (x + w) >= rect.x and y <= (rect.y + rect.h) and (y + h) >= rect.y;

	def render(self):
		if self.found_texture is not None:
			if self.superior:
				api.OpenGL.fill_shape(self.render_x, self.render_y, self.rect.w, self.rect.h, [self.color[0], self.color[1], self.color[2], 100]);

			api.OpenGL.fill_texture(self.render_x, self.render_y, self.rect.w, self.rect.h, self.texture_id, [self.color[1], self.color[2], self.color[2], self.alpha], None if self.get_mode() == "scaled" else [self.found_texture.image.get_width(), self.found_texture.image.get_height()]);

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
				self.batch_object.append(images.render);

		for ids in self.master.current_map.loaded_entity_list:
			entity = self.master.current_map.loaded_entity_list[ids];

			if entity.visibility:
				self.batch_entity.append(entity.render);

	def render(self, partial_ticks):
		if self.master.current_map is not None:
			api.OpenGL.fill_shape(0, 0, self.master.current_map.rect.w, self.master.current_map.rect.h, self.master.current_map.background_color);

			api.OpenGL.set(GL11.GL_SCISSOR_TEST);
			api.OpenGL.cut(0, 0, self.master.current_map.rect.w, self.master.current_map.rect.h, self.master.screen_rect);

			for invokable_render in self.batch_object:
				invokable_render();

			for invokable_render in self.batch_entity:
				invokable_render(partial_ticks);

			api.OpenGL.unset(GL11.GL_SCISSOR_TEST);

class Map:
	def __init__(self, master):
		self.master = master;

	def start(self, tag, id):
		self.tag = tag;
		self.id = id;

		self.rect = api.Rect(0, 0, 0, 0);
		self.size = 200;

		self.x = 0;
		self.y = 0;
		self.w = 0;
		self.h = 0;

		self.render_distance = 200;

		self.loaded_entity_list = {};
		self.loaded_image_list = {};

		self.player_spawn_state = False;
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

	def spawn_player(self):
		for i in self.loaded_image_list:
			image = self.loaded_image_list[i];

			if image.get_name() == "player_spawn":
				self.master.player.set_position(image.rect.x, image.rect.y);

				self.master.stage_input = 1;
				self.master.input_manager.entity_in = self.master.player;

				self.player_spawn_state = True;

	def end(self):
		self.current_image = None;
		self.loaded_entity_list.clear();
		self.loaded_image_list.clear();
		self.master.physic.shape_list.clear();

		self.loaded = False;

	def init(self):
		self.loaded = True;

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

	def on_mouse_motion(self, mx, my):
		self.update_drag_and_resize();

	def on_mouse_event(self, mx, my, button, state):
		boolean = False;

		if self.edit_mode:
			if state == Flag.KEYDOWN and self.mouse_over_something is False:
				if button == 1 and self.current_image is not None and self.current_image.collide_with_mouse([mx, my]):
					rect_image = api.Rect(self.current_image.render_x, self.current_image.render_y, self.current_image.rect.w, self.current_image.rect.h);

					rect = api.Rect(rect_image.x, rect_image.y, rect_image.w, rect_image.h);
					rect.set_position(rect_image.x + rect_image.w - 4, rect_image.y + rect_image.h - 4);
					rect.set_size(4, 4);

					if rect.collide_with_mouse(self.master.mouse_position):
						self.resize_x = mx - (self.current_image.render_x + self.current_image.rect.w);
						self.resize_y = my - (self.current_image.render_y + self.current_image.rect.h);

						self.dragging_image = False;
						self.resizing_image = True;
					else:
						self.drag_x = mx - self.current_image.render_x;
						self.drag_y = my - self.current_image.render_y;
	
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

			if state == Flag.KEYDOWN:
				self.update_drag_and_resize();

			if state is Flag.KEYUP:
				self.dragging_image = False;
				self.resizing_image = False;

	def update_drag_and_resize(self):
		if self.dragging_image and self.edit_mode and self.current_image is not None:
			the_x = self.master.mouse_position[0] - self.drag_x;
			the_y = self.master.mouse_position[1] - self.drag_y;

			x = the_x;
			y = the_y;

			if self.current_image.tile:
				mx = ((self.master.mouse_position[0] if self.current_image.rect.w == TILE_SIZE else the_x) + self.master.camera.x) // TILE_SIZE;
				my = ((self.master.mouse_position[1] if self.current_image.rect.h == TILE_SIZE else the_y) + self.master.camera.y) // TILE_SIZE;

				x = math.floor(mx) * TILE_SIZE;
				y = math.floor(my) * TILE_SIZE;

			self.current_image.rect.x = x;
			self.current_image.rect.y = y;

		if self.resizing_image and self.edit_mode and self.current_image is not None:
			the_x = self.master.mouse_position[0] - (self.current_image.render_x + self.resize_x);
			the_y = self.master.mouse_position[1] - (self.current_image.render_y + self.resize_y);

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

			self.current_image.rect.w = x;
			self.current_image.rect.h = y;

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
			size = [texture.rect.w, texture.rect.h];
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
			object_.set_mode(texture.get_mode(), self.master.texture_manager);

		object_.rect.w = size[0];
		object_.rect.h = size[1];

		if custom_init_position is not None:
			object_.rect.x = custom_init_position[0];
			object_.rect.y = custom_init_position[1];

			if len(custom_init_position) > 1:
				object_.rect.w = custom_init_position[2];
				object_.rect.h = custom_init_position[3];

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

		if len(self.loaded_image_list) == 0:
			return flag;

		for i, tags in enumerate(self.loaded_image_list):
			image = self.loaded_image_list[tags];

			rect = api.Rect(image.rect.x - 1, image.rect.y - 1, image.rect.w - 2, image.rect.h - 2);

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
			entity.init(self.master);
			self.loaded_entity_list[entity.get_id()] = entity;

	def remove_entity(self, id):
		if self.get_entity(id) is not None:
			del self.loaded_entity_list[id];

	def get_size(self):
		return [self.rect.w, self.rect.h];

	def get_relative_mouse_position(self):
		mx = (self.master.mouse_position[0] + self.master.camera.x) // TILE_SIZE;
		my = (self.master.mouse_position[1] + self.master.camera.y) // TILE_SIZE;

		return [math.floor(mx) * TILE_SIZE, math.floor(my) * TILE_SIZE];

	def update(self, partial_ticks):
		if not self.loaded:
			return;

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

		if self.event_list.__contains__(EVENT_REFRESH):
			self.event_list.remove(EVENT_REFRESH);

		self.rect.x = self.x + self.master.camera.x - self.render_distance;
		self.rect.y = self.y + self.master.camera.y - self.render_distance;

		self.rect.w = self.w + (self.render_distance * 2);
		self.rect.h = self.h + (self.render_distance * 2);

		if self.edit_mode is False:
			self.w = self.master.screen_rect.w;
			self.h = self.master.screen_rect.h;

			for ids in set(self.loaded_entity_list):
				entity = self.loaded_entity_list[ids];
				entity.update(self.loaded_image_list, partial_ticks, self.master.camera);

				if entity.rect.colliderect(self.rect) and entity.alive:
					entity.visibility = True;
				else:
					entity.visibility = False;

				if entity.alive is False:
					del self.loaded_entity_list[entity.get_id()];

			self.master.camera.last_tick_x = self.master.player.rect.x - (self.w / 2);
			self.master.camera.last_tick_y = self.master.player.rect.y - (self.h / 2);

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

		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

	def render(self, partial_ticks):
		pass;

class Camera:
	def __init__(self, master, initial_x, initial_y):
		self.master = master;

		self.x = initial_x;
		self.y = initial_y;

		self.last_tick_x = self.x;
		self.last_tick_y = self.y;

	def set_position(self, x, y):
		self.x = x;
		self.y = y;

		self.last_tick_x = x;
		self.last_tick_y = y;

	def get_position(self):
		return [self.last_tick_x, self.last_tick_y];

	def update(self, partial_ticks):
		self.x = util.lerp(self.x, self.last_tick_x, partial_ticks);
		self.y = util.lerp(self.y, self.last_tick_y, partial_ticks);