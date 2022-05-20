# Importamos principais libs pelo lib.py.
from .lib import pygame, sys, Flag, GL11, GLU, threading, time, tkinter;
from .    import ingame, api, util, imgui, universe, editor, physic, entity;

# Antes de tudo definios coisas basicas... que serão mudadas depois!
VERSION = "0.1";
NAME    = "Undefined";

# Os estagios de cada sessão do jogo.
# -1 fora de sessão...
#  0 dentro de uma sessão!
#
# As vezes em meio ao código você vai
# perceber que eu estou usando muitos 
# 1, 2... eles são alguns levels mais
# altos, talvez um menu, splash...
#
# Algumas vezes usarei mais numeros
# negativos tá bom!kkk
#
START_STAGE   = 0;
OUTGAME_STAGE = 0;

# As vezes um carregamento não dura
# alguns milessimos de segundo, mas
# mesmo assim assim vou manter uma 
# base de tempo, curta mas padrão
# para poupar muito processamento!
#
LOADING_BASE = 200;

# Eventos do jogo.
WORLD_RENDER_REFRESH = pygame.USEREVENT + 1;

# Damos inicio ao pygame.
pygame.init();
pygame.mixer.quit();

# Resolve algum problema com Tkinter.
tkinter.Tk().withdraw();

# Vi em um site.
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.VIDEORESIZE]);

# Surface pro icone.
ico_surface = pygame.image.load("data/ico.ico");

# Tarefas que uso.
def refresh_task_map_editor(args):
	args[0].current_map;
	args[0].client_map.end();
	args[0].map_editor.new_map("random", -1);
	args[0].map_editor.init();
	args[0].current_map.load(args[0].file);

	return 1;

