import math
import random

def funcao(p_i, p_i_min, parametros_obj):       
    return (parametros_obj[0] * (p_i**2)) + (parametros_obj[1] * p_i) + parametros_obj[2] + abs(parametros_obj[3] * math.sin(parametros_obj[4] * (p_i_min - p_i)))

def calcular_funcao_individuo(individuo, min, dados_objetivo):
    soma = 0

    for i in range(len(individuo)):
        parametros_obj = [dados_objetivo[0][i], dados_objetivo[1][i], dados_objetivo[2][i], dados_objetivo[3][i], dados_objetivo[4][i]]
        soma += funcao(individuo[i], min[i], parametros_obj)
    
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

        individuo = min.copy()
        for j in range(40):
            p_i = random.uniform((max[j] - min[j])*0.6, (max[j] - min[j]))
            if(montante-p_i < 0):
                individuo[j] += (montante)
                break
            individuo[j] += p_i
            montante -= p_i

        vi.append(individuo)

    return vi

def selecao_torneio(pop, t_size, min, dados_objetivo):
    pop_size = len(pop)
    best = pop[random.randint(0, pop_size-1)]

    contestant = best
    for j in range(1, t_size):
        contestant = pop[random.randint(0, pop_size-1)]
        if(calcular_funcao_individuo(contestant, min, dados_objetivo) < calcular_funcao_individuo(best, min, dados_objetivo)):
            best = contestant

    return best

def ajustar_ordem(a, b):
    return (a,b) if (a>b) else (b,a)

def cruzamento_simples(pais):
    filhos = []

    # Número ímpar vai dar um número diferente de filhos
    for i in range(math.floor(len(pais)/2)):

        filho1 = pais[i].copy()
        filho2 = pais[i].copy()
        filho3 = pais[i].copy()
        filho4 = pais[i].copy()

        ale1 = random.randint(0, 40)
        for j in range(ale1):
            filho1[j] = pais[len(pais)-i-1][j]
        
        for j in range(ale1, 40):
            filho2[j] = pais[len(pais)-i-1][j]
 
        ale2 = random.randint(0, 40)
        for j in range(ale2):
            filho3[j] = pais[len(pais)-i-1][j]
        
        for j in range(ale2, 40):
            filho4[j] = pais[len(pais)-i-1][j]

        filhos.append(filho1)
        filhos.append(filho2)
        filhos.append(filho3)
        filhos.append(filho4)

    return filhos

def mutacao_uniforme(pop, min, max):
    sigma = 2
    for i in range(len(pop)):
        for j in range(40):
            if(random.randint(1,50) == 1):
                pop[i][j] += sigma*(max[j]-min[j])*(2*random.uniform(0,1)-1)
    
    return pop

def restricao(somatorio_p_i):
    return (somatorio_p_i - 10500)

def regras_factibilidade(filhos, min, dados_objetivo):

    filhos_escolhidos = []

    for i in range(0, len(filhos), 2):
        ind1 = filhos[i]
        ind2 = filhos[i+1]

        fit1 = calcular_funcao_individuo(ind1, min, dados_objetivo)
        fit2 = calcular_funcao_individuo(ind2, min, dados_objetivo)

        r1 = restricao(sum(ind1))
        r2 = restricao(sum(ind2))

        fac_ind1 = abs(r1)

        fac_ind2 = abs(r2)

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
def selecao(pais, filhos):
    tam_pop = len(pais)

    pop = pais.copy()

    for i in range(len(filhos)):
        if(restricao(sum(filhos[i])) == 0):
            pop[random.randint(0, tam_pop-1)] = filhos[i]

    return pop

def atualiza_melhor(pop, melhor, min, dados_objetivo):

    for j in range(len(pop)):
        print("P: ", calcular_funcao_individuo(pop[j], min, dados_objetivo))
        
        if(restricao(sum(pop[j])) == 0 and
            calcular_funcao_individuo(pop[j], min, dados_objetivo) < calcular_funcao_individuo(melhor, min, dados_objetivo)):
            melhor = pop[j]
            print("M: ", calcular_funcao_individuo(melhor, min, dados_objetivo))

    return melhor

def algoritmo_genetico():
    min, max = retornar_intervalos()
    dados_objetivo = retornar_dados_objetivo()

    tam_pop = 10
    n_geracoes = 20 # Número de gerações sem melhoria para parar a execução do método

    cp = 0
    
    # Geração Inicial
    pop = inicializacao(tam_pop, min, max, dados_objetivo)

    melhor = pop[random.randint(0, len(pop)-1)]

    print("Checking: ", calcular_funcao_individuo(melhor, min, dados_objetivo))
    print("SMI: ", sum(melhor))

    while True:
        pais = []

        # Seleção para Cruzamento
        for i in range(tam_pop): pais.append(selecao_torneio(pop, 2, min, dados_objetivo))

        # Cruzamento (Gera o dobro de filhos se comparado ao número de pais)
        filhos = cruzamento_simples(pais.copy())

        # Mutação
        filhos = mutacao_uniforme(filhos.copy(), min, max)

        filhos = regras_factibilidade(filhos.copy(), min, dados_objetivo)

        # Seleção para Sobrevivência
        pop = selecao(pop.copy(), filhos.copy())

        # Atualiza o melhor indivíduo
        novo_melhor = atualiza_melhor(pop.copy(), melhor, min, dados_objetivo)
        print("Valor_NM: ",calcular_funcao_individuo(novo_melhor, min, dados_objetivo),  " Soma Pi: ", sum(novo_melhor), " Geração: ", cp)
        if(novo_melhor != melhor):
            melhor = novo_melhor
            cp +=1
        else: cp += 1

        # Critério de Parada
        if(cp == n_geracoes):
            print(melhor)
            print(calcular_funcao_individuo(melhor, min, dados_objetivo), " ", sum(melhor))
            break
            #return melhor, funcao(melhor[0], melhor[1])

if __name__ == '__main__':
    algoritmo_genetico()