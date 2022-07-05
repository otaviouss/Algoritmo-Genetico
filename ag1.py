import math
import random

def funcao(x,y):
    return (-(math.sin(2*math.pi*x)**3)*(math.sin(2*math.pi*y))/((x**3)*(x+y)))

def inicializacao(tam_pop, min, max):
    vi = []

    for i in range(tam_pop):
        vi.append([random.uniform(min[0], max[0]),random.uniform(min[1], max[1])])

    return vi

def fitness(pop):
    av = [[]]*len(pop)
    for i in range(len(pop)):
        av[i] = funcao(pop[i][0], pop[i][1])
    return av

# Seleção para Reprodução
def selecao_torneio(pop, t_size):
    pop_size = len(pop)
    contestant = [[]]*t_size
    best = pop[random.randint(0, pop_size-1)]

    contestant = best
    for j in range(1, t_size):
        contestant = pop[random.randint(0, pop_size-1)]
        if(funcao(contestant[0], contestant[1]) < funcao(best[0], best[1])):
            best = contestant

    return best

# Seleção para Sobrevivência
def selecao_estacionario(pais, filhos):
    tam_pop = len(pais)

    av_pais = fitness(pais)
    pais_ordenados = [x for _, x in sorted(zip(av_pais, pais))]

    av_filhos = fitness(filhos)
    filhos_ordenados = [x for _, x in sorted(zip(av_filhos, filhos))]

    t70 = math.floor(tam_pop*0.7)

    pop = pais_ordenados.copy()
    f = 0
    for i in range(t70, tam_pop):
        pop[i] = filhos_ordenados[f]
        f += 1

    return pop

def ajustar_ordem(a, b):
    return (a,b) if (a>b) else (b,a)

def cruzamento_flat(pais):
    filhos = []

    # Número ímpar vai dar um número diferente de filhos
    for i in range(math.floor(len(pais)/2)):
        x = ajustar_ordem(pais[i][0], pais[len(pais)-i-1][0])
        y = ajustar_ordem(pais[i][1], pais[len(pais)-i-1][1])
        filho = [random.uniform(x[0], x[1]), random.uniform(y[0], y[1])]

        filhos.append(filho)

        x = ajustar_ordem(pais[i][0], pais[len(pais)-i-1][0])
        y = ajustar_ordem(pais[i][1], pais[len(pais)-i-1][1])
        filho = [random.uniform(x[0], x[1]), random.uniform(y[0], y[1])]

        filhos.append(filho)

    return filhos

def mutacao_uniforme(pop, min, max):
    sigma = 0.5
    for i in range(len(pop)):
        if(random.randint(1,10)==1):
            pop[i][0] += sigma*(max[0]-min[0])*(2*random.uniform(0,1)-1)
            pop[i][1] += sigma*(max[1]-min[1])*(2*random.uniform(0,1)-1)
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

    tam_pop = 100

    pop = inicializacao(tam_pop, min, max)

    print(pop)

    pais = []

    for i in range(100):
        pais.append(selecao_torneio(pop, 2))
    
    print("\n\n\nPAIS:\n\n\n")
    print(pais)

    filhos = cruzamento_flat(pais)

    print("\n\n\nFILHOS:\n\n\n")
    print(filhos)

    filhos_mutacao = mutacao_uniforme(filhos, min, max)
    
    print("\n\n\nFILHOS MUTADOS:\n\n\n")
    print(filhos_mutacao)


if __name__ == '__main__':
    #arq = open('res.csv', 'w')
    #for i in range(30):
    #    sol, res = algoritmo_genetico()
    #    arq.write(str(sol[0]).replace('.',',')+';'+str(sol[1]).replace('.',',')+';'+str(res).replace('.',',')+'\n')
    #arq.close()
    algoritmo_genetico()
