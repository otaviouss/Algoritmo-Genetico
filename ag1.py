import math
import random

def funcao(x,y):
    try:
        return ((-(math.sin(2*math.pi*x)**3)*(math.sin(2*math.pi*y)))/((x**3)*(x+y)))
    except:
        return 10000000

def restricao1(x, y):
    return (x**2 - y + 1)

def restricao2(x, y):
    return (1 - x + (y-4)**2)

def inicializacao(tam_pop, min, max):
    vi = []

    for i in range(tam_pop):
        while True:
            x = random.uniform(min[0], max[0])
            y = random.uniform(min[1], max[1])
            if(restricao1(x, y) <= 0 and restricao2(x, y) <= 0): break

        vi.append([x,y])

    return vi

# Avalia o fitness de toda a população
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

    t60 = math.floor(tam_pop*0.6)

    pop = pais_ordenados.copy()
    f = 0
    for i in range(t60, tam_pop):
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
    sigma = 0.2
    for i in range(len(pop)):
        if(random.randint(1,50) == 1):
            pop[i][0] += sigma*(max[0]-min[0])*(2*random.uniform(0,1)-1)
            pop[i][1] += sigma*(max[1]-min[1])*(2*random.uniform(0,1)-1)
    return pop

def regras_factibilidade(filhos):

    filhos_escolhidos = []

    for i in range(0, len(filhos), 2):
        ind1 = filhos[i]
        ind2 = filhos[i+1]

        fit1 = funcao(ind1[0], ind1[1])
        fit2 = funcao(ind2[0], ind2[1])
        
        r11 = restricao1(ind1[0], ind1[1])
        r21 = restricao2(ind1[0], ind1[1])

        fac_ind1 = max(0, r11)**2 + max(0, r21)**2

        r12 = restricao1(ind2[0], ind2[1])
        r22 = restricao2(ind2[0], ind2[1])

        fac_ind2 = max(0, r12)**2 + max(0, r22)**2

        if(fac_ind1 == 0 and fac_ind2 == 0):
            if(fit1 >= fit2):
                filhos_escolhidos.append(ind1)
            else:
                filhos_escolhidos.append(ind2)
        
        elif(fac_ind1 > 0 and fac_ind2 == 0):
            filhos_escolhidos.append(ind2)
        
        elif(fac_ind2 > 0 and fac_ind1 == 0):
            filhos_escolhidos.append(ind1)
        
        else:
            if(fac_ind1 >= fac_ind2):
                filhos_escolhidos.append(ind2)
            else:
                filhos_escolhidos.append(ind1)
        
    return filhos_escolhidos

def atualiza_melhor(pais, melhor, min, max):
    av_pais = fitness(pais)
    pais_ordenados = [x for _, x in sorted(zip(av_pais, pais))]

    for j in range(len(pais_ordenados)):
        if(funcao(pais_ordenados[j][0], pais_ordenados[j][1]) < funcao(melhor[0], melhor[1]) and 
            restricao1(pais_ordenados[j][0], pais_ordenados[j][1]) <= 0                      and
            restricao2(pais_ordenados[j][0], pais_ordenados[j][1]) <= 0                      and
            pais_ordenados[j][0] >= min[0] and pais_ordenados[j][0] <= max[0]                and
            pais_ordenados[j][1] >= min[1] and pais_ordenados[j][1] <= max[1]):
            
            melhor = pais_ordenados[j]

    return melhor


def algoritmo_genetico():
    min = [0,0]
    max = [10,10]

    tam_pop = 500
    n_geracoes = 30 # Número de gerações sem melhoria para parar a execução do método

    melhor = [0,0]

    cp = 0

    # Geração Inicial
    pop = inicializacao(tam_pop, min, max)

    while True:
        pais = []

        # Seleção para Cruzamento
        for i in range(tam_pop): pais.append(selecao_torneio(pop, 3))

        # Cruzamento (Gera o dobro de filhos se comparado ao número de pais)
        filhos = cruzamento_flat(pais)

        # Mutação
        filhos = mutacao_uniforme(filhos, min, max)

        # Aplicação das Regras de Factibilidade
        filhos = regras_factibilidade(filhos)

        # Seleção para Sobrevivência
        pop = selecao_estacionario(pais, filhos)

        # Atualiza o melhor indivíduo
        novo_melhor = atualiza_melhor(pop, melhor, min, max)

        if(novo_melhor != melhor):
            melhor = novo_melhor
            cp = 0
        else: cp += 1

        # Critério de Parada
        if(cp == n_geracoes):
            print(melhor)
            print(funcao(melhor[0], melhor[1]))
            return melhor, funcao(melhor[0], melhor[1])

if __name__ == '__main__':
    arq = open('res1.csv', 'w')
    for i in range(30):
        sol, res = algoritmo_genetico()
        arq.write(str(sol[0]).replace('.',',')+';'+str(sol[1]).replace('.',',')+';'+str(res).replace('.',',')+'\n')
    arq.close()
