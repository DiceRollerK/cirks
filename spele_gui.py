#spele_gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame
pygame.mixer.init()

class SpeleGUI:
    def __init__(self, root):
        self.root = root
        self.volume = 50  # Default volume level (0-100)
        self.root.title("Spēle Cirks")

        # Main start menu frame.
        self.setup_frame = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief="groove")
        self.setup_frame.pack(padx=10, pady=10)

        # Instructions frame.
        instr_frame = tk.Frame(self.setup_frame, bg="#d9edf7", bd=2, relief="sunken")
        instr_frame.pack(fill="x", pady=5)
        self.instrukcija_button = tk.Button(
            instr_frame, text="ℹ️ Instrukcija",
            command=lambda: [self.play_sound("button.mp3"), self.toggle_instructions()],
            font=("Helvetica", 12, "bold"), bg="#5bc0de", fg="white", padx=10, pady=5)
        self.instrukcija_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.instructions_label = tk.Label(instr_frame, text="", justify="left", font=("Helvetica", 10), bg="#d9edf7")
        
        # Gamemode frame with mode options and buttons.
        gamemode_frame = tk.Frame(self.setup_frame, bg="#f7f7f7", bd=2, relief="groove")
        gamemode_frame.pack(fill="x", pady=5)
        self.game_mode = tk.StringVar(value="regular")
        regular_btn = tk.Radiobutton(
            gamemode_frame, text="🎲 Klasiskais Cirks",
            variable=self.game_mode, value="regular",
            indicatoron=0, command=lambda: [self.play_sound("button.mp3"), self.refresh_gamemode()],
            font=("Helvetica", 12, "bold"), bg="#5cb85c", fg="white", width=15)
        tournament_btn = tk.Radiobutton(
            gamemode_frame, text="🏆 Cirku Turnīrs",
            variable=self.game_mode, value="tournament",
            indicatoron=0, command=lambda: [self.play_sound("button.mp3"), self.refresh_gamemode()],
            font=("Helvetica", 12, "bold"), bg="#f0ad4e", fg="white", width=15)
        regular_btn.pack(side=tk.LEFT, padx=5, pady=5)
        tournament_btn.pack(side=tk.LEFT, padx=5, pady=5)
        statistika_btn = tk.Button(
            gamemode_frame, text="📊 Līderu saraksts",
            command=lambda: [self.play_sound("button.mp3"), self.show_statistika()],
            font=("Helvetica", 12, "bold"), bg="#337ab7", fg="white", width=15)
        statistika_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.iesatijumi_btn = tk.Button(
            gamemode_frame, text="⚙️ Iestatījumi",
            command=lambda: [self.play_sound("button.mp3"), self.show_iesatijumi(mode="start")],
            font=("Helvetica", 12, "bold"), bg="#337ab7", fg="white", width=15)
        self.iesatijumi_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.speletajuVar = tk.IntVar(value=2)
        self.action_frame = tk.Frame(self.setup_frame, bg="#e0e0e0")
        self.action_frame.pack(fill="x", pady=5)
        self.create_player_names_entries()
        self.create_player_amount_frame()

        self.computer_players_enabled = tk.BooleanVar(value=True)
        self.computer_players_check = tk.Checkbutton(
            self.action_frame, text="🤖 Datoru spēlētāji",
            variable=self.computer_players_enabled,
            command=lambda: self.play_sound("button.mp3"),
            font=("Helvetica", 12, "bold"), bg="#e0e0e0")
        self.computer_players_check.pack(anchor="w", pady=5)

        self.start_button = tk.Button(
            self.action_frame, text="▶️ Sākt spēli!",
            command=self.saktSpele,
            font=("Helvetica", 12, "bold"), bg="#5bc0de", fg="white", padx=20, pady=10)
        self.start_button.pack(pady=10)

        # Placeholder for Statistika frame and stats pop-up.
        self.statistika_frame = None
        self.stats_popup = None

    # ------------------ Sound Playback Helper ------------------
    def play_sound(self, sound_file):
        try:
            sound = pygame.mixer.Sound(sound_file)
            sound.set_volume(self.volume / 100)
            sound.play()
        except Exception as e:
            print(f"Sound error: {e}")

    # ------------------ Custom Error Dialog ------------------
    def custom_error(self, title, message):
        error_win = tk.Toplevel(self.root)
        error_win.title(title)
        error_win.geometry("350x150")
        error_win.configure(bg="#ffe6e6")
        error_label = tk.Label(error_win, text=message, font=("Helvetica", 12, "bold"),
                               bg="#ffe6e6", fg="#a80000", wraplength=300)
        error_label.pack(pady=20, padx=20)
        ok_button = tk.Button(error_win, text="OK", font=("Helvetica", 12, "bold"), bg="#a80000", fg="white",
                              command=lambda: [self.play_sound("button.mp3"), error_win.destroy()])
        ok_button.pack(pady=10)


    def toggle_instructions(self):
        if hasattr(self, 'instructions_panel') and self.instructions_panel.winfo_exists():
            self.instructions_panel.destroy()
        else:
            parent = self.instructions_label.master
            self.instructions_panel = tk.Frame(parent, bg="#d9edf7", bd=1, relief="sunken")
            self.instructions_panel.pack(fill="both", padx=5, pady=5)
            # --- Regular Gamemode Section ---
            reg_frame = tk.Frame(self.instructions_panel, bg="#d9edf7")
            reg_frame.pack(fill="x", padx=10, pady=(5,2))
            reg_header = tk.Label(
                reg_frame, 
                text="Klasiskais Cirks",
                font=("Helvetica", 12, "bold"), 
                bg="#5cb85c", fg="white",
                anchor="center", justify="center"
            )
            reg_header.pack(fill="x", pady=2)
            reg_text = (
                "1. Izvēlies dalībnieku skaitu (2 līdz 4) un ievadi katra tā vārdu.\n"
                "2. Spied 'Sākt spēli!' un seko norādēm uz spēles laukuma.\n"
                "3. Klikšķini uz kauliņa attēla, lai mestu kauliņu.\n"
                "4. Spēles beigās tiks parādīta iegūto vietu statistika."
            )
            reg_label = tk.Label(
                reg_frame, 
                text=reg_text,
                font=("Helvetica", 10, "bold"), 
                bg="#d9edf7", fg="black",
                anchor="w", justify="left"
            )
            reg_label.pack(fill="x", padx=5, pady=(2,5))
            sep1 = tk.Frame(self.instructions_panel, height=2, bg="gray")
            sep1.pack(fill="x", padx=10, pady=2)
            # --- Tournament Gamemode Section ---
            tourn_frame = tk.Frame(self.instructions_panel, bg="#d9edf7")
            tourn_frame.pack(fill="x", padx=10, pady=(5,2))
            tourn_header = tk.Label(
                tourn_frame, 
                text="Cirku Turnīrs",
                font=("Helvetica", 12, "bold"), 
                bg="#f0ad4e", fg="white",
                anchor="center", justify="center"
            )
            tourn_header.pack(fill="x", pady=2)
            tourn_text = (
                "1. 8 dalībnieki tiek sadalīti 2 atsevišķās grupās pa 4.\n"
                "2. Katrā grupā notiek spēles, lai noteiktu finālistus.\n"
                "3. Kreisajā grupā spied SPACE, labajā - ENTER, lai mestu kauliņu.\n"
                "4. Fināla spēlē tiek izmantoti tādi paši noteikumi kā klasiskajā režīmā."
            )
            tourn_label = tk.Label(
                tourn_frame, 
                text=tourn_text,
                font=("Helvetica", 10, "bold"), 
                bg="#d9edf7", fg="black",
                anchor="w", justify="left"
            )
            tourn_label.pack(fill="x", padx=5, pady=(2,5))
            sep2 = tk.Frame(self.instructions_panel, height=2, bg="gray")
            sep2.pack(fill="x", padx=10, pady=2)
            # --- Additional Information Section ---
            add_frame = tk.Frame(self.instructions_panel, bg="#d9edf7")
            add_frame.pack(fill="x", padx=10, pady=(5,5))
            add_header = tk.Label(
                add_frame, 
                text="Papildus Informācija",
                font=("Helvetica", 12, "bold"), 
                bg="#337ab7", fg="white",
                anchor="center", justify="center"
            )
            add_header.pack(fill="x", pady=2)
            add_text = ("- Vari izvēlēties pievienot datoru spēlētājus, lai piepildītu savu spēles pieredzi.\n"
                        "- Līderu sarakstā vari apskatīt savus un citu spēlētāju panākumus.\n"
                        "- Spēles gaitā dubultklikšķini uz spēlētāja vārda, lai apskatītu viņu statistiku.\n"
                        "- Iestatījumos vari pieregulēt pēc nepieciešamības skaļumu.\n"
                        )
            add_label = tk.Label(
                add_frame, 
                text=add_text,
                font=("Helvetica", 10, "bold"), 
                bg="#d9edf7", fg="black",
                anchor="w", justify="left"
            )
            add_label.pack(fill="x", padx=5, pady=(2,5))

    def refresh_gamemode(self):
        self.play_sound("button.mp3")
        self.create_player_names_entries()
        self.create_player_amount_frame()

    def create_player_names_entries(self):
        if hasattr(self, 'player_names_frame'):
            self.player_names_frame.destroy()
        self.player_names_frame = tk.Frame(self.setup_frame, bg="#F0F8FF", bd=2, relief="groove")
        self.player_names_frame.pack(fill="x", padx=10, pady=5, before=self.action_frame)
        self.player_names_frame.columnconfigure(0, weight=1)
        self.speletajuIevades = []
        if self.game_mode.get() == "regular":
            header_bg = "#5cb85c"
            header_text = "Spēlētāju vārdi:"
            num_entries = 4
        else:
            header_bg = "#f0ad4e"
            header_text = "Spēlētāju vārdi (Turnīra režīms):"
            num_entries = 8
        header = tk.Label(self.player_names_frame, text=header_text, 
                        font=("Helvetica", 12, "bold"), bg=header_bg, fg="white",
                        anchor="center", justify="center", padx=10, pady=5)
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5,2))
        for i in range(num_entries):
            row_frame = tk.Frame(self.player_names_frame, bg="#F0F8FF")
            row_frame.grid(row=i+1, column=0, sticky="ew", padx=10, pady=3)
            row_frame.columnconfigure(1, weight=1)
            lbl_entry = tk.Label(row_frame, text=f"{i+1}. Spēlētāja vārds:", 
                                font=("Helvetica", 10, "bold"), bg="#F0F8FF", anchor="center", justify="center")
            lbl_entry.grid(row=0, column=0, sticky="ew")
            entry = tk.Entry(row_frame, font=("Helvetica", 10))
            entry.grid(row=0, column=1, sticky="ew", padx=(5,0))
            self.speletajuIevades.append(entry)
        self.atjaunotIevades()

    def create_player_amount_frame(self):
        if hasattr(self, 'player_amount_frame'):
            self.player_amount_frame.destroy()
        self.player_amount_frame = tk.Frame(self.setup_frame, bg="#F0F8FF", bd=2, relief="groove")
        self.player_amount_frame.pack(fill="x", padx=10, pady=5, before=self.action_frame)
        self.player_amount_frame.columnconfigure(0, weight=1)
        if self.game_mode.get() == "regular":
            header_bg = "#5cb85c"
            header_text = "Izvēlies spēlētāju daudzumu:"
        else:
            header_bg = "#f0ad4e"
            header_text = "Spēlētāju daudzums: 8 (Turnīra režīms)"
        header = tk.Label(self.player_amount_frame, text=header_text, 
                        font=("Helvetica", 12, "bold"), bg=header_bg, fg="white",
                        anchor="center", justify="center", padx=10, pady=5)
        header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5,2))
        if self.game_mode.get() == "regular":
            btn_frame = tk.Frame(self.player_amount_frame, bg="#F0F8FF")
            btn_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,5))
            for idx in range(3):
                btn_frame.columnconfigure(idx, weight=1)
            for idx, n in enumerate([2, 3, 4]):
                rb = tk.Radiobutton(
                    btn_frame, text=str(n), variable=self.speletajuVar,
                    value=n, command=lambda: [self.play_sound("button.mp3"), self.atjaunotIevades()],
                    indicatoron=0, font=("Helvetica", 10, "bold"), bg="#dff0d8")
                rb.grid(row=0, column=idx, padx=5, sticky="ew")

    def atjaunotIevades(self):
        n = self.speletajuVar.get()
        for i, entry in enumerate(self.speletajuIevades):
            if self.game_mode.get() == "regular":
                if i < n:
                    entry.master.grid()
                else:
                    entry.master.grid_remove()
            else:
                entry.master.grid()

    def show_player_stats(self, player):
        self.play_sound("button.mp3")
        if self.stats_popup is not None:
            return
        self.stats_popup = tk.Toplevel(self.root)
        self.stats_popup.title(f"{player['vards']} Statistika")
        self.stats_popup.config(bg="#FAFAFA")
        self.stats_popup.geometry("500x300")
        self.stats_popup.resizable(False, False)
        self.stats_popup.protocol("WM_DELETE_WINDOW", self.close_stats_popup)
        header = tk.Label(self.stats_popup, text="Spēlētāja Statistika", 
                          font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        header.pack(fill="x", pady=(0, 10))
        info_frame = tk.Frame(self.stats_popup, bg="#FAFAFA", padx=15, pady=10)
        info_frame.pack(fill="x")
        pawn_img = self.spelKaulinAtteli(player["krasa"])
        img_label = tk.Label(info_frame, image=pawn_img, bg="#FAFAFA")
        img_label.image = pawn_img
        img_label.pack(side=tk.LEFT, padx=(0, 15))
        name_label = tk.Label(info_frame, text=player["vards"], font=("Helvetica", 20, "bold"),
                              bg="#FAFAFA", fg=player["krasa"])
        name_label.pack(side=tk.LEFT, anchor="center")
        table_frame = tk.Frame(self.stats_popup, bg="#FAFAFA", padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)
        headers = ["Režīms", "Spēles", "Uzvaras", "Attiecība"]
        for col, header_text in enumerate(headers):
            lbl = tk.Label(table_frame, text=header_text, font=("Helvetica", 14, "bold"),
                           bg="#D3E4CD", fg="#003300", borderwidth=1, relief="solid", padx=5, pady=5)
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)
        stats = self.player_stats.get(player["vards"], {
            "regular_games": 0, "regular_wins": 0,
            "tournament_games": 0, "tournament_wins": 0
        })
        reg_ratio = stats["regular_wins"] / stats["regular_games"] if stats["regular_games"] > 0 else 0
        tourn_ratio = stats["tournament_wins"] / stats["tournament_games"] if stats["tournament_games"] > 0 else 0
        data = [
            ["Klasiskā", str(stats["regular_games"]), str(stats["regular_wins"]), f"{reg_ratio:.2f}"],
            ["Turnīra", str(stats["tournament_games"]), str(stats["tournament_wins"]), f"{tourn_ratio:.2f}"]
        ]
        for row_idx, row_data in enumerate(data, start=1):
            for col_idx, val in enumerate(row_data):
                lbl = tk.Label(table_frame, text=val, font=("Helvetica", 14),
                               bg="white", fg="#333333", borderwidth=1, relief="solid", padx=5, pady=5)
                lbl.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
        close_btn = tk.Button(self.stats_popup, text="Aizvērt", font=("Helvetica", 12, "bold"),
                              bg="#337ab7", fg="white", command=lambda: [self.play_sound("button.mp3"), self.close_stats_popup()], padx=10, pady=5)
        close_btn.pack(pady=(5, 10))

    def close_stats_popup(self):
        if self.stats_popup is not None:
            self.stats_popup.destroy()
            self.stats_popup = None

    def izveidotRami(self):
        import random
        from PIL import Image, ImageTk
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.game_frame, width=self.board_width, height=self.board_height)
        self.canvas.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.board_image = ImageTk.PhotoImage(Image.open("circus_board.png").resize((self.board_width, self.board_height)))
        self.canvas.create_image(0, 0, anchor="nw", image=self.board_image)
        self.info_label = tk.Label(self.game_frame, text="", font=("Helvetica", 14), width=30)
        self.info_label.grid(row=0, column=1, sticky="nw")
        dice_frame = tk.Frame(self.game_frame)
        dice_frame.grid(row=1, column=1, columnspan=2, sticky="w")
        self.dice_text_label = tk.Label(dice_frame, text="Metamais kauliņš: ", font=("Helvetica", 12))
        self.dice_text_label.pack(side=tk.LEFT, padx=(0, 60))
        init_val = random.randint(1, 6)
        self.dice_photo = self.metKaulinAtteli(init_val)
        self.dice_image_label = tk.Label(dice_frame, image=self.dice_photo)
        self.dice_image_label.pack(side=tk.LEFT)
        self.dice_image_label.bind("<Button-1>", self.metKaulinu)
        self.message_label = tk.Label(self.game_frame, text="", justify="left", font=("Helvetica", 12))
        self.message_label.grid(row=2, column=1, sticky="nw")

        # Move the settings button below the message output
        self.iesatijumi_game_btn = tk.Button(self.game_frame, text="⚙️ Iestatījumi",
                                            command=lambda: [self.play_sound("button.mp3"), self.show_iesatijumi(mode="game")],
                                            font=("Helvetica", 12, "bold"), bg="#337ab7", fg="white")
        self.iesatijumi_game_btn.grid(row=3, column=1, sticky="nw", pady=(5,10))

        # Shift the score frame down by one row
        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.grid(row=4, column=1, sticky="nw", pady=10)
        self.score_labels = []
        for player in self.speletaji:
            lbl = tk.Label(self.score_frame, text=f"{player['vards']}: Plāksne {player['laukums']}",
                           fg=player["krasa"], font=("Helvetica", 12), bd=2, relief="ridge", width=30)
            lbl.pack(anchor="w", pady=2)
            if player.get("human", True):
                lbl.bind("<Double-Button-1>", lambda e, p=player: self.show_player_stats(p))
            self.score_labels.append(lbl)
        self.log_text = tk.Text(self.game_frame, height=10, width=45, state="disabled", font=("Helvetica", 10))
        self.log_text.grid(row=5, column=1, columnspan=2, sticky="nw", pady=5)
        for c in ["indianred", "blue", "green", "gold", "purple", "cyan", "orange", "pink"]:
            self.log_text.tag_config(c, foreground=c)
        self.pawn_images = []
        for player in self.speletaji:
            pawn_image = self.spelKaulinAtteli(player["krasa"])
            token = self.canvas.create_image(0, 0, image=pawn_image)
            player["figura_id"] = token
            player["pawn_image"] = pawn_image
            self.pawn_images.append(pawn_image)
        self.atjaunotFiguruPozicijas()
        self.atjaunotInfoEtiketi()
        self.atjaunotRezLapu()

    def createTournamentBoard(self, players, parent_frame, board_side):
        board = {}
        board["players"] = players
        board["active"] = list(range(len(players)))
        board["current"] = 0
        board["finished_order"] = []
        board["finished_recorded"] = False
        board["canvas"] = tk.Canvas(parent_frame, width=400, height=400)
        board["canvas"].pack(padx=5, pady=5)
        board["board_width"] = 400
        board["board_height"] = 400
        board["columns"] = 10
        board["rows"] = 12
        board["tile_width"] = board["board_width"] / board["columns"]
        board["tile_height"] = board["board_height"] / board["rows"]
        board_image = ImageTk.PhotoImage(Image.open("circus_board.png").resize((400,400)))
        board["canvas"].create_image(0, 0, anchor="nw", image=board_image)
        board["board_image"] = board_image
        board["info_label"] = tk.Label(parent_frame, text="", font=("Helvetica", 12, "bold"))
        board["info_label"].pack()
        init_val = random.randint(1,6)
        board["dice_photo"] = self.metKaulinAtteli(init_val)
        board["dice_label"] = tk.Label(parent_frame, image=board["dice_photo"])
        board["dice_label"].pack(padx=5, pady=5)
        board["dice_label"].bind("<Button-1>", lambda e, b=board: self.tournamentDiceThrow(b, e))
        board["log_text"] = tk.Text(parent_frame, height=5, width=60, state="disabled", font=("Helvetica", 10))
        board["log_text"].pack(pady=5)
        for c in ["indianred", "blue", "green", "gold", "purple", "cyan", "orange", "pink"]:
            board["log_text"].tag_config(c, foreground=c)
        board["score_frame"] = tk.Frame(parent_frame)
        board["score_frame"].pack(pady=5)
        board["score_labels"] = []
        for player in players:
            lbl = tk.Label(board["score_frame"], text=f"{player['vards']}: Plāksne {player['laukums']}",
                        fg=player["krasa"], font=("Helvetica", 12), bd=2, relief="ridge", width=30)
            lbl.pack(anchor="w", pady=2)
            if player.get("human", True):
                lbl.bind("<Double-Button-1>", lambda e, p=player: self.show_player_stats(p))
            board["score_labels"].append(lbl)
        board["pawn_images"] = []
        for player in players:
            pawn_image = self.spelKaulinAtteli_tournament(player["krasa"], board)
            token = board["canvas"].create_image(0, 0, image=pawn_image)
            player["figura_id"] = token
            player["pawn_image"] = pawn_image
            board["pawn_images"].append(pawn_image)
        self.tournamentUpdatePositions(board)
        self.tournamentUpdateInfo(board)
        self.tournamentUpdateScores(board)
        board["animating"] = False
        board["dice_on_cooldown"] = False
        board["animation_delay"] = 30
        board["animation_steps"] = 8
        return board

    def back_to_menu_from_statistika(self):
        self.play_sound("button.mp3")
        if self.statistika_frame:
            self.statistika_frame.destroy()
            self.statistika_frame = None
        self.setup_frame.pack(padx=10, pady=10)

    def show_statistika(self):
        self.play_sound("button.mp3")
        self.setup_frame.pack_forget()
        self.statistika_frame = tk.Frame(self.root, bg="#F0F8FF", bd=4, relief="groove")
        self.statistika_frame.pack(padx=30, pady=30, fill="both", expand=True)
        title = tk.Label(self.statistika_frame, text="Līderu saraksts", font=("Helvetica", 20, "bold"),
                         bg="#F0F8FF", fg="#003366")
        title.pack(pady=(20, 10))
        btn_frame = tk.Frame(self.statistika_frame, bg="#F0F8FF")
        btn_frame.pack(pady=10)
        cirks_btn = tk.Button(btn_frame, text="Klasiskais Cirks", font=("Helvetica", 14, "bold"),
                              bg="#5cb85c", fg="white", padx=15, pady=8,
                              command=lambda: [self.play_sound("button.mp3"), self.display_statistika("regular")])
        turnirs_btn = tk.Button(btn_frame, text="Cirku Turnīrs", font=("Helvetica", 14, "bold"),
                                bg="#f0ad4e", fg="white", padx=15, pady=8,
                                command=lambda: [self.play_sound("button.mp3"), self.display_statistika("tournament")])
        cirks_btn.grid(row=0, column=0, padx=15)
        turnirs_btn.grid(row=0, column=1, padx=15)
        container = tk.Frame(self.statistika_frame, bg="#F0F8FF")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        canvas = tk.Canvas(container, bg="#F0F8FF", highlightthickness=0, width=520)
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.stat_table_frame = tk.Frame(canvas, bg="#F0F8FF")
        canvas.create_window((0, 0), window=self.stat_table_frame, anchor="nw")
        self.stat_table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        headers = ["Pozīcija", "Dalībnieks", "Spēles", "Uzvaras", "Attiecība"]
        for col, header in enumerate(headers):
            lbl = tk.Label(self.stat_table_frame, text=header, font=("Helvetica", 14, "bold"),
                           bg="#D3E4CD", fg="#003300", borderwidth=1, relief="solid", padx=5, pady=5)
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        for col in range(len(headers)):
            self.stat_table_frame.grid_columnconfigure(col, weight=1)
        self.current_stat_mode = "regular"
        self.display_statistika("regular")
        back_btn = tk.Button(self.statistika_frame, text="← Atpakaļ", font=("Helvetica", 14, "bold"),
                             bg="#337ab7", fg="white", padx=15, pady=8,
                             command=lambda: [self.play_sound("button.mp3"), self.back_to_menu_from_statistika()])
        back_btn.pack(pady=(10, 20))

    def display_statistika(self, mode):
        for widget in self.stat_table_frame.winfo_children():
            info = widget.grid_info()
            if info.get("row", 0) != 0:
                widget.destroy()
        def sort_key(item):
            data = item[1]
            if mode == "regular":
                wins = data.get("regular_wins", 0)
                games = data.get("regular_games", 0)
            else:
                wins = data.get("tournament_wins", 0)
                games = data.get("tournament_games", 0)
            ratio = wins / games if games > 0 else 0
            return (wins, ratio)
        stats = {name: data for name, data in self.player_stats.items() if not name.startswith("Dators")} if hasattr(self, "player_stats") else {}
        sorted_stats = sorted(stats.items(), key=sort_key, reverse=True)
        if not sorted_stats:
            lbl = tk.Label(self.stat_table_frame, text="Nav pieejamu datu.", font=("Helvetica", 13),
                           bg="white", fg="#333333", padx=5, pady=5)
            lbl.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=1, pady=1)
        else:
            for i, (name, data) in enumerate(sorted_stats, start=1):
                if mode == "regular":
                    games = data.get("regular_games", 0)
                    wins = data.get("regular_wins", 0)
                    ratio = wins / games if games > 0 else 0
                else:
                    games = data.get("tournament_games", 0)
                    wins = data.get("tournament_wins", 0)
                    ratio = wins / games if games > 0 else 0
                values = [str(i), name, str(games), str(wins), f"{ratio:.2f}"]
                for col, val in enumerate(values):
                    lbl = tk.Label(self.stat_table_frame, text=val, font=("Helvetica", 13),
                                   bg="white", fg="#333333", borderwidth=1, relief="solid", padx=5, pady=5)
                    lbl.grid(row=i, column=col, sticky="nsew", padx=1, pady=1)
                    if i == 1:
                        lbl.config(fg="#FF8C00")
                    elif i == 2:
                        lbl.config(fg="#4682B4")
                    elif i == 3:
                        lbl.config(fg="#8B4513")
        for col in range(5):
            self.stat_table_frame.grid_columnconfigure(col, weight=1)

    # === NEW: Settings (Iestatījumi) Window Methods ===
    def show_iesatijumi(self, mode="start"):
        if mode == "start":
            # Hide the start menu frame
            self.setup_frame.pack_forget()
            # Create a new settings frame in the main window
            self.iesatijumi_frame = tk.Frame(self.root, bg="#F0F8FF", bd=2, relief="groove")
            self.iesatijumi_frame.pack(padx=30, pady=30, fill="both", expand=True)
        
            title = tk.Label(self.iesatijumi_frame, text="Iestatījumi", font=("Helvetica", 18, "bold"), bg="#F0F8FF")
            title.pack(pady=(10,10))
        
            # Volume slider section.
            volume_frame = tk.Frame(self.iesatijumi_frame, bg="#F0F8FF")
            volume_frame.pack(pady=10)
            vol_label = tk.Label(volume_frame, text="Skaļums:", font=("Helvetica", 14), bg="#F0F8FF")
            vol_label.pack(side=tk.LEFT, padx=5)
            self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                                        command=self.update_volume, bg="#F0F8FF")
            self.volume_slider.set(self.volume)
            self.volume_slider.pack(side=tk.LEFT)
        
            # Buttons section.
            btn_frame = tk.Frame(self.iesatijumi_frame, bg="#F0F8FF")
            btn_frame.pack(pady=20)
            turnoff_btn = tk.Button(btn_frame, text="Izslēgt programmu", font=("Helvetica", 14, "bold"),
                                    bg="#d9534f", fg="white", padx=10, pady=5, 
                                     command=lambda: [self.play_sound("button.mp3"), self.confirm_exit()])
            turnoff_btn.pack(side=tk.LEFT, padx=10)
            return_btn = tk.Button(btn_frame, text="Atgriezties", font=("Helvetica", 14, "bold"),
                                bg="#5cb85c", fg="white", padx=10, pady=5,
                                 command=lambda: [self.play_sound("button.mp3"), self.close_iesatijumi_start()])
            return_btn.pack(side=tk.LEFT, padx=10)
        else:
            # Existing logic for gameplay mode settings 
            if hasattr(self, 'iesatijumi_frame') and self.iesatijumi_frame and self.iesatijumi_frame.winfo_exists():
                return

            self.iesatijumi_frame = tk.Toplevel(self.root)
            self.iesatijumi_frame.title("Iestatījumi")
            self.iesatijumi_frame.geometry("600x300")
            self.iesatijumi_frame.resizable(False, False)
            frame = tk.Frame(self.iesatijumi_frame, bg="#F0F8FF", bd=2, relief="groove")
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            title = tk.Label(frame, text="Iestatījumi", font=("Helvetica", 18, "bold"), bg="#F0F8FF")
            title.pack(pady=(10,10))

            volume_frame = tk.Frame(frame, bg="#F0F8FF")
            volume_frame.pack(pady=10)
            vol_label = tk.Label(volume_frame, text="Skaļums:", font=("Helvetica", 14), bg="#F0F8FF")
            vol_label.pack(side=tk.LEFT, padx=5)
            self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                                      command=self.update_volume, bg="#F0F8FF")
            self.volume_slider.set(self.volume)
            self.volume_slider.pack(side=tk.LEFT)

            btn_frame = tk.Frame(frame, bg="#F0F8FF")
            btn_frame.pack(pady=20)
            ret_btn = tk.Button(btn_frame, text="Atgriezties uz sākumu", font=("Helvetica", 14, "bold"),
                                bg="#5cb85c", fg="white", padx=10, pady=5,
                                command=lambda: [self.play_sound("button.mp3"), self.confirm_game_end()])
            ret_btn.pack(side=tk.LEFT, padx=10)
            cont_btn = tk.Button(btn_frame, text="Turpināt spēli", font=("Helvetica", 14, "bold"),
                                 bg="#337ab7", fg="white", padx=10, pady=5,
                                 command=lambda: [self.play_sound("button.mp3"), self.close_iesatijumi_game()])
            cont_btn.pack(side=tk.LEFT, padx=10)
            
    def update_volume(self, val):
        self.volume = int(val)

    def show_confirm_in_frame(self, title, message, on_confirm, on_cancel):
        """
        Replaces the content of the current settings frame with a confirmation dialog.
        on_confirm: callback to execute if the user confirms.
        on_cancel: callback to execute if the user cancels.
        """
        # Clear existing content in the settings frame.
        for widget in self.iesatijumi_frame.winfo_children():
            widget.destroy()

        # Create a title label.
        title_lbl = tk.Label(self.iesatijumi_frame, text=title,
                            font=("Helvetica", 18, "bold"), bg="#F0F8FF")
        title_lbl.pack(pady=(20, 10))

        # Create a message label.
        msg_lbl = tk.Label(self.iesatijumi_frame, text=message,
                        font=("Helvetica", 12), bg="#F0F8FF")
        msg_lbl.pack(pady=10, padx=20)

        # Create a button frame.
        btn_frame = tk.Frame(self.iesatijumi_frame, bg="#F0F8FF")
        btn_frame.pack(pady=10)

        # "Yes" button.
        yes_btn = tk.Button(btn_frame, text="Jā", font=("Helvetica", 12, "bold"),
                            bg="#5cb85c", fg="white", padx=10, pady=5,
                            command=on_confirm)
        yes_btn.pack(side=tk.LEFT, padx=10)

        # "No" button uses the new _handle_cancel to destroy the frame before calling on_cancel.
        no_btn = tk.Button(btn_frame, text="Nē", font=("Helvetica", 12, "bold"),
                        bg="#d9534f", fg="white", padx=10, pady=5,
                        command=lambda: self._handle_cancel(on_cancel))
        no_btn.pack(side=tk.LEFT, padx=10)


    def _handle_cancel(self, on_cancel):
        if self.iesatijumi_frame:
            self.iesatijumi_frame.destroy()
            self.iesatijumi_frame = None
        on_cancel()

    def confirm_exit(self):
        def do_exit():
            # Confirmed: exit the application.
            self.root.destroy()

        def cancel_exit():
            # Cancelled: restore the original start settings view.
            self.show_iesatijumi(mode="start")

        self.show_confirm_in_frame("Apstiprinājums",
                                    "Vai tiešām vēlies izslēgt programmu?",
                                    do_exit, cancel_exit)


    def close_iesatijumi_start(self):
        if hasattr(self, "iesatijumi_frame") and self.iesatijumi_frame:
            self.iesatijumi_frame.destroy()
            self.iesatijumi_frame = None
        self.setup_frame.pack(padx=10, pady=10)

        # New: Close settings in game mode (do not reopen start menu)
    def close_iesatijumi_game(self):
        if hasattr(self, "iesatijumi_frame") and self.iesatijumi_frame:
            self.iesatijumi_frame.destroy()
            self.iesatijumi_frame = None
        # Only show the start menu if we are not in a game.
        if not hasattr(self, "in_game") or not self.in_game:
            self.setup_frame.pack(padx=10, pady=10)


    def confirm_game_end(self):
        def do_end_game():
            # Confirmed: destroy game/tournament frames and reset all game state.
            if self.iesatijumi_frame:
                self.iesatijumi_frame.destroy()
                self.iesatijumi_frame = None
            if hasattr(self, "game_frame") and self.game_frame:
                self.game_frame.destroy()
                self.game_frame = None
            if hasattr(self, "tournament_frame") and self.tournament_frame:
                self.tournament_frame.destroy()
                self.tournament_frame = None
            # Reset state flags and tournament-related variables.
            self.in_game = False
            self.dice_on_cooldown = False
            self.animating = False
            self.tournament_winners = []
            self.tournament_nonfinalists_left = []
            self.tournament_nonfinalists_right = []
            self.tournament_placement = []
            self.final_round_started = False
            # Return to start menu.
            self.setup_frame.pack(padx=10, pady=10)
        def cancel_end_game():
            # Cancelled: restore the settings content for game mode.
            self.show_iesatijumi(mode="game")
        self.show_confirm_in_frame("Apstiprinājums",
                                    "Vai tiešām vēlies beigt spēli un atgriezties uz sākumu?",
                                    do_end_game, cancel_end_game)


    def metKaulinAtteli(self, dice_value):
        dice_files = ["dice1.png", "dice2.png", "dice3.png", "dice4.png", "dice5.png", "dice6.png"]
        img = Image.open(dice_files[dice_value - 1])
        w, h = img.size
        new_w, new_h = int(w * 0.5), int(h * 0.5)
        img = img.resize((new_w, new_h))
        return ImageTk.PhotoImage(img)

    def spelKaulinAtteli(self, color):
        pawn_files = {"indianred": "red_pawn.png", "blue": "blue_pawn.png",
                      "green": "green_pawn.png", "gold": "yellow_pawn.png",
                      "purple": "purple_pawn.png", "cyan": "cyan_pawn.png",
                      "orange": "orange_pawn.png", "pink": "pink_pawn.png"}
        img = Image.open(pawn_files[color])
        orig_w, orig_h = img.size
        scale = min((self.tile_width * 0.7) / orig_w, (self.tile_height * 0.7) / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def spelKaulinAtteli_tournament(self, color, board):
        pawn_files = {"indianred": "red_pawn.png", "blue": "blue_pawn.png",
                      "green": "green_pawn.png", "gold": "yellow_pawn.png",
                      "purple": "purple_pawn.png", "cyan": "cyan_pawn.png",
                      "orange": "orange_pawn.png", "pink": "pink_pawn.png"}
        img = Image.open(pawn_files[color])
        orig_w, orig_h = img.size
        scale = min((board["tile_width"] * 0.7) / orig_w, (board["tile_height"] * 0.7) / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def atjaunotFiguruPozicijas(self):
        pawns_by_tile = {}
        for speletajs in self.speletaji:
            tile = speletajs["laukums"]
            pawns_by_tile.setdefault(tile, []).append(speletajs)
        for tile, pawns in pawns_by_tile.items():
            center_x, center_y = self.iegutFlizesCentru(tile)
            if len(pawns) == 1:
                self.canvas.coords(pawns[0]["figura_id"], center_x, center_y)
            else:
                import math
                radius = min(self.tile_width, self.tile_height) * 0.3
                angle_step = 2 * math.pi / len(pawns)
                for index, speletajs in enumerate(pawns):
                    angle = index * angle_step
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    self.canvas.coords(speletajs["figura_id"], x, y)

    def iegutFlizesCentru(self, tile):
        row = (tile - 1) // self.columns
        pos_in_row = (tile - 1) % self.columns
        col = pos_in_row if row % 2 == 0 else self.columns - 1 - pos_in_row
        x = col * self.tile_width + self.tile_width / 2
        y = self.board_height - (row * self.tile_height + self.tile_height / 2)
        return x, y

    def atjaunotInfoEtiketi(self):
        if self.aktiviSpeletaji:
            aktSpeletajs = self.speletaji[self.aktiviSpeletaji[self.aktualaisIndekss]]
            info = f"Piešķirtā kārta: {aktSpeletajs['vards']}"
            self.info_label.config(text=info, fg=aktSpeletajs["krasa"], bd=2, relief="ridge", bg="silver", width=30)
            if not aktSpeletajs.get("human", True):
                self.root.after(1000, self.metKaulinu)
        else:
            self.info_label.config(text="Spēles beigas!", fg="black")
        self.atjaunotRezLapu()

    def atjaunotRezLapu(self):
        for i, speletajs in enumerate(self.speletaji):
            text = f"{speletajs['vards']}: Plāksne {speletajs['laukums']}"
            bg = "silver"
            if self.aktiviSpeletaji and i == self.aktiviSpeletaji[self.aktualaisIndekss]:
                bg = "floralwhite"
            try:
                self.score_labels[i].config(text=text, bg=bg)
            except Exception:
                pass
