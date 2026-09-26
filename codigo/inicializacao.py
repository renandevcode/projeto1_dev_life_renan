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


def carrega_mapa_de_arquivo(caminho_arquivo, posicoes_ocupadas):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.read().splitlines()


    mapa=[]
    paredes=[]

    for y,linha in enumerate(linhas):
        linha_mapa=[]
        for x, caractere in enumerate(linha):
            if caractere == '#':
                paredes.append({
                    'tipo': PAREDE,
                    'posicao': [x, y],
                    'cor': MARROM_ESCURO,
                })
                posicoes_ocupadas.append([x, y])
            linha_mapa.append(' ')  # o mapa em si continua sendo só espaços
        mapa.append(linha_mapa)

    return mapa, paredes


def inicializa_estado():
    posicoes_ocupadas=[]

    mapa, paredes=carrega_mapa_de_arquivo('mapa.txt',posicoes_ocupadas)

    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    
    # Cria outros objetos do mapa
    posicoes_ocupadas.append(pos_jogador)

    objetos = list(paredes)
    objetos += gera_objetos(8, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(6, ESPINHO, AMARELO, largura_mapa, altura_mapa, posicoes_ocupadas)  # ← mudou para AMARELO
    objetos += gera_objetos(12, PAREDE, MARROM_ESCURO, largura_mapa, altura_mapa, posicoes_ocupadas)
    monstros = gera_objetos(4, MONSTRO, ROXO, largura_mapa, altura_mapa, posicoes_ocupadas)
    
    for monstro in monstros:
        monstro['vida'] = 3                    # cada monstro começa com 3 de vida
        monstro['probabilidade_de_ataque'] = 0.4   # 40%  de chance

    objetos+=monstros

    return {
        'tela_atual': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'mensagem': '',  # Mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
    }
