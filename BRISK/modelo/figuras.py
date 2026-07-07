class Figura:
    def __init__(self, cor_preenchimento, cor_borda):
        self.cor_preenchimento = cor_preenchimento
        self.cor_borda = cor_borda

    def desenhar(self, canvas, dash=None):
        pass

class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, tamEspessura):
        super().__init__("", cor_borda)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, 
                           fill=self.cor_borda, 
                           width=self.tamEspessura, 
                           dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Linha",
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2,
            "cor_borda": self.cor_borda,
            "tamEspessura": self.tamEspessura
        }
        
class Circulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamEspessura):
        super().__init__(cor_preenchimento, cor_borda)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        raio = ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2) ** 0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                           fill=self.cor_preenchimento, 
                           outline=self.cor_borda, 
                           width=self.tamEspessura, 
                           dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Circulo",
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamEspessura):
        super().__init__(cor_preenchimento, cor_borda)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           fill=self.cor_preenchimento,
                           outline=self.cor_borda,
                           width=self.tamEspessura,
                           dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Oval",
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }
        
class Rabisco(Figura):
    def __init__(self, pontos, cor_borda, tamEspessura):
        super().__init__("", cor_borda)
        self.pontos = pontos
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_borda, width=self.tamEspessura, dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Rabisco",
            "pontos": self.pontos,
            "cor_borda": self.cor_borda,
            "tamEspessura": self.tamEspessura
        }

class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento, tamEspessura):
        super().__init__(cor_preenchimento, cor_borda)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                 fill=self.cor_preenchimento,
                                 outline=self.cor_borda,
                                 width=self.tamEspessura, 
                                 dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Retangulo",
            "x1": self.x1, "y1": self.y1,
            "x2": self.x2, "y2": self.y2,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }

class Poligono(Figura):
    def __init__(self, pontosPoligonos, cor_borda, cor_preenchimento, tamEspessura):
        super().__init__(cor_preenchimento, cor_borda)
        self.pontosPoligonos = pontosPoligonos
        self.tamEspessura = tamEspessura

    def desenhar(self, canvas, dash=None):
        canvas.create_polygon(*self.pontosPoligonos,
                           fill=self.cor_preenchimento,
                           outline=self.cor_borda,
                           width=self.tamEspessura, 
                           dash=dash)

    def paraDicionario(self):
        return {
            "tipo": "Poligono",
            "pontosPoligonos": self.pontosPoligonos,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }


def criarFiguraDeDicionario(dados):
 
    tipo = dados["tipo"]
 
    match tipo:
 
        case "Linha":
            return Linha(
                dados["x1"], dados["y1"], dados["x2"], dados["y2"],
                dados["cor_borda"], dados["tamEspessura"]
            )
 
        case "Circulo":
            return Circulo(
                dados["x1"], dados["y1"], dados["x2"], dados["y2"],
                dados["cor_borda"], dados["cor_preenchimento"], dados["tamEspessura"]
            )
 
        case "Oval":
            return Oval(
                dados["x1"], dados["y1"], dados["x2"], dados["y2"],
                dados["cor_borda"], dados["cor_preenchimento"], dados["tamEspessura"]
            )
 
        case "Rabisco":
            return Rabisco(
                dados["pontos"], dados["cor_borda"], dados["tamEspessura"]
            )
 
        case "Retangulo":
            return Retangulo(
                dados["x1"], dados["y1"], dados["x2"], dados["y2"],
                dados["cor_borda"], dados["cor_preenchimento"], dados["tamEspessura"]
            )
 
        case "Poligono":
            return Poligono(
                dados["pontosPoligonos"], dados["cor_borda"],
                dados["cor_preenchimento"], dados["tamEspessura"]
            )
