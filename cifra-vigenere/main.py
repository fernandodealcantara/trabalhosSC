alfabeto = 'abcdefghijklmnopqrstuvwxyz'

frequencias_ingles = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 
                      0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                      0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

frequencias_portugues = [0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.0130, 0.0128, 0.0618, 0.040, 0.002, 
                          0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.0120, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 
                          0.001, 0.0021, 0.001, 0.0047]

utilizar_frequencias_portugues = False

# função decoradora responsavel por lidar com caracteres que não podem ser cifrados
def considerar_apenas_alfabeto(func):
    def inner(mensagem_para_tratar, chave=None):
        mensagem_final = [None] * len(mensagem_para_tratar)
        mensagem = ''

        for indice in range(len(mensagem_para_tratar)):
            if mensagem_para_tratar[indice] in alfabeto + alfabeto.upper():
                mensagem +=  mensagem_para_tratar[indice]
            else:
                mensagem_final[indice] = mensagem_para_tratar[indice]

        if chave:
            nova_mensagem = func(mensagem, chave)

            for caractere in nova_mensagem:
                mensagem_final[mensagem_final.index(None)] = caractere

            return ''.join(mensagem_final)
        else: 
            return func(mensagem.lower())

    return inner

# funcao responsavel por encriptar a mensagem
@considerar_apenas_alfabeto
def encriptar(mensagem, chave):
    mensagem_em_lista = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    encriptado = ''
    for pedaço in mensagem_em_lista:
        i = 0
        for letra in pedaço:
            indice = (alfabeto.index(letra.lower()) + alfabeto.index(chave[i].lower())) % len(alfabeto)
            encriptado += alfabeto[indice] if letra.islower() else alfabeto[indice].upper()
            i += 1

    return encriptado

# funcao responsavel por decriptar a mensagem
@considerar_apenas_alfabeto
def decriptar(mensagem, chave):
    mensagem_em_lista = [mensagem[i: i + len(chave)] for i in range(0, len(mensagem), len(chave))]

    decriptado = ''
    for pedaço in mensagem_em_lista:
        i = 0
        for letra in pedaço:
            indice = (alfabeto.index(letra.lower()) - alfabeto.index(chave[i].lower())) % len(alfabeto)
            decriptado += alfabeto[indice] if letra.islower() else alfabeto[indice].upper()
            i += 1

    return decriptado

# funcao responsavel de realizar o calculo de indice de coincidencia
def pegar_indice_coincidencia(sequencia):
    N = float(len(sequencia))
    soma_frequencia = 0.0

    for letra in alfabeto:
        soma_frequencia += sequencia.count(letra) * (sequencia.count(letra) - 1)

    indice_coincidencia = soma_frequencia/ (N*(N-1))

    return indice_coincidencia

# funcao responsavel de escolher o tamanho mais provavel da chave
def pegar_tamanho_chave(mensagem, tamanho: int = 20):
    tabela_ic = []
    tamanho_maximo_chave = tamanho

    for tamanho_suposto in range(tamanho_maximo_chave):
        soma_ic = 0.0

        for i in range(tamanho_suposto):
            sequencia = ''

            for j in range(0, len(mensagem[i:]), tamanho_suposto):
                sequencia += mensagem[i+j]

            if (len(sequencia) > 1):
                soma_ic += pegar_indice_coincidencia(sequencia)

        ic_medio = soma_ic / tamanho_suposto if not tamanho_suposto == 0 else 0.0
        tabela_ic.append(ic_medio)
    
    tabela_ic_ordenada = sorted(tabela_ic, reverse=True)

    melhores_suposições = list(map(lambda valor: tabela_ic.index(valor), tabela_ic_ordenada))
    melhores_suposições = [suposição for suposição in list(dict.fromkeys(melhores_suposições)) if suposição != 0]

    return melhores_suposições[:5]
    

