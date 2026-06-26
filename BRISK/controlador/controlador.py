from tkinter.colorchooser import askcolor
from visao.Interface import *
from modelo.figuras import *

class Controlador:
    def __init__(self, janela):
    
        self.figuras = []
        self.figura_nova = None