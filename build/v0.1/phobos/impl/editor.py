from .lib import pygame, Flag, tkinter, filedialog, shutil, GL11, os, sys, askcolor, messagebox;
from .    import universe, api, util, imgui;

def task_save(args):
	args[0].save(args[1])
	return 1;

class LabelObject(imgui.Label):
	def __init__(self, master, text, x = 0, y = 0):
		super().__init__(master, text);

		self.show = True;

		self.offset_x = 0;
		self.offset_y = 0;

		self.scroll = 0;

		self.object_update = universe.Object(text, x, y);
		self.object_update.static = True;
		self.object_update.color = util.check_if_is_superior(self.object_update.get_name());

		util.apply_superior(self.object_update.get_name(), self.object_update);

		self.tick_alpha = 0;
		self.last_tick_alpha = 0;

		self.mouse_over = False;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		pass

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

	def render(self):
		self.object_update.rect = self.rect;
		self.object_update.update(self.master.partial_ticks, self.master.texture_manager, self.master.camera);

		if self.object_update.found_texture is not None:
			api.OpenGL.fill_texture(self.object_update.rect.x, self.object_update.rect.y, self.object_update.rect.w, self.object_update.rect.h, self.object_update.texture_id, [255, 255, 255, self.object_update.alpha]);

		if self.object_update.superior:
			api.OpenGL.fill_shape(self.object_update.rect.x, self.object_update.rect.y, self.object_update.rect.w, self.object_update.rect.h, [self.object_update.color[0], self.object_update.color[1], self.object_update.color[2], 100]);

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

		self.tick_alpha = 50 if self.mouse_over else 0;
		self.last_tick_alpha = util.lerp(self.last_tick_alpha, self.tick_alpha, self.master.partial_ticks);

		api.OpenGL.fill_line_rect(self.rect, [255, 255, 255, self.last_tick_alpha], 2, "all");

class FrameData(imgui.Element):
	def __init__(self, master, x = 0, y = 0, w = 0, h = 0):
		super().__init__(master, "frame");

		self.background = [255, 255, 255, 50];
		self.rect_name = api.Rect(x, y, w, h);

		self.show = True;

		self.offset_x = 0;
		self.offset_y = 0;

		self.scroll = 0;

		self.last_tick_height = 0;

		self.loaded_widgets_list = {};
		self.scale = 3;

		self.font_renderer = self.master.font_renderer;
		self.theme = self.master.theme;

		self.current_sprite = None;
		self.focused_sprite = None;

		self.the_type = "?";

	def registry(self, widget):
		widget.set_theme();
		widget.id = 999;

		return widget;

	def add(self, object_):
		if object_ is None:
			return;

		f0rmatted = object_ if type(object_) is str else object_.tag;

		if self.loaded_widgets_list.__contains__(f0rmatted) is False:
			tag = f0rmatted;

			self.loaded_widgets_list[tag] = self.registry(LabelObject(self.master, tag, 0, 0));

			if self.current_sprite is None:
				self.current_sprite = self.loaded_widgets_list[tag].object_update;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		for widget in self.loaded_widgets_list:
			widgets = self.loaded_widgets_list[widget];
			widgets.on_key_event(key, state);

		if self.focused_sprite is not None and key == pygame.K_DELETE and state == Flag.KEYDOWN:
			self.focused_sprite = None;

	def on_mouse_event(self, mx, my, button, state):
		boolean = self.master.current_map.mouse_over_something;

		for widget in self.loaded_widgets_list:
			widgets = self.loaded_widgets_list[widget];

			widgets.on_mouse_event(mx, my, button, state);

			if widgets.mouse_over and button == 1 and state == Flag.KEYUP:
				boolean = True;

				self.current_sprite = widgets.object_update;
				self.focused_sprite = widgets.object_update;

				break;

		if boolean is False and state == Flag.KEYUP:
			self.focused_sprite = None;

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

	def render(self):
		height = 1;

		x = 1;
		y = 1;
		
		api.OpenGL.set(GL11.GL_SCISSOR_TEST);
		api.OpenGL.cut(self.rect.x, self.rect.y, self.rect.w, self.rect.h, self.master.screen_rect);

		for widget in self.loaded_widgets_list:
			widgets = self.loaded_widgets_list[widget];

			if widgets.show is False:
				continue;
	
			widgets.render();
			widgets.update_mouse_over();
	
			widgets.string = [255, 255, 255, 255];
	
			widgets.offset_x = 2;
			widgets.offset_y = self.scale;
	
			widgets.rect.w = 30;
			widgets.rect.h = 30;
	
			widgets.rect.y = self.rect.y + self.scroll + y;
			widgets.rect.x = self.rect.x + x;

			if height is 1:
				height += widgets.rect.h + 1;

			if widgets.rect.x + widgets.rect.w + 6 >= self.rect.x + self.rect.w:
				x = 1;
				y += widgets.rect.h + 1;
				height += widgets.rect.h + 1;
			else:
				x += widgets.rect.w + 1;

		if self.current_sprite is not None:
			api.OpenGL.fill_line_shape(self.current_sprite.rect.x, self.current_sprite.rect.y, self.current_sprite.rect.w, self.current_sprite.rect.h, [0, 190, 190, 200], 1, "all");

		if self.focused_sprite is not None:
			api.OpenGL.fill_line_shape(self.current_sprite.rect.x, self.current_sprite.rect.y, self.current_sprite.rect.w, self.current_sprite.rect.h, [0, 255, 0, 200], 1, "all");

		api.OpenGL.unset(GL11.GL_SCISSOR_TEST);

		self.rect.h = util.clamp(height, 0, 400);

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

