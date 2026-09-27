<div align="center">

# 🕹️ 404: Vida Não Encontrada

**Um roguelike de terminal sobre sobreviver aos bugs da vida de desenvolvedor**

![Python](https://img.shields.io/badge/Python-3-14151a?style=for-the-badge&logo=python&logoColor=3776AB)
![Terminal](https://img.shields.io/badge/Interface-Terminal-14151a?style=for-the-badge&logo=gnometerminal&logoColor=2E8B57)
![Roguelike](https://img.shields.io/badge/Gênero-Roguelike-14151a?style=for-the-badge&logo=gamejolt&logoColor=8A2BE2)
![Insper](https://img.shields.io/badge/Insper-Developer%20Life-14151a?style=for-the-badge&logo=googlescholar&logoColor=FF6B00)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-14151a?style=for-the-badge&logo=progress&logoColor=FFD500)
</div>

---

## 📖 Sobre o projeto

Este é um jogo [**roguelike**](https://pt.wikipedia.org/wiki/Roguelike) desenvolvido por **Renan Ramos** como projeto individual na disciplina *Developer Life*, do primeiro semestre do curso de Ciência da Computação do Insper.

O jogo foi construído em **Python**, utilizando o módulo [`curses`](https://docs.python.org/3/library/curses.html) para renderizar toda a interface gráfica diretamente no terminal.

## 🎮 Descrição do jogo

Você controla um personagem explorando um calabouço gerado a partir de um mapa em arquivo. Pelo caminho, é preciso enfrentar monstros, desviar de armadilhas, coletar itens e, no fim, encarar o chefão da masmorra.

Como todo bom roguelike, o jogo traz:

- 💀 **Morte permanente** (*permadeath*) — sem checkpoints, sem segunda chance
- ⚔️ **Combate por turnos** contra diferentes tipos de inimigos
- 🗺️ **Mapa maior que a tela**, com câmera centralizada no personagem
- 🎒 **Sistema de itens e inventário**
- 🚪 **Salas secretas** escondidas pelo mapa
- 👹 **Um chefão** te esperando no fim da jornada

## ⌨️ Como jogar

Pré-requisito: ter o **Python 3** instalado na máquina.

> No Windows, siga primeiro o [guia abaixo](#-jogando-no-windows) antes de continuar.

Clone este repositório e execute o arquivo `jogo.py`, dentro da pasta `codigo`:

```bash
python3 jogo.py
```

O jogo abre em uma janela de terminal e é controlado assim:

| Tecla | Ação |
|---|---|
| ⬆️⬇️⬅️➡️ | Mover o personagem |
| `i` | Abrir/fechar inventário |
| `esc` | Fechar o jogo |

## 🪟 Jogando no Windows

O módulo `curses` não funciona corretamente no prompt de comando padrão do Windows. Por isso:

1. Instale o **Windows Terminal** seguindo [este guia oficial](https://learn.microsoft.com/pt-br/windows/terminal/install)
2. Instale o módulo `windows-curses` via pip:

```bash
pip install windows-curses
```

Pronto! Agora é só seguir os passos da seção [Como jogar](#️-como-jogar).

## 🔗 Outros links

- 📋 [Enunciado do projeto](docs/enunciado.md)
- ✅ [Funcionalidades implementadas](docs/funcionalidades-implementadas.md)
- 📚 [Documentação das funções do motor gráfico](codigo/motor_grafico/README.md)

---

