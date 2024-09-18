# state.py

from turtle import Turtle


# Class representing an individual state or region
from turtle import Turtle

class State:
    def __init__(self, name, x, y):
        self.name = name
        self.x = int(x)
        self.y = int(y)

    def display_on_map(self):
        """Exibe o nome do estado no mapa nas coordenadas corretas."""
        t = Turtle()
        t.hideturtle()
        t.penup()
        t.goto(self.x, self.y)
        t.write(self.name, align="center", font=("Arial", 10, "normal"))