class Menu(imgui.Element):
	def __init__(self, master, x = 0, y = 0, w = 0, h = 0):
		super().__init__(master, "frame");

		self.background = [255, 255, 255, 50];
		self.rect_name = api.Rect(x, y, w, h);

		self.show = True;

		self.offset_x = 0;
		self.offset_y = 0;

		self.scroll = 0;

		self.open = False;
		self.last_tick_height = 0;

		self.loaded_widgets_list = [];
		self.scale = 3;

		self.button_load = self.add(imgui.Button(self.master, "Carregar", 0, 0));
		self.button_load.set_theme();
		self.button_load.background = [0, 0, 0, 0];
		self.button_load.id = 0;

		self.button_save = self.add(imgui.Button(self.master, "Salvar", 0, 0));
		self.button_save.set_theme();
		self.button_save.background = [0, 0, 0, 0];
		self.button_save.id = 1;
		self.button_save.show = False;

		self.button_save_as = self.add(imgui.Button(self.master, "Salvar Como", 0, 0));
		self.button_save_as.set_theme();
		self.button_save_as.background = [0, 0, 0, 0];
		self.button_save_as.id = 9;

		self.button_background = self.add(imgui.Button(self.master, "Background", 0, 0));
		self.button_background.set_theme();
		self.button_background.background = [0, 0, 0, 0];
		self.button_background.id = 2;

		self.button_exit = self.add(imgui.Button(self.master, "Sair", 0, 0));
		self.button_exit.set_theme();
		self.button_exit.background = [0, 0, 0, 0];
		self.button_exit.id = 3;

		self.font_renderer = self.master.font_renderer;
		self.theme = self.master.theme;

		self.last_dir = "/";
		self.loop_load = 0;
		self.loop_exit = 0;
		self.last_file = None;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		for widgets in self.loaded_widgets_list:
			widgets.on_key_event(key, state);

	def on_mouse_event(self, mx, my, button, state):
		for widgets in self.loaded_widgets_list:
			widgets.on_mouse_event(mx, my, button, state);

		if self.button_background.button_pressed:
			color = askcolor(title = "Escolha a cor!", color = (int(self.master.current_map.background_color[0]), int(self.master.current_map.background_color[1]), int(self.master.current_map.background_color[2])));

			if color[0] is not None:
				r, g, b = color[0];

				self.master.current_map.background_color = [r, g, b, 255];

			self.button_background.button_pressed = False;

		if self.button_save.button_pressed:
			if self.last_file is not None:
				self.master.current_map.save(self.last_file);

			self.button_save.button_pressed = False;

		if self.button_load.button_pressed or self.loop_load:
			if len(self.master.current_map.loaded_entity_list) != 0 or len(self.master.current_map.loaded_image_list) != 0:
				flag = messagebox.askquestion('Carregar', 'Você gostaria de salvar o mapa atual?', icon = 'warning');

				if flag == "yes":
					if self.last_file is None:
						file = tkinter.filedialog.asksaveasfile(initialdir = self.last_dir, mode = "w", defaultextension = ".json");

						if file is None:
							self.loop_load = 1;
						else:
							self.master.current_map.save(file.name);
							self.loop_load = 0;
					else:
						self.master.current_map.save(self.last_file);
						self.loop_load = 0;
				else:
					self.loop_load = 0;

			if self.loop_load is 0:
				file = tkinter.filedialog.askopenfilename(initialdir = self.last_dir, title = "Carregar", filetypes=[("Json files.", "*.json")]);

				if file != "":
					try:
						self.master.current_map.read(file);

						self.master.map_editor.leave();
						self.master.stage_map_editor = 2;
						self.master.file = file;
						self.master.loaded = False;					
						self.last_file = file;
						self.button_save.show = True;
						self.loop_load = 0;
					except:
						messagebox.showerror("Erro", "Este arquivo não condiz com os parametrôs do jogo ou está corrompido");

						util.log("Issue related, invalid file or corrupted.", "MAIN");

			self.button_load.button_pressed = False;

		if self.button_save_as.button_pressed:
			file = tkinter.filedialog.asksaveasfile(initialdir = self.last_dir, mode = "w", filetypes=[("Json files.", "*.json")]);

			if file is not None:
				self.master.current_map.save(file.name);

				self.last_file = file.name;
				self.button_save.show = True;

			self.button_save_as.button_pressed = False;

		if self.button_exit.button_pressed or self.loop_exit:
			flag_exit = messagebox.askokcancel("Sair", "Sair?", icon = "warning");

			if flag_exit == 0:
				self.button_exit.button_pressed = False;
				self.loop_exit = 0;

				return;

			if self.last_file is not None or (len(self.master.current_map.loaded_entity_list) != 0 or len(self.master.current_map.loaded_image_list) != 0 and self.last_file is None):
				flag = messagebox.askquestion('Sair', 'Você gostaria de salvar o mapa atual?', icon = 'warning')

				if self.last_file is not None and flag == "yes":
					self.master.task_manager.task("saving", task_save, [self.master.current_map, self.last_file]);
				else:
					if flag == "yes":
						file = tkinter.filedialog.asksaveasfile(initialdir = self.last_dir, mode = "w", filetypes=[("Json files.", "*.json")]);

						if file is None:
							self.loop_exit = 1;
						else:
							self.master.current_map.save(file.name);
							self.loop_exit = 0;
					else:
						self.loop_exit = 0;

			if self.loop_exit is 0:
				self.master.map_editor.leave();
				self.master.stage_map_editor = -1;
				self.master.stage_outgame = 0;
				self.loop_exit = 0;

			self.button_exit.button_pressed = False;

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

	def add(self, widget):
		self.loaded_widgets_list.append(widget);

		return widget;

	def render(self):
		api.OpenGL.fill(self.rect, [255, 255, 255, 50]);

		width = 4;
		height = 1;

		for widgets in self.loaded_widgets_list:
			if widgets.show is False:
				continue;
	
			widgets.render();
			widgets.update_mouse_over();
	
			widgets.string = [255, 255, 255, 255];
	
			widgets.offset_x = 2;
			widgets.offset_y = self.scale;
	
			widgets.rect.w = 150;
	
			widgets.rect.y = 4;
			widgets.rect.x = self.rect.x + width;
	
			width += widgets.rect.w + 2; #AAAA EU QUERO UM NAMOROADO
			height = widgets.rect.h;

		self.rect.h = height + 4 * 2;
		self.rect.w = self.master.screen_rect.w;

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

