import tkinter as tk

from Code.control import controller_impl
from Code.enums.pin_enum import Pin
from Code.enums.game_mode_enum import GameMode
from Code.enums.roles_enum import Role
from Code.enums.event_enum import Event
from Code.enums.game_state_enum import GameStates


class Ui:

    def __init__(self):
        # Speicherung der Button- und Label-Referenzen
        self.feedback_buttons = {}
        self.buttons = {}
        self.selected_button = tk.Button
        self.lebels = [[], [], [], [], [], [], [], [], [], [], [], []]
        self.feedback_lebls = []

        # Fenster erstellen
        self.root = tk.Tk()
        self.root.title("Superhirn")

        # Frames erstellen
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid()

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.grid()

        self.network_menu_frame = tk.Frame(self.root)
        self.network_menu_frame.grid()

        # Speichern des Spielmodus (mastermind/supermastermind, guesser/coder/observer)
        self.game_mode = GameMode.MASTERMIND
        self.is_online = False

        self.dd_role = tk.StringVar(self.root)
        self.dd_mode = tk.StringVar(self.root)

        self.roles_online = ["Rater", "Zuschuaer"]
        self.modes = ["superhirn", "supersuperhirn"]
        self.roles_offline = ["Rater", "Codierer"]

        # Speichern von Textfeldern
        self.game_id_entry = tk.Entry(self.menu_frame)
        self.port_entry = tk.Entry(self.menu_frame)
        self.ip_entry = tk.Entry(self.menu_frame)

        # Spielbrettgröße definieren
        self.num_rows = 10
        self.num_columns = 0

        # Start view and create controller
        self.controller = controller_impl.Controller()
        self.controller.add_listener(self)
        self.build_networkt_menu_view()

    def build_networkt_menu_view(self):
        lbl_welcome = tk.Label(self.network_menu_frame, text="Willkommen bei Superhirn", font=("Arial", 14))
        lbl_welcome.grid(row=0, column=1, padx=5, pady=5)

        lbl_welcome = tk.Label(self.network_menu_frame, text="Netzwerkmodus auswählen:", font=("Arial", 12))
        lbl_welcome.grid(row=2, column=1, padx=5, pady=5)

        btn_online = tk.Button(self.network_menu_frame, bg="darkgrey", relief="raised",
                               text="Online", font=("Arial", 12), command=self._play_online)
        btn_online.grid(row=3, column=1, padx=5, pady=5)

        btn_offline = tk.Button(self.network_menu_frame, bg="darkgrey", relief="raised",
                                text="Offline", font=("Arial", 12), command=self._play_offline)
        btn_offline.grid(row=4, column=1, padx=5, pady=5)

        btn_rules = tk.Button(self.network_menu_frame, bg="darkgrey", relief="raised",
                              text="Regeln", font=("Arial", 12), command=self.rules_pop_up)
        btn_rules.grid(row=5, column=1, padx=5, pady=5)

    # Spielbrett erstellen und mit Spielsteinen füllen
    def build_board_view(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                self.create_peg_board(row, col)

            self.create_peg_feedback(row)

        for col in range(self.num_columns):
            self.create_peg_play_row(col)

        if self.dd_role.get() == "Codierer":
            feedback_frame = tk.Frame(self.board_frame)
            feedback_frame.grid(row=self.num_rows + 2, column=self.num_columns + 1, padx=0, pady=0)
            for i in range(2):
                for j in range(2):
                    self.create_peg_fedback_buttons(i, j, feedback_frame)
            if self.num_columns == 5:
                self.create_peg_fedback_buttons(0, 3, feedback_frame)
            check_in_button = tk.Button(self.board_frame, bg="lightblue", relief="raised",
                                        text="Check\nIn", command=self.check_in)
            check_in_button.grid(row=self.num_rows + 2, column=self.num_columns + 2, padx=5, pady=5)

            btn_rules = tk.Button(self.board_frame, bg="lightblue", relief="raised",
                                  text="Regeln", font=("Arial", 12), command=self.rules_pop_up)
            btn_rules.grid(row=self.num_rows + 1, column=self.num_columns + 2, padx=5, pady=5)
        else:
            check_in_button = tk.Button(self.board_frame, bg="lightblue", relief="raised",
                                        text="Check\nIn", command=self.check_in)
            check_in_button.grid(row=self.num_rows + 2, column=self.num_columns + 1, padx=5, pady=5)

            btn_rules = tk.Button(self.board_frame, bg="lightblue", relief="raised",
                                  text="Regeln", font=("Arial", 12), command=self.rules_pop_up)
            btn_rules.grid(row=self.num_rows + 2, column=self.num_columns + 2, padx=5, pady=5)

    # Hauptmenü erstelllen
    def build_main_menu_view(self):
        if self.is_online:
            lbl_welcome = tk.Label(self.menu_frame, text="Willkommen im Online-Mode", font=("Arial", 14))
            dropdown_role = tk.OptionMenu(self.menu_frame, self.dd_role, *self.roles_online)
            dropdown_mode = tk.OptionMenu(self.menu_frame, self.dd_mode, *self.modes)

            lbl_game_id = tk.Label(self.menu_frame, text="GameId:")
            lbl_game_id.grid(row=5, column=0, padx=5, pady=3)
            lbl_port = tk.Label(self.menu_frame, text="Port:")
            lbl_port.grid(row=5, column=1, padx=5, pady=3)
            lbl_ip = tk.Label(self.menu_frame, text="Ip-Adresse:")
            lbl_ip.grid(row=5, column=2, padx=5, pady=3)

            self.game_id_entry.grid(row=6, column=0, padx=5, pady=3)
            self.port_entry.grid(row=6, column=1, padx=5, pady=3)
            self.ip_entry.grid(row=6, column=2, padx=5, pady=3)

        else:
            lbl_welcome = tk.Label(self.menu_frame, text="Willkommen im Offline-Mode", font=("Arial", 14))
            dropdown_role = tk.OptionMenu(self.menu_frame, self.dd_role, *self.roles_offline)
            dropdown_mode = tk.OptionMenu(self.menu_frame, self.dd_mode, *self.modes)

        lbl_welcome.grid(row=0, column=1, padx=5, pady=5)

        lbl_choose_game = tk.Label(self.menu_frame, text="Einen Spielmodus wählen:", font=("Arial", 12))
        lbl_choose_game.grid(row=2, column=1, padx=5, pady=5)

        dropdown_role.grid(row=3, column=1, padx=5, pady=5)
        dropdown_mode.grid(row=4, column=1, padx=5, pady=5)

        btn_play = tk.Button(self.menu_frame, bg="white", relief="raised", text="Spielen", font=("Arial", 12),
                             command=self.start_game)
        btn_play.grid(row=7, column=1, padx=5, pady=5)

        btn_rules = tk.Button(self.menu_frame, bg="darkgrey", relief="raised",
                              text="Regeln", font=("Arial", 12), command=self.rules_pop_up)
        btn_rules.grid(row=8, column=1, padx=5, pady=5)

    def _play_online(self):
        self.network_menu_frame.destroy()
        self.is_online = True
        self.build_main_menu_view()

    def _play_offline(self):
        self.network_menu_frame.destroy()
        self.is_online = False
        self.build_main_menu_view()

    def start_game(self):
        self._set_game_mode()

        self.menu_frame.destroy()
        self.build_board_view()

        if self.is_online:
            self.controller.start_game(Role.get_role_by_description(self.dd_role.get()), self.game_mode,
                                       self.game_id_entry.get(),
                                       self.ip_entry.get(), self.port_entry.get())
        else:
            self.controller.start_game(Role.get_role_by_description(self.dd_role.get()), self.game_mode)

    def _set_game_mode(self):
        if self.dd_mode.get() == "superhirn":
            if self.is_online == "online":
                self.game_mode = GameMode.ONLINE_MASTERMIND
            else:
                self.game_mode = GameMode.MASTERMIND
        else:
            if self.is_online == "online":
                self.game_mode = GameMode.ONLINE_SUPER_MASTERMIND
            else:
                self.game_mode = GameMode.SUPER_MASTERMIND
        self.num_columns = self.game_mode.code_length

    # Funktion zum Erstellen der Spielsteinfelder
    def create_peg_board(self, r, c):
        peg = tk.Label(self.board_frame, width=4, height=2, bg="white", relief="raised")
        peg.grid(row=r, column=c, padx=5, pady=5)
        self.lebels[r].append(peg)

    # Funktion zur erstellung der Feedbackfelder
    def create_peg_feedback(self, r):
        feedback_frame = tk.Frame(self.board_frame)
        feedback_frame.grid(row=r, column=self.num_columns + 1, padx=0, pady=0)
        temp_lebels = []
        for i in range(2):
            for j in range(2):
                lebel_feedback = tk.Label(feedback_frame, width=2, bg="lightgrey", relief="raised")
                lebel_feedback.grid(row=i, column=j, padx=0, pady=0)
                temp_lebels.append(lebel_feedback)

        if self.num_columns == 5:  # erstellen eines 5ten feedbacl pins wenn supermastermind gespielt wird
            lebel_feedback5 = tk.Label(feedback_frame, width=2, bg="lightgrey", relief="raised")
            lebel_feedback5.grid(row=0, column=3, padx=0, pady=0)
            temp_lebels.append(lebel_feedback5)

        self.feedback_lebls.append(temp_lebels)

    def create_peg_fedback_buttons(self, i, j, frame):
        peg = tk.Label(frame, width=2, bg="lightgrey", relief="raised")
        peg.bind("<Button-1>", lambda event: self.open_feedback_popup(event, peg))
        peg.grid(row=i, column=j, padx=0, pady=0)
        self.feedback_buttons[f"{str(i) + str(j)}"] = peg

    # Funktion zum befuellen des den Spielbretts
    def fill_board(self, board):
        print(board)
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                if board[1][r][c] != Pin.HOLE:
                    selected_lebel = self.lebels[r][c]
                    selected_lebel.config(bg=board[1][r][c].color)

                    selected_feedback_lebel = self.feedback_lebls[r][c]
                    selected_feedback_lebel.config(bg=board[2][r][c].color)

    def _change_color_btn(self, btn):
        self.selected_button = btn

    def _change_color_feedback_btn(self, btn):
        self.selected_feedback_button = btn

    def create_peg_play_row(self, column):
        peg = tk.Label(self.board_frame, width=4, height=2, bg="darkgrey", relief="raised")
        peg.grid(row=self.num_rows + 2, column=column, padx=5, pady=5)
        peg.bind("<Button-1>", lambda event: self.open_popup(event, peg))
        self.buttons[f"{column}"] = peg

    def open_popup(self, event, btn):
        # PinPopup-Menü erstellen
        popup_menu = tk.Menu(self.root, tearoff=0)

        # Setzt selected button
        self._change_color_btn(btn)

        popup_menu.add_command(label="Rot", command=self.option_red)
        popup_menu.add_command(label="Grün", command=self.option_green)
        popup_menu.add_command(label="Gelb", command=self.option_yellow)
        popup_menu.add_command(label="Blau", command=self.option_blue)
        popup_menu.add_command(label="Orange", command=self.option_orange)
        popup_menu.add_command(label="Braun", command=self.option_brown)

        if self.num_columns >= 5:
            popup_menu.add_command(label="Weiß", command=self.option_white)
            popup_menu.add_command(label="Schwarz", command=self.option_black)

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(event.x_root, event.y_root)

    def open_feedback_popup(self, event, btn):
        # Setzt selected button
        self._change_color_btn(btn)

        # PinPopup-Menü erstellen
        popup_menu = tk.Menu(self.root, tearoff=0)

        popup_menu.add_command(label="Weiß", command=self.option_white)
        popup_menu.add_command(label="Schwarz", command=self.option_black)
        popup_menu.add_command(label="Leeren", command=self.option_empty)

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(event.x_root, event.y_root)

    def option_empty(self):
        self.selected_button.config(bg="lightgrey")

    def option_red(self):
        self.selected_button.config(bg="red")

    def option_blue(self):
        self.selected_button.config(bg="blue")

    def option_yellow(self):
        self.selected_button.config(bg="yellow")

    def option_brown(self):
        self.selected_button.config(bg="brown")

    def option_green(self):
        self.selected_button.config(bg="green")

    def option_orange(self):
        self.selected_button.config(bg="orange")

    def option_white(self):
        self.selected_button.config(bg="white")

    def option_black(self):
        self.selected_button.config(bg="black")

    def check_in(self):
        temp = []
        temp_values = None
        if self.dd_role.get() == "Zuschauer":
            pass
        elif self.dd_role.get() == "Rater" or self.controller.get_game_state() == GameStates.PLACE_CODE:
            temp_values = self.buttons.values()
        else:
            temp_values = self.feedback_buttons.values()
        for b in temp_values:
            temp.append(Pin.get_pin_by_color(b.cget("bg")))
        if not self.controller.check_in_code(Role.get_role_by_description(self.dd_role.get()), temp):
            self.input_exeption_pop_up()

    def input_exeption_pop_up(self):
        popup_menu = tk.Menu(self.board_frame, tearoff=0)

        popup_menu.add_command(label="Falsche eingabe!", foreground="red")
        popup_menu.add_command(label="les dir nochmal die regel durch!")

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(self.board_frame.winfo_x() // 2, self.board_frame.winfo_y() // 2)

    def winner_pop_up(self):
        popup_menu = tk.Menu(self.board_frame, tearoff=0)

        popup_menu.add_command(label="HERZLICHENN GLÜCKWUNSCH SIE HABEN GEWONNEN!", foreground="green")
        popup_menu.add_command(label="Nochmal spielen? Klich hier!", command=self.play_again)

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(self.board_frame.winfo_x() // 2, self.board_frame.winfo_y() // 2)

    def looser_pop_up(self):
        popup_menu = tk.Menu(self.board_frame, tearoff=0)

        popup_menu.add_command(label="Leider veloren", foreground="blue")
        popup_menu.add_command(label="der richtige code wäre gewesen:")
        popup_menu.add_command(label=self.controller.get_final_code())
        popup_menu.add_command(label="Nochmal spielen? Klich hier!", command=self.play_again)

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(self.board_frame.winfo_x() // 2, self.board_frame.winfo_y() // 2)

    def cheater_pop_up(self):
        popup_menu = tk.Menu(self.board_frame, tearoff=0)

        popup_menu.add_command(label="DU CHEATER!!!!!", foreground="pink")
        popup_menu.add_command(label="ok", command=self.play_again)

        # Position des Popup-Menüs festlegen
        popup_menu.tk_popup(self.board_frame.winfo_x() // 2, self.board_frame.winfo_y() // 2)

    def rules_pop_up(self):
        rules = tk.Tk()
        rules.title("Regeln")
        rules_frame = tk.Frame(rules, background="lightblue")
        rules_frame.pack()
        quote = """In Superhirn kann man entwerder als Rater oder als Codierer Spielen
        
        Rls Rater:
        Dein Ziel ist es den Farbcode zuerraten, dazu kannst du auf die grauen Felder 
        im unteren Bereich klicken und einen Pin auswählen 
        wenn du in jedem feld eine Farbe ausgewählt hast kannst du auf Check In klicken
        Dann bekommst du ein Feedback auf deinen Zug. weiß bedeuetet richtige Farbe
        aber flasche Position und schwarz bedeutet richtige Farbe und richtige Position 
        Allerdings weißt du nie um welchen Pin es  sich handelt.
        
        Als Codierer:
        Du legst am anfang des Spiels einen code fest 
        Du bekommst jede Runde eineen neuen code als versuch den du bewerten musst.
        Dafür klickst du auf die kleineren grauen Felder unten und wählst einen Pin aus
        weiß bedeuetet richtige Farbe aber flasche Position und schwarz bedeutet richtige
        Farbe und richtige Position. Dabei musst du aber nicht auf die reinfolde der pins achten."""
        text = tk.Label(rules, text=quote)
        text.pack()

    def play_again(self):
        self.controller.play_again()
        self.controller.add_listener(self)
        self.start_game()

    def event_handler(self, event, detail):
        if event == Event.GAMESTATECHANGE:
            self.fill_board(self.controller.get_board())
        elif event == Event.WINNER:
            if detail == Role.get_role_by_description(self.dd_role.get()):
                self.winner_pop_up()
            else:
                self.looser_pop_up()

        elif event == Event.CHEATER:
            self.cheater_pop_up()

    def get_root(self):
        return self.root


if __name__ == '__main__':
    ui = Ui()

    # Starte das Hauptfenster
    ui.get_root().mainloop()
