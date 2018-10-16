# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:42:42 2018

@author: Keven
"""
from random import random
import matplotlib.pyplot as plt

class Papel():
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
        
class Individuo():
    def __init__(self, valores, valor_investimento, parte, geracao=0):
        self.valores = valores
        self.valor_investimento = valor_investimento
        self.parte = parte
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.cromossomo = []
        
        for i in range(len(valores)):
            valor_min = 0
            j_min = 0
            for j in range(100):
                valor_min = j*valores[i]
                if valor_min/self.valor_investimento > self.parte:
                    j_min = j
                    break
            valor_max = 9999999999999999
            j_max = 0
            for j in range(100,1,-1):
                valor_max = j*valores[i]
                if valor_max/self.valor_investimento < self.parte:
                    j_max= j
                    break
            if random() < 0.5:
                self.cromossomo.append(j_min)
            else:
                self.cromossomo.append(j_max)
        
    def avaliacao(self):
        nota = 0
        soma_investimento = 0
        for i in range(len(self.cromossomo)):
            soma_investimento += self.cromossomo[i]*self.valores[i]
            nota += (abs((self.cromossomo[i]*self.valores[i]/self.valor_investimento)-self.parte))
        if soma_investimento > self.valor_investimento:
            nota = 1
        else:
            nota = 1/nota
        self.nota_avaliacao = nota
        self.valor_usado = soma_investimento
        
    def crossover(self, outro_individuo):
        corte = round(random()  * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.valores, self.valor_investimento, self.parte, self.geracao + 1),
                  Individuo(self.valores, self.valor_investimento, self.parte, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
                
    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if random() > 0.5:
                    self.cromossomo[i] += 1
                else:
                    self.cromossomo[i] -= 1
        return self
    
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.lista_solucoes = []
        self.geracao = 0
        self.melhor_solucao = 0
        
    def inicializa_populacao(self, valores, valor_investimento, parte):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(valores,valor_investimento,parte))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
                
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Nota: %s Valor_usado: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.valor_usado,
                                                               melhor.cromossomo))
        
    def resolver(self, taxa_mutacao, numero_geracoes, valores, valor_investimento,parte):
        self.inicializa_populacao(valores, valor_investimento, parte)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.valor_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao
                
if __name__ == '__main__':
    lista_papeis = []
    lista_papeis.append(Papel("IRBR3F", 63.30))
    lista_papeis.append(Papel("VALE3F", 57.80))
    lista_papeis.append(Papel("GGBR4F", 15.55))
    lista_papeis.append(Papel("ITSA4F", 10.82))
    lista_papeis.append(Papel("EQTL3F", 58.22))
    lista_papeis.append(Papel("BBAS3F", 37.71))
    lista_papeis.append(Papel("ABEV3F", 16.98))
    lista_papeis.append(Papel("TUPY3F", 18.30))
    parte = 1 / len(lista_papeis)

    valores = []
    nomes = []
    for papel in lista_papeis:
        valores.append(papel.valor)
        nomes.append(papel.nome)
    valor_investimento = 5000
    tamanho_populacao = 20
    numero_geracoes = 100
    taxa_mutacao = 0.01
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, valores, valor_investimento,parte)
    for i in range(len(lista_papeis)):
        print("Nome: %s R$ %s Quantidade: %s" % (lista_papeis[i].nome,
                                                 resultado.valores[i],
                                                 resultado.cromossomo[i]))
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()