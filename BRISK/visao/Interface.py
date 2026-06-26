from tkinter import *
from tkinter import ttk

ICONE_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAADs0lEQVR4nO2bW1bjMBBEnZzZDY9FwLonixgm62E+OGIUY9mS9aruqvvFD0ZRXVUrAS5LR55e3j57Pp+F+8ft0uvZTR+swMfQUogmD1Lwc2ghQtUDFDwGNSKc+kYFj8kZEa6l36DwcTmTTZEACh+f0oyyKkPB2yRnJBw2gMK3S052uwIofPscZVh8CRS+SAqg0++HvSw3BVD4/khl+kMAhe+XrWx1ByDnQQCdfv+sM1YDkPMtgE4/D3HWagByrsui089IyFwNQI4EIIdegL9/fs9ewlSumv+8PL28fVI3QDj9zC1ALYCQAPTQCrCufdYxQCuA+EICkEMpAGvdb0EpQApGMSQAOXQCMJ7yPegEOIJNEAlADpUAbKc7ByoBcmEShUYAplBLoBFAbCMBErA0BoUALGGegUIAkUYC7MDQHO4FYAixBvcCiH0kADmuBWhR/95HiGsBxDESgBy3ArSsbs9j4NL7fwM9b94Inl/fuz6/ewP0fgGeGbF33RsgRm2Qx8hDM/QOoDY4ZvQeDW2AGLXBI7MOx7R3AWqD/8zci6lvAyXB/D2YNgLWsI2E2cEHYD4IQtmQESC9VpgGiPHaBkjBB2AaIAZxo2pBfU2QDRBjvQ1Qgw9ANkAM+gbuYWHt8AIsi42NXGNlzfAjYA36SLASfMBEA8QgbzDy2lKYa4AYlDawGHzAXAPEIGw8whpqMC2AqMe0AAgjAGENNZgWQNQjAcgxKwBS9SKtpRSzAog2SAByJAA5JgVAnLmIa8rBpACiHRKAHHMCIFct8tpSmBOgNdZ/mVPLr9kLmEUcfPja4gmuxVQDtAoodepbtIE1iagaICdgtjYw1QA1lJ5ulruBmT8JO3sia4Oc9XNH4boBWoTw/PpuJswzuBSgR2heJTAxAkpqeERQueuxII2bBhhZ1RaCzcWFADMC8XI3MC0AQgizf34t8AKk5i3SxqfWYuHDJHOfBCIFH2P1E0T4BohBDT/GwhpjoN8GhtNkbVMDFtYP3wDIm3eEhbVDN4DoD3wDiL5IAHIkADkSgBwJQI4EIOd6/7hdZi9CzOH+cbuoAciRAORIAHKuy/I1C2YvRIwlZK4GIOdbALUAD3HWagByHgRQC/hnnbEagJwfAqgF/LKV7WYDSAJ/pDJNjgBJ4Ie9LHUHIGdXALWAfY4yPGwASWCXnOyKwtWfkNug5NAW3QHUBviUZlR8CZQEuJzJpipMjQQMag5lk9MsEebQoo2b1rlEGEPLMdx1nkuINvS8d/0DPxM1mEiFzwwAAAAASUVORK5CYII=
"""
class Interface:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Brisk - App de Desenhos")

        self.icone = PhotoImage(data=ICONE_BASE64)
        self.janela.iconphoto(True, self.icone)

        self.style = ttk.Style()
        self.style.configure(
            'Estilo_Frame.TFrame',
            background="#2b2b2b"
        )

        self.style.configure(
            'Estilo_Rotulo.TLabel',
            background="#2b2b2b",
            foreground="white"
        )

        self.barra = Frame(
            self.janela,
            bg="#2b2b2b"
        )
        self.barra.pack(fill=X)

        self.criar_interface()
        self.criar_canvas()

    def criar_interface(self):
        margens = {"padx": 4, "pady": 5}

        organizar = ttk.Frame(
            self.barra,
            style='Estilo_Frame.TFrame'
        )
        organizar.grid(column=0, row=0, sticky=W)

        # -------- Ferramenta --------
        frame_ferramenta = ttk.Frame(
            organizar,
            style='Estilo_Frame.TFrame'
        )
        frame_ferramenta.pack(side=LEFT, **margens)

        ttk.Label(
            frame_ferramenta,
            text='Ferramenta:',
            style='Estilo_Rotulo.TLabel'
        ).pack(side=LEFT)

        self.tipo_figura_var = StringVar(self.janela)

        self.option_menu = ttk.OptionMenu(
            frame_ferramenta,
            self.tipo_figura_var,
            'Linha',
            'Linha',
            'Rabisco',
            'Retângulo',
            'Círculo',
            'Oval',
            'Polígono'
        )

        self.option_menu.pack(side=LEFT, padx=4)

        # -------- Cores --------
        frame_cores = ttk.Frame(
            organizar,
            style='Estilo_Frame.TFrame'
        )
        frame_cores.pack(side=LEFT, **margens)

        ttk.Label(
            frame_cores,
            text='Preenchimento:',
            style='Estilo_Rotulo.TLabel'
        ).pack(side=LEFT)

        self.swatch_preenchimento = Button(
            frame_cores,
            bg="white",
            width=2,
            relief="ridge"
        )

        self.swatch_preenchimento.pack(
            side=LEFT,
            padx=(2, 10)
        )

        ttk.Label(
            frame_cores,
            text='Borda:',
            style='Estilo_Rotulo.TLabel'
        ).pack(side=LEFT)

        self.swatch_borda = Button(
            frame_cores,
            bg="black",
            width=2,
            relief="ridge"
        )

        self.swatch_borda.pack(
            side=LEFT,
            padx=2
        )

        # -------- Espessura --------
        frame_espessura = ttk.Frame(
            organizar,
            style='Estilo_Frame.TFrame'
        )
        frame_espessura.pack(
            side=LEFT,
            **margens
        )

        ttk.Label(
            frame_espessura,
            text='Espessura:',
            style='Estilo_Rotulo.TLabel'
        ).pack(side=LEFT)

        self.tamanho_espessura_esc = ttk.Scale(
            frame_espessura,
            from_=1,
            to=10,
            orient=HORIZONTAL,
            length=80
        )

        self.tamanho_espessura_esc.set(1)
        self.tamanho_espessura_esc.pack(
            side=LEFT,
            padx=4
        )

        # -------- Limpar --------
        frame_acoes = ttk.Frame(
            organizar,
            style='Estilo_Frame.TFrame'
        )
        frame_acoes.pack(
            side=LEFT,
            **margens
        )

        self.botao_limpar = ttk.Button(
            frame_acoes,
            text="Limpar"
        )

        self.botao_limpar.pack(side=LEFT)

    def criar_canvas(self):
        self.canvas = Canvas(
            self.janela,
            bg='white',
            width=self.janela.winfo_screenwidth(),
            height=self.janela.winfo_screenheight()
        )

        self.canvas.pack(
            fill=BOTH,
            expand=True
        )