import math
import random

def funcao(x,y):
    return (-(math.sin(2*math.pi*x)**3)*(math.sin(2*math.pi*y))/((x**3)*(x+y)))

def inicializacao(min, max, tam_pop):
    vi = [[0,0]*tam_pop]

    for i in range(0, tam_pop):
        for j in range(0, 2):
            vi[i][j] = random.uniform(min[i], max[i])

    return vi

def fitness(pop):
    tam_pop = len(pop)
    av = []*tam_pop
    for i in range(0, tam_pop):
        av[i] = funcao(pop[i][0], pop[i][1])
    return av

# Seleção para Reprodução
def selecao_torneio_binario(pop):
    pop_size = len(pop)
    best = [[0,0]*math.ceil(pop_size/2)]
    for j in range(0, pop_size):
        contestant1 = pop[random.randint(0, pop_size)]
        contestant2 = pop[random.randint(0, pop_size)]
        if(funcao(contestant1[0], contestant1[1]) <= funcao(contestant2[0], contestant2[1])):
            best[j] = contestant1
        else:
            best[j] = contestant2
    return best

# Seleção para Sobrevivência
def selecao_mais_apto(pais, filhos):
    tam_pais = len(pais)
    tam_filhos = len(filhos)
    quant = random.randint(1,tam_pais-1)

    res = []*quant

    av_pais = fitness(pais)
    av_pais, pais = zip(*sorted(zip(av_pais, pais)))

    av_filhos = fitness(filhos)
    av_filhos, filhos = zip(*sorted(zip(av_filhos, filhos)))

    r = 0
    tp = math.floor(tam_pais*0.3)
    for i in range(0, tp):
        res[r] = pais[i]
        r += 1
    
    tf = math.floor(tam_filhos*0.3)
    for i in range(0, tf):
        res[r] = filhos[i]
        r += 1
    
    pais = pais[math.floor(tam_pais*0.3)]
    filhos = filhos[math.floor(tam_pais*0.3)]
    
    pf = pais + filhos
    q = tam_pais - tp - tf

    v = random.sample(range(len(pf)), q)

    for i in v:
        res[r] = pf[i]
        r += 1

    return res

def cruzamento(pais):
    filhos = [[],[]]*len(pais)
    c = 0
    for i in range(len(pais)):
        for j in range(i, len(pais)):
            
            if(pais[i][0] < pais[j][0]):
                filhos[c][0] = random.uniform(pais[i][0], pais[j][0])
            else:
                filhos[c][0] = random.uniform(pais[j][0], pais[i][0])
            
            if(pais[i][1] < pais[j][1]):
                filhos[c][1] = random.uniform(pais[i][1], pais[j][1])
            else:
                filhos[c][1] = random.uniform(pais[j][1], pais[i][1])
            c += 1

    return filhos

def mutacao_uniforme(pop, min, max):
    for i in range(len(pop)):
        pop[i][0] += random.uniform(0,1)*(max[0]-min[0])*(2*random.uniform(0,1)-1) # SOMA?
        pop[i][1] += random.uniform(0,1)*(max[1]-min[1])*(2*random.uniform(0,1)-1) # SOMA?
    return pop

def rest1(x, y):
    return x**2 - y + 1

def rest2(x, y):
    return 1 - x + (y - 4)**2

def regras_factibilidade(ind):
    if(rest1(ind[0], ind[1]) >= 0 and rest2(ind[0], ind[1]) >= 0): return 1
    else: return 0

def criterio_parada(pop, melhores):
    av_pop = fitness(pop)
    av_pop, pop = zip(*sorted(zip(av_pop, pop)))

    melhores.append(pop[0])

    for i in range(1,10):
        if(melhores[-i] != pop[0]):
            return 0
    
    return 1


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
