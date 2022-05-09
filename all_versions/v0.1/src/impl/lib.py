# Importes que vamos usar aqui.
# A biblioteica que vamos utilizar é a Pygame.
# Eu usaria pyglet, mas é um jogo 2D e eu não to afim de usar SDL.
# Mesmo Pygame sendo em SDL.
import pygame;

# Tambem usaremos OpenGL legacy!
from OpenGL import GL as GL11; # v1.1;
from OpenGL import GLU;

# Outros.
from tkinter import filedialog;
from tkinter.colorchooser import askcolor
from tkinter import messagebox;

import tkinter as tkinter;

import threading;
import colorsys;
import time;
import math;
import json;
import csv;
import shutil;
import sys;
import os;

RANGE = range if sys.version_info[0] >= 3 else xrange;

# Também criamos as flags que para o processo do jogo!
class Flag:
	KEYDOWN = 0;
	KEYUP = 1;

	LOADING_NEEDED = 2;
	LOADED_ENDED = 3;

	NO_LOADING = 4;

	MBUTTON_LEFT = 1;
	MBUTTON_RIGHT = 3;
	MBUTTON_MIDDLE = 2;

	DISABLED = 0;
	LIMITED = 1;
	CONFLICT = 2;