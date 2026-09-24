# Importation des modules
from curl_cffi import requests
import json
import logging


# Création de la classe joueur
class Player:
     def __init__(self, pseudo, rank, peak, season, wins):
          self.pseudo = pseudo
          self.rank = rank
          self.peak = peak
          self.season = season
          self.wins = wins


# Constantes
URI = "ws://127.0.0.1:49124"
joueur = input("Indiquez votre pseudo ingame : ")
joueurs_liste = [joueur]


def parser_rl_tracker(pseudo: str, platform: str, id_joueur: str) -> Player: 
    """Fonction qui récupère les informations voulues sur un joueur donnés

    Args:
        pseudo (str): Pseudo du joueur ingame
        platform (str): Platforme du joueur
        id_joueur (str): Id du joueur (utile uniquement pour les joueurs steam)

    Returns:
        Player: Instance du joueur avec ses informations
    """
    # Choix de l'url
    if platform != "steam":
        url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{pseudo}?"
    else:
         url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{id_joueur}?"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://rocketleague.tracker.network/",
    "Origin": "https://rocketleague.tracker.network",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"}  
    data = None

    # Envoi d'une requête au server
    try:
        logging.info("Envoie de la requête en cours")
        response = requests.get(url, headers=headers, impersonate="chrome120")
        logging.info(response.status_code)

        if response.status_code == 200:
            data = json.loads(response.text)

        if response.status_code == 404:
            logging.info("Le joueur n'est pas dans la base de donnée de RL Tracker")

    except Exception :
        logging.exception("Erreur lors de la requête : ")

    # Gestion du cas ou la data est vide
    if not data or "data" not in data or data["data"] is None:
        logging.info("La requête est vide")
        return Player(pseudo=pseudo, rank="Unranked", peak="???", season="???", wins="???")

    # Récupération des informations
    rang = "Unranked"
    peak = "N/A"
    season = 37
    nb_win = 0
    peak_2v2 = "Unranked"

    segments = data["data"]["segments"]
    for segment in segments:
        nom_mode = segment.get("metadata", {}).get("name")

        # Rang Actuel en 2v2
        if segment["type"] == "playlist" and nom_mode == "Ranked Doubles 2v2":
            rang = segment["stats"]["tier"]["metadata"]["name"]

        # Peak historique en 2v2
        elif (segment["type"] == "peak-rating" and nom_mode == "Ranked Doubles 2v2"):
            peak_rank = segment["stats"]["peakRating"]["metadata"]["name"]
            season = segment["attributes"]["season"]
            mmr = segment["stats"]["peakRating"]["value"]
            peak_2v2 = f"{peak_rank} ({mmr}) en saison {season - 14}"

        # On recherche le nombre de game gagnées
        elif (segment["type"] == "overview"):
            nb_win = segment["stats"]["wins"] ["value"]

    # On renvoie le peak en diminutif
    try :
        liste = peak_2v2.split(" ")
        if liste[0] == "Grand":
            peak = f"{liste[0][0]}{liste[1][0]}" + rom_to_num(liste[2]) + " " + liste[3]
        elif liste[0] == "Supersonic":
            peak = "SSL" + " " + liste[2]
        elif liste[0] == "Unranked" :
            peak = "Unranked"
        else:
            peak = f"{liste[0][0]}" + rom_to_num(liste[1]) + " " + liste[2]
    except :
        logging.exception("Erreur lors de la prise d'information : ")

    # On retourne une instance pour le joueur trouvé
    return Player(pseudo=pseudo, rank=rang, peak=peak, season=(season - 14), wins=nb_win)


def rom_to_num(str: str) -> str:
    """Fonction qui transforme les chiffres romains en chiffre numérique (de 1 à 3)

    Args:
        str (str): Chiffre romain

    Returns:
        str: Chiffre numérique
    """
    if str == "I":
        return "1"
    elif str == "II":
        return "2"
    else:
        return "3"


def get_platform(platform_brut):
    platform = platform_brut.split("|")[0].lower()
    id_joueur = platform_brut.split("|")[1]

    if platform == "xboxone" :
        platform = "xbl"
    
    if platform == "ps4" or platform == "ps5" :
        platform = "psn"

    return platform, id_joueur


if __name__ == "__main__":
    player = parser_rl_tracker("TheLuge", "epic", "TheLuge")
    print(player.pseudo, player.rank, player.peak, player.season, player.wins)