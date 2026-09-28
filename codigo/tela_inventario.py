from constantes import *
import motor_grafico as motor

# Função responsável pela tela de inventário 
def desenha_tela(janela, estado, altura, largura):
    motor.preenche_fundo(janela, PRETO)
    motor.desenha_string(janela, 2, 1, 'INVENTARIO', BRANCO, PRETO)
    inventario = estado.get('inventario', [])
    
    if not inventario:
        motor.desenha_string(janela, 2, 3, 'Vazio...', CINZA, PRETO)
    # Preenche inventário com oos  emojis dos respectivos  itens
    else:
        for i, item in enumerate(inventario):
            motor.desenha_string(
                janela, 2, 3 + i,
                f"{item['tipo']}  ({item['tipo']})",
                CINZA, item['cor'])
    
    motor.desenha_string(janela, 2, altura - 2, "Pressione 'i' ou ESC para voltar", CINZA, PRETO)

def atualiza_estado(estado, tecla_apertada):
    if tecla_apertada == 'i':
        estado['tela_atual'] = TELA_JOGO
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR