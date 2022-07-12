import math
import random
import csv
from time import sleep

def funcao(p_i, p_i_min, parametros_obj):       
    return (parametros_obj[0] * (p_i**2)) + (parametros_obj[1] * p_i) + parametros_obj[2] + abs(parametros_obj[3] * math.sin(parametros_obj[4] * (p_i_min - p_i)))

def calcular_funcao_individuo(individuo, min, dados_objetivo):
    soma = 0

    for i in range(len(individuo)):
        parametros_obj = [dados_objetivo[0][i], dados_objetivo[1][i], dados_objetivo[2][i], dados_objetivo[3][i], dados_objetivo[4][i]]
        #print("PArametos: ", parametros_obj)
        soma += funcao(individuo[i], min[i], parametros_obj)
        #print(soma)
    
    return soma


def retornar_intervalos():
    min = []
    max = []
    with open('dadosMaquinasGeradoras.txt', 'r') as fileObj:
        stripped = (line.strip() for line in fileObj)
        lines = (line.split(" ") for line in stripped if line)
        for line in lines:
            min.append(int(line[1]))
            max.append(int(line[2]))
    
    fileObj.close()

    return min, max

def retornar_dados_objetivo():
    a = []
    b = []
    c = []
    e = []
    f = []
    
    with open('dadosMaquinasGeradoras.txt', 'r') as fileObj:
        stripped = (line.strip() for line in fileObj)
        lines = (line.split(" ") for line in stripped if line)
        for line in lines:
            a.append(float(line[3]))
            b.append(float(line[4]))
            c.append(float(line[5]))
            e.append(float(line[6]))
            f.append(float(line[7]))
    
    fileObj.close()

    dados_objetivo = [a, b, c, e, f]

    return dados_objetivo

def inicializacao(tam_pop, min, max, dados_objetivo):
    vi = []
    for i in range(tam_pop):
        montante = 10500 - sum(min)

        individuo = min
        for j in range(40):
            p_i = random.uniform(min[j], (max[j] - min[j]))
            individuo[j] += p_i
            montante -= p_i
            if montante <= 100:
                break
            
        print("SOMA: ", sum(individuo), " VALOR FO: ", calcular_funcao_individuo(individuo, min, dados_objetivo))
        sleep(1)
            
        vi.append(individuo)

    return vi

def selecao_torneio(pop, t_size, min, dados_objetivo):
    pop_size = len(pop)
    #contestant = [[]]*t_size
    best = pop[random.randint(0, pop_size-1)]

    contestant = best
    for j in range(1, t_size):
        contestant = pop[random.randint(0, pop_size-1)]
        #print("Calculo: ", calcular_funcao_individuo(contestant, min, dados_objetivo))
        if(calcular_funcao_individuo(contestant, min, dados_objetivo) < calcular_funcao_individuo(best, min, dados_objetivo)):
            best = contestant

    return best

def ajustar_ordem(a, b):
    return (a,b) if (a>b) else (b,a)

def cruzamento_flat(pais):
    filhos = []

    # Número ímpar vai dar um número diferente de filhos
    for i in range(math.floor(len(pais)/2)):

        filho = []
        for j in range(40):
            p_i = ajustar_ordem(pais[i][j], pais[len(pais)-i-1][j])
            filho.append( random.uniform(p_i[0], p_i[1]) )
 
        filhos.append(filho)

        filho = []
        for j in range(40):
            p_i = ajustar_ordem(pais[i][j], pais[len(pais)-i-1][j])
            filho.append( random.uniform(p_i[0], p_i[1]) )
 
        filhos.append(filho)

        filho = []
        for j in range(40):
            p_i = ajustar_ordem(pais[i][j], pais[len(pais)-i-1][j])
            filho.append( random.uniform(p_i[0], p_i[1]) )
 
        filhos.append(filho)

        filho = []
        for j in range(40):
            p_i = ajustar_ordem(pais[i][j], pais[len(pais)-i-1][j])
            filho.append( random.uniform(p_i[0], p_i[1]) )
 
        filhos.append(filho)

    return filhos

def mutacao_uniforme(pop, min, max):
    sigma = 0.2
    for i in range(len(pop)):
        for j in range(40):
            if(random.randint(1,50) == 1):
                #print('.')
                pop[i][j] += sigma*(max[j]-min[j])*(2*random.uniform(0,1)-1)
    
    return pop

def restricao(somatorio_p_i):
    return (somatorio_p_i - 10500)

def check_restricao(r):
    if r <= 0 and r >= -1:
        return 0
    if r > 0:
        return 1
    
    return -1

