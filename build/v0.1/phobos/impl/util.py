from .lib import colorsys, time as time_, GL11, os, math;
from .    import api, universe, physic;

#
# IMPORTANTE:
# Você vai ver um monte de if e elif em alguns momentos,
# eu preferi não usar dict ou listas pra armazenar algumas informações.
#
# É PROPOSITAL!
#
PHOBOS_TEXTURE_MODE = {"repeat": [0, GL11.GL_REPEAT],
					   "mir. repeat": [1, GL11.GL_MIRRORED_REPEAT],
					   "clamp to edge": [2, GL11.GL_CLAMP_TO_EDGE],
					   "scaled": [4, GL11.GL_REPEAT]};

PHOBOS_OBJECT_ID = {"solid": 1,
				    "liquid": 2};

PHOBOS_SPECIAL_RENDER = {"player_spawn": [0, 190, 190],
						 "mob_spawn": [190, 0, 0],
						 "passive_spawn": [190, 190, 0],
						 "collision": [190, 0, 190]};

def read_history(data):
	data["finished"];
	data["first_time"];
	data["last_time"];
	data["current_time"];
	data["quest_done_count"];
	data["rounds"];

def load_history(history, data):
	history.finished = data["finished"];
	history.first_time = data["first_time"];
	history.last_time = data["last_time"];
	history.current_image = data["current_time"];
	history.quest_done_count = data["quest_done_count"];
	history.rounds = data["rounds"];

def save_history(history):
	data = {};

	data["finished"] = history.finished;
	data["first_time"] = history.first_time;
	data["last_time"] = history.last_time;
	data["current_time"] = history.current_time;
	data["quest_done_count"] = history.quest_done_count;
	data["rounds"] = history.rounds;

	return data;

# Beijinhos da rina.
def create_data_map(the_map):
	data = {};

	data["id"] = the_map.id;
	data["textures"] = [];
	data["color"] = the_map.background_color;

	for i, tags in enumerate(the_map.master.texture_manager.textures):
		textures = the_map.master.texture_manager.textures[tags];
		texture = {};

		texture["tag"] = textures.tag;
		texture["path"] = textures.path;

		data["textures"].append(texture);

	data["images"] = [];

	for i, tags in enumerate(the_map.loaded_image_list):
		images = the_map.loaded_image_list[tags];
		image = {};

		# Flags do objeto.
		image["tag"] = images.get_tag();
		image["name"] = images.get_name();
		image["mode"] = images.get_mode();
		image["id"] = images.get_id();
		
		# Estados importantes.
		image["alpha"] = images.alpha;
		image["static"] = images.static;
		image["tile"] = images.tile;
		image["visibility"] = images.visibility;
		
		# Tamanhos.
		image["x"] = images.rect.x;
		image["y"] = images.rect.y;
		image["w"] = images.rect.w;
		image["h"] = images.rect.h;

		data["images"].append(image);

	for i, ids in enumerate(the_map.loaded_entity_list):
		pass;

	return data;

# Rina.
def read_data_map(the_map, data):
	data["id"];
	data["color"];

	for textures in data["textures"]:
		continue;

	for images in data["images"]:
		images["tag"];
		images["name"];
		images["mode"];
		images["id"];
		images["alpha"];
		images["static"];
		images["tile"];
		images["visibility"];
		images["x"];
		images["y"];
		images["w"];
		images["h"];

# Rina.
def load_data_map(the_map, data):
	the_map.id = data["id"];
	texture_data = data["textures"];
	the_map.background_color = data["color"];

	the_map.loaded_image_list.clear();
	the_map.loaded_entity_list.clear();

	for textures in texture_data:
		if the_map.loaded_image_list.__contains__(textures["tag"]) is False:
			the_map.master.texture_manager.load(api.Texture(textures["tag"], "nn", "data/" + os.path.basename(textures["path"])), instant = True);

	image_data = data["images"];

	for images in image_data:
		tag = images["tag"];
		name = images["name"];
		mode = images["mode"];
		id = images["id"];

		alpha = images["alpha"];
		static = images["static"];
		tile = images["tile"];
		visibility = images["visibility"];

		x = images["x"];
		y = images["y"];
		w = images["w"];
		h = images["h"];

		if (name == "collision"):
			collide_rigid_rect = physic.Rectangle(physic.Math.vec2(x - (w / 2), y - (h / 2)), w, h);
			collide_rigid_rect.push(the_map.master.physic);
			continue;

		object_ = universe.Object(tag, x, y);
		object_.w = w;
		object_.h = h;

		object_.set_name(name);
		object_.set_tag(tag);
		object_.set_id(id);
		object_.set_mode(mode, the_map.master.texture_manager);

		object_.alpha = alpha;
		object_.static = static;
		object_.tile = tile;
		object_.visibility = visibility;

		the_map.add_image(object_, [x, y, w, h]);

# Rina.
def path_split(path):
	tup = os.path.split(str(path));
	tag = tup[len(tup) - 1].split(".")[0];

	return [tag, tup];

# Rina.
def convert_mode_to_position(mode):
	if PHOBOS_TEXTURE_MODE.__contains__(mode):
		return PHOBOS_TEXTURE_MODE[mode][0];

	return 3;

# Rina.
def convert_mode_to_byte(mode):
	if PHOBOS_TEXTURE_MODE.__contains__(mode):
		return PHOBOS_TEXTURE_MODE[mode][1];

	return GL11.GL_CLAMP_TO_BORDER;

