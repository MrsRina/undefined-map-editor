# Como o jogo terá apenas suporte a Windows, vamos ter certeza
# de rodar apenas no CMD do Windows.
import sys
import os

# Limpamos os logs antigos!
os.system("cls");

# Obtemos o path deste arquivo.
abs_path = os.getcwd();

print("#################################");
print("# Phobos Game Base");
print("# Autores ");
print("# Programador (a): Rina");
print("# Design: werneck, ranklee, cosmic");
print(" ");

# Damos inicio ao segmento.
# Com log!
print("Buscando por arquivos Python em: " + abs_path);

# Cortamos ele.
abs_split = abs_path.split("\\")

# Criamos o counter e o path para ser injetavel.
counter = 0;
path = "";

# Listamos cada modulo ("/modulo/").
# Modules não é a definição correta pra isso,
# mas é melhor assim.
for modules in abs_split:
	# Verificamos antes se dá sim pra colocar / ou não.
	folder_separator = "" if counter >= len(abs_split) - 2 else "/";

	# Aplicamos a adição de string.
	if counter < len(abs_split) - 1:
		path = path + modules + folder_separator;

	# $$ Contamos@!!! :")
	counter += 1;

# Printamos o achado!
print("Caminho encontrado: " + path);

# Log pra ficar bonitinho!
print("Python injetado em: " + path + "/" + "python" + "/" + "phobos.py");
print(" ");

# Inserimos o caminho correto de todo o projeto/jogo.
sys.path.insert(1, path);
os.chdir(path);

# Removes o message do pygame.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide";

# Executamos.
exec(open(path + "/" + "game.py").read());