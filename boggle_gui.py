###########################
# FILE: boggle.py
# WRITER: michal ivianski , michaliv , 207182452
#         maya kedem, maya_kedem, 209544121
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A program that runs Boggle game using GUI.
# WEB PAGES I USED: https://katzr.net/9da5f0
#                   https://katzr.net/d47847
##########################
import tkinter as tk
from ex12_utils import all_coords
from boggle_board_randomizer import randomize_board

class BoggleGui:
    """
    The class which creates the GUI elements of the game
    """

    # color palettes:
    BUTTON_COLOR = "#3c8c9e"
    BUTTON_ACTIVE_COLOR = "#0980ab"
    CHECK_BUTTON_COLOR = "#c2f2fc"
    DISPLAY_BARS_COLOR = "#bdbebf"
    OUTER_FRAME_COLOR = "#879ded"
    MINI_CANVAS_COLOR = "#a3cfc9"

    BUTTON_STYLE = {"font": ("Cambria", 20), "borderwidth": 1, "relief":
        tk.RAISED, "bg": BUTTON_COLOR, "activebackground": BUTTON_ACTIVE_COLOR}

    # storing class data:
    WORDS_FOUND = []

    CUR_WORD = ""

    buttons_dict = {}

    # text messages:
    INVALID_WORD = "Invalid word, try again!"
    WORD_REP = "Oops, already found this word, try again!"
    RULES = "1. A valid word is between 3 to 16 characters. \n" \
            "2. If you choose a letter, the next letter could be only in the" \
            " 8 cubes which are next to this letter in order for the word " \
            "to be valid. \n" \
            "3. You have 3 minutes to find as many words as possible. \n"\
            "4. You get the power of 2 to the length of the word you found " \
            "points. \n" \
            "5. You don't get points for a word if you already found it. \n" \
            "6. Every new round the points count goes back to zero. \n" \
            "7. ENJOY!"

    def __init__(self,activate_func, restart_activate, check_word_activate):
        """
        The constructor of the GUI object of the game
        :param activate_func: a function which activates the buttons
        :param restart_activate: a function which activates the restart button
        :param check_word_activate: a function which activates the check word
        button
        """
        root = tk.Tk()
        root.title("Boggle Game")
        root.resizable(False, False)
        self._board = randomize_board()
        self._main_window = root
        self.activate = activate_func
        self.restart_activate = restart_activate
        self.check_word_activate = check_word_activate

        self._pointscount = 0

        # creates the display:
        self._outer_frame = tk.Frame(root, bg=self.OUTER_FRAME_COLOR,
                                     highlightbackground=self.OUTER_FRAME_COLOR,
                                     highlightthickness=5)
        self._outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._display_label = tk.Label(root, font=("Castellar", 25),
                                       bg=self.DISPLAY_BARS_COLOR, width=23,
                                       relief="ridge",
                                       text="BOGGLE GAME")
        self._display_label.pack(side=tk.TOP, fill=tk.BOTH)

        self._down_bar = tk.Label(root, font=("Courier", 30),
                                  bg=self.DISPLAY_BARS_COLOR, width=23,
                                  relief="ridge")
        self._down_bar.pack(side=tk.BOTTOM, fill=tk.BOTH)

        bg_image = tk.PhotoImage(file="codeblauw.png")

        self.label = tk.Label(root, height=500, width=500, image=bg_image)
        self.label.photo = bg_image
        self.label.pack(fill=tk.BOTH)

        self.mini_canvas = tk.Canvas(self.label, height=400, width=400,
                                     bg=self.BUTTON_COLOR)
        self.mini_canvas.place(relwidth=0.5, relheight=0.5, relx=0.5,
                               rely=0.5, anchor='c')

        self._points = tk.Label(self.label, font=(30),
                                bg=self.DISPLAY_BARS_COLOR, width=23,
                                relief="ridge",
                                text="Points: " + str(self._pointscount))
        self._points.place(relwidth=0.5, relheight=0.05, relx=0.5,
                           rely=0.02, anchor='n')

        self._cur_word = tk.Label(self.label, font=(10),
                                  bg=self.DISPLAY_BARS_COLOR,
                                  width=23, relief="ridge", text=self.CUR_WORD)
        self._cur_word.place(relwidth=0.5, relheight=0.1, relx=0.5, rely=0.1,
                             anchor='n')

        self._check_word = tk.Button(self.label, bg=self.CHECK_BUTTON_COLOR,
                                     activebackground=self.BUTTON_ACTIVE_COLOR,
                                     text="check word", width=8, height=4)
        self._check_word.place(relwidth=0.3, relheight=0.05, relx=0.5,
                               rely=0.2, anchor='n')

        self._words_found = tk.Label(self.label, font=(20),
                                     bg=self.DISPLAY_BARS_COLOR, width=23,
                                     relief="ridge")
        self._words_found.place(relwidth=0.8, relheight=0.2, relx=0.5,
                                rely=0.77, anchor='n')

        self._quit = tk.Button(self._display_label, text="Quit",
                               command=self.close_window)
        self._quit.place(relwidth=0.1, relheight=1, relx=0.9,
                           rely=0.02, anchor='n')

        self._rules = tk.Button(self._display_label, text="Rules",
                                 command=self.popup_window)
        self._rules.place(relwidth=0.1, relheight=1, relx=0.1,
                           rely=0.02, anchor='n')

        # variables of the countdown:
        self.state = False
        self.limit_minutes = 3
        self.limit_seconds = 0

        self.minutes = 3
        self.seconds = 0

        self.create_countdown()

    #####################################################################

    # creating the board and initializing the game:
    def create_a_new_board(self):
        """
        initizalizes a new board using a different function
        :return: a list of lists (4*4) which represents the board
        """
        return randomize_board()

    def get_existing_board(self):
        """
        returns the current board
        :return: the current board (a list of lists)
        """
        return self._board

    def create_board(self, board):
        """
        creates a matrix of buttons, each containing the char from the matching
        index in the board object which was randomized.
        :return: None
        """
        for i in range(4):
            tk.Grid.columnconfigure(self.mini_canvas, i, weight=1)
        for j in range(4):
            tk.Grid.rowconfigure(self.mini_canvas, j, weight=1)

        board_dict = all_coords(board)
        for coord, value in board_dict.items():
            self.create_button(value, coord[0], coord[1])

    def create_button(self, button_char, row, col):
        """
        creates a grid of buttons which is the board of the game.
        :param button_char: the char to appear on the button
        :param row: x coord
        :param col: y coord
        :return: None
        """
        button = tk.Button(self.mini_canvas, text=button_char,
                           **BoggleGui.BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, ipadx=16, ipady=4.4)

        self.buttons_dict[button] = [button_char, (row, col)]


        def button_pressed(event):
            button["bg"] = self.BUTTON_ACTIVE_COLOR

        button.bind("<Button-1>", button_pressed)


    def initialize_game(self):
        """
        creates a new board object in the game when a new round starts
        :return: None
        """
        self._board = self.create_a_new_board()
        self.create_board(self._board)

    def create_countdown(self):
        """
        creates a countdown clock
        :return: None
        """

        self.display = tk.Label(self._down_bar, height=30, width=30,
                                textvariable="", bg=self.DISPLAY_BARS_COLOR)
        self.display.config(text="00:00", font=("Castellar", 30))
        self.display.place(relwidth=1, relheight=1, relx=0.5, rely=0.1,
                           anchor='n')

        if self.state == False:
            self.start_button = \
                tk.Button(self.display, bg=self.BUTTON_COLOR,
                          activebackground=self.BUTTON_ACTIVE_COLOR,
                          text="Start", width=8, height=4,
                          command=self.start)
            self.start_button.place(relwidth=0.5, relheight=1, relx=0.25,
                                    rely=0.5,anchor='w')

        self.countdown()

    def countdown(self):
        """
        The function which displays the countdown
        :return: None
        """

        if self.state == True:
            if self.seconds < 10:
                if self.minutes < 10:
                    self.display.config(text="0%d : 0%d" % (self.minutes,
                                                            self.seconds))
                else:
                    self.display.config(text="%d : 0%d" % (self.minutes,
                                                           self.seconds))
            else:
                if self.minutes < 10:
                    self.display.config(text="0%d : %d" % (self.minutes,
                                                           self.seconds))
                else:
                    self.display.config(text="%d : %d" % (self.minutes,
                                                          self.seconds))

            if (self.minutes == 0) and (self.seconds == 0):
                self.display.config(text="Times up!")
                self.end_of_game()

            else:
                if self.seconds == 0:
                    self.minutes -= 1
                    self.seconds = 59
                else:
                    self.seconds -= 1

                self.display.after(1000, self.countdown)
        else:
            self.display.after(100, self.countdown)

    def start(self):
        """
        the command of the start buttons, initializes the game
        :return: None
        """
        if self.state == False:
            self.state = True
            self.minutes = self.limit_minutes # restart minute count
            self.seconds = self.limit_seconds # restart seconds count
            self.initialize_game()
            self.activate() # activate buttons board
            self.check_word_activate() # activate check word button
        self.start_button.destroy()

    def popup_window(self):
        """
        creates the popup window which is the rules of the game
        :return: None
        """
        window = tk.Toplevel()

        label = tk.Label(window, text=self.RULES)
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')

    #####################################################################

    # setters and getters of the labels and buttons:
    def set_points(self, points):
        """
        sets the points board and points count
        :param points: the updated point count of the player
        :return: None
        """
        self._points["text"] = "Points: " + str(points)
        self._pointscount = points

    def set_words_found_canvas(self, word):
        """
        sets the board which shows the words that were found
        :param word: the updated list of word that were found
        :return: None
        """
        words_found = ""
        for i in word:
            words_found += i + ", "
        self._words_found["text"] = words_found

    def set_word_to_check(self, char):
        """
        sets the text in the current word to check display
        :param char: the char to add to the display
        :return: None
        """
        self._cur_word["text"] = char
        if char == self.INVALID_WORD or char == self.WORD_REP:
            self._cur_word["fg"] = "red"
        else:
            self._cur_word["fg"] = "black"


    def set_button_command(self, button_object, cmd):
        """
        is given a button name and a command, find this button in the dict of
        all buttons and configures this command to it
        :param button_name: the name of the button
        :param cmd: the command to configure
        :return: None
        """
        for key, value in self.buttons_dict.items():
            if key == button_object:
                button_object.configure(command=cmd)

    def set_check_word_button_command(self, cmd):
        """
        sets the command which belongs to the check word button
        :param cmd: the command
        :return: None
        """
        self._check_word.config(command=cmd)

    def get_buttons_dict(self):
        """
        returns the dict of buttons
        :return: the dict of buttons
        """
        return self.buttons_dict

    #####################################################################
    # end of game:
    def reset_board(self):
        """
        resets all buttons which were pressed to their original color
        :return: None
        """
        for button in self.buttons_dict.keys():
            button["bg"] = self.BUTTON_COLOR

    def end_of_game(self):
        """
        when the time runs out, clears all the boards, creates a restart button
        and shows the player how many points he achieved.
        :return: None
        """
        self.create_restart_button()
        self._points["text"] = "Congrats! You scored " +\
                               str(self._pointscount) + " Points"
        self.set_word_to_check("")
        self.set_words_found_canvas("")
        self.clear_board()
        self.restart_activate()

    def create_restart_button(self):
        """
        creates the restart button when the countdown ends
        :return: None
        """
        self.restart_button = tk.Button(self.display, bg=self.BUTTON_COLOR,
                                      activebackground=self.BUTTON_ACTIVE_COLOR,
                                      text="Play again?", width=8, height=4)
        self.restart_button.place(relwidth=0.5, relheight=1, relx=0.25,
                                  rely=0.5, anchor='w')

    def set_restart_command(self, cmd):
        """
        sets the command of the restart button
        :param cmd: the command
        :return: None
        """
        if self.state == True:
            self.state = False
        self.restart_button["command"] = cmd

    def set_state_to_false(self):
        """
        sets the state(flag) to False
        :return: None
        """
        self.state = False

    def clear_board(self):
        """
        when the countdown ends, clears the buttons boards
        :return: None
        """
        for button_object in self.buttons_dict.keys():
            button_object["text"] = ""
            button_object["bg"] = self.BUTTON_COLOR
            button_object.bind("<Button-1>", "disabled")
            button_object.forget()

    def close_window(self):
        self._main_window.destroy()

    #####################################################################
    # run game:
    def run(self):
        """
        runs the mainloop of the game
        :return: None
        """
        self._main_window.mainloop()
