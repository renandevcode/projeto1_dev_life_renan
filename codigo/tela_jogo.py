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
    inicio_altura_tela=int((altura_tela-len(estado['mapa']))/2)
    inicio_largura_tela=int((largura_tela-len(estado['mapa'][0]))/2)

    # O seu código deve desenhar a tela do jogo aqui a partir dos valores no dicionário "estado"
    # APAGUE ESTA LINHA E A LINHA ABAIXO E ESCREVA SEU CÓDIGO AQUI
    for y in range(inicio_altura_tela,len(estado['mapa'])+inicio_altura_tela):
        for x in range(inicio_largura_tela,len(estado['mapa'][0])+inicio_largura_tela):
            motor.desenha_string(janela,x,y,' ',VERDE_CLARO,VERDE_ESCURO)



    for objeto in estado['objetos']:
        motor.desenha_string(janela,objeto['posicao'][0]+inicio_largura_tela,objeto['posicao'][1]+inicio_altura_tela,objeto['tipo'],objeto['cor'],VERDE_CLARO)


    pos_jogador=estado['pos_jogador']
    motor.desenha_string(janela,(pos_jogador[0]+inicio_largura_tela),(pos_jogador[1]+inicio_altura_tela),JOGADOR,VERDE_CLARO,PRETO)
        


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR
    elif tecla == motor.SETA_ESQUERDA :
            estado['pos_jogador'][0]-=1
    elif tecla == motor.SETA_DIREITA :
                estado['pos_jogador'][0]+=1
    elif tecla == motor.SETA_BAIXO :
                estado['pos_jogador'][1]+=1
    elif tecla == motor.SETA_CIMA :
                estado['pos_jogador'][1]-=1
    
    