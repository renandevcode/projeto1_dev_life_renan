from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto

from inicializacao import gera_posicao_desocupada,gera_objetos
from random import random,choice

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)

    altura_mapa=len(estado['mapa'])
    largura_mapa=len(estado['mapa'][0])
    pos_jogador=estado['pos_jogador']

    # Evitar o canto inferior direito (limitação do curses)
    largura_util = largura_tela - 1
    altura_util = altura_tela - 1


    # Define a centralização da tela com base no personagem
    inicio_largura_tela = largura_util // 2 - pos_jogador[0]
    inicio_altura_tela = altura_util // 2 - pos_jogador[1]

    if largura_mapa > largura_util:
        inicio_largura_tela = max(largura_util - largura_mapa, min(0, inicio_largura_tela))
    else:
        inicio_largura_tela = (largura_util - largura_mapa) // 2

    if altura_mapa > altura_util:
        inicio_altura_tela = max(altura_util - altura_mapa, min(0, inicio_altura_tela))
    else:
        inicio_altura_tela = (altura_util - altura_mapa) // 2


    for y in range(altura_mapa):
        for x in range(largura_mapa):
            tela_x = x + inicio_largura_tela
            tela_y = y + inicio_altura_tela
            if 0 <= tela_x < largura_util and 0 <= tela_y < altura_util:
                motor.desenha_string(janela, tela_x, tela_y, ' ', VERDE_CLARO, VERDE_ESCURO)

    for objeto in estado['objetos']:
        tela_x = objeto['posicao'][0] + inicio_largura_tela
        tela_y = objeto['posicao'][1] + inicio_altura_tela
        if 0 <= tela_x < largura_util and 0 <= tela_y < altura_util:
            motor.desenha_string(janela, tela_x, tela_y, objeto['tipo'], VERDE_CLARO, objeto['cor'])


    tela_x = pos_jogador[0] + inicio_largura_tela
    tela_y = pos_jogador[1] + inicio_altura_tela
    if 0 <= tela_x < largura_util and 0 <= tela_y < altura_util:
        motor.desenha_string(janela, tela_x, tela_y, JOGADOR, VERDE_CLARO, PRETO)


    # Desenha vidas 
    x_vidas =2
    y_vidas =1

    for i in range(estado['max_vidas']):
        if i < estado['vidas']:
            motor.desenha_string(janela, x_vidas+i, y_vidas, CORACAO, PRETO, VERMELHO)
        else:
            motor.desenha_string(janela, x_vidas+i, y_vidas, CORACAO, PRETO,BRANCO)

    if estado.get('mensagem'):
        x_mensagem = 2
        y_mensagem = 2
        motor.desenha_string(janela, x_mensagem, y_mensagem, estado['mensagem'], PRETO, AMARELO)