class FrameObject(imgui.Element):
	def __init__(self, master, x = 0, y = 0, w = 0, h = 0):
		super().__init__(master, "frame");

		self.background = [255, 255, 255, 50];
		self.rect_name = api.Rect(x, y, w, h);

		self.show = True;

		self.offset_x = 0;
		self.offset_y = 0;

		self.scroll = 0;

		self.open = False;
		self.last_tick_height = 0;

		self.loaded_widgets_list = [];
		self.scale = 3;

		self.label_title = self.add(imgui.Label(self.master, "Nome: ", 0, 0));
		self.label_title.set_theme();
		self.label_title.id = 0;

		self.label_path = self.add(imgui.Label(self.master, "Caminho: ", 0, 0));
		self.label_path.set_theme();
		self.label_path.id = 1;

		self.button_tile = self.add(imgui.Button(self.master, "Tile", 0, 0));
		self.button_tile.set_theme();
		self.button_tile.id = 8;
		self.button_tile.check_box = True;

		self.button_id = self.add(imgui.Mode(self.master, text = "Tipo", value = "phase", values = ["phase", "solid", "liquid"]));
		self.button_id.set_theme();
		self.button_id.id = 2;

		self.button_mode = self.add(imgui.Mode(self.master, "Mode", value = "repeat", values = ["repeat", "mir. repeat", "clamp to edge", "cla. to border", "scaled"]));
		self.button_mode.set_theme();
		self.button_mode.id = 7;

		self.button_static = self.add(imgui.Button(self.master, "Estatico", 0, 0));
		self.button_static.set_theme();
		self.button_static.id = 6;
		self.button_static.check_box = True;

		self.slider_alpha = self.add(imgui.Slider(self.master, "Alpha: ", 0, 0, 0, 255));
		self.slider_alpha.set_theme();
		self.slider_alpha.id = 3;

		self.font_renderer = self.master.font_renderer;
		self.theme = self.master.theme;

		self.current_object = None;
		self.the_type = "?";
		self.i = 0;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		if self.open is False:
			return;

		for widgets in self.loaded_widgets_list:
			widgets.on_key_event(key, state);

	def on_mouse_event(self, mx, my, button, state):
		if self.open is False:
			return;

		for widgets in self.loaded_widgets_list:
			widgets.on_mouse_event(mx, my, button, state);

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);

	def add(self, widget):
		self.loaded_widgets_list.append(widget);

		return widget;

	def refresh_object(self, object_):
		if object_ is None:
			self.current_object = None;
			self.open = False;

			return;

		if self.current_object is not object_:
			self.label_title.rect.tag = "Nome: " + object_.get_tag();
			self.label_path.rect.tag = "Caminho: " + object_.get_name();
			self.button_id.show = True;
			self.button_id.value = object_.get_id();
			self.slider_alpha.value = object_.alpha;
			self.slider_alpha.show = True;
			self.button_static.show = True;
			self.button_static.value = object_.static;
			self.button_mode.value = util.convert_mode_to_position(object_.get_mode());
			self.button_tile.button_pressed = object_.tile;
			self.button_tile.check_box = True;

			self.open = True;
			self.current_object = object_;

	def render(self):
		height = 1;
		
		api.OpenGL.set(GL11.GL_SCISSOR_TEST);
		api.OpenGL.cut(self.rect.x, self.rect.y, self.rect.w, self.rect.h, self.master.screen_rect);

		for widgets in self.loaded_widgets_list:
			if widgets.show is False:
				continue;
	
			widgets.render();
			widgets.update_mouse_over();
	
			widgets.string = [255, 255, 255, 255];
	
			widgets.offset_x = 2;
			widgets.offset_y = self.scale;
	
			widgets.rect.w = self.rect.w;
			widgets.rect.h = self.scale + self.font_renderer.get_height() + self.scale;
	
			widgets.rect.y = self.rect.y + self.scroll + height;
			widgets.rect.x = self.rect.x;
	
			height += widgets.rect.h + 4; # 4 suggestion by: Sakuya <3

		api.OpenGL.unset(GL11.GL_SCISSOR_TEST);

		self.last_tick_height = util.lerp(self.last_tick_height, height if self.open else 4, self.master.partial_ticks);
		self.rect.h = self.last_tick_height;

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

		if self.current_object is not None:
			self.current_object.alpha  = self.slider_alpha.value;
			
			if self.current_object.static is False and self.button_static.button_pressed:
				self.current_object.x = self.master.current_map.rect.x;
				self.current_object.y = self.master.current_map.rect.y;

				self.current_object.static = self.button_static.button_pressed;
			else:
				self.current_object.static = self.button_static.button_pressed;

			self.current_object.set_id(self.button_id.value);
			self.current_object.tile = self.button_tile.button_pressed;

			if self.button_mode.value != self.current_object.get_mode():
				self.current_object.set_mode(self.button_mode.value, self.master.texture_manager);

