from .lib import Flag;
from .    import api, util;

class Element:
	def __init__(self, master, tag):
		self.master = master;

		self.rect = api.Rect(0, 0, 0, 0);
		self.rect.tag = tag;

		self.id = -1;

	def tag(self):
		return self.rect.tag;

class Theme:
	def __init__(self, master):
		self.master = master;

		self.background = [0, 0, 0, 255];
		self.string     = [255, 255, 255, 255];
		self.pressed    = [190, 190, 190, 200];
		self.unpressed  = [190, 190, 190, 100];
		self.highlight  = [190, 190, 190, 200];

class Label(Element):
	def __init__(self, master, text = "default", x = 0, y = 0):
		super().__init__(master, text);

		self.rect.x = x;
		self.rect.y = y;

		self.show = True;

		self.theme = self.master.theme;
		self.color = [255, 255, 255, 255];

		self.offset_x = 1;
		self.offset_y = 3;

		self.size = 3;

	def set_theme(self, color = None):
		if color is None:
			self.color = self.theme.string;
		else:
			self.color = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		pass

	def update_mouse_over(self):
		pass

	def render(self):
		self.rect.h = self.size + self.master.font_renderer.get_height() + self.size;

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, self.rect.h);

		self.master.font_renderer.render(self.tag(), self.rect.x + self.offset_x, self.rect.y + self.offset_y, self.color);

class Slider(Element):
	def __init__(self, master, text = "slider", x = 0, y = 0, minimum = 0, maximum = 0):
		super().__init__(master, text);

		self.show = True;
		self.button_pressed = False;

		self.offset_x = 0;
		self.offset_y = 0;

		self.theme = self.master.theme;

		self.string = [255, 255, 255, 255];
		self.background = [255, 255, 255, 50];
		self.pressed = [255, 255, 255, 50];
		self.highlight = [255, 255, 255, 50];

		self.offset_width = 0;
		self.offset_height = 0;

		self.value = 0;
		self.minimum = minimum;
		self.maximum = maximum;

		self.last_tick_highlight_alpha = 0;
		self.tick_highlight_alpha = 0;

		self.mouse_over = False;
		self.horizontal = True;
		self.mouse_clicked_left = False;

		self.size = 3;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		if state == Flag.KEYUP:
			if self.mouse_clicked_left and self.mouse_over:
				self.button_pressed = True;

			self.mouse_clicked_left = False;

		if self.mouse_over and self.show and button == 1 and state == Flag.KEYDOWN:
			self.mouse_clicked_left = True;

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);
		self.tick_highlight_alpha = self.background[3] if self.mouse_over else 0;

	def render(self):
		rect_animation = self.rect;

		api.OpenGL.fill_shape_rect(rect_animation, self.background);

		if self.horizontal:
			self.offset_width = ((self.rect.w) * (self.value - self.minimum) / (self.maximum - self.minimum));
		else:
			self.offset_height = ((self.rect.h) * (self.value - self.minimum) / (self.maximum - self.minimum));

		mouse = min(self.rect.w, max(0, self.master.mouse_position[0] - self.rect.x));

		if self.horizontal is False:
			mouse = min(self.rect.h, max(0, self.master.mouse_position[1] - self.rect.y));

		if self.mouse_clicked_left:
			if mouse == 0:
				self.value = self.minimum;
			else:
				rounded = int((mouse / (self.rect.w if self.horizontal else self.rect.h)) * (self.maximum - self.minimum) + self.minimum);

				self.value = rounded;

		api.OpenGL.fill_line_rect(self.rect.add(-2, 2), [0, 0, 0, 30], 2, "min_x-min_y-max_x");

		if self.tick_highlight_alpha != 0 and self.show:
			api.OpenGL.fill_shape_rect(rect_animation, [self.highlight[0], self.highlight[1], self.highlight[2], self.last_tick_highlight_alpha]);

		if self.horizontal:
			api.OpenGL.fill_shape(self.rect.x + self.offset_width, self.rect.y, self.size, self.rect.h, self.pressed);
		else:
			api.OpenGL.fill_shape(self.rect.x + self.rect.w, self.rect.y + self.offset_height, self.rect.w, self.pressed);

		self.last_tick_highlight_alpha = util.lerp(self.last_tick_highlight_alpha, self.tick_highlight_alpha, self.master.partial_ticks);

		self.rect.set_size(self.rect.w, self.rect.h);
		self.rect.set_position(self.rect.x, self.rect.y);

		if self.horizontal:
			self.master.font_renderer.render(self.tag() + " | " + str(self.value), rect_animation.x + self.offset_x, rect_animation.y + self.offset_y, self.string);

