# Importation des modules
from PyQt6 import QtCore, QtGui, QtWidgets
import asyncio
import websockets
import ctypes
import sys
from api import *


# Mise en place du systeme de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(threadName)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("app.log", encoding="utf-8")]
)


# Classe de la fenêtre principale
class Ui_MainWindow(object):
    def __init__(self):
            super().__init__()
            self.setup_ui()


    def setup_ui(self):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 600)
        main_window.setWindowIcon(QtGui.QIcon("images/logo.png"))
        self.centralwidget = QtWidgets.QWidget(parent=main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.fr_all = QtWidgets.QFrame(parent=self.centralwidget)
        self.fr_all.setGeometry(QtCore.QRect(-30, -30, 841, 641))
        self.fr_all.setAutoFillBackground(False)
        self.fr_all.setStyleSheet("background-color: rgb(0, 19, 56);")
        self.fr_all.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.fr_all.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fr_all.setLineWidth(1)
        self.fr_all.setObjectName("fr_all")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.fr_all)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 29, 801, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Vlayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Vlayout.setContentsMargins(0, 0, 0, 0)
        self.Vlayout.setObjectName("Vlayout")
        self.fr_entete = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.fr_entete.setStyleSheet("background-color: rgb(0, 30, 78);")
        self.fr_entete.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fr_entete.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fr_entete.setObjectName("fr_entete")
        self.lb_titre = QtWidgets.QLabel(parent=self.fr_entete)
        self.lb_titre.setGeometry(QtCore.QRect(120, 0, 681, 111))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.lb_titre.setFont(font)
        self.lb_titre.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_titre.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_titre.setObjectName("lb_titre")
        self.lb_logo = QtWidgets.QLabel(parent=self.fr_entete)
        self.lb_logo.setGeometry(QtCore.QRect(30, -7, 121, 121))
        self.lb_logo.setText("")
        self.lb_logo.setPixmap(QtGui.QPixmap("images/logo.png"))
        self.lb_logo.setScaledContents(True)
        self.lb_logo.setObjectName("lb_logo")
        self.Vlayout.addWidget(self.fr_entete)
        self.lw_main = QtWidgets.QListWidget(parent=self.fr_all)
        self.lw_main.setGeometry(QtCore.QRect(20, 140, 811, 501))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lw_main.setFont(font)
        self.lw_main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.lw_main.setLineWidth(1)
        self.lw_main.setAutoScrollMargin(18)
        self.lw_main.setAlternatingRowColors(False)
        self.lw_main.setProperty("isWrapping", False)
        self.lw_main.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
        self.lw_main.setObjectName("lw_main")
        self.lw_main.setStyleSheet(scrollbar_style)
        main_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rocket League Tracker"))
        self.lb_titre.setText(_translate("MainWindow", "Rocket League Tracker"))
        self.lw_main.setSortingEnabled(False)


    def add_item(self, player: Player):
        """Fonction qui permet d'ajouter un item dans la liste, en l'occurence un joueur

        Args:
            player (Player): Instance de Player qu'on veut ajouter dans la liste
        """
        player_widget = Player_item(player)
        item = QtWidgets.QListWidgetItem(self.lw_main)
        item.setSizeHint(QtCore.QSize(780, 160))
        self.lw_main.addItem(item)
        self.lw_main.setItemWidget(item, player_widget)