def atualiza_estado(estado, tecla):
    estado['mensagem'] = ''

    # Retém a posição jogador para atualizar ao fim do ciclo
    nova_pos=estado['pos_jogador'][:]

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO

    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR

    # Movimento do jogador, sendo limitado com base nas bordas do mapa
    elif tecla == motor.SETA_ESQUERDA :
        if estado['pos_jogador'][0]>0:
            nova_pos[0]-=1
    elif tecla == motor.SETA_DIREITA :
        if estado['pos_jogador'][0]<len(estado['mapa'][0])-1:
            nova_pos[0]+=1
    elif tecla == motor.SETA_BAIXO :
        if estado['pos_jogador'][1]<len(estado['mapa'])-1:
            nova_pos[1]+=1
    elif tecla == motor.SETA_CIMA :
        if estado['pos_jogador'][1] > 0:
            nova_pos[1] -= 1
    


    # Indica colisão com a parede 
    for objeto  in estado['objetos']:
        if objeto['posicao']== nova_pos and objeto['tipo'] == PAREDE:
            estado['mensagem'] = 'Há uma parede no caminho!'
            return


    monstro_alvo = None
    for objeto in estado['objetos']:
        if objeto['posicao'] == nova_pos and objeto['tipo'] == MONSTRO:
            monstro_alvo = objeto
            break

    if monstro_alvo is not None:
        # Sorteia quem ataca
        if random() < monstro_alvo['probabilidade_de_ataque']:
            # Monstro ataca o jogador
            estado['vidas'] -= 1
            estado['mensagem'] = 'O monstro te atacou! -1 vida'
            if estado['vidas'] <= 0:
                estado['mensagem'] = 'Você morreu!'
                estado['tela_atual'] = SAIR
        else:
            # Jogador ataca o monstro
            monstro_alvo['vida'] -= 1
            estado['mensagem'] = f'Você atacou o monstro! Vida do monstro: {monstro_alvo["vida"]}'
            
            if monstro_alvo['vida'] <= 0:
                # Monstro morre e remove e o jogador, ocupando sua posição
                estado['objetos'].remove(monstro_alvo)
                estado['pos_jogador'] = nova_pos
                estado['mensagem'] = 'Você derrotou o monstro!'
        return   # não continua o movimento normal

    estado['pos_jogador']=nova_pos

    # Revela a sala secreta quando o jogador se aproxima
    if estado.get('pos_sala_secreta') and not estado['sala_secreta_revelada']:
        px, py = estado['pos_jogador']
        sx, sy = estado['pos_sala_secreta']
        if abs(px - sx) + abs(py - sy) <= 1:
            estado['sala_secreta_revelada'] = True
            estado['mapa'][sy][sx] = ' '  # abre a passagem visualmente
            estado['mensagem'] = 'Você encontrou uma sala secreta!'
 
            # Recompensa: adiciona um item de valor dentro da sala
            posicoes_coracoes = [
                [sx - 2, sy + 2],
                [sx,     sy + 2],
                [sx + 2, sy + 2],
                [sx - 1, sy + 4],
                [sx + 1, sy + 4],
            ]
            
            for posicao in posicoes_coracoes:
                estado['objetos'].append({
                    'tipo': CORACAO,
                    'posicao': posicao,
                    'cor': VERMELHO,
                })
    
    # Vidas do jogador 

    pos_jogador = estado['pos_jogador']
    objetos_para_remover = []

    for objeto in estado['objetos']:
        if objeto['posicao'] == pos_jogador:   # jogador pisou no objeto
                
            if objeto['tipo'] == CORACAO:
                # Ganha vida (sem passar do máximo)
                if estado['vidas'] < estado['max_vidas']:
                    estado['vidas'] += 1
                    estado['mensagem'] = 'Você ganhou uma vida!'
                else:
                    estado['mensagem'] = 'Vidas já estão no máximo!'
                objetos_para_remover.append(objeto)

            elif objeto['tipo'] == ESPINHO:
                estado['vidas'] -= 1         # perde vida
                estado['mensagem'] = 'Você perdeu uma vida!'
                objetos_para_remover.append(objeto)

                # Se as vidas acabaram
                if estado['vidas'] <= 0:
                    estado['mensagem'] = 'Você morreu!'
                    estado['tela_atual'] = SAIR

    # Remove os objetos que o jogador pegou
    for objeto in objetos_para_remover:
        estado['objetos'].remove(objeto)

    # Movimentação aleatória dos monstros
    direcoes = [
        (-1, 0),  # esquerda
        (1, 0),   # direita
        (0, -1),  # cima
        (0, 1),   # baixo
        (0, 0),   # ficar parado
    ]

    for objeto in list(estado['objetos']):
        if objeto['tipo'] != MONSTRO:
            continue

        px, py = estado['pos_jogador']
        mx, my = objeto['posicao']
        distancia = abs(px - mx) + abs(py - my)

        if distancia == 1:
            # Monstro está colado no jogador: ataca direto, sem se mover
            if random() < objeto['probabilidade_de_ataque']:
                estado['vidas'] -= 1
                estado['mensagem'] = f'O monstro te atacou! Vida restante: {estado["vidas"]}'
                if estado['vidas'] <= 0:
                    estado['mensagem'] = 'Você morreu!'
                    estado['tela_atual'] = SAIR
            else:
                objeto['vida'] -= 1
                estado['mensagem'] = f'Você revidou! Vida do monstro: {objeto["vida"]}'
                if objeto['vida'] <= 0:
                    estado['objetos'].remove(objeto)
                    estado['mensagem'] = 'Você derrotou o monstro!'
            continue  # não se move nesse turno


        dx, dy = choice(direcoes)       # Sorteia uma nova direção
        nova_pos_monstro = [mx + dx, my + dy]  # Alterando posição

        # Verifica se a nova posição está dentro do mapa
        if not (0 <= nova_pos_monstro[0] < len(estado['mapa'][0]) and
                0 <= nova_pos_monstro[1] < len(estado['mapa'])):
            continue

        posicao_ocupada = any(o['posicao'] == nova_pos_monstro for o in estado['objetos'])
        if not posicao_ocupada:
            objeto['posicao'] = nova_pos_monstro

        