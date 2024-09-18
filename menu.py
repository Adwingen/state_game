# menu.py

import turtle
from ranking import get_top_ranking

# Dicionário de mapas disponíveis, incluindo as miniaturas
available_maps = {
    "USA": {"image": "usa_map.gif", "states_file": "usa_states.csv", "thumbnail": "usa_thumbnail.gif"},
    "Portugal": {"image": "portugal_map.gif", "states_file": "portugal_regions.csv", "thumbnail": "portugal_thumbnail"
                                                                                                  ".gif"}
}

# Função para desenhar o menu com miniaturas dos mapas e o texto de ranking
def draw_menu():
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("lightblue")

    # Adicionar as miniaturas ao turtle screen
    for map_data in available_maps.values():
        screen.addshape(map_data["thumbnail"])

    # Criar uma tartaruga para desenhar o título
    menu_turtle = turtle.Turtle()
    menu_turtle.hideturtle()
    menu_turtle.penup()
    menu_turtle.goto(0, 200)
    menu_turtle.write("Selecione um mapa", align="center", font=("Arial", 24, "bold"))

    # Definir as posições para as miniaturas dos mapas
    positions = [(0, 100), (0, -100)]
    thumbnails = []
    map_names = list(available_maps.keys())

    # Colocar as miniaturas na tela
    for i, map_name in enumerate(map_names):
        thumbnail_turtle = turtle.Turtle()
        thumbnail_turtle.shape(available_maps[map_name]["thumbnail"])
        thumbnail_turtle.penup()
        thumbnail_turtle.goto(positions[i])
        thumbnails.append((thumbnail_turtle, map_name))

    # Adicionar texto para ver o ranking
    ranking_text_turtle = turtle.Turtle()
    ranking_text_turtle.hideturtle()
    ranking_text_turtle.penup()
    ranking_text_turtle.goto(0, -250)
    ranking_text_turtle.write("Ver Ranking", align="center", font=("Arial", 18, "bold"))

    return thumbnails, menu_turtle, ranking_text_turtle, screen

# Função para lidar com o clique nas miniaturas ou no texto de ranking
def handle_click(x, y, thumbnails, menu_turtle, ranking_text_turtle, game_class):
    for thumbnail, map_name in thumbnails:
        if thumbnail.distance(x, y) < 50:
            selected_map = available_maps[map_name]
            hide_menu(menu_turtle, thumbnails, ranking_text_turtle)  # Esconder o menu
            # Iniciar o jogo com o mapa selecionado
            game = game_class(map_image=selected_map["image"], states_file=selected_map["states_file"])
            game.start()

    # Verificar se o botão de ranking foi clicado
    if -60 < x < 60 and -270 < y < -230:
        show_ranking()  # Chama a função para exibir o ranking


# Função para esconder o menu ao clicar em uma miniatura
def hide_menu(menu_turtle, thumbnails, ranking_text_turtle):
    menu_turtle.clear()  # Limpar o texto "Selecione um Mapa"
    for thumbnail, _ in thumbnails:
        thumbnail.hideturtle()  # Esconder todas as miniaturas
    ranking_text_turtle.clear()  # Esconder o texto de ranking



# Função para exibir o ranking
def show_ranking():
    top_ranking = get_top_ranking()

    if not top_ranking:  # Se o ranking estiver vazio
        ranking_message = "Sem dados de ranking disponíveis!"
    else:
        ranking_message = "Ranking:\n"
        for idx, entry in enumerate(top_ranking, start=1):
            ranking_message += f"{idx}. {entry['Nome']} - {entry['Pontuação']} ({entry['Mapa']})\n"

    # Exibir o ranking na tela
    ranking_turtle = turtle.Turtle()
    ranking_turtle.hideturtle()
    ranking_turtle.penup()
    ranking_turtle.goto(y=-200, x=-300)
    ranking_turtle.write(ranking_message, align="left", font=("Arial", 14, "bold"))

    # Espera 5 segundos e limpa o ranking da tela
    turtle.ontimer(ranking_turtle.clear, 5000)


