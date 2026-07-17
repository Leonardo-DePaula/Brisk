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

    def clique_esquerdo(self, evento):
        pass

    def clique_direito(self, evento):
        pass

    def duplo_clique(self, evento):
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

class FerramentaPoligonoRegular(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)
        self.id_clique = None
        self.arrastando = False
        self.x_inicio = 0
        self.y_inicio = 0

    def iniciar(self, evento):
        self.x_inicio = evento.x
        self.y_inicio = evento.y
        self.arrastando = True

        if self.controlador.poligono_regular is None:
            self.controlador.poligono_regular = PoligonoRegular(
                evento.x,
                evento.y,
                0,
                3,
                self.controlador.cor_borda,
                self.controlador.cor_preenchimento,
                self.controlador.tamEspessura
            )
            self.controlador.desenhar()

    def atualizar(self, evento):
        poligono = self.controlador.poligono_regular
        if poligono is None:
            return

        poligono.raio = math.hypot(
            evento.x - poligono.cx,
            evento.y - poligono.cy
        )
        self.controlador.desenhar()

    def finalizar(self, evento):
        distancia = math.hypot(evento.x - self.x_inicio, evento.y - self.y_inicio)
        if distancia > 3:
            self.arrastando = True
        else:
            self.arrastando = False

    def clique_esquerdo(self, evento):
        if self.arrastando:
            self.arrastando = False
            return

        if self.controlador.poligono_regular is None:
            return

        self.id_clique = self.controlador.janela.after(
            200,
            self.aumentar_lado
        )

    def aumentar_lado(self):
        poligono = self.controlador.poligono_regular
        if poligono is None:
            return

        poligono.lados += 1
        self.id_clique = None
        self.controlador.desenhar()

    def clique_direito(self, evento):
        poligono = self.controlador.poligono_regular
        if poligono is None:
            return

        if poligono.lados > 3:
            poligono.lados -= 1
            self.controlador.desenhar()

    def duplo_clique(self, evento):
        if self.id_clique is not None:
            self.controlador.janela.after_cancel(self.id_clique)
            self.id_clique = None

        poligono = self.controlador.poligono_regular
        if poligono is None:
            return

        self.controlador.figuras.append(poligono)
        self.controlador.poligono_regular = None
        self.controlador.desenhar()

