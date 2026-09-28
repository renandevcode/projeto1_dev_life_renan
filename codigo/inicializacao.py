from random import randint

from constantes import *  

def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):
    while True:
        x = randint(1, largura_mapa-2)
        y = randint(1, altura_mapa-2)
        posicao = [x, y]
        if posicao not in posicoes_ocupadas:
            break
    posicoes_ocupadas.append(posicao)

    return posicao


def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas):
    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        objetos.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
        })

    return objetos

# Essa função seŕa responsável por carregar o arquivo mapa.txt e adionar as posições  aos seus respectivos TIPOS
def carrega_mapa_de_arquivo(caminho_arquivo, posicoes_ocupadas):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.read().splitlines()

    mapa=[]
    paredes=[]
    portas=[]
    pos_sala_secreta = None
    pos_chefao = None

    for y,linha in enumerate(linhas):
        linha_mapa=[]
        for x, caractere in enumerate(linha):
            # "#" no arquivo mapa.txt será preenchido com emoji de parede
            # "S" será a entrada da sala secreta
            # "B" posição chefão
            # "D" posição da porta da sala trancada 
            if caractere == '#':
                paredes.append({
                    'tipo': PAREDE,
                    'posicao': [x, y],
                    'cor': MARROM_ESCURO,
                })
                posicoes_ocupadas.append([x, y])
            elif caractere == 'S':
                pos_sala_secreta = [x,y]
            elif caractere == 'B':
                pos_chefao = [x, y]
            elif caractere == 'D':
                portas.append({
                    'tipo': PORTA,
                    'posicao': [x, y],
                    'cor': MARROM_ESCURO,
                    'trancada': True,
                })
                posicoes_ocupadas.append([x, y])
            linha_mapa.append(' ') 
        mapa.append(linha_mapa)

    return mapa, paredes, portas, pos_sala_secreta, pos_chefao


def inicializa_estado():
    posicoes_ocupadas=[]

    mapa, paredes, portas, pos_sala_secreta, pos_chefao = carrega_mapa_de_arquivo('mapa.txt', posicoes_ocupadas)

    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)

    # Adiciona jogador ao meio do mapa e insere essa posição nas ocupadas
    pos_jogador = [largura_mapa//2, altura_mapa//2]  
    posicoes_ocupadas.append(pos_jogador)

    # Adiciona  elementos ao mapa 
    objetos = list(paredes)
    objetos += list(portas)
    objetos += gera_objetos(50, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(30, ESPINHO, AMARELO, largura_mapa, altura_mapa, posicoes_ocupadas) 
    monstros = gera_objetos(20, MONSTRO, ROXO, largura_mapa, altura_mapa, posicoes_ocupadas)
    
    for monstro in monstros:
        monstro['vida'] = 3         # cada monstro começa com 3 de vida
        monstro['probabilidade_de_ataque'] = 0.4        # 40%  de chance

    objetos+=monstros

    # Verifica a posição "B" no mapa.txt para adicioná-la
    if pos_chefao:
        chefao = {
            'tipo': MONSTRO,
            'posicao': pos_chefao,
            'cor': ROXO,
            'vida': 10,
            'probabilidade_de_ataque': 0.5,
            'eh_chefao': True,
        }
        objetos.append(chefao)

    return {
        'tela_atual': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'mensagem': '',  # Mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'pos_sala_secreta': pos_sala_secreta,
        'pos_chefao': pos_chefao,
        'sala_secreta_revelada': False,
        'inventario':[]
    }