# Classe des items pour chaque joueur
class Player_item(QtWidgets.QWidget):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.setup_ui()


    def setup_ui(self):
        self.resize(798, 164)
        self.fr_all = QtWidgets.QFrame(parent=self)
        self.fr_all.setGeometry(QtCore.QRect(-31, -21, 851, 241))
        self.fr_all.setStyleSheet("background-color: rgb(0, 19, 56);")
        self.fr_all.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fr_all.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fr_all.setObjectName("fr_all")
        self.lb_logo = QtWidgets.QLabel(parent=self.fr_all)
        self.lb_logo.setGeometry(QtCore.QRect(50, 50, 121, 111))
        self.lb_logo.setText("")
        self.lb_logo.setPixmap(QtGui.QPixmap(f"images/{self.player.rank}.png"))
        self.lb_logo.setScaledContents(True)
        self.lb_logo.setObjectName("lb_logo")
        self.lb_pseudo = QtWidgets.QLabel(parent=self.fr_all)
        self.lb_pseudo.setGeometry(QtCore.QRect(190, 50, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        font.setStrikeOut(False)
        self.lb_pseudo.setFont(font)
        self.lb_pseudo.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_pseudo.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.lb_pseudo.setObjectName("lb_pseudo")
        set_autoscale_text(self.lb_pseudo, self.player.pseudo)
        self.ln_wins = QtWidgets.QLabel(parent=self.fr_all)
        self.ln_wins.setGeometry(QtCore.QRect(190, 120, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        self.ln_wins.setFont(font)
        self.ln_wins.setStyleSheet("color: rgb(255, 255, 255);")
        self.ln_wins.setObjectName("ln_wins")
        self.lb_description = QtWidgets.QLabel(parent=self.fr_all)
        self.lb_description.setGeometry(QtCore.QRect(650, 70, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(22)
        self.lb_description.setFont(font)
        self.lb_description.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lb_description.setObjectName("lb_description")
        self.lb_peak = QtWidgets.QLabel(parent=self.fr_all)
        self.lb_peak.setGeometry(QtCore.QRect(580, 110, 221, 41))
        self.lb_peak.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        self.lb_peak.setFont(font)
        self.lb_peak.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_peak.setObjectName("lb_peak")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lb_pseudo.setText(_translate("Form", f"{self.player.pseudo}"))
        self.ln_wins.setText(_translate("Form", f"{self.player.wins} wins"))
        self.lb_description.setText(_translate("Form", "Peak :"))
        self.lb_peak.setText(_translate("Form", f"{self.player.peak} s{self.player.season}"))


# Classe de la seconde fenêtre
class Ui_SecondWindow(object):
    def __init__(self, nb_wins, nb_looses):
        """Init the window"""
        super().__init__()
        self.nb_wins = nb_wins
        self.nb_looses = nb_looses
        self.setup_ui() 


    def setup_ui(self):
        second_window.setObjectName("second_window")
        second_window.resize(400, 286)
        second_window.setWindowIcon(QtGui.QIcon("images/logo.png"))
        self.frame = QtWidgets.QFrame(parent=second_window)
        self.frame.setGeometry(QtCore.QRect(-10, -10, 421, 331))
        self.frame.setStyleSheet("background-color: rgb(0, 19, 56);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.lb_info_win = QtWidgets.QLabel(parent=self.frame)
        self.lb_info_win.setGeometry(QtCore.QRect(30, 30, 261, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_info_win.setFont(font)
        self.lb_info_win.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_info_win.setObjectName("lb_info_win")
        self.lb_info_loose = QtWidgets.QLabel(parent=self.frame)
        self.lb_info_loose.setGeometry(QtCore.QRect(30, 110, 261, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_info_loose.setFont(font)
        self.lb_info_loose.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_info_loose.setObjectName("lb_info_loose")
        self.lb_info_games = QtWidgets.QLabel(parent=self.frame)
        self.lb_info_games.setGeometry(QtCore.QRect(30, 190, 261, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_info_games.setFont(font)
        self.lb_info_games.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_info_games.setObjectName("lb_info_games")
        self.lb_wins = QtWidgets.QLabel(parent=self.frame)
        self.lb_wins.setGeometry(QtCore.QRect(330, 34, 70, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_wins.setFont(font)
        self.lb_wins.setStyleSheet("color: rgb(0, 170, 0);")
        self.lb_wins.setObjectName("lb_wins")
        self.lb_wins.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.lb_wins.mousePressEvent = self.click_win #type: ignore
        self.lb_looses = QtWidgets.QLabel(parent=self.frame)
        self.lb_looses.setGeometry(QtCore.QRect(328, 113, 70, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_looses.setFont(font)
        self.lb_looses.setStyleSheet("color: rgb(170, 0, 0);")
        self.lb_looses.setObjectName("lb_looses")
        self.lb_looses.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.lb_looses.mousePressEvent = self.click_loose #type: ignore
        self.lb_games = QtWidgets.QLabel(parent=self.frame)
        self.lb_games.setGeometry(QtCore.QRect(327, 193, 70, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(30)
        self.lb_games.setFont(font)
        self.lb_games.setStyleSheet("color: rgb(255, 255, 255);")
        self.lb_games.setObjectName("lb_games")

        self.retranslateUi(second_window)
        QtCore.QMetaObject.connectSlotsByName(second_window)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Suivi de session"))
        self.lb_info_win.setText(_translate("Form", "Victoire(s) :"))
        self.lb_info_loose.setText(_translate("Form", "Défaite(s) :"))
        self.lb_info_games.setText(_translate("Form", "Partie(s) :"))
        self.lb_wins.setText(_translate("Form", f"{self.nb_wins}"))
        self.lb_looses.setText(_translate("Form", f"{self.nb_looses}"))
        self.lb_games.setText(_translate("Form", f"{self.nb_wins + self.nb_looses}"))


    # Fonction pour incrémenter le compteur de victoire
    def win(self):
        self.nb_wins += 1
        self.reload()


    # Fonction pour incrémenter le compteur de défaite
    def loose(self):
        self.nb_looses += 1
        self.reload()


    # Fonction pour incrémenter le compteur de victoire manuellement
    def click_win(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton :
            self.nb_wins += 1
        elif event.button() == QtCore.Qt.MouseButton.RightButton :
            if self.nb_wins >= 1 :
                self.nb_wins -= 1

        self.reload()


    # Fonction pour incrémenter le compteur de défaite manuellement
    def click_loose(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton :
            self.nb_looses += 1
        elif event.button() == QtCore.Qt.MouseButton.RightButton :
            if self.nb_looses >= 1 :
                self.nb_looses -= 1

        self.reload()


    # Fonction pour recharger l'affichage
    def reload(self):
        self.lb_looses.clear()
        self.lb_wins.clear()
        self.lb_games.clear()
        self.lb_looses.setText(f"{self.nb_looses}")
        self.lb_wins.setText(f"{self.nb_wins}")
        self.lb_games.setText(f"{self.nb_looses + self.nb_wins}")


# Classe pour créer un thread pour la lecture du jeu
class GameWorkerThread(QtCore.QThread):
    player_detected = QtCore.pyqtSignal(Player)
    win = QtCore.pyqtSignal()
    loose = QtCore.pyqtSignal()

    def run(self):
        asyncio.run(self.async_main())

    # Fonction principal d'écoute du jeu
    async def async_main(self):
        while True:
            try:
                # Essaie de se connecter à la socket
                async with websockets.connect(URI) as websocket:
                    await process_game_data(self, websocket)
            except (ConnectionRefusedError, TimeoutError, OSError):
                # Jeu pas lancé
                await asyncio.sleep(2)

            except websockets.exceptions.WebSocketException as e:
                logging.info(f"Connexion WebSocket interrompue ({type(e).__name__}). Nouvelle tentative dans 2s...")
                await asyncio.sleep(2)

            except Exception as e:
                # Sécurité pour éviter tout autre crash inattendu du thread
                logging.exception("Erreur inattendue dans la boucle async_main :")
                await asyncio.sleep(2)
            

# Fonction qui traite les évenements envoyé par le jeu
async def process_game_data(self, websocket):
    team = -1 
    async for message in websocket:
        event = json.loads(message)
        data = json.loads(event["Data"])

        # On récupère les pseudos et platformes des joueurs dans la partie
        if event["Event"] == "PlayerJoined" and data["MatchGuid"] != "" :
            pseudo = data["PlayerName"]
            platform, id_joueur = get_platform(data["PrimaryId"])

            if (pseudo not in joueurs_liste and platform != "unknown" and pseudo != "Unknown") :
                logging.info(f"{pseudo}, {platform}")
                player = parser_rl_tracker(pseudo, platform, id_joueur)
                joueurs_liste.append(pseudo)
                self.player_detected.emit(player)

            else:
                pass
                # logging.info("Pseudo déja dans la liste/Bot")
         

        # On récupère le numéro de ma team et on ajoute les joueurs pas encore vus
        if event["Event"] == "UpdateState" and data["MatchGuid"] != "" :
            for player in data["Players"] :
                if player["Name"] == joueur :
                    team = player["TeamNum"]
                else :
                    pseudo = player["Name"]
                    platform, id_joueur = get_platform(player["PrimaryId"])

                    
                    if (pseudo not in joueurs_liste and platform != "unknown" and pseudo != "Unknown") :
                        logging.info(f"{pseudo}, {platform}")
                        player = parser_rl_tracker(pseudo, platform, id_joueur)
                        joueurs_liste.append(pseudo)
                        self.player_detected.emit(player)

                    else :
                        pass
                        # logging.info("Pseudo déja dans la liste/Bot")


        # On annonce si le match est gagné ou perdu
        if event["Event"] == "MatchEnded" and data["MatchGuid"] != "" :
            if data["WinnerTeamNum"] == team :
                self.win.emit()
                logging.info(f"Game Gagnée, team : {team}")
            else :
                self.loose.emit()
                logging.info(f"Game Perdue, team : {team}")


# Fonction pour gérer les pseudo trop grand
def set_autoscale_text(label, text, min_font_size=8):
    """Réduit la taille de la police du QLabel pour faire rentrer le texte sans coupure"""
    font = label.font()
    max_width = label.width() if label.width() > 0 else 150

    # On teste des tailles de police de plus en plus petites
    for size in range(font.pointSize(), min_font_size - 1, -1):
        font.setPointSize(size)
        metrics = QtGui.QFontMetrics(font)
        # Si le texte rentre dans la largeur du label, on s'arrête
        if metrics.horizontalAdvance(text) <= max_width:
            break

    label.setFont(font)
    label.setText(text)


# Fonction pour avoir une barre de couleur
def set_custom_title_bar(window, hex_color="#001338"):
    """Définit une couleur exacte pour la barre sous Windows 11 (Format BGR)."""
    if sys.platform == "win32":
        hwnd = int(window.winId())
        # Convertir HEX (#RRGGBB) en format BGR (utilisé par Windows API)
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        bgr_color = (b << 16) | (g << 8) | r

        DWMWA_CAPTION_COLOR = 35  # Attribut Windows 11 pour la couleur
        
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 
            DWMWA_CAPTION_COLOR, 
            ctypes.byref(ctypes.c_int(bgr_color)), 
            ctypes.sizeof(ctypes.c_int)
        )


# Style pour la barre de scroll
scrollbar_style = """
QListWidget QScrollBar:vertical {
    border: none;
    background-color: #001338; 
    width: 10px;               
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

/* Le curseur (la partie qui glisse) */
QListWidget QScrollBar::handle:vertical {
    background-color: #001e4e; 
    min-height: 20px;
    border-radius: 5px;
}

/* Masquer les flèches haut/bas pour un rendu moderne */
QListWidget QScrollBar::add-line:vertical,
QListWidget QScrollBar::sub-line:vertical {
    height: 0px;
    background: none;
}

QListWidget QScrollBar::add-page:vertical,
QListWidget QScrollBar::sub-page:vertical {
    background: none;
}
"""

# Création de l'application
app = QtWidgets.QApplication(sys.argv)


# Création de la fenêtre principale
main_window = QtWidgets.QMainWindow()
ui = Ui_MainWindow()


# Création de la fenêtre secondaire
second_window = QtWidgets.QWidget()
ui2 = Ui_SecondWindow(0, 0)


# Création du thread
worker = GameWorkerThread()
worker.player_detected.connect(ui.add_item)
worker.win.connect(ui2.win)
worker.loose.connect(ui2.loose)
worker.start()


set_custom_title_bar(main_window, "#001e4e")
set_custom_title_bar(second_window)


# Ouverture des fenêtres
main_window.show()
second_window.show()


# Fermeture de l'application
sys.exit(app.exec())