class FerramentaSelecionar(Ferramenta):

    def __init__(self, controlador):
        super().__init__(controlador)
        self.ponto_inicial_retangulo = None

    def _figura_no_ponto(self, x, y):
        for figura in reversed(self.controlador.figuras):
            if figura.contem(x, y):
                return figura
        return None

    def _ctrl_pressionado(self, evento):
        return bool(evento.state & 0x0004)

    def iniciar(self, evento):

        self.controlador.posicao_anterior = (evento.x, evento.y)
        self.controlador.figuras_candidatas = []

        ctrl = self._ctrl_pressionado(evento)
        figura = self._figura_no_ponto(evento.x, evento.y)

        if figura is not None:
            if ctrl:
                if figura in self.controlador.figuras_selecionadas:
                    self.controlador.figuras_selecionadas.remove(figura)

                else:
                    self.controlador.figuras_selecionadas.append(figura)
            else:

                if figura not in self.controlador.figuras_selecionadas:
                    self.controlador.figuras_selecionadas = [figura]

            self.ponto_inicial_retangulo = None
            self.controlador.retangulo_selecao = None

        else:
            if not ctrl:
                self.controlador.figuras_selecionadas = []

            self.ponto_inicial_retangulo = (evento.x, evento.y)
            self.controlador.retangulo_selecao = (evento.x, evento.y, evento.x, evento.y)

        if self.controlador.figuras_selecionadas:
            self.controlador.atualizar_controles_com_figura(
                self.controlador.figuras_selecionadas[-1]
            )

        self.controlador.desenhar()

    def atualizar(self, evento):

        if self.ponto_inicial_retangulo is not None:
            x0, y0 = self.ponto_inicial_retangulo
            self.controlador.retangulo_selecao = (x0, y0, evento.x, evento.y)

            rx1, rx2 = min(x0, evento.x), max(x0, evento.x)
            ry1, ry2 = min(y0, evento.y), max(y0, evento.y)

            self.controlador.figuras_candidatas = [
              figura for figura in self.controlador.figuras
              if figura.contido_em_retangulo(rx1, ry1, rx2, ry2)
            ]

            self.controlador.desenhar()
            return

        x_anterior, y_anterior = self.controlador.posicao_anterior
        dx = evento.x - x_anterior
        dy = evento.y - y_anterior

        for figura in self.controlador.figuras_selecionadas:
            figura.mover(dx, dy)

        self.controlador.posicao_anterior = (evento.x, evento.y)
        self.controlador.desenhar()

    def finalizar(self, evento):

        if self.ponto_inicial_retangulo is not None:

            x0, y0 = self.ponto_inicial_retangulo
            x1, y1 = evento.x, evento.y

            rx1, rx2 = min(x0, x1), max(x0, x1)
            ry1, ry2 = min(y0, y1), max(y0, y1)

            capturadas = [
              figura for figura in self.controlador.figuras
              if figura.contido_em_retangulo(rx1, ry1, rx2, ry2)
             ]

            for figura in capturadas:
                if figura not in self.controlador.figuras_selecionadas:
                    self.controlador.figuras_selecionadas.append(figura)

            self.ponto_inicial_retangulo = None
            self.controlador.retangulo_selecao = None
            self.controlador.figuras_candidatas = []

            if self.controlador.figuras_selecionadas:
                self.controlador.atualizar_controles_com_figura(
                    self.controlador.figuras_selecionadas[-1]
                )

            self.controlador.desenhar()

    def apagar(self, evento):
        for figura in self.controlador.figuras_selecionadas:
            if figura in self.controlador.figuras:
                self.controlador.figuras.remove(figura)
        self.controlador.figuras_selecionadas = []
        self.controlador.desenhar()

    def copiar(self, evento):
        self.controlador.buffer_copia = [
            figura.copiar() for figura in self.controlador.figuras_selecionadas
        ]

    def colar(self, evento):
        if not self.controlador.buffer_copia:
            return

        novas_figuras = []

        for figura in self.controlador.buffer_copia:

            nova_figura = figura.copiar()
            nova_figura.mover(15, 15)

            self.controlador.figuras.append(nova_figura)
            novas_figuras.append(nova_figura)

        self.controlador.figuras_selecionadas = novas_figuras
        self.controlador.buffer_copia = [f.copiar() for f in novas_figuras]
        self.controlador.desenhar()

    def mover_para_frente(self, evento):

        for figura in self.controlador.figuras_selecionadas:
            if figura in self.controlador.figuras:

                idx = self.controlador.figuras.index(figura)

                if idx < len(self.controlador.figuras) - 1:
                    self.controlador.figuras[idx], self.controlador.figuras[idx + 1] = \
                        self.controlador.figuras[idx + 1], self.controlador.figuras[idx]
                    
        self.controlador.desenhar()

    def mover_para_tras(self, evento):

        for figura in self.controlador.figuras_selecionadas:

            if figura in self.controlador.figuras:

                idx = self.controlador.figuras.index(figura)

                if idx > 0:
                    self.controlador.figuras[idx], self.controlador.figuras[idx - 1] = \
                        self.controlador.figuras[idx - 1], self.controlador.figuras[idx]
                    
        self.controlador.desenhar()

    def mover_para_topo(self, evento):

        for figura in self.controlador.figuras_selecionadas:

            if figura in self.controlador.figuras:
                self.controlador.figuras.remove(figura)
                self.controlador.figuras.append(figura)

        self.controlador.desenhar()

    def mover_para_fundo(self, evento):
        for figura in reversed(self.controlador.figuras_selecionadas):

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
    "Polígono Regular": FerramentaPoligonoRegular,
}
