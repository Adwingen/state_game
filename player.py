# player.py

from turtle import Turtle

# Classe que gerencia o jogador, o input e o score
class Player:
    def __init__(self, total_states):
        self.score = 0
        self.current_input = ""
        self.guessed_states = []
        self.input_turtle = Turtle()
        self.input_turtle.hideturtle()
        self.input_turtle.penup()
        self.input_turtle.goto(0, -280)  # Posiciona o input na parte inferior da tela

        # Tartaruga para exibir o score
        self.score_turtle = Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.goto(-200, 260)  # Posiciona o score no topo esquerdo

        # Armazena o número total de estados
        self.total_states = total_states

    def update_input(self, key):
        """Atualiza o input do jogador com base nas teclas pressionadas."""
        if key == "BackSpace":
            self.current_input = self.current_input[:-1]
        elif key == "Return":  # Ao pressionar Enter, retorna o input atual
            return self.current_input
        elif len(key) == 1:
            self.current_input += key

        self.display_input()  # Exibir o input atualizado na tela
        return None

    def display_input(self):
        """Exibe o input atual do jogador."""
        self.input_turtle.clear()
        self.input_turtle.write(f"Input: {self.current_input}", align="center", font=("Arial", 16, "normal"))

    def reset_input(self):
        """Reseta o input após a submissão."""
        self.current_input = ""
        self.input_turtle.clear()

    def add_guessed_state(self, state_name):
        """Adiciona um estado acertado e atualiza o score."""
        self.guessed_states.append(state_name)
        self.score += 10

    def penalize(self):
        """Penaliza o jogador por um input incorreto."""
        self.score -= 5

    def update_score_display(self):
        """Atualiza o score exibido na tela."""
        self.score_turtle.clear()
        # Mostra o número de estados adivinhados versus o total
        self.score_turtle.write(f"Score: {self.score} Guess: {len(self.guessed_states)}/{self.total_states}",
                                align="center", font=("Arial", 16, "normal"))

