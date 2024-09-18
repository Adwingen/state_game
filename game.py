# game.py

import turtle
from player import Player
from map import Map
import pygame
import random
import os
from ranking import save_ranking

# Inicializar pygame para som
pygame.mixer.init()

# Sons
correct_sound = pygame.mixer.Sound("correct_answer.mp3")
incorrect_sound = pygame.mixer.Sound("wrong_answer.mp3")
start_sound = pygame.mixer.Sound("game_bonus.mp3")
end_sound = pygame.mixer.Sound("yaaas.mp3")
warning_sound = pygame.mixer.Sound("game_countdown.mp3")
success_sound = pygame.mixer.Sound("mission_success.mp3")

class Game:
    def __init__(self, map_image, states_file):
        self.map = Map(map_image, states_file)
        total_states = len(self.map.states_data)

        self.player_name = turtle.textinput("Jogador", "Digite seu nome:")
        self.player = Player(total_states)
        self.screen = self.map.setup_screen()
        self.paused = False
        self.time_limit = 300
        self.total_states = total_states
        self.map_name = os.path.basename(map_image).split('_')[0]

        self.hint_count = 0
        self.max_hints = 10

        self.screen.addshape("lamp_thumbnail_small.gif")
        self.hint_button = turtle.Turtle()
        self.hint_button.shape("lamp_thumbnail_small.gif")
        self.hint_button.penup()
        self.hint_button.goto(-300, 200)

        self.timer_turtle = turtle.Turtle()
        self.timer_turtle.hideturtle()
        self.timer_turtle.penup()
        self.timer_turtle.goto(200, 260)

        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.goto(0, 200)

    def give_hint(self):
        if self.hint_count >= self.max_hints:
            self.display_message("Você já usou todas as suas dicas!", color="red", duration=2000)
            return
        remaining_states = [state for state in self.map.states if state.name not in self.player.guessed_states]
        if remaining_states:
            state_to_hint = random.choice(remaining_states)
            hint_message = f"Dica: O estado começa com '{state_to_hint.name[:3]}'"
            self.display_message(hint_message, color="blue", duration=3000)
            self.hint_count += 1
            self.player.score -= 5
        else:
            self.display_message("Todos os estados foram adivinhados!", color="green", duration=2000)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.display_message("Jogo Pausado - Pressione 'Ctrl' para Retomar", color="blue")
        else:
            self.screen.title(f"{len(self.player.guessed_states)}/{self.total_states} Estados Corretos")
            self.update_timer()

    def update_timer(self):
        if not self.paused and self.time_limit > 0:
            self.timer_turtle.clear()
            self.timer_turtle.write(f"Tempo Restante: {self.time_limit}s", align="center", font=("Arial", 16, "normal"))
            if self.time_limit == 8:
                warning_sound.play()
            self.time_limit -= 1
            if len(self.player.guessed_states) == self.total_states:
                self.end_game(won=True)
            else:
                self.screen.ontimer(self.update_timer, 1000)
        elif self.time_limit <= 0:
            self.end_game()

    def display_message(self, text, color="black", duration=2000):
        self.message_turtle.clear()
        self.message_turtle.color(color)
        self.message_turtle.write(text, align="center", font=("Arial", 20, "normal"))
        self.screen.ontimer(self.message_turtle.clear, duration)

    def process_input(self):
        answer_state = self.player.current_input.title()
        self.player.reset_input()

        if self.map.get_state_by_name(answer_state):
            if answer_state in self.player.guessed_states:
                self.display_message("Você já adivinhou esse estado!", color="red")
            else:
                if self.hint_count > 0:
                    self.player.add_guessed_state(answer_state)
                    self.player.score += 5
                else:
                    self.player.add_guessed_state(answer_state)
                    self.player.score += 10

                self.map.display_state(answer_state)
                correct_sound.play()
                self.display_message("Correto!", color="green")
                self.update_score()

                if len(self.player.guessed_states) == self.total_states:
                    self.end_game(won=True)
        else:
            self.player.penalize()
            incorrect_sound.play()
            self.display_message("Esse estado não existe!", color="red")
            self.update_score()

    def update_score(self):
        self.player.update_score_display()

    def update_input(self):
        self.player.display_input()

    def end_game(self, won=False):
        pygame.mixer.music.stop()
        if won:
            success_sound.play()
            self.display_message(f"Parabéns! Você adivinhou todos os estados! Pontuação: {self.player.score}", color="green")
        else:
            end_sound.play()
            self.display_message(f"Tempo esgotado! Sua pontuação final é: {self.player.score}", color="black")

        save_ranking(self.player_name, self.player.score, self.map_name)

        play_again = turtle.textinput("Fim de Jogo", "Deseja jogar novamente? (Sim/Não)").lower()

        if play_again == "sim":
            self.screen.clearscreen()
            from main import return_to_menu  # Importa aqui
            return_to_menu()  # Volta para o menu inicial
        else:
            self.screen.bye()

    def bind_keys(self):
        self.screen.onkeypress(self.toggle_pause, "Control_L")
        self.screen.onkeypress(self.toggle_pause, "Control_R")
        self.screen.onkeypress(lambda: self.on_key("BackSpace"), "BackSpace")
        self.screen.onkeypress(lambda: self.on_key("Return"), "Return")

        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ":
            self.screen.onkeypress(lambda c=char: self.on_key(c), char)

        self.screen.listen()

    def on_key(self, key):
        if not self.paused:
            result = self.player.update_input(key)
            if result is not None:
                self.process_input()

    def start(self):
        start_sound.play()
        self.bind_keys()
        self.update_timer()
        self.update_score()

        self.screen.onscreenclick(self.check_hint_click)
        self.screen.mainloop()

    def check_hint_click(self, x, y):
        if self.hint_button.distance(x, y) < 50:
            self.give_hint()


















