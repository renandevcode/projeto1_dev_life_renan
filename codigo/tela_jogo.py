from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto

from inicializacao import gera_posicao_desocupada,gera_objetos

def desenha_tela(janela, estado, altura_tela, largura_tela):
    # Utilize o dicionário estado para saber onde o jogador e os outros objetos estão.
    # Por exemplo, para saber a posição do jogador, use estado['pos_jogador']
    # O mapa esta armazenado em estado['mapa'].
    motor.preenche_fundo(janela, PRETO)
    inicio_altura_tela=(altura_tela-len(estado['mapa']))//2
    inicio_largura_tela=(largura_tela-len(estado['mapa'][0]))//2

    # O seu código deve desenhar a tela do jogo aqui a partir dos valores no dicionário "estado"
    # APAGUE ESTA LINHA E A LINHA ABAIXO E ESCREVA SEU CÓDIGO AQUI
    for y in range(inicio_altura_tela,len(estado['mapa'])+inicio_altura_tela):
        for x in range(inicio_largura_tela,len(estado['mapa'][0])+inicio_largura_tela):
            motor.desenha_string(janela,x,y,' ',VERDE_CLARO,VERDE_ESCURO)



    for objeto in estado['objetos']:
        motor.desenha_string(
            janela,
            objeto['posicao'][0] + inicio_largura_tela,
            objeto['posicao'][1] + inicio_altura_tela,
            objeto['tipo'],
            objeto['cor'],
            VERDE_CLARO
        )

    # Desenha o jogador 
    pos_jogador=estado['pos_jogador']
    motor.desenha_string(
        janela,
        pos_jogador[0] + inicio_largura_tela,
        pos_jogador[1] + inicio_altura_tela,
        JOGADOR,
        VERDE_CLARO,
        PRETO
    )
    # Desenha vidas 
    x_vidas =2
    y_vidas =1

    for i in range(estado['max_vidas']):
        if i < estado['vidas']:
            motor.desenha_string(janela, x_vidas+i, y_vidas, CORACAO, VERMELHO, VERMELHO)
        else:
            motor.desenha_string(janela, x_vidas+i, y_vidas, CORACAO, BRANCO, BRANCO)


def atualiza_estado(estado, tecla):
    # O dicionário "estado" é atualizado com base na tecla apertada pelo jogador

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO

    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR


    # Movimento do jogador, sendo limitado com base nas bordas do mapa
    elif tecla == motor.SETA_ESQUERDA :
        if estado['pos_jogador'][0]>0:
            estado['pos_jogador'][0]-=1
    elif tecla == motor.SETA_DIREITA :
        if estado['pos_jogador'][0]<len(estado['mapa'][0])-1:
            estado['pos_jogador'][0]+=1
    elif tecla == motor.SETA_BAIXO :
        if estado['pos_jogador'][1]<len(estado['mapa'])-1:
            estado['pos_jogador'][1]+=1
    elif tecla == motor.SETA_CIMA :
        if estado['pos_jogador'][1] > 0:
            estado['pos_jogador'][1] -= 1

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
    
    