# modulo main.py

import turtle
import pygame
from menu import draw_menu, handle_click  # Importa as funções do menu
from game import Game  # Importa a classe Game diretamente aqui

# Inicializar pygame para som
pygame.mixer.init()

# Sons de fundo
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Função para voltar ao menu inicial
def return_to_menu():
    thumbnails, menu_turtle, ranking_text_turtle, screen = draw_menu()
    screen.onscreenclick(lambda x, y: handle_click(x, y, thumbnails, menu_turtle, ranking_text_turtle, Game))

# Desenhar o menu com miniaturas e capturar os eventos de clique
return_to_menu()

# Manter a tela aberta
turtle.mainloop()





























