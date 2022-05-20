from .lib import pygame, Flag, math, os, json, GL11;
from .    import api, util, imgui, universe;

class Logo:
	def __init__(self, master):
		self.master = master;
		self.master.texture_manager.load(api.Texture("logo", "ranklee", "data/logo.png"), instant = True);

		self.logo_texture = self.master.texture_manager.get("logo");
		self.start = 0;

		self.x = 0;
		self.y = 0;

		self.last_pos_w = 0;
		self.w = 0;

		self.texture_id = GL11.glGenTextures(1);

		data = pygame.image.tostring(self.logo_texture.image, "RGBA");

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.texture_id);

		GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_NEAREST);
		GL11.glTexParameterf(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_NEAREST);

		GL11.glTexImage2D(GL11.GL_TEXTURE_2D, 0, GL11.GL_RGBA, self.logo_texture.image.get_width(), self.logo_texture.image.get_height(), 0, GL11.GL_RGBA, GL11.GL_UNSIGNED_BYTE, data);
		
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

	def render(self, partial_ticks):
		self.last_pos_w = util.lerp(self.last_pos_w, self.w, partial_ticks);

		api.OpenGL.set(GL11.GL_SCISSOR_TEST);
		api.OpenGL.cut(self.x, self.y, self.last_pos_w, self.logo_texture.image.get_height(), self.master.screen_rect);
		api.OpenGL.fill_texture(self.x, self.y, self.logo_texture.image.get_width(), self.logo_texture.image.get_height(), self.texture_id, [255, 255, 255, 255]);
		api.OpenGL.unset(GL11.GL_SCISSOR_TEST);

class History:
	def __init__(self, master):
		self.master = master;

		# AQUI E LITERALMENTE A HISTORIA DO JOGO!
		self.finished = 0;
		self.first_time = 0;
		self.last_time = 0;
		self.current_time = 0;

		self.quest_done_count = 0;
		self.rounds = 0;

		# Salvamentos e coisas!
		self.data = None;

	def save(self):
		path = "history.dat";
		erase = open(str(path), 'w').close();

		self.data = util.save_history(self);

		file = open(str(path), 'w', encoding = 'utf-8');
		json.dump(self.data, file, ensure_ascii = 0, indent = 4);
		file.close();

		util.log("Saved game history successfully!", "MAIN");

	def read(self):
		path = "history.dat";

		if os.path.exists(path) is False:
			util.log("First time! :)", "MAIN-HISTORY");

			return;

		try:
			file = open(path, 'r');
			self.data = json.load(file);
			file.close();

			util.read_history(self.data);
		except:
			util.log("GAME CORRUPTED :(", "MAIN");

	def load(self):
		util.load_history(self, self.data);
		util.log("Game history loaded successfully!", "MAIN");

class Scene:
	def __init__(self, tag, callback):
		self.tag = tag;
		self.visiblity = False;
		self.callback = callback;

	def set_visibility(self):
		self.visiblity = True;

	def unset_visiblity(self):
		self.visiblity = False;

	def call(self, master):
		self.callback(master);

class SceneGroup:
	def __init__(self, master):
		self.master = master;
		self.scenes = {};

		self.current = "null";

	def add_scene(self, scene):
		if self.scenes.__contains__(scene.tag) is False:
			self.scenes[scene.tag] = scene;

	def remove_scene(self, scene):
		if self.scenes.__contains__(scene.tag):
			del self.scenes[scene.tag];

	def unset_scene(self, tag):
		if self.scenes.__contains__(tag):
			self.scenes[tag].unset_visiblity();
			self.current = "null";

	def set_visiblity_and_current(self, tag):
		if self.scenes.__contains__(tag):
			self.scenes[tag].set_visibility();
			self.current = tag;

	def process(self):
		if self.current is not "null":
			if self.scenes.__contains__(self.current):
				if self.scenes[self.current].visiblity:
					self.scenes[self.current].call(self.master);
			else:
				self.current = "null";

