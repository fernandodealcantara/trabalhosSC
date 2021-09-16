from random import randint # usado apenas para gerar chave de 16 bytes com valores aleatorios entre 0x0 e 0xFF
from hashlib import sha1 # usado apenas para gerar o hash
from PIL import Image # usado para tratar imagem .bmp
from os import system, name # limpar terminal

################################################################################################
# TABELAS S_BOX, SBOX_INVERSA E RCON
# tabela de subtituicao com todas as combinacoes de 0 a 255 util para geracao de subchaves e aes
s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
# tabela inversa de subtituicao com todas as combinacoes de 0 a 255 util para aes
s_box_inversa = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)
# tabela rcon util para gerar subchaves
r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 
    0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 
    0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 
    0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 
    0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 
    0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 
    0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 
    0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 
    0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 
    0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d
)
################################################################################################
################################################################################################
# FUNCOES UTEIS TANTO PARA GERAR CHAVES, AES E MODOS DE OPERACAO
# funcao para imprimir valores no formato hexadecimal -> usada para debug
hexValues = lambda mensagem: [hex(m) for m in mensagem]
# funcao que rotaciona a palavra n vezes
rotacionar = lambda palavra, n: palavra[n:] + palavra[0:n]
# funcao que efetua um xor entre cada byte da palavra com a tabela de round constants aka  r_con
palavra_xor_rcon = lambda palavra, pos: [palavra[0] ^ r_con[pos%len(r_con)]] + palavra[1:]
# funcao que efetua xor entre duas palavras
palavra_xor_outra_palavra = lambda palavra, outra_palavra: [i^j for i, j in zip(palavra, outra_palavra)]
# funcao que nivela uma lista que tem sublista exemplo uma lista [[1], [2]] vira [1, 2]
flatten = lambda lista: [item for sublista in lista for item in sublista]
# transpõe a matriz (é uma lista só que referenciada aqui como matriz)
pegar_matriz_transposta = lambda matriz: flatten([[matriz[(4*j)+i] for j in range(4)] for i in range(4)])
################################################################################################
# FUNCOES AES E DE MODOS DE OPERACAO
# seleciona as 4 subchaves da rodada (pega 4 subchaves de 4 bytes e concatena em uma de 16 bytes)
pegar_chave_da_rodada = lambda subchaves, rodada: pegar_matriz_transposta(flatten(subchaves[rodada*4:(rodada*4)+4]))
# funcao que adiciona a chave para o estado (em aes, adicao eh sempre a operacao xor)
add_round_key = lambda estado, chave_da_rodada: [estado[i] ^ chave_da_rodada[i] for i in range(16)]
# funcao que substitui os valores do estado utilizando a tabela de substituicao s_box
sub_bytes = lambda palavra: [s_box[pos] for pos in palavra]
# funcao que substitui os valores do estado utilizando a tabela de substituicao inversa
sub_bytes_inversa = lambda estado: [s_box_inversa[pos] for pos in estado]
# funcao que rotaciona as linhas da matriz de estado
shift_rows = lambda estado: flatten([rotacionar(estado[i*4:(i*4)+4], i) for i in range(4)])
# funcao que rotaciona as linhas da matriz de estado inversamente a funcao shift_rows 
shift_rows_inverso = lambda estado: flatten([rotacionar(estado[i*4:(i*4)+4], -i) for i in range(4)])

# funcao que realiza a operacao de multiplicacao -> galois multiplication
def gm(a, b):
    p = 0
    hiBitSet = 0

    for _ in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1

    return p % 256

# funcao que incrementa um array de bytes -> utilizada no modo ctr
def incrementar(contador):
    for i in reversed(range(len(contador))):
        if contador[i] == 0xFF:
            contador[i] = 0
        else:
            contador[i] += 1
            break
        
    return contador

