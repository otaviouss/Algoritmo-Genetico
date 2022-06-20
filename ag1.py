import math
import random

def funcao(x,y):
    return (-(math.sin(2*math.pi*x)**3)*(math.sin(2*math.pi*y))/((x**3)*(x+y)))

def inicializacao(min, max):
    vi = [[0,0],[0,0]]

    for i in range(0, 2):
        for j in range(0, 2):
            vi[i][j] = random.uniform(min[i], max[i])

    return vi

def fitness(tam_pop, pop):
    av = []*tam_pop
    for i in range(0, tam_pop):
        av[i] = funcao(pop[i][0], pop[i][1])
    return av

# Seleção para Reprodução
def selecao_torneio_binario(pop, t_size):
    pop_size = len(pop)
    best = pop[random.randint(0, pop_size)]
    contestant = 0
    for j in range(0, t_size):
        contestant = pop[random.randint(0, pop_size)]
        if(funcao(contestant[0], contestant[1]) < funcao(best[0], best[1])):
            best = contestant
    return best

# Seleção para Sobrevivência
def selecao_mais_apto(pais, filhos):
    tam_pop = len(pais)
    quant = random.randint(1,tam_pop-1)
    pais.sort()
    filhos.sort()

    for i in range(quant):
        pais[tam_pop-i-1] = filhos[i]

    return pais

def cruzamento(pais):
    filhos = [[],[]]*len(pais)
    c = 0
    for i in range(len(pais)/2):
        if(pais[i] <= pais[len(pais)-i-1]):
            filhos[c][0] = random.randint(pais[i][0], pais[len(pais)-i-1][0])
            filhos[c][1] = random.randint(pais[i][1], pais[len(pais)-i-1][1])
            c += 1
            filhos[c][0] = random.randint(pais[i][0], pais[len(pais)-i-1][0])
            filhos[c][1] = random.randint(pais[i][1], pais[len(pais)-i-1][1])
        else:
            filhos[c][0] = random.randint(pais[len(pais)-i-1][0], pais[i][0])
            filhos[c][1] = random.randint(pais[len(pais)-i-1][1], pais[i][1])
            c += 1
            filhos[c][0] = random.randint(pais[len(pais)-i-1][0], pais[i][0])
            filhos[c][1] = random.randint(pais[len(pais)-i-1][1], pais[i][1])
    return filhos

def mutacao_uniforme(pop, min, max):
    for i in range(len(pop)):
        pop[i][0] += (max[0]-min[0])*(2*random.rand(0,1)-1) # SOMA?
        pop[i][1] += (max[1]-min[1])*(2*random.rand(0,1)-1) # SOMA?
    return pop

def regras_factibilidade():
    # Restrições
    # x**2 - y + 1 <= 0
    # 1 - x + (y-4)**2 <= 0
    pass

def criterio_parada():
    pass


def algoritmo_genetico():
    min = [0,0]
    max = [10,10]
    pass


if __name__ == '__main__':
    arq = open('res.csv', 'w')
    for i in range(30):
        sol, res = algoritmo_genetico()
        arq.write(str(sol[0]).replace('.',',')+';'+str(sol[1]).replace('.',',')+';'+str(res).replace('.',',')+'\n')
    arq.close()
