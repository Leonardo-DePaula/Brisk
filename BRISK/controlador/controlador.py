import math
from tkinter.colorchooser import askcolor
from visao.Interface import *
from modelo.figuras import *

class Controlador:
    def __init__(self, janela):
        self.janela = janela
        self.interface = Interface(janela)

        self.figuras = []
        self.figura_nova = self.poligono_em_construcao = self.poligono_preview = None
        self.ini_x = self.ini_y = 0

        self.cor_preenchimento, self.cor_borda, self.tamEspessura = "", "black", 1

        self.conectar_eventos()

    def conectar_eventos(self):

        self.interface.swatch_preenchimento.config(command=self.escolher_cor_pr)
        self.interface.swatch_borda.config(command=self.escolher_cor_brd)

        self.interface.tamanho_espessura_esc.bind(
            "<ButtonRelease-1>", self.escolher_tamEspessura
        )

        self.interface.botao_limpar.config(command=self.limpar_tela)

        canvas = self.interface.canvas
        canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        canvas.bind('<Motion>', self.atualizar_preview_poligono)

    def iniciar_figura_nova(self, event):
        self.ini_x, self.ini_y = event.x, event.y
        c = (event.x, event.y, event.x, event.y)
        tipo = self.interface.tipo_figura_var.get()

        match tipo:
            case "Linha":
                self.figura_nova = Linha(*c, self.cor_borda, self.tamEspessura)
            case "Rabisco":
                self.figura_nova = Rabisco([(event.x, event.y)], self.cor_borda, self.tamEspessura)
            case "Círculo":
                self.figura_nova = Circulo(*c, self.cor_borda, self.cor_preenchimento, self.tamEspessura)
            case "Oval":
                self.figura_nova = Oval(*c, self.cor_borda, self.cor_preenchimento, self.tamEspessura)
            case "Retângulo":
                self.figura_nova = Retangulo(*c, self.cor_borda, self.cor_preenchimento, self.tamEspessura)
            case "Polígono":
                if self.poligono_em_construcao is None:
                    self.poligono_em_construcao = Poligono(
                        [event.x, event.y],
                        self.cor_borda,
                        self.cor_preenchimento,
                        self.tamEspessura
                    )
                else:
                    pontos = self.poligono_em_construcao.pontosPoligonos
                    primeiro_x, primeiro_y = pontos[0], pontos[1]
                    distancia = math.hypot(event.x - primeiro_x, event.y - primeiro_y)

                    if len(pontos) >= 6 and distancia <= 8:
                        self.fechar_poligono()
                    else:
                        pontos.extend([event.x, event.y])

                self.desenhar()

    def atualizar_figura_nova(self, event):
        if not self.figura_nova:
            return

        if isinstance(self.figura_nova, Rabisco):
            self.figura_nova.pontos.append((event.x, event.y))
        else:
            self.figura_nova.x2 = event.x
            self.figura_nova.y2 = event.y

        self.desenhar()

    def incluir_figura_nova(self, event):
        if self.interface.tipo_figura_var.get() == "Polígono":
            return

        if self.figura_nova:
            self.figuras.append(self.figura_nova)
            self.figura_nova = None
        self.desenhar()

    def atualizar_preview_poligono(self, event):
        if self.poligono_em_construcao is None:
            return
        self.poligono_preview = (event.x, event.y)
        self.desenhar()

    def fechar_poligono(self):
        self.figuras.append(self.poligono_em_construcao)
        self.poligono_em_construcao = None
        self.poligono_preview = None

    def desenhar(self, dash=None):
        canvas = self.interface.canvas
        canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(canvas)

        if self.figura_nova:
            self.figura_nova.desenhar(canvas, dash=(4, 2))

        if self.poligono_em_construcao:
            pontos = self.poligono_em_construcao.pontosPoligonos

            if len(pontos) >= 4:
                canvas.create_line(
                    *pontos,
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura
                )

            if self.poligono_preview:
                canvas.create_line(
                    pontos[-2], pontos[-1],
                    self.poligono_preview[0], self.poligono_preview[1],
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura,
                    dash=(4, 2)
                )

            raio_destaque = 4
            canvas.create_oval(
                pontos[0] - raio_destaque, pontos[1] - raio_destaque,
                pontos[0] + raio_destaque, pontos[1] + raio_destaque,
                outline="red", width=1
            )

    def escolher_cor_pr(self):
        cor = askcolor()[1]
        if cor:
            self.cor_preenchimento = cor
            self.interface.swatch_preenchimento.config(bg=cor)

    def escolher_cor_brd(self):
        cor = askcolor()[1]
        if cor:
            self.cor_borda = cor
            self.interface.swatch_borda.config(bg=cor)

    def escolher_tamEspessura(self, event):
        self.tamEspessura = int(event.widget.get())

    def limpar_tela(self):
        self.figuras.clear()
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_preview = None
        self.interface.canvas.delete("all")
