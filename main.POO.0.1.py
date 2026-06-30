import math
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from figuras import Linha, Rabisco, Circulo, Oval, Retangulo, Poligono

class ProgramaPrincipal:
    def __init__(self, janela):
        self.figuras, self.figura_nova = [], None
        self.poligono_em_construcao = self.poligono_preview = None
        self.ini_x = self.ini_y = 0

        self.cor_preenchimento, self.cor_borda, self.tamEspessura = "", "black", 1
        self.num_lados = 3

        self.janela = janela
        self.janela.title("Brisk - App de Desenhos")

        self.icone = PhotoImage(data=ICONE_BASE64)
        self.janela.iconphoto(True, self.icone)

        # Definição dos estilos
        self.style = ttk.Style()
        self.style.configure('Estilo_Frame.TFrame', background="#2b2b2b")
        self.style.configure('Estilo_Rotulo.TLabel', background="#2b2b2b", foreground="white")

        self.barra = Frame(janela, bg="#2b2b2b")
        self.barra.pack(fill=X)

        self.criar_interface()
        self.criar_canvas()

    def criar_interface(self):
        margens = {"padx": 4, "pady": 5}

        organizar = ttk.Frame(self.barra, style='Estilo_Frame.TFrame')
        organizar.grid(column=0, row=0, sticky=W)

        # --- ferramenta ---
        frame_ferramenta = ttk.Frame(organizar, style='Estilo_Frame.TFrame')
        frame_ferramenta.pack(side=LEFT, **margens)

        ttk.Label(frame_ferramenta, text='Ferramenta:', style='Estilo_Rotulo.TLabel').pack(side=LEFT)
        self.tipo_figura_var = StringVar(self.janela)

        option_menu = ttk.OptionMenu(frame_ferramenta, self.tipo_figura_var,
                                      'Linha',
                                      'Linha', 
                                      'Rabisco',
                                      'Retângulo', 
                                      'Círculo', 
                                      'Oval', 
                                      'Polígono')
        
        option_menu.pack(side=LEFT, padx=4)

        # --- cores  ---
        frame_cores = ttk.Frame(organizar, style='Estilo_Frame.TFrame')
        frame_cores.pack(side=LEFT, **margens)

        ttk.Label(frame_cores, text='Preenchimento:', style='Estilo_Rotulo.TLabel').pack(side=LEFT)

        self.swatch_preenchimento = Button(frame_cores, 
                                           bg="white", 
                                           width=2,
                                           relief="ridge", 
                                           command=self.escolher_cor_pr)
        
        self.swatch_preenchimento.pack(side=LEFT, padx=(2, 10))

        ttk.Label(frame_cores, text='Borda:', style='Estilo_Rotulo.TLabel').pack(side=LEFT)

        self.swatch_borda = Button(frame_cores, 
                                   bg="black", 
                                   width=2,
                                   relief="ridge", 
                                   command=self.escolher_cor_brd)
        
        self.swatch_borda.pack(side=LEFT, padx=2)

        # --- espessura ---
        frame_espessura = ttk.Frame(organizar, style='Estilo_Frame.TFrame')
        frame_espessura.pack(side=LEFT, **margens)

        ttk.Label(frame_espessura, text='Espessura:', style='Estilo_Rotulo.TLabel').pack(side=LEFT)

        TamanhoEspessuraEsc = ttk.Scale(frame_espessura, 
                                        from_=1, 
                                        to=10,
                                        orient=HORIZONTAL, length=80)
        
        TamanhoEspessuraEsc.set(1)
        TamanhoEspessuraEsc.bind("<ButtonRelease-1>", self.escolher_tamEspessura)
        TamanhoEspessuraEsc.pack(side=LEFT, padx=4)

        # --- limpar  ---
        frame_acoes = ttk.Frame(organizar, style='Estilo_Frame.TFrame')
        frame_acoes.pack(side=LEFT, **margens)

        ttk.Button(frame_acoes, text="Limpar", command=self.limpar_tela).pack(side=LEFT)

    def criar_canvas(self):
        self.canvas = Canvas(self.janela, 
                            bg='white', 
                            width=janela.winfo_screenwidth(), 
                            height=janela.winfo_screenheight())
        
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        self.canvas.bind('<Motion>', self.atualizar_preview_poligono)

    def iniciar_figura_nova(self, event):
        self.ini_x, self.ini_y = event.x, event.y
        c = (event.x, event.y, event.x, event.y)
        pontosPoligonos = [event.x, event.y]
        tipo = self.tipo_figura_var.get()
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
        
        elif isinstance(self.figura_nova, Rabisco):
            self.figura_nova.pontos.append((event.x, event.y))

        else:
            self.figura_nova.x2 = event.x
            self.figura_nova.y2 = event.y
            
        self.desenhar()

    def incluir_figura_nova(self, event):
        if self.tipo_figura_var.get() == "Polígono":
            return
        
        if self.figura_nova:
            self.figuras.append(self.figura_nova)
            self.figura_nova = None
        self.desenhar()

    def desenhar(self, dash=None):
        self.canvas.delete("all")
        for figura in self.figuras:
            figura.desenhar(self.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar(self.canvas, dash=(4, 2))

        if self.poligono_em_construcao:
            pontos = self.poligono_em_construcao.pontosPoligonos

            if len(pontos) >= 4:
                self.canvas.create_line(
                    *pontos,
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura
                )
        
            if self.poligono_preview:
                self.canvas.create_line(
                    pontos[-2], pontos[-1],
                    self.poligono_preview[0], self.poligono_preview[1],
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura,
                    dash=(4, 2)
                )

            raio_destaque = 4
            self.canvas.create_oval(
                pontos[0] - raio_destaque, pontos[1] - raio_destaque,
                pontos[0] + raio_destaque, pontos[1] + raio_destaque,
                outline="red", width=1
            )
    def escolher_cor_pr(self):
        cor = askcolor()[1]
        if cor:
            self.cor_preenchimento = cor
            self.swatch_preenchimento.config(bg=cor)

    def escolher_cor_brd(self):
        cor = askcolor()[1]
        if cor:
            self.cor_borda = cor
            self.swatch_borda.config(bg=cor)

    def escolher_tamEspessura(self, event):
        self.tamEspessura = int(event.widget.get())

    def limpar_tela(self):
        self.figuras.clear()
        self.figura_nova = None

        # resetando
        self.poligono_em_construcao = None
        self.poligono_preview = None

        self.canvas.delete("all")

    def fechar_poligono(self):
        self.figuras.append(self.poligono_em_construcao)
        self.poligono_em_construcao = None
        self.poligono_preview = None

    def atualizar_preview_poligono(self, event):
        if self.poligono_em_construcao is None:
            return
        self.poligono_preview = (event.x, event.y)
        self.desenhar()

ICONE_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAADs0lEQVR4nO2bW1bjMBBEnZzZDY9FwLonixgm62E+OGIUY9mS9aruqvvFD0ZRXVUrAS5LR55e3j57Pp+F+8ft0uvZTR+swMfQUogmD1Lwc2ghQtUDFDwGNSKc+kYFj8kZEa6l36DwcTmTTZEACh+f0oyyKkPB2yRnJBw2gMK3S052uwIofPscZVh8CRS+SAqg0++HvSw3BVD4/khl+kMAhe+XrWx1ByDnQQCdfv+sM1YDkPMtgE4/D3HWagByrsui089IyFwNQI4EIIdegL9/fs9ewlSumv+8PL28fVI3QDj9zC1ALYCQAPTQCrCufdYxQCuA+EICkEMpAGvdb0EpQApGMSQAOXQCMJ7yPegEOIJNEAlADpUAbKc7ByoBcmEShUYAplBLoBFAbCMBErA0BoUALGGegUIAkUYC7MDQHO4FYAixBvcCiH0kADmuBWhR/95HiGsBxDESgBy3ArSsbs9j4NL7fwM9b94Inl/fuz6/ewP0fgGeGbF33RsgRm2Qx8hDM/QOoDY4ZvQeDW2AGLXBI7MOx7R3AWqD/8zci6lvAyXB/D2YNgLWsI2E2cEHYD4IQtmQESC9VpgGiPHaBkjBB2AaIAZxo2pBfU2QDRBjvQ1Qgw9ANkAM+gbuYWHt8AIsi42NXGNlzfAjYA36SLASfMBEA8QgbzDy2lKYa4AYlDawGHzAXAPEIGw8whpqMC2AqMe0AAgjAGENNZgWQNQjAcgxKwBS9SKtpRSzAog2SAByJAA5JgVAnLmIa8rBpACiHRKAHHMCIFct8tpSmBOgNdZ/mVPLr9kLmEUcfPja4gmuxVQDtAoodepbtIE1iagaICdgtjYw1QA1lJ5ulruBmT8JO3sia4Oc9XNH4boBWoTw/PpuJswzuBSgR2heJTAxAkpqeERQueuxII2bBhhZ1RaCzcWFADMC8XI3MC0AQgizf34t8AKk5i3SxqfWYuHDJHOfBCIFH2P1E0T4BohBDT/GwhpjoN8GhtNkbVMDFtYP3wDIm3eEhbVDN4DoD3wDiL5IAHIkADkSgBwJQI4EIOd6/7hdZi9CzOH+cbuoAciRAORIAHKuy/I1C2YvRIwlZK4GIOdbALUAD3HWagByHgRQC/hnnbEagJwfAqgF/LKV7WYDSAJ/pDJNjgBJ4Ie9LHUHIGdXALWAfY4yPGwASWCXnOyKwtWfkNug5NAW3QHUBviUZlR8CZQEuJzJpipMjQQMag5lk9MsEebQoo2b1rlEGEPLMdx1nkuINvS8d/0DPxM1mEiFzwwAAAAASUVORK5CYII=
"""

janela = Tk()
Programa = ProgramaPrincipal(janela)
janela.mainloop()