class Game:
	def __init__(self):
		util.log("Preparing Phobos base for init...");

		# Iniciamos as settings do jogo!
		self.game_settings = api.GameSetting(self);
		self.game_settings.init();

		# Carrega as configuracoes do jogo.
		self.game_settings.on_load();

		self.screen_width = self.game_settings.setting_fullscreen.value("width");
		self.screen_height = self.game_settings.setting_fullscreen.value("height");

		self.update_display();
		self.update_title();

		util.log("Window created and update!");

		self.game_gui = api.GameGui(self);
		self.game_gui.init();

		self.texture_manager = api.TextureManager(self);
		self.render_manager  = universe.RenderManager(self);
		self.task_manager = api.TaskManager();

		util.log("Settings & managers was initialized!");

		self.camera = universe.Camera(self, 0, 0);

		util.log("Camera created!");

		self.map_editor = editor.Editor(self);

		util.log("Map editor created!");

		self.physic = physic.Physic(self);
		self.input_manager = api.InputManager(self);
		self.history = ingame.History(self);

		util.log("Input, physic & history created!");

	def update_display(self):
		flags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE;

		if self.game_settings.setting_fullscreen.value("active"):
			flags |= pygame.FULLSCREEN;

		self.display = pygame.display.set_mode((self.screen_width, self.screen_height), flags);

		# ...
		pygame.display.set_icon(ico_surface);

	def update_title(self):
		pygame.display.set_caption(NAME + " " + VERSION);

	def init(self):
		self.updating_settings = True;
		self.mouse_position = [0, 0];

		# Variaveis importantes para processamento de efeitos e fisica!
		self.clock = pygame.time.Clock();
		self.partial_ticks = 0.0;
		self.last_delta_ticks = 0.0;
		self.delta_ticks = 0.0;
		self.timer = 60;
		self.fps = 1000;
		self.interval = 1000/self.fps;

		# Coloracao do jogo!
		self.background_color = [0, 0, 0];
		self.background_main_menu_color = 0;

		self.running = True;
		self.screen_rect = api.Rect(0, 0, self.screen_width, self.screen_height);

		# Tema e o render da font!
		self.font_renderer = api.FontRenderer(self, font = "Verdana", size = 16);
		self.theme = imgui.Theme(self);

		# Estagios importantes para o funcionamento de GUIs em geral.
		self.stage_start = START_STAGE;
		self.stage_outgame = OUTGAME_STAGE;
		self.stage_map_editor = -1;
		self.stage_input = 0;

		# Loadings e besteiras.
		self.loading_now  = "no";
		self.loading_time = -1;

		# Alguns stamps...
		self.loading_stamp = api.TimerStamp();
		self.running_stamp = api.TimerStamp();
		self.update_stamp = api.TimerStamp();

		self.current_map = None;
		self.client_map = universe.Map(self);
		self.loaded = False;
		self.file = "";

		self.player = None;
		self.create_player("SrRina", -1337);

		util.log("All GUIs initialized and registered!");
		util.log(NAME + " " + VERSION + " successfully started!");

		pygame.time.set_timer(WORLD_RENDER_REFRESH, 500);

		self.history.read();

	def run(self):
		while 1:
			self.wait();
			self.mouse_position = pygame.mouse.get_pos();

			# Manuzeamos os eventos.
			self.handler_for_loop_event();

			# Fizemos o update da tela!
			if self.update_stamp.is_passed(self.interval):
				self.update_stamp.reset();

				# Calculamos os partial ticks.
				self.partial_ticks = self.clock.tick(self.fps) / self.timer;

				# Diferenciamos a tela de loading!
				self.handle_loading_event();

				# Terminamos os updates!
				self.handler_out_event();
				self.update();

				# Antes de tudo devemos limpar a tela!
				self.clear();
				self.render();
				
				# Ciclo do jogo!
				self.mainloop();

				# Ler o fps...
				# util.log("FPS: " + str(self.clock.get_fps()), "INFO-VIDEO");

	def call_update(int, self):
		pass

	def create_player(self, name, id):
		self.player = entity.EntityPlayer(name, id);

	def wait(self):
		if self.updating_settings:
			self.fps = self.game_settings.setting_framerate.value("value");
			self.updating_settings = False;

	def clear(self):
		GL11.glClearColor(self.background_color[0] / 255.0, self.background_color[1] / 255.0, self.background_color[2] / 255.0, 1);
		GL11.glClear(GL11.GL_DEPTH_BUFFER_BIT | GL11.GL_COLOR_BUFFER_BIT);

		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();
		GL11.glOrtho(0, self.screen_rect.w, self.screen_rect.h, 0, -1, 1)

		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glDepthFunc(GL11.GL_NEVER);

	def update(self):
		self.camera.update(self.partial_ticks);
		self.input_manager.update();

		if self.stage_outgame == -2 and self.current_map is not None and self.stage_map_editor != 2:
			self.current_map.update(self.partial_ticks);
			self.physic.update();

	def render(self):
		if (self.stage_outgame is not -2 or self.loading_now == "refresh") and self.background_main_menu_color < 50:
			self.background_main_menu_color = util.lerp(self.background_main_menu_color, 50, self.partial_ticks * 0.3);

		if (self.stage_outgame is -2 and self.loading_now != "refresh") and self.background_main_menu_color > 0:
			self.background_main_menu_color = util.lerp(self.background_main_menu_color, 0, self.partial_ticks);

		if self.background_main_menu_color != 0:
			api.OpenGL.fill_shape(self.screen_rect.x, self.screen_rect.y, self.screen_rect.w, self.screen_rect.h, [255, 255, 255, self.background_main_menu_color]);

		self.game_gui.process_render(self.mouse_position[0], self.mouse_position[1], self.partial_ticks);

		if self.stage_outgame == -2 and self.current_map is not None and self.stage_map_editor != 2:
			self.render_manager.render(self.partial_ticks);

			if self.stage_input == 1:
				self.input_manager.render();

		if self.stage_map_editor == 1:
			self.map_editor.render(self.partial_ticks);

	def handler_for_loop_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				util.log(NAME + " " + VERSION + " was closed!");

				self.ruinning = False;

				self.history.save();
				self.game_settings.on_save();

				pygame.quit();
				sys.exit();

			if event.type == WORLD_RENDER_REFRESH and self.current_map != None:
				self.render_manager.refresh();

			if event.type == pygame.MOUSEMOTION:
				if self.stage_map_editor == 1:
					self.map_editor.on_mouse_motion(event.pos[0], event.pos[1]);

				if self.current_map is not None:
					self.current_map.on_mouse_motion(event.pos[0], event.pos[1]);

			if event.type == pygame.VIDEORESIZE:
				self.screen_width = event.size[0];
				self.screen_height = event.size[1];

				self.screen_rect.set_position(0, 0);
				self.screen_rect.set_size(self.screen_width, self.screen_height);

			if event.type == pygame.KEYUP:
				self.game_gui.process_key_event(event.key, Flag.KEYUP);
				self.map_editor.process_key_event(event.key, Flag.KEYUP);

				if self.stage_input == 1:
					self.input_manager.on_key_event(event.key, Flag.KEYUP);

				if self.current_map is not None:
					self.current_map.on_key_event(event.key, Flag.KEYUP);

			if event.type == pygame.KEYDOWN:
				self.game_gui.process_key_event(event.key, Flag.KEYDOWN);
				self.map_editor.process_key_event(event.key, Flag.KEYDOWN);

				if self.stage_input == 1:
					self.input_manager.on_key_event(event.key, Flag.KEYDOWN);

				if self.current_map is not None:
					self.current_map.on_key_event(event.key, Flag.KEYDOWN);

			if event.type == pygame.MOUSEBUTTONUP:
				self.game_gui.process_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYUP);
				self.map_editor.process_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYUP);

				if self.stage_input == 1:
					self.input_manager.on_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYUP);

				if self.current_map is not None:
					self.current_map.on_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYUP);

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.game_gui.process_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYDOWN);
				self.map_editor.process_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYDOWN);

				if self.stage_input == 1:
					self.input_manager.on_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYDOWN);

				if self.current_map is not None:
					self.current_map.on_mouse_event(event.pos[0], event.pos[1], event.button, Flag.KEYDOWN);

	def handler_out_event(self):
		if self.game_gui.current_gui is not None and self.game_gui.current_gui.active is False:
			self.game_gui.current_gui = None;

		if self.stage_start == 0 and type(self.game_gui.current_gui) != ingame.StartGameGui and self.current_map is None:
			self.game_gui.open(ingame.StartGameGui(self));

		if self.stage_start == 2 and self.stage_outgame == 0 and self.current_map is not None and type(self.game_gui.current_gui) != ingame.Loading:
			self.game_gui.open(ingame.Loading(self));
			self.loading_stamp.reset();
			
			self.loading_time = LOADING_BASE;
			self.loading_now = "map-loading";

			self.stage_outgame = -1;

		if self.stage_start == 2 and self.stage_outgame == 0 and self.stage_map_editor == 0 and type(self.game_gui.current_gui) != ingame.Loading:
			self.game_gui.open(ingame.Loading(self));
			self.loading_stamp.reset();

			self.loading_time = LOADING_BASE;
			self.loading_now = "map-editor-loading";

			self.stage_outgame = -1;

		if self.stage_start == 1 and type(self.game_gui.current_gui) != ingame.Loading:
			self.game_gui.open(ingame.Loading(self));
			self.loading_stamp.reset();

			self.loading_time = LOADING_BASE;
			self.loading_now = "start-loading";

		if self.stage_start == 2 and self.stage_outgame == 0 and type(self.game_gui.current_gui) != ingame.MainMenu:
			self.game_gui.open(ingame.MainMenu(self));

		if self.stage_start == 2 and self.stage_outgame == -2 and self.stage_map_editor == 2 and type(self.game_gui.current_gui) != ingame.Loading:
			self.game_gui.open(ingame.Loading(self));
			self.loading_now = "refresh";
			self.loading_time = 1500;
			self.loading_stamp.reset();

	def handle_loading_event(self):
		if self.loading_now == "start-loading":
			if self.loading_stamp.is_passed(self.loading_time):
				self.game_gui.close();
				self.loading_now = "no";
				self.stage_start = 2;

			if self.texture_manager.unloaded_count == self.texture_manager.loaded_count and self.texture_manager.loaded_count != 0:
				if self.texture_manager.initialized is False:
					self.loading_time += 10 * self.texture_manager.loaded_count;
					self.texture_manager.set_initialized();
			else:
				self.texture_manager.init();

		if self.loading_now == "refresh":
			if self.loaded is False and self.file is not "":
				self.task_manager.task("refresh", refresh_task_map_editor, [self]);
				self.loaded = True;

			if self.task_manager.is_task_done("refresh"):
				self.map_editor.init();
				self.map_editor.load_image_from_manager();
				self.map_editor.interface.container_menu.last_file = self.file;
				self.map_editor.interface.container_menu.button_save.show = True;

				self.game_gui.close();
				self.stage_map_editor = 1;
				self.loading_now = "no";

		if self.loading_now == "map-loading":
			if self.loading_stamp.is_passed(self.loading_time):
				self.game_gui.close();
				self.stage_outgame = -2;
				self.loading_now = "no";

		if self.loading_now == "map-editor-loading":
			if self.map_editor.interface is None:
				self.map_editor.init();

			if self.map_editor.operable is False:
				# Criamos um mapa vazio e sincronizamos o "DATA" com os materais registrados do jogo/client!
				self.map_editor.new_map("undefined", -999);
				self.map_editor.load_image_from_manager();

				self.loading_time += 500;

			if self.loading_stamp.is_passed(self.loading_time):
				self.game_gui.close();
				self.stage_outgame = -2;
				self.stage_map_editor = 1;
				self.stage_input = 0;
				self.loading_now = "no";

	def mainloop(self):
		pygame.display.flip();