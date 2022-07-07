import math
import random

def funcao(x,y):
    try:
        return (-(math.sin(2*math.pi*x)**3)*(math.sin(2*math.pi*y))/((x**3)*(x+y)))
    except:
        return 10000000

def restricao1(x, y):
    return (x**2 - y + 1)

def restricao2(x, y):
    return (1 - x + (y-4)**2)

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

def criterio_parada(pais, melhores):
    av_pais = fitness(pais)
    pais_ordenados = [x for _, x in sorted(zip(av_pais, pais))]

    for i in range(len(melhores)):
        if(funcao(pais_ordenados[0][0], pais_ordenados[0][1]) < funcao(melhores[i][0], melhores[i][1])):
            melhores[i] = pais_ordenados[0]
            return 0

    return 1


def algoritmo_genetico():
    min = [0,0]
    max = [10,10]

    tam_pop = 400
    n_geracoes = 7

    pais = []
    melhores = [[0.0,0.0]]*n_geracoes

    cp = 0

    # Geração Inicial
    pop = inicializacao(tam_pop, min, max)

    while True:
        # Seleção para Cruzamento
        for i in range(100): pais.append(selecao_torneio(pop, 2))

        # Cruzamento (Gera o dobro de filhos se comparado ao número de pais)
        filhos = cruzamento_flat(pais)

        # Mutação
        filhos_mutacao = mutacao_uniforme(filhos, min, max)

        # Aplicação das Regras de Factibilidade
        pais = regras_factibilidade(filhos_mutacao)

        # Observância dos critérios de parada
        c = criterio_parada(pais, melhores)

        if(c==1): cp += 1
        else:     cp = 0
        
        # Finalização
        if(cp == n_geracoes):
            av_melhores = fitness(melhores)
            melhores = [x for _, x in sorted(zip(av_melhores, melhores))]
            for i in range(n_geracoes):
                if(melhores[i][0] >= 0 and melhores[i][1] >= 0 and melhores[i][0] <= 10 and melhores[i][1] <= 10 and
                    restricao1(melhores[i][0], melhores[i][1]) >= 0 and restricao2(melhores[i][0], melhores[i][1]) >= 0):
                    print("RES: ", melhores[i])
                    print(funcao(melhores[i][0], melhores[i][1]))
                    #for melhor in melhores:
                    #    print(melhor)
                    print()
                    return melhores[i], funcao(melhores[i][0], melhores[i][1])
            
            pais = []
            melhores = [[0.0,0.0]]*n_geracoes

            cp = 0

            # Re-Geração Inicial
            pop = inicializacao(tam_pop, min, max)


if __name__ == '__main__':
    arq = open('res1.csv', 'w')
    for i in range(30):
        sol, res = algoritmo_genetico()
        arq.write(str(sol[0]).replace('.',',')+';'+str(sol[1]).replace('.',',')+';'+str(res).replace('.',',')+'\n')
    arq.close()
    algoritmo_genetico()
