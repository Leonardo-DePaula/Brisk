from modelo.figuras import *
import math


class Ferramenta:

    def __init__(self, controlador):
        self.controlador = controlador

    def iniciar(self, evento):
        pass

    def atualizar(self, evento):
        pass

    def finalizar(self, evento):
        pass

    def prever(self, evento):
        pass
    
    def apagar(self, evento):
        pass


class FerramentaLinha(Ferramenta):

    def iniciar(self, evento):

        self.controlador.figura_nova = Linha(
            evento.x, evento.y,
            evento.x, evento.y,
            self.controlador.cor_borda,
            self.controlador.tamEspessura
        )

    def atualizar(self, evento):

        self.controlador.figura_nova.x2 = evento.x
        self.controlador.figura_nova.y2 = evento.y
        self.controlador.desenhar()

    def finalizar(self, evento):

        self.controlador.figuras.append(self.controlador.figura_nova)
        self.controlador.figura_nova = None
        self.controlador.desenhar()


class FerramentaRetangulo(Ferramenta):

    def iniciar(self, evento):

        self.controlador.figura_nova = Retangulo(
            evento.x, evento.y,
            evento.x, evento.y,
            self.controlador.cor_borda,
            self.controlador.cor_preenchimento,
            self.controlador.tamEspessura
        )

    def atualizar(self, evento):

        self.controlador.figura_nova.x2 = evento.x
        self.controlador.figura_nova.y2 = evento.y
        self.controlador.desenhar()

    def finalizar(self, evento):

        self.controlador.figuras.append(self.controlador.figura_nova)
        self.controlador.figura_nova = None
        self.controlador.desenhar()


class FerramentaCirculo(Ferramenta):

    def iniciar(self, evento):

        self.controlador.figura_nova = Circulo(
            evento.x, evento.y,
            evento.x, evento.y,
            self.controlador.cor_borda,
            self.controlador.cor_preenchimento,
            self.controlador.tamEspessura
        )

    def atualizar(self, evento):

        self.controlador.figura_nova.x2 = evento.x
        self.controlador.figura_nova.y2 = evento.y
        self.controlador.desenhar()

    def finalizar(self, evento):

        self.controlador.figuras.append(self.controlador.figura_nova)
        self.controlador.figura_nova = None
        self.controlador.desenhar()


class FerramentaOval(Ferramenta):

    def iniciar(self, evento):

        self.controlador.figura_nova = Oval(
            evento.x, evento.y,
            evento.x, evento.y,
            self.controlador.cor_borda,
            self.controlador.cor_preenchimento,
            self.controlador.tamEspessura
        )

    def atualizar(self, evento):

        self.controlador.figura_nova.x2 = evento.x
        self.controlador.figura_nova.y2 = evento.y
        self.controlador.desenhar()

    def finalizar(self, evento):

        self.controlador.figuras.append(self.controlador.figura_nova)
        self.controlador.figura_nova = None
        self.controlador.desenhar()


class FerramentaRabisco(Ferramenta):

    def iniciar(self, evento):

        self.controlador.figura_nova = Rabisco(
            [(evento.x, evento.y)],
            self.controlador.cor_borda,
            self.controlador.tamEspessura
        )

    def atualizar(self, evento):

        self.controlador.figura_nova.pontos.append((evento.x, evento.y))
        self.controlador.desenhar()

    def finalizar(self, evento):

        self.controlador.figuras.append(self.controlador.figura_nova)
        self.controlador.figura_nova = None
        self.controlador.desenhar()


class FerramentaPoligono(Ferramenta):

    def iniciar(self, evento):

        if self.controlador.poligono_em_construcao is None:

            self.controlador.poligono_em_construcao = Poligono(
                [evento.x, evento.y],
                self.controlador.cor_borda,
                self.controlador.cor_preenchimento,
                self.controlador.tamEspessura
            )

        else:

            pontos = self.controlador.poligono_em_construcao.pontosPoligonos

            px = pontos[0]
            py = pontos[1]

            distancia = math.hypot(
                evento.x - px,
                evento.y - py
            )

            if len(pontos) >= 6 and distancia <= 8:
                self.controlador.fechar_poligono()

            else:
                pontos.extend([evento.x, evento.y])

        self.controlador.desenhar()

    def atualizar(self, evento):

        self.controlador.poligono_preview = (evento.x, evento.y)
        self.controlador.desenhar()

    def finalizar(self, evento):
        pass

    def prever(self, evento):
        if self.controlador.poligono_em_construcao:
            self.controlador.poligono_preview = (evento.x, evento.y)
            self.controlador.desenhar()


class FerramentaSelecionar(Ferramenta):

    def iniciar(self, evento):

        self.controlador.posicao_anterior = (evento.x, evento.y)

        self.controlador.figura_selecionada = None

        encontrado = False

        for figura in reversed(self.controlador.figuras):

            if figura.contem(evento.x, evento.y) and not encontrado:

                self.controlador.figura_selecionada = figura
                encontrado = True

        self.controlador.desenhar()

    def atualizar(self, evento):

        if self.controlador.figura_selecionada:

            x_anterior, y_anterior = self.controlador.posicao_anterior

            dx = evento.x - x_anterior
            dy = evento.y - y_anterior

            self.controlador.figura_selecionada.mover(dx, dy)

            self.controlador.posicao_anterior = (evento.x, evento.y)

            self.controlador.desenhar()

    def finalizar(self, evento):
        pass

    def apagar(self, evento):

        if self.controlador.figura_selecionada:

            self.controlador.figuras.remove(
                self.controlador.figura_selecionada
            )

            self.controlador.figura_selecionada = None

            self.controlador.desenhar()

FERRAMENTAS = {
    "Linha": FerramentaLinha,
    "Retângulo": FerramentaRetangulo,
    "Círculo": FerramentaCirculo,
    "Oval": FerramentaOval,
    "Rabisco": FerramentaRabisco,
    "Polígono": FerramentaPoligono,
    "Selecionar": FerramentaSelecionar,
}