def regras_factibilidade(filhos, min, dados_objetivo):

    filhos_escolhidos = []

    for i in range(0, len(filhos), 2):
        ind1 = filhos[i]
        ind2 = filhos[i+1]

        fit1 = calcular_funcao_individuo(ind1, min, dados_objetivo)
        fit2 = calcular_funcao_individuo(ind2, min, dados_objetivo)

        r1 = restricao(sum(ind1))
        r2 = restricao(sum(ind2))

        fac_ind1 = check_restricao(r1)

        fac_ind2 = check_restricao(r2)

        if(fac_ind1 == 0 and fac_ind2 == 0):
            if(fit1 >= fit2): # aquele que tiver menor valor da FO é o desejado
                filhos_escolhidos.append(ind2)
            else:
                filhos_escolhidos.append(ind1)
        
        elif(fac_ind1 != 0 and fac_ind2 == 0):
            filhos_escolhidos.append(ind2)
        
        elif(fac_ind2 != 0 and fac_ind1 == 0):
            filhos_escolhidos.append(ind1)
        
        else:
            if(fac_ind1 >= fac_ind2):
                filhos_escolhidos.append(ind2)
            else:
                filhos_escolhidos.append(ind1)
        
    return filhos_escolhidos

def fitness(pop, min, dados_objetivo):
    av = []
    for i in range(len(pop)):
        av.append(calcular_funcao_individuo(pop[i], min, dados_objetivo))
    return av

# Seleção para Sobrevivência
def selecao_estacionario(pais, filhos, min, dados_objetivo):
    tam_pop = len(pais)

    av_pais = fitness(pais, min, dados_objetivo)
    pais_ordenados = [x for _, x in sorted(zip(av_pais, pais))]

    av_filhos = fitness(filhos, min, dados_objetivo)
    filhos_ordenados = [x for _, x in sorted(zip(av_filhos, filhos))]

    t60 = math.floor(tam_pop*0.6)

    pop = pais_ordenados.copy()
    f = 0
    for i in range(t60, tam_pop):
        pop[i] = filhos_ordenados[f]
        f += 1

    return pop

def atualiza_melhor(pais, melhor, min, dados_objetivo):
    av_pais = fitness(pais, min, dados_objetivo)
    pais_ordenados = [x for _, x in sorted(zip(av_pais, pais))]

    for j in range(len(pais_ordenados)):
        fit_pai = calcular_funcao_individuo(pais_ordenados[j], min, dados_objetivo)
        print("Comparacao: ", fit_pai, " -/- ", calcular_funcao_individuo(melhor, min, dados_objetivo))
        print("Solucao analisada, result rest: ", abs(restricao(sum(pais_ordenados[j]))))
        
        if(abs(restricao(sum(pais_ordenados[j]))) <= 50 and fit_pai < calcular_funcao_individuo(melhor, min, dados_objetivo) ):
                    
            melhor = pais_ordenados[j]

    return melhor

def algoritmo_genetico():
    min, max = retornar_intervalos()
    dados_objetivo = retornar_dados_objetivo()

    print("MIN: ", sum(min), "Valor Fo: ",calcular_funcao_individuo(min, min, dados_objetivo))
    print("MAX: ", sum(max), "Valor Fo: ",calcular_funcao_individuo(max, min, dados_objetivo))
    tam_pop = 10
    n_geracoes = 30 # Número de gerações sem melhoria para parar a execução do método

    cp = 0
    
    # Geração Inicial
    pop = inicializacao(tam_pop, min, max, dados_objetivo)

    melhor = pop[random.randint(0, len(pop)-1)]

    print("Checking: ", calcular_funcao_individuo(melhor, min, dados_objetivo))


    while True:
        pais = []

        # Seleção para Cruzamento
        for i in range(tam_pop): pais.append(selecao_torneio(pop, 3, min, dados_objetivo))

        # Cruzamento (Gera o dobro de filhos se comparado ao número de pais)
        filhos = cruzamento_flat(pais)


        # Mutação
        filhos = mutacao_uniforme(filhos, min, max)


        filhos = regras_factibilidade(filhos, min, dados_objetivo)

        # Seleção para Sobrevivência
        pop = selecao_estacionario(pais, filhos, min, dados_objetivo)


        # Atualiza o melhor indivíduo
        novo_melhor = atualiza_melhor(pop, melhor, min, dados_objetivo)
        print("Valor: ",calcular_funcao_individuo(novo_melhor, min, dados_objetivo),  " Soma Pi: ", sum(novo_melhor), " Geração: ", cp)
        if(novo_melhor != melhor):
            melhor = novo_melhor
            cp = 0
        else: cp += 1

        # Critério de Parada
        if(cp == n_geracoes):
            #print(melhor)
            print(calcular_funcao_individuo(melhor, min, dados_objetivo), " ", sum(melhor))
            break
            #return melhor, funcao(melhor[0], melhor[1])

if __name__ == '__main__':
    algoritmo_genetico()