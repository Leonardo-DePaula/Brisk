from tkinter.colorchooser import askcolor
from tkinter import filedialog

from visao.Interface import Interface
from modelo.desenhos import *
from modelo.figuras import *
from controlador.ferramentas import *


class Controlador(Desenhos):

    def __init__(self, janela):

        self.janela = janela
        self.interface = Interface(janela)
        
        Desenhos.__init__(self)

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

        self.interface.botao_salvar.config(
            command=self.salvar_arquivo
        )

        self.interface.botao_abrir.config(
            command=self.abrir_arquivo
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

    def atualizar_desenho(self, evento):
       self.ferramenta.atualizar(evento)

    def finalizar_desenho(self, evento):
        self.ferramenta.finalizar(evento)

    def atualizar_previsao(self, evento):
        self.ferramenta.prever(evento)

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

    def salvar_arquivo(self):

        caminho = filedialog.asksaveasfilename(
            defaultextension=".brisk",
            filetypes=[("Arquivo Brisk", "*.brisk")]
        )

        if caminho:
            self.salvar(caminho)

    def abrir_arquivo(self):

        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivo Brisk", "*.brisk")]
        )

        if caminho:
            self.abrir(caminho)