# funcao responsavel por gerar as subchaves que serao utilizadas pelo aes passo -> add_round_key().
def gerar_subchaves(chave128bits, rodadas=10):
    palavras_geradas_por_passo = 4
    subchaves = [chave128bits[i:i+4] for i in range(0, 16, 4)]

    for i in range(4, (4*rodadas)+4):
        if i % 4 == 0:
            nova_palavra = rotacionar(subchaves[i-1], 1)
            nova_palavra = sub_bytes(nova_palavra) # aka sub_bytes
            nova_palavra = palavra_xor_rcon(nova_palavra, i//4)
        nova_palavra = palavra_xor_outra_palavra(nova_palavra, subchaves[i-palavras_geradas_por_passo])
        subchaves.append(nova_palavra)

    return subchaves

# funcao que cria uma nova coluna dependendo do valor de vm 'valores da matriz'
# se vm = [1, 1, 2, 3] (gera matriz normal) realiza a operacao mix column normal
# se vm = [0x09, 0x0d, 0x0e, 0x0b] (gera matriz inversa) realiza a operacao mix column inversa
def mix_column(coluna, vm):
    nova_coluna = [0] * 4
    nova_coluna[0] = gm(coluna[0], vm[2]) ^ gm(coluna[1], vm[3]) ^ gm(coluna[2], vm[1]) ^ gm(coluna[3], vm[0])
    nova_coluna[1] = gm(coluna[0], vm[0]) ^ gm(coluna[1], vm[2]) ^ gm(coluna[2], vm[3]) ^ gm(coluna[3], vm[1])
    nova_coluna[2] = gm(coluna[0], vm[1]) ^ gm(coluna[1], vm[0]) ^ gm(coluna[2], vm[2]) ^ gm(coluna[3], vm[3])
    nova_coluna[3] = gm(coluna[0], vm[3]) ^ gm(coluna[1], vm[1]) ^ gm(coluna[2], vm[0]) ^ gm(coluna[3], vm[2])
    return nova_coluna

# funcao que embaralha a matriz de estado
def mix_columns(estado, valores_matriz):
    novo_estado = pegar_matriz_transposta(estado) # transpor facilita as outras operacoes

    for i in range(4):
        novo_estado[i*4:(i*4)+4] = mix_column(novo_estado[i*4:(i*4)+4], valores_matriz)

    return pegar_matriz_transposta(novo_estado) # transpõe novamente para voltar ao normal

# funcao aes que executa o processo cifrar
def aes_cifrar(mensagem, subchaves, rodadas):
    valores_para_gerar_matriz_para_mix_columns = [1, 1, 2, 3]
    estado = mensagem

    chave_da_rodada = pegar_chave_da_rodada(subchaves, 0)
    estado = add_round_key(estado, chave_da_rodada)

    for rodada in range(1, rodadas):
        estado = sub_bytes(estado)
        estado = shift_rows(estado)
        estado = mix_columns(estado, valores_para_gerar_matriz_para_mix_columns)
        chave_da_rodada = pegar_chave_da_rodada(subchaves, rodada)
        estado = add_round_key(estado, chave_da_rodada)
 
    estado = sub_bytes(estado)
    estado = shift_rows(estado)
    chave_da_rodada = pegar_chave_da_rodada(subchaves, rodadas)
    estado = add_round_key(estado, chave_da_rodada)

    return estado

# funcao aes que executa o processo decifrar
def aes_decifrar(mensagem, subchaves, rodadas):
    valores_para_gerar_matriz_para_mix_columns_inversa = [0x09, 0x0d, 0x0e, 0x0b]
    estado = mensagem

    chave_da_rodada = pegar_chave_da_rodada(subchaves, rodadas)
    estado = add_round_key(estado, chave_da_rodada)
    estado = shift_rows_inverso(estado)
    estado = sub_bytes_inversa(estado)

    for rodada in range(rodadas-1, 0, -1):
        chave_da_rodada = pegar_chave_da_rodada(subchaves, rodada)
        estado = add_round_key(estado, chave_da_rodada)
        estado = mix_columns(estado, valores_para_gerar_matriz_para_mix_columns_inversa)
        estado = shift_rows_inverso(estado)
        estado = sub_bytes_inversa(estado)

    chave_da_rodada = pegar_chave_da_rodada(subchaves, 0)
    estado = add_round_key(estado, chave_da_rodada)

    return estado

# funcao que realiza o modo ecb - electronic codebook
def ecb(chave, blocos, rodadas, modo):
    subchaves = gerar_subchaves(chave, rodadas)

    blocos_gerados = []
    for bloco in blocos:
        bloco = pegar_matriz_transposta(bloco)
        if modo == 'cifrar':
            novo_bloco = pegar_matriz_transposta(aes_cifrar(bloco, subchaves, rodadas))
        elif modo == 'decifrar':
            novo_bloco = pegar_matriz_transposta(aes_decifrar(bloco, subchaves, rodadas))
        blocos_gerados.append(novo_bloco)

    return blocos_gerados # retorna os blocos cifrados ou decifrados, depende do valor de modo = cifrar | decifrar

# funcao que realiza o modo ctr - counter
def ctr(chave, blocos, rodadas):
    subchaves = gerar_subchaves(chave, rodadas)
    contador = [0x0] * 16
    
    blocos_gerados = []
    for bloco in blocos:
        res = pegar_matriz_transposta(aes_cifrar(pegar_matriz_transposta(contador.copy()), subchaves, rodadas))
        novo_bloco = palavra_xor_outra_palavra(res, bloco)
        blocos_gerados.append(novo_bloco)
        contador = incrementar(contador.copy())

    return blocos_gerados # 

# funcao pega os bytes de image data entre os marcadores de start of scan 0xffda e o de final do arquivo 0xffd9
# e transforma em blocos de 16 bytes (que serao usados no aes)
# retorna um dict com os blocos e informacoes do marcador start of scan
def criar_blocos_jpg(lista_de_bytes):
    sos_marker = {}

    for i in range(len(lista_de_bytes)-1):
        if lista_de_bytes[i] == 0xff and lista_de_bytes[i+1] == 0xda:
            sos_marker['começo'] = i+1 
            sos_marker['tamanho'] = (lista_de_bytes[i+2]*256) + lista_de_bytes[i+3]
            break # consideramos apenas o primeiro marcador sos encontrado

    inicio_dados_bloco = sos_marker['começo'] + sos_marker['tamanho'] + 1
    fim_dados_bloco = -2 # em um arquivo jpg normal, os 2 ultimos bytes são ff d9 que indicam o fim do jpg
    image_data = lista_de_bytes[inicio_dados_bloco:fim_dados_bloco]

    for i in range(0, len(image_data)-1):
        if image_data[i] == 0xff and image_data[i+1] == 0x00:
            image_data[i+1] = None

    image_data = [value for value in image_data if value != None] # retira o valor 0x0 que acompanha o ff -> 0xff 0x0 == 0xff em jpg

    blocos = []
    for i in range(0, len(image_data), 16):
        novo_bloco = image_data[i:i+16]
        if len(novo_bloco) < 16:
            preencher_restante = [0x0] * (16-len(novo_bloco)) # padding
            novo_bloco += preencher_restante
        blocos.append(novo_bloco.copy())
    sos_marker['blocos'] = blocos.copy()

    return sos_marker

# adiciona o valor 0x0 para os bytes com valor 0xff novamente 0xff -> 0xff 0x0
def substituir_bytes_jpg(parte_modificada):
    copia_parte_modificada = parte_modificada.copy()
    i = 0
    while (True):
        if copia_parte_modificada[i] == 0xff:
            copia_parte_modificada.insert(i+1, 0x0)
        i += 1
        if i >= len(copia_parte_modificada):
            break

    return copia_parte_modificada

def criar_blocos_bmp(imgname):
    img = Image.open(imgname)
    imgInBytes = list(img.tobytes())
    blocos = []
    resto = []
    for i in range(0, len(imgInBytes), 16):
        novo_bloco = imgInBytes[i:i+16]
        if len(novo_bloco) < 16:
            resto = novo_bloco
            break
        blocos.append(novo_bloco.copy())
    return (blocos, resto, img.size)

def montar_imagem(img, resto, tam, name):
    d = img + resto
    d = bytes(d)
    im = Image.frombytes(mode = "RGB", size = tam, data= d)
    im.show()
    im.save(name + '.bmp')
    return d

def main():
    try:      
        while (True):
            opcao = input('Modo de execucao\n1 - para cifrar\n2 - para decifrar\nOpcao: ')
            modo = input('Modo de operacao\n1 - ecb\n2 - ctr\nOpcao: ')

            if opcao not in ['1', '2'] or modo not in ['1', '2']:
                print('Opcao ou modo invalido.')
                continue

            nome_imagem_entrada = str(input('Insira o nome da imagem com extensao[.bmp ou .jpg] em que sera aplicado o algoritmo: '))
            rodadas = int(input('Quantidade de rodadas: '))
            chave = input('Informe a chave (16 bytes separados por espaço) ou gere automaticamente (pressione enter): ').split()
            
            if not rodadas > 0 and not rodadas < 250:
                print('Excedeu o valor de rodada maximo (250)')
                continue

            if '.jpg' in nome_imagem_entrada:
                with open(nome_imagem_entrada, mode='rb') as original_file:
                    original_image = list(original_file.read())
                # dict sos marker que contem blocos a ser cifrados, inicio do marcador e tamanho do marcador -> jpg
                sos_marker_info = criar_blocos_jpg(original_image.copy()) 
                # cabecalho da nova imagem 
                nova_imagem = original_image.copy()[0:sos_marker_info['começo'] + sos_marker_info['tamanho'] + 1]
                blocos = sos_marker_info['blocos'].copy() # blocos de 16 bytes jpg

            elif '.bmp' in nome_imagem_entrada:
                blocos, resto, size = criar_blocos_bmp(nome_imagem_entrada)
            else:
                print('Extensão da imagem não identificada.')
                continue

            if len(chave) == 16:
                chave = [int(value, 16) for value in chave]
            else:
                chave = [randint(0, 255) for _ in range(16)]

            print('Chave:', *hexValues(chave))
            print('Realizando operações. Aguarde.')

            nome_imagem_saida = nome_imagem_entrada[0:-4] + '-'
            if opcao == '1': nome_imagem_saida += 'cifrar-'
            else: nome_imagem_saida += 'decifrar-'
            if modo == '1': nome_imagem_saida += 'ecb-'
            else: nome_imagem_saida += 'ctr-'
            nome_imagem_saida += str(rodadas)

            blocos_gerados = [] # blocos modificados
            if opcao == '1': # cifrar
                if modo == '1':
                    blocos_gerados = ecb(chave, blocos, rodadas, 'cifrar')
                elif modo == '2':
                    blocos_gerados = ctr(chave, blocos, rodadas)
            elif opcao == '2': # decifrar
                if modo == '1':
                    blocos_gerados = ecb(chave, blocos, rodadas, 'decifrar')
                elif modo == '2':
                    blocos_gerados = ctr(chave, blocos, rodadas)

            bloco_unico = flatten(blocos_gerados) # junta todos os blocos de 16 bytes modificados em apenas uma

            if '.jpg' in nome_imagem_entrada:
                nova_imagem += substituir_bytes_jpg(bloco_unico) # montando jpg
                nova_imagem += [0xff, 0xd9] # adiciona o marcador do final da imagem
                out_file_image = open(f'{nome_imagem_saida}.jpg', mode='wb') # salvando jpg
                out_file_image.write(bytes(nova_imagem))
                out_file_image.close()
            else:
                nova_imagem = montar_imagem(bloco_unico, resto, size, nome_imagem_saida)

            result_hash = sha1(bytes(nova_imagem)).hexdigest()
            
            out_file_infos_execution = open(f'chave e hash.txt', mode='w') # salvando hash em txt
            out_file_infos_execution.write('Chave:' + ' '.join(hexValues(chave)) + '\n') # chave
            out_file_infos_execution.write('Hash:' + result_hash) # hash
            out_file_infos_execution.close()

            print('Chave e hash salvos em: chave e hash.txt ')
            print(f'Imagem resultante salva em: {nome_imagem_saida}')
            print("O hash hexadecimal gerado:", result_hash)
            print('Finalizado!')
            break
    except:
        print('Algo deu errado!')

if __name__ == '__main__':
    while (True):
        main()
        continuar = input('Continuar execução [s/n]?')
        if continuar not in 'sim':
            break
        system('cls' if name == 'nt' else 'clear')