class UI:
	def __init__(self, master):
		self.master = master;

		self.rect = api.Rect(0, 0, 0, 0);
		self.title_rect = api.Rect(0, 0, 0, 0);

		self.title_rect.tag = "Caixa de Ferramentas!";
	
		self.mouse_click_left = False;
		self.mouse_over = False;

		self.recovery_y = 0;
		self.synced_y = True;

		self.drag_x = 0;
		self.drag_y = 0;

		self.offset_x = 0;
		self.offset_y = 0;

		self.loaded_widgets_list = [];
		self.background = [255, 255, 255, 50];

		self.font_renderer = None;

		self.scale = 3;
		self.width = 200;
		self.height = 0;

		self.current_map_tag = "Vazio";

	def init(self):
		self.rect.x = self.master.master.screen_rect.w / 2 - (50); # 100 / 2;
		self.rect.y = self.master.master.screen_rect.h / 2 - (self.master.master.screen_rect.h / 3);

		self.button_image = self.add(imgui.Button(self.master.master, "Adicionar", 0, 0));
		self.button_image.set_theme();
		self.button_image.id = 2;

		self.container_data = self.add(FrameData(self.master.master, 0, 0, 0, 0));
		self.container_data.set_theme();
		self.container_data.id = 8;

		self.container_object = self.add(FrameObject(self.master.master, 0, 0, 0, 0));
		self.container_object.set_theme();
		self.container_object.id = 5;

		self.container_menu = self.add(Menu(self.master.master, 0, 0, 0, 0));
		self.container_menu.set_theme();
		self.container_menu.id = 7;

		self.font_renderer = self.master.master.font_renderer;
		self.last_dir = "/"

	def add(self, widget):
		self.loaded_widgets_list.append(widget);

		return widget;

	def on_key_event(self, key, state):
		for widgets in self.loaded_widgets_list:
			widgets.on_key_event(key, state);

	def on_mouse_event(self, mx, my, button, state):
		rect = api.Rect(self.title_rect.x, self.title_rect.y, 10, self.rect.h);

		if state is Flag.KEYDOWN and button is 1 and self.mouse_over and rect.collide_with_mouse([mx, my]):
			self.mouse_click_left = True;

			self.drag_x = mx - rect.x;
			self.drag_y = my - rect.y;

		if state is Flag.KEYUP:
			self.mouse_click_left = False;

		for widgets in self.loaded_widgets_list:
			widgets.on_mouse_event(mx, my, button, state);

		if self.master.get_current_map() is None:
			return;

		current_sprite = self.container_data.current_sprite;
		current_image = self.master.get_current_map().current_image;

		if current_sprite is not None:
			self.container_object.refresh_object(current_sprite);

		if current_image is not None:
			self.container_object.refresh_object(current_image);

		if current_image is None and current_sprite is None and self.container_data.current_sprite is not None:
			self.container_data.refresh_object(None);

	def render(self, partial_ticks):
		if self.master.operable is False or self.master.get_current_map() is None:
			return;

		self.master.get_current_map().rect.x = 0;
		self.master.get_current_map().rect.y = self.container_menu.rect.h; # O menu.

		api.OpenGL.fill(self.rect, [0, 0, 0, 255]);
		api.OpenGL.fill(self.rect, self.background);

		rect_line = self.title_rect.add(2, 0);
		rect_line.set_size(self.width - 4, self.title_rect.h);

		api.OpenGL.fill_line_rect(rect_line, [0, 0, 0, 50], 2, "min_y-max_x");

		height_string = (self.scale + self.font_renderer.get_height() + self.scale);
		height_aligned = height_string;

		if self.button_image.button_pressed:
			file = tkinter.filedialog.askopenfilename(initialdir = self.last_dir, title = "Selecione arquivos!", filetypes = (("Arquivos PNG.", "*.png"), ("Todos os arquivos.", "*.*")));

			if file != "":
				try:
					shutil.copyfile(file, "data/" + os.path.basename(file));
				except:
					pass

				self.last_dir = os.path.split(file)[0];
				tag = util.path_split(file)[0];

				texture = api.Texture(tag, "nn", "data/" + os.path.basename(file), sheet = False);

				if self.master.master.texture_manager.get(tag) is None:
					self.master.master.texture_manager.load(texture, instant = True);
					self.container_data.add(texture);
				else:
					util.log("Detected a equals texture value.", "INFO-OBJECT");

			self.button_image.button_pressed = False;

		self.height = height_aligned + 6;

		self.mouse_over = self.rect.collide_with_mouse(self.master.master.mouse_position);
		self.offset_y = self.rect.y;

		for widgets in self.loaded_widgets_list:
			if widgets.show is False:
				continue;

			widgets.render();
			widgets.update_mouse_over();

			if type(widgets) is Menu:
				widgets.rect.x = 0;
				widgets.rect.y = 0;

				continue;

			widgets.string = [255, 255, 255, 255];

			widgets.offset_x = 2;
			widgets.offset_y = self.scale;

			widgets.rect.w = self.width - (12);

			widgets.rect.y = self.offset_y + self.height;
			widgets.rect.x = self.rect.x + 6;

			self.height += widgets.rect.h + 4; # 4 suggestion by: Sakuya <3

		if self.master.operable is False or self.master.get_current_map() is None:
			return;

		if self.mouse_click_left:
			x = (self.master.master.screen_rect.w - self.master.master.mouse_position[0]) + (self.drag_x);

			if x <= 200:
				x = 200;

			self.width = x;

		self.rect.set_position(self.master.master.screen_rect.w - self.width, self.master.get_current_map().rect.y);
		self.rect.set_size(self.width, self.master.master.screen_rect.h);

		self.font_renderer.render(self.title_rect.tag, self.title_rect.x + (self.width / 2) - (self.font_renderer.get_width(self.title_rect.tag) / 2), self.title_rect.y + 5, [255, 255, 255, 255]);
		self.master.get_current_map().mouse_over_something = self.mouse_over or self.container_menu.rect.collide_with_mouse(self.master.master.mouse_position);

		self.title_rect.set_position(self.rect.x, self.rect.y);
		self.title_rect.set_size(self.rect.w, height_aligned);