class MainMenu(api.Gui):
	def __init__(self, master):
		super().__init__("MainMenu");

		self.master = master;
		self.logo = Logo(self.master);

		self.loaded_widgets_list = [];
		self.offset = self.master.screen_rect.h;

		# Jogar!
		self.button_play = imgui.Button(self.master, "Jogar", 0, 0);
		self.button_play.set_theme();
		self.button_play.id = 0;

		# Quando ter algo salvo, vai buscar por continuar!
		self.button_resume = imgui.Button(self.master, "Continuar", 0, 0);
		self.button_resume.set_theme();
		self.button_resume.id = 1;
		self.button_resume.show = False;

		# Editor de mapas fofo da rina!
		self.button_map_editor = imgui.Button(self.master, "Editor de Mapas", 0, 0);
		self.button_map_editor.set_theme();
		self.button_map_editor.id = 2;

		# Área de configuração!
		self.button_settings = imgui.Button(self.master, "Configuração", 0, 0);
		self.button_settings.set_theme();
		self.button_settings.id = 3;
		self.button_settings.show = False;

		# Sair, pra fazer sair do jogo!
		self.button_exit = imgui.Button(self.master, "Sair", 0, 0);
		self.button_exit.set_theme();
		self.button_exit.id = 4;

		# Registramos os botões.
		self.loaded_widgets_list.append(self.button_play);
		self.loaded_widgets_list.append(self.button_resume);
		self.loaded_widgets_list.append(self.button_map_editor);
		self.loaded_widgets_list.append(self.button_settings);
		self.loaded_widgets_list.append(self.button_exit);

	def on_close(self):
		self.offset = self.master.screen_rect.h;
		self.logo.last_pos_w = 0;
		self.logo.w = self.logo.logo_texture.image.get_width();

	def on_open(self):
		self.offset = self.master.screen_rect.h;
		self.logo.last_pos_w = 0;
		self.logo.w = self.logo.logo_texture.image.get_width();

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		for widgets in self.loaded_widgets_list:
			widgets.on_mouse_event(mx, my, button, state);

		if self.button_play.button_pressed:
			if self.master.history.first_time == 0:
				self.master.current_map = self.master.client_map.start("level_1", 1);
				self.master.current_map.load("map/level1/level_1.json");
				self.master.current_map.add_entity(self.master.player);
				self.master.current_map.spawn_player();

			self.button_map_editor.button_pressed = False;

		if self.button_resume.button_pressed:
			self.button_resume.button_pressed = False;

		if self.button_map_editor.button_pressed:
			self.master.stage_map_editor = 0;

			self.button_map_editor.button_pressed = False;

		if self.button_settings.button_pressed:
			self.button_settings.button_pressed = False;

		if self.button_exit.button_pressed:
			# Dizemos ao pygame para fecha-lo!
			pygame.event.post(pygame.event.Event(pygame.QUIT));

			self.button_exit.button_pressed = False;

	def on_render(self, mx, my, partial_ticks):
		self.logo.x = (self.master.screen_rect.w / 2) - (self.logo.logo_texture.image.get_width() / 2);
		self.logo.y = (self.master.screen_rect.h / 2) - (self.logo.logo_texture.image.get_height());

		self.logo.render(partial_ticks);

		self.master.font_renderer.render("Versão 0.7a - Phobos Base - Programado por Rina - Design por Werneck, Ranklee & Cosmic 2.0", 1, self.master.screen_rect.h - self.master.font_renderer.get_height() - 1, [255, 255, 255, self.last_tick_alpha_255]);
		self.offset = util.lerp(self.offset, (self.logo.y + self.logo.logo_texture.image.get_height() + (self.logo.logo_texture.image.get_height() / 6)), partial_ticks * 0.5);

		position_y = self.offset;

		for widgets in self.loaded_widgets_list:
			if widgets.show is False:
				continue;

			widgets.render();
			widgets.update_mouse_over();

			widgets.string = [255, 255, 255, self.last_tick_alpha_255];

			uvu = self.master.font_renderer.get_width(widgets.tag());
			uuv = self.master.font_renderer.get_width(widgets.tag()) / 2;

			widgets.offset_x = uuv;
			widgets.offset_y = 3;

			widgets.rect.w = uuv + uvu + uuv;

			widgets.rect.y = position_y;
			widgets.rect.x = ((self.master.screen_rect.w / 2) - (widgets.rect.w / 2));

			position_y += widgets.rect.h + 4; # 4 suggestion by: Sakuya <3

