from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor

# Valores padrão
cor_preenchimento = ""
cor_borda = "black"

ICONE_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAADs0lEQVR4nO2bW1bjMBBEnZzZDY9FwLonixgm62E+OGIUY9mS9aruqvvFD0ZRXVUrAS5LR55e3j57Pp+F+8ft0uvZTR+swMfQUogmD1Lwc2ghQtUDFDwGNSKc+kYFj8kZEa6l36DwcTmTTZEACh+f0oyyKkPB2yRnJBw2gMK3S052uwIofPscZVh8CRS+SAqg0++HvSw3BVD4/khl+kMAhe+XrWx1ByDnQQCdfv+sM1YDkPMtgE4/D3HWagByrsui089IyFwNQI4EIIdegL9/fs9ewlSumv+8PL28fVI3QDj9zC1ALYCQAPTQCrCufdYxQCuA+EICkEMpAGvdb0EpQApGMSQAOXQCMJ7yPegEOIJNEAlADpUAbKc7ByoBcmEShUYAplBLoBFAbCMBErA0BoUALGGegUIAkUYC7MDQHO4FYAixBvcCiH0kADmuBWhR/95HiGsBxDESgBy3ArSsbs9j4NL7fwM9b94Inl/fuz6/ewP0fgGeGbF33RsgRm2Qx8hDM/QOoDY4ZvQeDW2AGLXBI7MOx7R3AWqD/8zci6lvAyXB/D2YNgLWsI2E2cEHYD4IQtmQESC9VpgGiPHaBkjBB2AaIAZxo2pBfU2QDRBjvQ1Qgw9ANkAM+gbuYWHt8AIsi42NXGNlzfAjYA36SLASfMBEA8QgbzDy2lKYa4AYlDawGHzAXAPEIGw8whpqMC2AqMe0AAgjAGENNZgWQNQjAcgxKwBS9SKtpRSzAog2SAByJAA5JgVAnLmIa8rBpACiHRKAHHMCIFct8tpSmBOgNdZ/mVPLr9kLmEUcfPja4gmuxVQDtAoodepbtIE1iagaICdgtjYw1QA1lJ5ulruBmT8JO3sia4Oc9XNH4boBWoTw/PpuJswzuBSgR2heJTAxAkpqeERQueuxII2bBhhZ1RaCzcWFADMC8XI3MC0AQgizf34t8AKk5i3SxqfWYuHDJHOfBCIFH2P1E0T4BohBDT/GwhpjoN8GhtNkbVMDFtYP3wDIm3eEhbVDN4DoD3wDiL5IAHIkADkSgBwJQI4EIOd6/7hdZi9CzOH+cbuoAciRAORIAHKuy/I1C2YvRIwlZK4GIOdbALUAD3HWagByHgRQC/hnnbEagJwfAqgF/LKV7WYDSAJ/pDJNjgBJ4Ie9LHUHIGdXALWAfY4yPGwASWCXnOyKwtWfkNug5NAW3QHUBviUZlR8CZQEuJzJpipMjQQMag5lk9MsEebQoo2b1rlEGEPLMdx1nkuINvS8d/0DPxM1mEiFzwwAAAAASUVORK5CYII=
"""

def iniciar_figura_nova(event) :
    global figura_nova, ini_x, ini_y
    ini_x, ini_y = event.x, event.y

    if tipo_figura_var.get() in ("Linha", "Retângulo", "Oval", "Círculo") :
        figura_nova = (tipo_figura_var.get(), 
                      (event.x, event.y, event.x, event.y),
                       cor_preenchimento,
                       cor_borda)

    elif tipo_figura_var.get() == "Rabisco" :
        figura_nova = ("Rabisco", [(event.x, event.y)], cor_preenchimento, cor_borda)

def atualizar_figura_nova(event) :
    global figura_nova

    if figura_nova[0] == "Rabisco" :
        figura_nova[1].append((event.x, event.y))

    elif figura_nova[0] in ("Linha", "Retângulo", "Oval", "Círculo") :

        raio = ((event.x - ini_x)**2 + (event.y - ini_y)**2) ** 0.5

        coordenadas = (
            (ini_x - raio, ini_y - raio, ini_x + raio, ini_y + raio) if figura_nova[0] == "Círculo" 
            else (ini_x, ini_y, event.x, event.y)
        )

        figura_nova = (figura_nova[0], coordenadas, figura_nova[2], figura_nova[3])

    desenhar_figuras()
    desenhar_figura_nova()

def incluir_figura_nova(event) :
    if not incompleta(figura_nova) :
        figuras.append(figura_nova)

    desenhar_figuras()

def desenhar_figuras() :
    canvas.delete("all")

    for fig, values, cor_pr, cor_brd in figuras :

        if fig in ("Retângulo", "Oval", "Círculo") :
            ferramentas[fig](values, fill=cor_pr, outline=cor_brd)
            
        elif fig in ("Linha", "Rabisco"):
            ferramentas[fig](values, fill=cor_brd)

def desenhar_figura_nova() :
    fig, values, cor_pr_nova, cor_brd_nova = figura_nova

    if fig in ("Retângulo", "Oval", "Círculo") :
        ferramentas[fig](values, fill=cor_pr_nova, outline=cor_brd_nova, dash=(4,2))

    elif fig in ("Linha", "Rabisco") :
        ferramentas[fig](values, fill=cor_brd_nova, dash=(4,2))

def incompleta(figura_nova) :
    fig, values, cor_pr, cor_brd = figura_nova

    if fig in ("Linha", "Retângulo", "Oval", "Círculo") :
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "Rabisco" :
        return len(values) <= 1

def escolher_cor_pr():
    global cor_preenchimento
    nova_cor_preenchimento = askcolor()[1]
    if nova_cor_preenchimento:
        cor_preenchimento = nova_cor_preenchimento

def escolher_cor_brd():
    global cor_borda
    nova_cor_borda = askcolor()[1]
    if nova_cor_borda:
        cor_borda = nova_cor_borda

def limpar_tela():
    global figuras, figura_nova
    canvas.delete("all")
    figuras.clear()
    figura_nova = None

######## Programa Principal ########

figuras = []
figura_nova = None

janela = Tk()
janela.title("Brisk - App de Desenhos")
organizar = Frame(janela)

icone = PhotoImage(data=ICONE_BASE64)
janela.iconphoto(True, icone) 

paddings = {"padx" : 5, "pady" : 5}

# Rótulo
label = ttk.Label(organizar,  text='Escolha sua ferramenta')
label.grid(column=0, row=0, sticky=W, **paddings)

# Menu
tipo_figura_var = StringVar(janela)
option_menu = ttk.OptionMenu(organizar, tipo_figura_var,
                             'Linha',
                             'Linha',
                             'Rabisco',
                             'Retângulo',
                             'Oval',
                             'Círculo')

preenchimentoCor = ttk.Button(organizar, text="Cor de Preenchimento", command=escolher_cor_pr)
bordaCor = ttk.Button(organizar, text="Cor da Borda", command=escolher_cor_brd)
limparTela = ttk.Button(organizar, text="Limpar Tela", command= limpar_tela)

preenchimentoCor.grid(column=1, row=0, sticky=W, **paddings)
bordaCor.grid(column=2, row=0, sticky=W, **paddings)
option_menu.grid(column=3, row=0, sticky=W, **paddings)
limparTela.grid(column=4, row=0, sticky=W, **paddings)
# Área de desenho
canvas = Canvas(organizar, bg='white', width=janela.winfo_screenwidth(), height=janela.winfo_screenheight())
canvas.grid(column=0, row=1, columnspan=5, sticky=W, **paddings)

ferramentas = {
        "Linha" : canvas.create_line,
        "Rabisco": canvas.create_line,
        "Retângulo" : canvas.create_rectangle,
        "Oval" : canvas.create_oval,
        "Círculo" : canvas.create_oval
    }

organizar.pack()

# Eventos de mouse
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

janela.mainloop()