class Editor:
	def __init__(self, master):
		self.master = master;
		self.interface = None;

		self.operable = False;
		self.mouse_click_middle = False;
		self.mouse_click_left = False;
		self.mouse_click_right = False;

	def init(self):
		if self.interface == None:
			self.interface = UI(self);
			self.interface.init();

	def new_map(self, tag, id):
		self.operable = True;

		map_ = self.master.client_map.start(tag, id);
		map_.edit_mode = True;
		map_.grid = True;

		map_.init();

		del self.master.current_map;
		self.master.current_map = map_;

		self.master.camera.last_tick_x = 0;
		self.master.camera.last_tick_y = 0;

		self.master.camera.x = 0;
		self.master.camera.y = 0;

	def load_image_from_manager(self):
		for textures in self.master.texture_manager.textures:
			self.interface.container_data.add(textures);

	def leave(self):
		self.interface.container_data.loaded_widgets_list.clear();
		self.interface.container_object.loaded_widgets_list.clear();
		self.interface.loaded_widgets_list.clear();

		self.master.current_map.loaded_entity_list.clear();
		self.master.current_map.loaded_image_list.clear();

		self.interface = None;
		self.operable = False;
		self.master.current_map = None;

	def get_current_map(self):
		return self.master.current_map;

	def process_key_event(self, key, state):
		if self.interface is not None and self.operable:
			self.interface.on_key_event(key, state);

			if state is Flag.KEYDOWN and key == pygame.K_LEFT:
				self.master.camera.last_tick_x -= 5;

			if state is Flag.KEYDOWN and key == pygame.K_RIGHT:
				self.master.camera.last_tick_x += 5;

			if state is Flag.KEYDOWN and key == pygame.K_UP:
				self.master.camera.last_tick_y -= 5;

			if state is Flag.KEYDOWN and key == pygame.K_DOWN:
				self.master.camera.last_tick_y += 5;

	def process_mouse_event(self, mx, my, button, state):
		if self.interface is not None and self.operable:
			self.interface.on_mouse_event(mx, my, button, state);

			if state is Flag.KEYDOWN and self.get_current_map().mouse_over and (button == 1 or button == 3) and self.get_current_map().mouse_over_something is False and self.get_current_map().rect.collide_with_mouse([mx, my]):
				self.mouse_click_left = button == 1;
				self.mouse_click_right = button == 3;

			if state is Flag.KEYDOWN and self.get_current_map().mouse_over and button == 2 and self.get_current_map().mouse_over_something is False:
				self.drag_x = mx - self.master.camera.x;
				self.drag_y = my - self.master.camera.y;

				self.mouse_click_middle = True;

			if state is Flag.KEYUP:
				self.mouse_click_middle = False;
				self.mouse_click_right = False;
				self.mouse_click_left = False;
			else:
				self.tile_add_update();
				self.tile_remove_update();

	def tile_remove_update(self):
		if self.mouse_click_right and self.get_current_map().current_image is None:
			object_over = self.get_current_map().get_image(self.master.mouse_position, tile = True);

			if object_over is not None:
				del self.get_current_map().loaded_image_list[object_over.get_tag()];

	def tile_add_update(self):
		if self.mouse_click_left and self.get_current_map().current_image is None and self.get_current_map().mouse_over and self.interface.container_data.current_sprite is not None:
			if self.get_current_map().image_collide_with_mouse(self.master.mouse_position) is False:
				relative = self.get_current_map().get_relative_mouse_position();

				if self.interface.container_data.current_sprite.tile is False:
					relative = self.master.mouse_position;

				texture = self.master.texture_manager.get(self.interface.container_data.current_sprite.get_tag());
				image = self.get_current_map().add_image(self.interface.container_data.current_sprite, [relative[0], relative[1], universe.TILE_SIZE, universe.TILE_SIZE]);

	def on_mouse_motion(self, mx, my):
		if self.mouse_click_middle:
			self.master.camera.last_tick_x = mx - self.drag_x;
			self.master.camera.last_tick_y = my - self.drag_y;

		self.tile_add_update();
		self.tile_remove_update();

	def render(self, partial_ticks):
		if self.interface is not None and self.operable:
			self.get_current_map().w = self.master.screen_rect.w - self.interface.width;
			self.get_current_map().h = self.master.screen_rect.h;

			# Renderizamos antes dos widgets!
			if self.get_current_map().current_image is not None:
				image = self.get_current_map().current_image;

				if self.get_current_map().dragging_image:
					api.OpenGL.fill_shape(image.render_x, image.render_y, image.rect.w, image.rect.h, [0, 190, 190, 200]);	
				else:
					api.OpenGL.fill_line_shape(image.render_x, image.render_y, image.rect.w, image.rect.h, [0, 190, 190, 200], 1, "all");

			self.interface.render(partial_ticks);

			self.totally_images = 0 if self.get_current_map() is None else len(self.get_current_map().loaded_image_list);
			self.current_map_tag = "Vazio" if self.get_current_map() is None else self.get_current_map().tag;

			self.master.font_renderer.render("XY " + "[" + str(self.master.camera.x) + ", " + str(self.master.camera.y) + "] " + "Mapa: " + self.current_map_tag + " Img. Totais: " + str(self.totally_images) + " FPS: " + str(self.master.clock.get_fps()), 1, self.master.screen_rect.h - self.master.font_renderer.get_height() - 1, [255, 255, 255, 255]);