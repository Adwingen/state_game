# map.py

from PIL import Image
import turtle
import os
import pandas as pd
from state import State

class Map:
    def __init__(self, image, states_file):
        self.image = image
        self.states_file = states_file  # Armazena o caminho do arquivo CSV
        # Garantir que o arquivo CSV seja lido corretamente com codificação UTF-8
        self.states_data = pd.read_csv(states_file, encoding="utf-8")
        self.states = [State(row['state'], row['x'], row['y']) for index, row in self.states_data.iterrows()]

    def setup_screen(self):
        screen = turtle.Screen()

        # Definir um tamanho fixo da tela (por exemplo, 1024x768) para deixar espaço para jogabilidade
        screen.setup(width=1024, height=768)

        # Obter o tamanho da imagem original
        img = Image.open(self.image)
        original_width, original_height = img.size

        # Definir a área do mapa na janela (exemplo: 800x600, deixando espaço para os elementos)
        map_width = 800
        map_height = 600

        # Redimensionar a imagem do mapa para caber nessa área
        img_resized = img.resize((map_width, map_height))

        # Salvar a imagem redimensionada temporariamente
        resized_image_path = os.path.splitext(self.image)[0] + "_resized.gif"
        img_resized.save(resized_image_path)

        # Usar a imagem redimensionada no Turtle
        screen.addshape(resized_image_path)
        turtle.shape(resized_image_path)
        turtle.penup()

        # Definir o fundo da tela para a imagem redimensionada
        screen.bgpic(resized_image_path)

        # Adicionar o detetor de clique para obter coordenadas do mouse
        def get_mouse_on_click(x, y):
            print(f"Coordenadas do clique: {x}, {y}")

        screen.onscreenclick(get_mouse_on_click)

        return screen

    def get_state_by_name(self, state_name):
        # Certificar que a comparação está em title case
        for state in self.states:
            if state.name.title() == state_name.title():
                return state
        return None

    def display_state(self, state_name):
        """Exibe o nome do estado no mapa nas coordenadas corretas."""
        # Obtenha as coordenadas do estado a partir do CSV
        state = self.get_state_by_name(state_name)
        if state:
            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            t.goto(state.x, state.y)
            t.write(state.name, align="center", font=("Arial", 10, "normal"))