# funcao responsavel de escolher a melhor letra baseado em analise de frequencia
def analise_frequencia(sequencia):
    todos_qui_quadrados = [0] * 26

    for i in range(26):
        sequencia_deslocada = [alfabeto[(alfabeto.index(letra.lower())-i)%26] for letra in sequencia]

        frequencias_ocorrencias_letras = [float(sequencia_deslocada.count(letra))/float(len(sequencia)) for letra in alfabeto]

        soma_qui_quadrado = 0.0
        frequencia = frequencias_portugues if utilizar_frequencias_portugues else frequencias_ingles
        for j in range(26):
            soma_qui_quadrado+=((frequencias_ocorrencias_letras[j] - float(frequencia[j]))**2)/float(frequencia[j])

        todos_qui_quadrados[i] = soma_qui_quadrado

    letra_com_menor_qui_quadrado = todos_qui_quadrados.index(min(todos_qui_quadrados))
    
    for qui_quadrado in sorted(todos_qui_quadrados)[:5]:
        print(f'({alfabeto[todos_qui_quadrados.index(qui_quadrado)]}:{qui_quadrado:.2f})', end = ' ')
    letra = input('Escolha uma letra ou aperte enter: ')
    return letra if len(letra) == 1 and letra in alfabeto else alfabeto[letra_com_menor_qui_quadrado]

# funcao responsavel por 'montar' a chave final
def pegar_chave(mensagem, tamanho_chave):
    chave = ''

    for i in range(tamanho_chave):
        sequencia = ''

        for j in range(0, len(mensagem[i:]), tamanho_chave):
            sequencia += mensagem[i+j]

        chave += analise_frequencia(sequencia)

    return chave

# funcao que executa os passos de ataque para achar uma chave
@considerar_apenas_alfabeto
def atacar(mensagem):
    tamanho_chave = pegar_tamanho_chave(mensagem)
    if tamanho_chave == 0:
        return None
    else:
        print('Tamanhos de chaves encontradas (em ordem de possivel melhor tamanho): ', *[{i: tamanho_chave[i]} for i in range(len(tamanho_chave))])
        tamanho_escolhido = input('Escolha uma começando do índice 0 ou aperte enter: ', )
        tamanho_escolhido = int(tamanho_escolhido)%len(tamanho_chave) if tamanho_escolhido.isnumeric() else 0
    chave = pegar_chave(mensagem, tamanho_chave[tamanho_escolhido])

    return chave

# DAQUI PARA BAIXO É APENAS INPUT DE DADOS DO USUARIO,
# NADA RELACIONADO COM AS FUNÇÕES DA CIFRA
def formatar_chave(chave):
    return ''.join([char for char in chave if char.lower() in alfabeto])

def selecionar_modo():
    print('Selecione o que fazer:')
    print('1 - Encriptar mensagem')
    print('2 - Decriptar mensagem')
    print('3 - Atacar')
    print('Any key - Cancelar')
    modo = input('Opção: ')
    if modo == '1':
        return 'cifrar'
    elif modo == '2':
        return 'decifrar'
    elif modo == '3':
        return 'atacar'
    return None

def main():
    global utilizar_frequencias_portugues
    try:
        resultado = ''
        modo = selecionar_modo()
        
        if modo == 'cifrar':
            mensagem = input('Mensagem: ')
            chave = formatar_chave(input('Chave: '))
            resultado = encriptar(mensagem, chave)

        elif modo == 'decifrar':
            mensagem = input('Mensagem: ')
            chave = formatar_chave(input('Chave: '))
            resultado = decriptar(mensagem, chave)

        elif modo == 'atacar':
            mensagem = input('Mensagem: ')
            utilizar_opcao = input('Utilizar frequencias em português [s/n]? ')
            if utilizar_opcao.lower() in 'simyes' and len(utilizar_opcao) > 0: 
                utilizar_frequencias_portugues = True 
            chave = atacar(mensagem)
            if chave: resultado = decriptar(mensagem, chave)

        filename = 'saida.txt'
        if len(resultado):
            f = open(filename, "w")
            f.write(resultado)
            f.close()

        print(f'Resultado salvo em {filename}')
        mostrar = input('Mostrar resultado [s/n]? ')
        if mostrar.lower() in 'simyes' and len(mostrar) > 0: print(resultado)
        input('Pressione para encerrar.')
    except:
        pass

if __name__ == '__main__':
    main()
