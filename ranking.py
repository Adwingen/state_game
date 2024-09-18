# ranking.py

import csv
import os

RANKING_FILE = "ranking.csv"


def load_ranking():
    """Carrega o ranking do arquivo CSV"""
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_ranking(name, score, map_name):
    """Salva a pontuação do jogador no ranking"""
    fieldnames = ['Nome', 'Pontuação', 'Mapa']
    file_exists = os.path.exists(RANKING_FILE)

    with open(RANKING_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Escreve o cabeçalho se o arquivo não existir
        if not file_exists:
            writer.writeheader()

        # Escreve a pontuação do jogador
        writer.writerow({'Nome': name, 'Pontuação': score, 'Mapa': map_name})


def get_top_ranking(limit=10):
    """Retorna os melhores jogadores, ordenados por pontuação"""
    ranking = load_ranking()
    ranking_sorted = sorted(ranking, key=lambda x: int(x['Pontuação']), reverse=True)
    return ranking_sorted[:limit]