# Rina.
def amount(value, maximum, distance):
	h = (value * 100) / maximum;
	l = distance / 100;

	return (h * l);

# Rina.
def convert_tag_to_id(tag):
	if PHOBOS_OBJECT_ID.__contains__(tag):
		return PHOBOS_OBJECT_ID[tag];

	return 0;

# Rina.
def convert_id_to_string(id):
	if id == 1:
		return "solid";
	elif id == 2:
		return "liquid";

	return "phase";

# Rina.
def clamp_rect(rect1, rect2, diff):
	x = rect1.x;
	y = rect1.y;

	w = rect1.w;
	h = rect1.h;

	if x <= diff[0]:
		x = diff[0];

	if y <= diff[1]:
		y = diff[1];

	if x + w >= (rect2.x + rect2.w) - diff[2]:
		x = (rect2.x + rect2.w) - w - diff[2];

	if y + h >= (rect2.y + rect2.h) - diff[3]:
		y = (rect2.y + rect2.h) - diff[3];

	rect1.x = x;
	rect1.y = y;

def collide_y(rect, i):
	return (rect.y + rect.h >= i.y and rect.y <= i.y + i.h) or (rect.y <= i.y + i.h and rect.y + rect.h >= i.y + i.h);

def get_colliding_side_rect(rect, i):
	side = {"up": False, "down": False, "left": False, "right": False};

	if rect.x + rect.w >= i.w and rect.x <= i.x + i.w and collide_y(rect, i):
		side["left"] = True;

	if rect.x <= i.x + i.w and rect.x + rect.w >= i.w and collide_y(rect, i):
		side["right"] = True;

	if rect.y + rect.h >= i.y and rect.y <= i.y + i.h:
		side["down"] = True;

	if rect.y <= i.y + i.h and rect.y + rect.h >= i.y + i.h:
		side["up"] = True;

	return [rect, side];

# Rina.
def registry(module_list, tag):
	if module_list.__contains__(tag) is False:
		module_list[tag] = tag;

	return tag;

# Rina.
def get_game_path(path, level):
	abs_split = path.split("\\")

	counter = 0;
	path = "";
	
	for modules in abs_split:
		folder_separator = "" if counter >= len(abs_split) - (level + 1) else "/";
	
		if counter < len(abs_split) - level:
			path = path + modules + folder_separator;

		counter += 1;

	return path;

# Rina.
def load_tiles(data, path):
	try:
		file = open(path);

		for i in json.load(file)["tiles"]:
			registry(data, i["state"]);
	except IOError as exc:
		util.log("Read tile exception: " + str(exc), "TILE-LOAD");

		return -1;

# Rina.
def save_tiles(data, path):
	try:
		with open("tiles.json", "w") as file:
			json.dump(data, file);
	except IOError as exc:
		util.log("Save tile exception: " + str(exc), "TILE-SAVE");

		return -1;

# Rina.
def add_angle_length(a, l, aa, ll):
	x, y = math.sin(a) * l + math.sin(aa) * ll, math.cos(a) * l + math.cos(aa) * ll;

	angle  = 0.5 * math.pi - math.atan2(x, y);
	length = math.hypot(x, y);

	return angle, length; 

# Rina.
def log(string_log, info = "MAIN"):
	print("[" + info + "] " + string_log);

# Rina.
def clamp(value, minimum, maximum):
	return minimum if value <= minimum else (maximum if value >= maximum else value);

# Rina.
def lerp(a, b, t):
	if t == 0 or a == b or t >= 1:
		return b;

	return a + (b - a) * t;

def apply_superior(name, image):
	image.superior = PHOBOS_SPECIAL_RENDER.__contains__(name);

def check_if_is_superior(name):
	if PHOBOS_SPECIAL_RENDER.__contains__(name):
		return PHOBOS_SPECIAL_RENDER[name];

	return [255, 255, 255];

# https://www.w3resource.com/python-exercises/math/python-math-exercise-77.php
# Tive que pegar, em java e mais facil fazer a conversao, isso ai ja e suficiente.
def rgb_to_hsb(r, g, b):
	r, g, b = r, g, b;

	mx = max(r, g, b);
	mn = min(r, g, b);

	df = mx - mn;

	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360
	if mx == 0:
		s = 0
	else:
		s = (df/mx)*100
	
	b = mx * 100
	
	return h, s, v

# Rina.
def currentTimeMillis():
	return time_.time() * 1000;

# RETIRADO DO colorsys.
def hsb_to_rgb(h, s, v):
	if s == 0.0:
		return v, v, v
	i = int(h*6.0) # XXX assume int() truncates!
	f = (h*6.0) - i
	p = v*(1.0 - s)
	q = v*(1.0 - s*f)
	t = v*(1.0 - s*(1.0-f))
	i = i%6
	if i == 0:
		return v, t, p
	if i == 1:
		return q, v, p
	if i == 2:
		return p, v, t
	if i == 3:
		return p, q, v
	if i == 4:
		return t, p, v
	if i == 5:
		return v, p, q

# Rina.
def hue_cycle(s, b):
	hue = currentTimeMillis() % (360.0 * 32.0) / (360.0 * 32.0);

	return hsb_to_rgb(hue, s * 100, b * 100);