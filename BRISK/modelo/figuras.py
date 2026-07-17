import math
import copy


class Figura:
    def __init__(self, cor_preenchimento, cor_borda):
        self.cor_preenchimento = cor_preenchimento
        self.cor_borda = cor_borda

    def distancia(self, x1, y1, x2, y2, px, py):

        dx = x2 - x1
        dy = y2 - y1

        ab_len_sq = dx**2 + dy**2

        if ab_len_sq == 0:
            return math.sqrt((px - x1)**2 + (py - y1)**2)

        ap_x = px - x1
        ap_y = py - y1

        t = (ap_x * dx + ap_y * dy) / ab_len_sq

        t = max(0.0, min(1.0, t))

        ponto_proximo_x = x1 + t * dx
        ponto_proximo_y = y1 + t * dy

        return math.sqrt(
            (px - ponto_proximo_x)**2 +
            (py - ponto_proximo_y)**2
        )

    def desenhar(self, canvas, dash=None):
        pass

    def contem(self, x, y):
        return False

    def mover(self, dx, dy):
        pass

    def obter_bbox(self):
        return None
    
    def intersecta_retangulo(self, rx1, ry1, rx2, ry2):
        bbox = self.obter_bbox()

        if bbox is None:
            return False

        x1, y1, x2, y2 = bbox

        return not (x2 < rx1 or x1 > rx2 or y2 < ry1 or y1 > ry2)
        
    def contido_em_retangulo(self, rx1, ry1, rx2, ry2):
        bbox = self.obter_bbox()

        if bbox is None:
            return False

        x1, y1, x2, y2 = bbox

        return x1 >= rx1 and x2 <= rx2 and y1 >= ry1 and y2 <= ry2
    
    def copiar(self):
        return copy.deepcopy(self)

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

    def contem(self, x, y):

        return self.distancia(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            x,
            y
        ) <= 5

    def mover(self, dx, dy):

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def obter_bbox(self):
        return (
            min(self.x1, self.x2), min(self.y1, self.y2),
            max(self.x1, self.x2), max(self.y1, self.y2)
        )

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

        canvas.create_oval(
            self.x1 - raio,
            self.y1 - raio,
            self.x1 + raio,
            self.y1 + raio,
            fill=self.cor_preenchimento,
            outline=self.cor_borda,
            width=self.tamEspessura,
            dash=dash
        )

    def contem(self, x, y):

        raio = ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2) ** 0.5

        distancia_centro = math.sqrt(
            (x - self.x1)**2 +
            (y - self.y1)**2
        )

        return distancia_centro <= raio

    def mover(self, dx, dy):

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def obter_bbox(self):
        raio = ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2) ** 0.5
        return (
            self.x1 - raio, self.y1 - raio,
            self.x1 + raio, self.y1 + raio
        )

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

    def contem(self, x, y):

        centro_x = (self.x1 + self.x2) / 2
        centro_y = (self.y1 + self.y2) / 2

        raio_x = abs(self.x2 - self.x1) / 2
        raio_y = abs(self.y2 - self.y1) / 2

        if raio_x == 0 or raio_y == 0:
            return False

        valor = ((x - centro_x) ** 2) / (raio_x ** 2) + ((y - centro_y) ** 2) / (raio_y ** 2)

        return valor <= 1

    def mover(self, dx, dy):

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def obter_bbox(self):
        return (
            min(self.x1, self.x2), min(self.y1, self.y2),
            max(self.x1, self.x2), max(self.y1, self.y2)
        )

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

    def contem(self, x, y):

        for i in range(len(self.pontos) - 1):

            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]

            if self.distancia(x1, y1, x2, y2, x, y) <= 5:
                return True

        return False

    def mover(self, dx, dy):

        novos_pontos = []

        for x, y in self.pontos:
            novos_pontos.append((x + dx, y + dy))

        self.pontos = novos_pontos

    def obter_bbox(self):

        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]

        return (min(xs), min(ys), max(xs), max(ys))

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

    def contem(self, x, y):

        menor_x = min(self.x1, self.x2)
        maior_x = max(self.x1, self.x2)

        menor_y = min(self.y1, self.y2)
        maior_y = max(self.y1, self.y2)

        return menor_x <= x <= maior_x and menor_y <= y <= maior_y

    def mover(self, dx, dy):

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def obter_bbox(self):
        return (
            min(self.x1, self.x2), min(self.y1, self.y2),
            max(self.x1, self.x2), max(self.y1, self.y2)
        )

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

    def contem(self, x, y):

        pontos = []

        for i in range(0, len(self.pontosPoligonos), 2):
            pontos.append(
                (
                    self.pontosPoligonos[i],
                    self.pontosPoligonos[i + 1]
                )
            )

        dentro = False
        n = len(pontos)

        if n < 3:
            return False

        p1x, p1y = pontos[0]

        for i in range(n + 1):

            p2x, p2y = pontos[i % n]

            if y > min(p1y, p2y):

                if y <= max(p1y, p2y):

                    if x <= max(p1x, p2x):

                        if p1y != p2y:

                            x_interceptado = (
                                (y - p1y) *
                                (p2x - p1x) /
                                (p2y - p1y)
                            ) + p1x

                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

    def mover(self, dx, dy):

        novos_pontos = []

        for i in range(0, len(self.pontosPoligonos), 2):

            novos_pontos.append(self.pontosPoligonos[i] + dx)
            novos_pontos.append(self.pontosPoligonos[i + 1] + dy)

        self.pontosPoligonos = novos_pontos

    def obter_bbox(self):

        xs = self.pontosPoligonos[0::2]
        ys = self.pontosPoligonos[1::2]

        return (min(xs), min(ys), max(xs), max(ys))

    def paraDicionario(self):
        return {
            "tipo": "Poligono",
            "pontosPoligonos": self.pontosPoligonos,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }

class PoligonoRegular(Figura):
    def __init__(self, cx, cy, raio, lados,
                 cor_borda, cor_preenchimento, tamEspessura):

        super().__init__(cor_preenchimento, cor_borda)

        self.cx = cx
        self.cy = cy
        self.raio = raio
        self.lados = lados
        self.tamEspessura = tamEspessura

    def calcular_pontos(self):

        pontos = []

        for i in range(self.lados):

            angulo = (2 * math.pi * i / self.lados) - math.pi / 2

            x = self.cx + self.raio * math.cos(angulo)
            y = self.cy + self.raio * math.sin(angulo)

            pontos.extend([x, y])

        return pontos

    def desenhar(self, canvas, dash=None):

        canvas.create_polygon(
            *self.calcular_pontos(),
            fill=self.cor_preenchimento,
            outline=self.cor_borda,
            width=self.tamEspessura,
            dash=dash
        )

    def contem(self, x, y):

        pontos = self.calcular_pontos()

        vertices = []

        for i in range(0, len(pontos), 2):
            vertices.append((pontos[i], pontos[i + 1]))

        dentro = False
        n = len(vertices)

        p1x, p1y = vertices[0]

        for i in range(n + 1):

            p2x, p2y = vertices[i % n]

            if y > min(p1y, p2y):

                if y <= max(p1y, p2y):

                    if x <= max(p1x, p2x):

                        if p1y != p2y:

                            x_interceptado = (
                                (y - p1y) *
                                (p2x - p1x) /
                                (p2y - p1y)
                            ) + p1x

                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

    def mover(self, dx, dy):

        self.cx += dx
        self.cy += dy

    def obter_bbox(self):

        pontos = self.calcular_pontos()

        xs = pontos[0::2]
        ys = pontos[1::2]

        return (
            min(xs),
            min(ys),
            max(xs),
            max(ys)
        )

    def paraDicionario(self):

        return {
            "tipo": "PoligonoRegular",
            "cx": self.cx,
            "cy": self.cy,
            "raio": self.raio,
            "lados": self.lados,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "tamEspessura": self.tamEspessura
        }

class FiguraComposta(Figura):
    def __init__(self, figuras):
        super().__init__("", "")
        self.figuras = figuras

    def desenhar(self, canvas, dash=None):
        for figura in self.figuras:
            figura.desenhar(canvas, dash=dash)

    def contem(self, x, y):
        return any(figura.contem(x, y) for figura in self.figuras)

    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)

    def obter_bbox(self):

        bboxes = [figura.obter_bbox() for figura in self.figuras if figura.obter_bbox()]

        if not bboxes:
            return None

        xs1 = [b[0] for b in bboxes]
        ys1 = [b[1] for b in bboxes]
        xs2 = [b[2] for b in bboxes]
        ys2 = [b[3] for b in bboxes]

        return (min(xs1), min(ys1), max(xs2), max(ys2))

    def paraDicionario(self):
        return {
            "tipo": "FiguraComposta",
            "figuras": [figura.paraDicionario() for figura in self.figuras]
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
        
        case "PoligonoRegular":
            return PoligonoRegular(
                dados["cx"],
                dados["cy"],
                dados["raio"],
                dados["lados"],
                dados["cor_borda"],
                dados["cor_preenchimento"],
                dados["tamEspessura"]
            )

        case "FiguraComposta":
            return FiguraComposta(
                [criarFiguraDeDicionario(item) for item in dados["figuras"]]
            )