class Button(Element):
	def __init__(self, master, text = "button", x = 0, y = 0):
		super().__init__(master, text);

		self.show = True;
		self.button_pressed = False;

		self.offset_x = 0;
		self.offset_y = 0;

		self.theme = self.master.theme;

		self.string = [0, 0, 0, 0];
		self.background = [255, 255, 255, 50];
		self.pressed = [255, 255, 255, 50];
		self.highlight = [255, 255, 255, 50];

		self.last_tick_highlight_alpha = 0;
		self.tick_highlight_alpha = 0;

		self.mouse_over = False;
		self.mouse_clicked_left = False;
		self.check_box = False;

		self.size = 3;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		if state == Flag.KEYUP:
			if self.mouse_clicked_left and self.mouse_over:
				if self.check_box:
					self.button_pressed = False if self.button_pressed else True;
				else:
					self.button_pressed = True;

			self.mouse_clicked_left = False;

		if self.mouse_over and self.show and button == 1 and state == Flag.KEYDOWN:
			self.mouse_clicked_left = True;

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);
		self.tick_highlight_alpha = self.background[3] if self.mouse_over else 0;

	def render(self):
		rect_animation = self.rect.add(-2, 2) if self.mouse_clicked_left else self.rect;

		self.master.font_renderer.render(self.tag(), rect_animation.x + self.offset_x, rect_animation.y + self.offset_y, self.string);

		if self.check_box is False or (self.check_box and self.button_pressed):
			api.OpenGL.fill_shape_rect(rect_animation, self.background);

		if self.mouse_clicked_left is False:
			api.OpenGL.fill_line_rect(self.rect.add(-2, 2), [0, 0, 0, 30], 2, "min_x-min_y-max_x");

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, (self.size + self.master.font_renderer.get_height() + self.size));

		if self.tick_highlight_alpha != 0 and self.show:
			api.OpenGL.fill_shape_rect(rect_animation, [self.highlight[0], self.highlight[1], self.highlight[2], self.last_tick_highlight_alpha]);

		if self.mouse_clicked_left and self.show:
			api.OpenGL.fill_shape_rect(rect_animation, self.pressed);

		self.last_tick_highlight_alpha = util.lerp(self.last_tick_highlight_alpha, self.tick_highlight_alpha, self.master.partial_ticks);

class Mode(Element):
	def __init__(self, master, text = "Mode", value = None, values = [None]):
		super().__init__(master, text);

		self.show = True;
		self.button_pressed = False;

		self.offset_x = 0;
		self.offset_y = 0;

		self.theme = self.master.theme;

		self.string = [0, 0, 0, 0];
		self.background = [255, 255, 255, 50];
		self.pressed = [255, 255, 255, 50];
		self.highlight = [255, 255, 255, 50];

		self.last_tick_highlight_alpha = 0;
		self.tick_highlight_alpha = 0;

		self.value = value;
		self.values = values;

		self.index = 0;

		self.mouse_over = False;
		self.mouse_clicked_left = False;
		self.check_box = False;

		self.size = 3;

	def set_theme(self, color = None):
		if color is None:
			self.string = self.theme.string;
		else:
			self.string = color;

	def set_tag(self, string_tag):
		self.rect.tag = string_tag;

	def on_key_event(self, key, state):
		pass

	def on_mouse_event(self, mx, my, button, state):
		if state == Flag.KEYUP:
			if self.mouse_clicked_left and self.mouse_over:
				self.button_pressed = True;

			self.mouse_clicked_left = False;

		if self.mouse_over and self.show and button == 1 and state == Flag.KEYDOWN:
			self.mouse_clicked_left = True;

	def update_mouse_over(self):
		self.mouse_over = self.rect.collide_with_mouse(self.master.mouse_position);
		self.tick_highlight_alpha = self.background[3] if self.mouse_over else 0;

	def render(self):
		rect_animation = self.rect.add(-2, 2) if self.mouse_clicked_left else self.rect;

		api.OpenGL.fill_shape_rect(rect_animation, self.background);

		if self.mouse_clicked_left is False:
			api.OpenGL.fill_line_rect(self.rect.add(-2, 2), [0, 0, 0, 30], 2, "min_x-min_y-max_x");

		self.rect.set_position(self.rect.x, self.rect.y);
		self.rect.set_size(self.rect.w, (self.size + self.master.font_renderer.get_height() + self.size));

		if self.tick_highlight_alpha != 0 and self.show:
			api.OpenGL.fill_shape_rect(rect_animation, [self.highlight[0], self.highlight[1], self.highlight[2], self.last_tick_highlight_alpha]);

		if self.mouse_clicked_left and self.show:
			api.OpenGL.fill_shape_rect(rect_animation, self.pressed);

		if self.button_pressed:
			if self.index >= len(self.values) - 1:
				self.index = 0;
			else:
				self.index += 1;

			self.button_pressed = False;

		self.value = self.values[self.index];

		self.last_tick_highlight_alpha = util.lerp(self.last_tick_highlight_alpha, self.tick_highlight_alpha, self.master.partial_ticks);
		self.master.font_renderer.render(self.tag() + ": "  + self.value, rect_animation.x + self.offset_x, rect_animation.y + self.offset_y, self.string);