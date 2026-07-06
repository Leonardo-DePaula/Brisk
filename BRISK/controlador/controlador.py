from tkinter.colorchooser import askcolor

from visao.Interface import Interface
from modelo.figuras import *
from controlador.ferramentas import *


class Controlador:

    def __init__(self, janela):

        self.janela = janela
        self.interface = Interface(janela)

        self.figuras = []

        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_preview = None

        self.cor_preenchimento = ""
        self.cor_borda = "black"
        self.tamEspessura = 1

        tipo_inicial = self.interface.tipo_figura_var.get()
        self.ferramenta = FERRAMENTAS[tipo_inicial](self)

        self.conectar_eventos()

    def conectar_eventos(self):

        self.interface.swatch_preenchimento.config(
            command=self.escolher_cor_preenchimento
        )

        self.interface.swatch_borda.config(
            command=self.escolher_cor_borda
        )

        self.interface.tamanho_espessura_esc.bind(
            "<ButtonRelease-1>",
            self.escolher_espessura
        )

        self.interface.botao_limpar.config(
            command=self.limpar_tela
        )

        canvas = self.interface.canvas

        canvas.bind("<ButtonPress-1>", self.iniciar_desenho)
        canvas.bind("<B1-Motion>", self.atualizar_desenho)
        canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)
        canvas.bind("<Motion>", self.atualizar_previsao)

    def iniciar_desenho(self, evento):

        tipo = self.interface.tipo_figura_var.get()

        self.ferramenta = FERRAMENTAS[tipo](self)
        self.ferramenta.iniciar(evento)

    def iniciar_desenho(self, evento):
        tipo = self.interface.tipo_figura_var.get()
        self.ferramenta = FERRAMENTAS[tipo](self)
        self.ferramenta.iniciar(evento)

    def atualizar_desenho(self, evento):
       self.ferramenta.atualizar(evento)

    def finalizar_desenho(self, evento):
        self.ferramenta.finalizar(evento)

    def atualizar_previsao(self, evento):
        self.ferramenta.prever(evento)

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
                    pontos[-2],
                    pontos[-1],
                    self.poligono_preview[0],
                    self.poligono_preview[1],
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura,
                    dash=(4, 2)
                )

            raio = 4

            canvas.create_oval(
                pontos[0] - raio,
                pontos[1] - raio,
                pontos[0] + raio,
                pontos[1] + raio,
                outline="red",
                width=1
            )

    def fechar_poligono(self):

        self.figuras.append(self.poligono_em_construcao)

        self.poligono_em_construcao = None
        self.poligono_preview = None

        self.desenhar()

    def escolher_cor_preenchimento(self):

        cor = askcolor()[1]

        if cor:
            self.cor_preenchimento = cor
            self.interface.swatch_preenchimento.config(bg=cor)

    def escolher_cor_borda(self):

        cor = askcolor()[1]

        if cor:
            self.cor_borda = cor
            self.interface.swatch_borda.config(bg=cor)

    def escolher_espessura(self, evento):

        self.tamEspessura = int(evento.widget.get())

    def limpar_tela(self):

        self.figuras.clear()

        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_preview = None

        self.interface.canvas.delete("all")