class Loading(api.Gui):
	def __init__(self, master):
		super().__init__("Loading");

		self.master = master;

		self.rect = api.Rect(0, 0, 0, 0);
		self.rect.tag = "loading...";

		self.tick_offset = 0;
		self.last_tick_offset = 0;

		self.rotation = 1;

		self.stage = 0;

		self.flag = 0;
		self.rgb = [0, 0, 0];

	def on_close(self):
		self.last_tick_offset = 0;

	def on_open(self):
		self.tick_offset = 25;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		pass

	def on_render(self, mx, my, partial_ticks):
		rgb = util.hue_cycle(1, 1);

		if self.stage != 0:
			self.rotation = 361;
		else:
			self.rotation = -361;

		if self.rect.angle > 360:
			self.stage = 0;
			self.rotation

		if self.rect.angle < -360:
			self.stage = 1;
			self.rotation = 1;

		self.rect.angle = util.lerp(self.rect.angle, self.rotation, partial_ticks * 0.1);
		self.last_tick_offset = util.lerp(self.last_tick_offset, self.tick_offset, partial_ticks * 0.1);

		clamp50 = util.clamp(self.tick_alpha_255, 0, 50);

		self.rect.set_position(self.master.screen_rect.w - self.rect.w - self.last_tick_offset, self.master.screen_rect.h - self.rect.h - self.last_tick_offset);
		self.rect.set_size(clamp50, clamp50);

		api.OpenGL.fill(self.rect, [255, 255, 255, clamp50]);
		api.OpenGL.fill(self.rect, [255, 255, 255, clamp50]);

class StartGameGui(api.Gui):
	def first_scene(master):
		text = "Phobos team apresenta...";

		if master.timer.is_passed(500) and master.timer.is_passed(2000) is False and master.skip is False:
			master.tick_alpha_text = 255;

		if master.timer.is_passed(2000) or master.skip:
			master.tick_alpha_text = 0;

			if master.last_tick_alpha_text <= 10:
				if master.skip:
					master.skip = False;

				master.scene_group.unset_scene("FirstScene");
				master.timer.reset();
				master.stage = 1;

		x = (master.master.screen_rect.w / 2) - (master.master.font_renderer.get_width(text) / 2);
		y = (master.master.screen_rect.h / 2) - (master.master.font_renderer.get_height() / 2);

		master.master.font_renderer.render(text, x, y, [255, 255, 255, master.last_tick_alpha_text]);

	def second_scene(master):
		text = "Undefined!";

		if master.timer.is_passed(500) and master.timer.is_passed(2000) is False and master.skip is False:
			master.tick_alpha_text = 255;

		if master.timer.is_passed(2000) or master.skip:
			master.tick_alpha_text = 0;

			if master.last_tick_alpha_text <= 10:
				if master.skip:
					master.skip = False;

				master.scene_group.unset_scene("SecondScene");
				master.close();

		x = (master.master.screen_rect.w / 2) - (master.master.font_renderer.get_width(text) / 2);
		y = (master.master.screen_rect.h / 2) - (master.master.font_renderer.get_height() / 2);

		master.master.font_renderer.render(text, x, y, [255, 255, 255, master.last_tick_alpha_text]);

	def __init__(self, master):
		super().__init__("StartGameGui");

		self.master = master;
		self.stage = 0;
		self.timer = api.TimerStamp();

		self.scene_group = SceneGroup(self);

		self.scene_group.add_scene(Scene("FirstScene", StartGameGui.first_scene));
		self.scene_group.add_scene(Scene("SecondScene", StartGameGui.second_scene));

		self.tick_alpha_text = 0;
		self.last_tick_alpha_text = 0;

		self.skip = False;

	def on_close(self):
		self.master.stage_start = 1;
		self.skip = False;

	def on_open(self):
		self.timer.reset();
		self.stage = 0;
		self.skip = False;

	def on_key_event(self, key, state):
		if key == pygame.K_SPACE and state == Flag.KEYDOWN:
			self.skip = True;

	def on_mouse_event(self, mx, my, button, state):
		pass

	def on_render(self, mx, my, partial_ticks):
		self.last_tick_alpha_text = util.lerp(self.last_tick_alpha_text, self.tick_alpha_text, partial_ticks);

		if self.stage == 0:
			self.scene_group.set_visiblity_and_current("FirstScene");

		if self.stage == 1:
			self.scene_group.set_visiblity_and_current("SecondScene");

		self.scene_group.process();