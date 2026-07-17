import json

from modelo.figuras import criarFiguraDeDicionario


class Desenhos:

    def __init__(self):

        self.figuras = []
        self.figura_nova = self.poligono_em_construcao = self.poligono_preview = None
        self.figuras_selecionadas = []
        self.figuras_candidatas = []
        self.retangulo_selecao = None
        self.posicao_anterior = None
        self.buffer_copia = None

    def desenhar(self, dash=None):

        canvas = self.interface.canvas
        canvas.delete("all")

        for figura in self.figuras:

            figura.desenhar(canvas)

            if figura in self.figuras_selecionadas:
                self.desenhar_caixa_selecao(figura, canvas, cor="red")
            elif figura in self.figuras_candidatas:
                self.desenhar_caixa_selecao(figura, canvas, cor="blue")

        if self.figura_nova:
            self.figura_nova.desenhar(canvas, dash=(4, 2))

        if self.poligono_em_construcao:

            pontos = self.poligono_em_construcao.pontosPoligonos

            if len(pontos) >= 4:

                canvas.create_line(
                    *pontos,
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura
                )

            if self.poligono_preview:

                canvas.create_line(
                    pontos[-2],
                    pontos[-1],
                    self.poligono_preview[0],
                    self.poligono_preview[1],
                    fill=self.poligono_em_construcao.cor_borda,
                    width=self.poligono_em_construcao.tamEspessura,
                    dash=(4, 2)
                )

            raio = max(4, self.poligono_em_construcao.tamEspessura + 3)

            canvas.create_oval(
                pontos[0] - raio,
                pontos[1] - raio,
                pontos[0] + raio,
                pontos[1] + raio,
                outline="red",
                width=1
            )

        if self.retangulo_selecao:
            x1, y1, x2, y2 = self.retangulo_selecao
            canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="blue",
                dash=(3, 2)
            )

    def desenhar_caixa_selecao(self, figura, canvas, cor="red"):

        bbox = figura.obter_bbox()

        if bbox is None:
            return

        x1, y1, x2, y2 = bbox

        margem = 6 + getattr(figura, "tamEspessura", 1)

        canvas.create_rectangle(
            x1 - margem,
            y1 - margem,
            x2 + margem,
            y2 + margem,
            outline=cor,
            width=1,
            dash=(4, 2)
        )

    def fechar_poligono(self):

        self.figuras.append(self.poligono_em_construcao)

        self.poligono_em_construcao = None
        self.poligono_preview = None

        self.desenhar()

    def limpar(self):

        self.figuras.clear()

        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_preview = None
        self.figuras_selecionadas = []
        self.figuras_candidatas = []
        self.retangulo_selecao = None
        self.posicao_anterior = None
        self.buffer_copia = None

        self.interface.canvas.delete("all")

    def salvar(self, caminho):

        dados = [figura.paraDicionario() for figura in self.figuras]

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2)

    def abrir(self, caminho):

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.figuras = [criarFiguraDeDicionario(item) for item in dados]

        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_preview = None
        self.figuras_selecionadas = []
        self.figuras_candidatas = []
        self.retangulo_selecao = None
        self.posicao_anterior = None

        self.desenhar()
