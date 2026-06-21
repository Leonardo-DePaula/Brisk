from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor

class Figura:
    def __init__(self, cor_preenchimento, cor_borda):
        self.cor_preenchimento = cor_preenchimento
        self.cor_borda = cor_borda

    def desenhar(self, canvas, dash=None):
        pass

class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda):
        super().__init__("", cor_borda)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def desenhar(self, canvas, dash=None):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.cor_borda,
            dash=dash
        )

class Rabisco(Figura):
    def __init__(self, pontos, cor_borda):
        super().__init__("", cor_borda)
        self.pontos = pontos

    def desenhar(self, canvas, dash=None):
        canvas.create_line(
            self.pontos,
            fill=self.cor_borda,
            dash=dash
        )

class ProgramaPrincipal:
    def __init__(self, janela):
        #Valores Padrdão
        self.figuras = []
        self.figura_nova = None
        self.ini_x = 0
        self.ini_y = 0
        self.cor_preenchimento = ""
        self.cor_borda = "black"
        #Organização 
        self.janela = janela
        self.janela.title("Brisk - App de Desenhos")
        
        self.icone = PhotoImage(data=ICONE_BASE64)
        self.janela.iconphoto(True, self.icone)
    
        self.organizar = Frame(janela)
        self.organizar.pack()
        
        self.tipo_figura_var = StringVar(janela)

        self.criar_interface()
        self.criar_canvas()

    def criar_interface(self):
        paddings = {"padx" : 5, "pady" : 5}
    
        # Rótulo
        label = ttk.Label(self.organizar,  text='Escolha sua ferramenta')
        label.grid(column=0, row=0, sticky=W, **paddings)

        # Menu
        self.tipo_figura_var = StringVar(janela)
        option_menu = ttk.OptionMenu(self.organizar, self.tipo_figura_var,
                                     'Linha',
                                     'Linha',
                                     'Rabisco',
                                     'Retângulo',
                                     'Oval',
                                     'Círculo')

        preenchimentoCor = ttk.Button(self.organizar, text="Cor de Preenchimento", command=self.escolher_cor_pr)
        bordaCor = ttk.Button(self.organizar, text="Cor da Borda", command=self.escolher_cor_brd)
        limparTela = ttk.Button(self.organizar, text="Limpar Tela", command=self.limpar_tela)
        preenchimentoCor.grid(column=1, row=0, sticky=W, **paddings)
        bordaCor.grid(column=2, row=0, sticky=W, **paddings)
        option_menu.grid(column=3, row=0, sticky=W, **paddings)
        limparTela.grid(column=4, row=0, sticky=W, **paddings)
    
    def criar_canvas(self):
        # Área de desenho
        self.canvas = Canvas(self.organizar, bg='white', width=self.janela.winfo_screenwidth(), height=self.janela.winfo_screenheight())
        self.canvas.grid(column=0, row=1, columnspan=5, sticky=W)

        # Eventos de mouse
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
    
    def iniciar_figura_nova(self, event):
        self.ini_x, self.ini_y = event.x, event.y
        tipo = self.tipo_figura_var.get()

        if tipo == "Linha":
            self.figura_nova = Linha(event.x, event.y, event.x, event.y,
                                     self.cor_borda)

        elif tipo == "Rabisco":
            self.figura_nova = Rabisco([(event.x, event.y)], self.cor_borda)    

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
        if self.figura_nova:
            if isinstance(self.figura_nova, Rabisco):
                if len(self.figura_nova.pontos) < 2:
                    self.figura_nova = None
                    return
            self.figuras.append(self.figura_nova)
            self.figura_nova = None

        self.desenhar()

    def desenhar(self):
        self.canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(self.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar(self.canvas, dash=(4, 2))
    
    def escolher_cor_pr(self):
        cor = askcolor()[1]
        if cor:
            self.cor_preenchimento = cor


    def escolher_cor_brd(self):
        cor = askcolor()[1]
        if cor:
            self.cor_borda = cor

    def limpar_tela(self):
        self.figuras.clear()
        self.figura_nova = None
        self.canvas.delete("all")

ICONE_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAADs0lEQVR4nO2bW1bjMBBEnZzZDY9FwLonixgm62E+OGIUY9mS9aruqvvFD0ZRXVUrAS5LR55e3j57Pp+F+8ft0uvZTR+swMfQUogmD1Lwc2ghQtUDFDwGNSKc+kYFj8kZEa6l36DwcTmTTZEACh+f0oyyKkPB2yRnJBw2gMK3S052uwIofPscZVh8CRS+SAqg0++HvSw3BVD4/khl+kMAhe+XrWx1ByDnQQCdfv+sM1YDkPMtgE4/D3HWagByrsui089IyFwNQI4EIIdegL9/fs9ewlSumv+8PL28fVI3QDj9zC1ALYCQAPTQCrCufdYxQCuA+EICkEMpAGvdb0EpQApGMSQAOXQCMJ7yPegEOIJNEAlADpUAbKc7ByoBcmEShUYAplBLoBFAbCMBErA0BoUALGGegUIAkUYC7MDQHO4FYAixBvcCiH0kADmuBWhR/95HiGsBxDESgBy3ArSsbs9j4NL7fwM9b94Inl/fuz6/ewP0fgGeGbF33RsgRm2Qx8hDM/QOoDY4ZvQeDW2AGLXBI7MOx7R3AWqD/8zci6lvAyXB/D2YNgLWsI2E2cEHYD4IQtmQESC9VpgGiPHaBkjBB2AaIAZxo2pBfU2QDRBjvQ1Qgw9ANkAM+gbuYWHt8AIsi42NXGNlzfAjYA36SLASfMBEA8QgbzDy2lKYa4AYlDawGHzAXAPEIGw8whpqMC2AqMe0AAgjAGENNZgWQNQjAcgxKwBS9SKtpRSzAog2SAByJAA5JgVAnLmIa8rBpACiHRKAHHMCIFct8tpSmBOgNdZ/mVPLr9kLmEUcfPja4gmuxVQDtAoodepbtIE1iagaICdgtjYw1QA1lJ5ulruBmT8JO3sia4Oc9XNH4boBWoTw/PpuJswzuBSgR2heJTAxAkpqeERQueuxII2bBhhZ1RaCzcWFADMC8XI3MC0AQgizf34t8AKk5i3SxqfWYuHDJHOfBCIFH2P1E0T4BohBDT/GwhpjoN8GhtNkbVMDFtYP3wDIm3eEhbVDN4DoD3wDiL5IAHIkADkSgBwJQI4EIOd6/7hdZi9CzOH+cbuoAciRAORIAHKuy/I1C2YvRIwlZK4GIOdbALUAD3HWagByHgRQC/hnnbEagJwfAqgF/LKV7WYDSAJ/pDJNjgBJ4Ie9LHUHIGdXALWAfY4yPGwASWCXnOyKwtWfkNug5NAW3QHUBviUZlR8CZQEuJzJpipMjQQMag5lk9MsEebQoo2b1rlEGEPLMdx1nkuINvS8d/0DPxM1mEiFzwwAAAAASUVORK5CYII=
"""

janela = Tk()
Programa = ProgramaPrincipal(janela)
janela.mainloop()
