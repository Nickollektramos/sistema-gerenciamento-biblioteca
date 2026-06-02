class No:
    def __init__(self, cod, pos):
        self.cod = cod
        self.pos = pos
        self.esq = None
        self.dir = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir_no(self, cod, pos):
        if self.raiz is None:
            self.raiz = No(cod, pos)
        else: 
            self.inserir_no_filho(self.raiz, cod, pos)
        
    def inserir_no_filho(self, pai, cod, pos):
        if cod < pai.cod: 
            if pai.esq is None:
                pai.esq = No(cod, pos)
            else: 
                self.inserir_no_filho(pai.esq, cod, pos)
        elif cod > pai.cod:
            if pai.dir is None:
                pai.dir = No(cod, pos)
            else:
                self.inserir_no_filho(pai.dir, cod, pos)
        else:
            pai.pos = pos

    def buscar(self, cod):
        return self.buscar_cod(self.raiz, cod)
    
    def buscar_cod(self, raiz, cod):
        if raiz is None:
            return None
        elif raiz.cod == cod:
            return raiz.pos
        elif cod < raiz.cod:
            return self.buscar_cod(raiz.esq, cod)
        else:
            return self.buscar_cod(raiz.dir, cod)

    def deletar(self, cod):
        self.raiz = self.excluir(self.raiz, cod)
        
    def excluir(self, raiz, cod):
        if raiz is None:
            return None
        if cod < raiz.cod:
            raiz.esq = self.excluir(raiz.esq, cod)
        elif cod > raiz.cod:
            raiz.dir = self.excluir(raiz.dir, cod)
        else:
            if raiz.esq is None:
                return raiz.dir
            elif raiz.dir is None:
                return raiz.esq
            else:
                ex = self.minimo(raiz.dir)
                raiz.cod = ex.cod
                raiz.pos = ex.pos
                raiz.dir = self.excluir(raiz.dir, ex.cod)
        return raiz
        
    def minimo(self, pai):
        atual = pai
        while atual.esq is not None:
            atual = atual.esq
        return atual
    
    def lerEmOrdem(self, arquivo, exibir, contadores=None, filtro=None, dataI=None, dataF=None):
        with open(arquivo, 'rt', encoding="utf-8") as arq:
            registros = arq.readlines()
            def percorrer(no):
                if no is not None:
                    percorrer(no.esq)
                    exibir(registros[no.pos], contadores, filtro, dataI, dataF)
                    percorrer(no.dir)
            percorrer(self.raiz)
        