###########################
# FILE: boggle.py
# WRITER: michal ivianski , michaliv , 207182452
#         maya kedem, maya_kedem, 209544121
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A program that runs Boggle game using GUI.
# WEB PAGES I USED: https://katzr.net/9da5f0
#                   https://katzr.net/d47847
##########################

from boggle_gui import BoggleGui
from boggle_logic import BoggleLogic
from ex12_utils import *

class BoggleController:
    """
    The class which runs the game of Boggle
    """
    def __init__(self, words_dict):
        """
        the constructor of Boggle game
        :param words_dict: a dict of all valid words of the game
        """
        # creates gui and logic objects:
        self._gui = BoggleGui(self.activate_buttons,
                              self.restart_button,
                              self.create_check_word_action)
        self._logic = BoggleLogic()

        self._words_dict = words_dict
        self._board = self._gui.get_existing_board()
        self._words_that_were_found = self._logic.get_found_words()
        self.pressed = []
        self._buttons = self._gui.get_buttons_dict()


    def activate_buttons(self):
        """
        activates the buttons which represent the board and the check word
        buttons
        :return:
        """
        for button_object, button_deatils in self._buttons.items():
            action = self.create_button_action(button_deatils[0],
                                               button_deatils[1],
                                               button_object)
            self._gui.set_button_command(button_object, action)

        check_action = self.create_check_word_action()
        self._gui.set_check_word_button_command(check_action)

    def create_button_action(self, button_name, button_coords, button_object):
        """
        creates the command which the buttons which are the board perform
        after being pressed
        :param button_name: the char on the button
        :param button_coords: the coord on the board which belongs to button
        :param button_object: the button object
        :return: the func which is the command
        """
        def func():
            self._logic.type_in(button_name)
            self._gui.set_word_to_check(self._logic.get_display())
            self.pressed.append(button_coords)
            button_object["state"] = "disabled"
        return func

    def create_check_word_action(self):
        """
        creates the action the check word button performs
        :return: the func which is the command
        """
        def func():
            the_word = self._logic.get_display()
            self._board = self._gui.get_existing_board()

            # checks if the word pressed by the user is a valid word:
            if self.check_if_word_is_valid(self._board, self.get_coords(),
                                           self._words_dict):
                # checks if he didn't find this word before:
                if the_word not in self._words_that_were_found:
                    self.the_word_is_valid(the_word)
                else: # word was already found
                    self._logic.set_display_to_word_repetition()
                    self._gui.set_word_to_check(self._logic.get_display())
            else: # invalid word
                self._logic.set_disaplay_to_error()
                self._gui.set_word_to_check(self._logic.get_display())

            # resets all boards so a new word could be guessed:
            self.pressed = []
            self._gui.reset_board()
            self._logic.do_clear()

            # makes buttons that were pressed active again:
            for button_object in self._buttons.keys():
                button_object["state"] = "normal"

        return func

    def the_word_is_valid(self, the_word):
        """
        is given the word that wad approved to be valid and performs all the
        actions accordingly
        :param the_word: the valid word the player found
        :return: None
        """
        points_to_add = len(the_word) ** 2
        self._logic.set_points(points_to_add)
        self._gui.set_points(self._logic.get_points())
        self._logic.add_word_to_board(the_word)
        self._gui.set_words_found_canvas \
            (self._words_that_were_found)
        self._logic.do_clear()
        self._gui.set_word_to_check(self._logic.get_display())


    def check_if_word_is_valid(self, board, path, words):
        """
        is given a word guessed by the user and it's path and checks if it's
        valid using an helper function.
        :param board: board object of the game
        :param path: the path of the word (coords on the board)
        :param words: the dict of all possible words
        :return:
        """
        if is_valid_path(board, path, words):
            return True
        else:
            return False

    def get_coords(self):
        """
        returns the coords of a word being guessed by the used
        :return: a list of coords (tuples)
        """
        return self.pressed

    def restart_button(self):
        """
        sets the action the restart button performs
        :return: None
        """
        action = self.clear_game()
        self._gui.set_restart_command(action)

    def clear_game(self):
        """
        the action of the restart buttons- cleares all elemants of the game
        :return: the func which is the command of the restart button
        """
        def func():
            self._gui.set_state_to_false()
            self._logic.reset_all()
            self._gui.set_points(self._logic.get_points())
            self._gui.set_word_to_check(self._logic.get_display())
            self._gui.set_words_found_canvas(self._logic.get_found_words())
            self._gui.create_countdown()
            self._gui.clear_board()
            self._board = self._gui.get_existing_board()
            self._words_that_were_found = self._logic.get_found_words()
            self.pressed = []
            self._buttons = self._gui.get_buttons_dict()
        return func

    def run(self):
        """
        runs the game
        :return: None
        """
        self._gui.run()


if __name__ == '__main__':
    words_dict = load_words_dict("boggle_dict.txt")
    bog = BoggleController(words_dict)
    bog.run()