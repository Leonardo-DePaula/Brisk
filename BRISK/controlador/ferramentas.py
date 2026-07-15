from modelo.figuras import *
import math

class Ferramenta:

    def __init__(self, controlador):
        self.controlador = controlador
        self.controlador.figura_selecionada = None
        self.controlador.figura_selecionadas = []

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

    def copiar(self, evento):
        pass

    def colar(self, evento):
        pass

    def mover_para_frente(self, evento):
        pass

    def mover_para_tras(self, evento):
        pass

    def mover_para_topo(self, evento):
        pass

    def mover_para_fundo(self, evento):
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

            raio_fechamento = max(4, self.controlador.tamEspessura + 3)
            tolerancia_fechamento = raio_fechamento * 2

            if len(pontos) >= 6 and distancia <= tolerancia_fechamento:
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

        encontrado = False

        for figura in reversed(self.controlador.figuras):

            if figura.contem(evento.x, evento.y) and not encontrado:

                self.controlador.figura_selecionadas.append(figura)
                encontrado = True

        for i in range(0, len(self.controlador.figuras_selecionadas)) :
            self.controlador.atualizar_controles_com_figura(
                    self.controlador.figura_selecionada[i]
                )

        self.controlador.desenhar()

    def atualizar(self, evento):

        for fig in self.controlador.figuras_selecionadas :
            x_anterior, y_anterior = self.controlador.posicao_anterior

            dx = evento.x - x_anterior
            dy = evento.y - y_anterior

            self.controlador.figura_selecionada.mover(dx, dy)

            self.controlador.posicao_anterior = (evento.x, evento.y)

            self.controlador.desenhar()

    def finalizar(self, evento):
        pass

    def apagar(self, evento):

        for i in range(0, len(self.controlador.figuras_selecionadas)) :

                self.controlador.figuras.remove(
                    self.controlador.figura_selecionadas[i]
                )

                self.controlador.figura_selecionadas[i] = None

                self.controlador.desenhar()

    def copiar(self, evento):

        for i in range(0, len(self.controlador.figuras_selecionadas)) :

            self.controlador.buffer_copia = self.controlador.figura_selecionadas[i].copiar()

    def colar(self, evento):

        for i in range(0, len(self.controlador.figuras_selecionadas)) :

            if self.controlador.buffer_copia:

                nova_figura = self.controlador.buffer_copia.copiar()
                nova_figura.mover(15, 15)

                self.controlador.figuras.append(nova_figura)
                self.controlador.figura_selecionadas[i] = nova_figura
                self.controlador.buffer_copia = nova_figura.copiar()

                self.controlador.desenhar()

    def mover_para_frente(self, evento):
        for i in range(0, len(self.controlador.figuras_selecionadas)) :
            figura = self.controlador.figura_selecionadas[i]

            if figura in self.controlador.figuras:

                idx = self.controlador.figuras.index(figura)

                if idx < len(self.controlador.figuras) - 1:

                    self.controlador.figuras[idx], self.controlador.figuras[idx + 1] = \
                        self.controlador.figuras[idx + 1], self.controlador.figuras[idx]

                    self.controlador.desenhar()

    def mover_para_tras(self, evento):

        figura = self.controlador.figura_selecionada

        if figura in self.controlador.figuras:

            idx = self.controlador.figuras.index(figura)

            if idx > 0:

                self.controlador.figuras[idx], self.controlador.figuras[idx - 1] = \
                    self.controlador.figuras[idx - 1], self.controlador.figuras[idx]

                self.controlador.desenhar()

    def mover_para_topo(self, evento):

        figura = self.controlador.figura_selecionada

        if figura in self.controlador.figuras:

            self.controlador.figuras.remove(figura)
            self.controlador.figuras.append(figura)

            self.controlador.desenhar()

    def mover_para_fundo(self, evento):

        figura = self.controlador.figura_selecionada

        if figura in self.controlador.figuras:

            self.controlador.figuras.remove(figura)
            self.controlador.figuras.insert(0, figura)

            self.controlador.desenhar()


FERRAMENTAS = {
    "Linha": FerramentaLinha,
    "Retângulo": FerramentaRetangulo,
    "Círculo": FerramentaCirculo,
    "Oval": FerramentaOval,
    "Rabisco": FerramentaRabisco,
    "Polígono": FerramentaPoligono,
    "Seleção": FerramentaSelecionar,
}
