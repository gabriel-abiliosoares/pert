import networkx as nx
from collections import deque
import heapq



def lerGrafo(caminho):
    G = nx.DiGraph()

    with open(caminho, 'r') as f:
        for linha in f:
            u, v, d = linha.strip().split()
            G.add_edge(u, v, weight=float(d))

    return G

def ordenacao(G):
    grau_entrada = {no: 0 for no in G.nodes}

    # calcula grau de entrada
    for u, v in G.edges:
        grau_entrada[v] += 1

    fila = []
    for no in grau_entrada:
        if grau_entrada[no] == 0:
            fila.append(no)

    ordem = []

    while fila:
        no = fila.pop(0)
        ordem.append(no)

        for vizinho in G.successors(no):
            grau_entrada[vizinho] -= 1

            if grau_entrada[vizinho] == 0:
                fila.append(vizinho)

    if len(ordem) != len(G.nodes):
        raise ValueError("O grafo tem ciclo!")

    return ordem

def min(G, ordem):
    ES = {no: 0 for no in G.nodes}

    for no in ordem:
        for v in G.successors(no):
            peso = G[no][v]['weight']
            if ES[no] + peso > ES[v]:
                ES[v] = ES[no] + peso

    return ES

def max(G, ordem, tempo_total):
    LS = {no: tempo_total for no in G.nodes}

    for no in reversed(ordem):
        for v in G.successors(no):
            peso = G[no][v]['weight']
            if LS[v] - peso < LS[no]:
                LS[no] = LS[v] - peso

    return LS

def caminho_critico(G, ES, LS):
    critico = []

    for u, v in G.edges:
        peso = G[u][v]['weight']
        folga = LS[v] - ES[u] - peso

        if folga == 0:
            critico.append((u, v))

    return critico

def calcular_tempo_total(G, minimo):
    nos_finais = []

    for n in G.nodes:
        if len(list(G.successors(n))) == 0:
            nos_finais.append(n)

    if not nos_finais:
        raise ValueError("O grafo não possui nó final!")

    tempo_total = minimo[nos_finais[0]]

    for n in nos_finais:
        if minimo[n] > tempo_total:
            tempo_total = minimo[n]

    return tempo_total
caminho = input("Digite o caminho do arquivo de entrada: ")

G = lerGrafo(caminho)

ordem = ordenacao(G)

minimo = min(G, ordem)

tempo_total = calcular_tempo_total(G, minimo)

maximo = max(G, ordem, tempo_total)

critico = caminho_critico(G, minimo, maximo)

print("Ordem topológica:", ordem)
print("Tempo total:", tempo_total)

print("\nCaminho mínimo:")
for no in minimo:
    print(no, minimo[no])

print("\nCaminho máximo:")
for no in maximo:
    print(no, maximo[no])

print("\nCaminho crítico:")
for u, v in critico:
    print(f"{u} -> {v}")