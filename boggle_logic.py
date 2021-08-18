###########################
# FILE: boggle.py
# WRITER: michal ivianski , michaliv , 207182452
#         maya kedem, maya_kedem, 209544121
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A program that runs Boggle game using GUI.
# WEB PAGES I USED: https://katzr.net/9da5f0
#                   https://katzr.net/d47847
##########################
class BoggleLogic():
    """
    a class which is responsible for the logic behind the Boggle game
    """
    CURRRENT_DISPLAY = ""
    FOUND_WORDS = []
    point_count = 0

    INVALID_WORD = "Invalid word, try again!"
    WORD_REP = "Oops, already found this word, try again!"

    def __init__(self):
        pass

    def get_display(self):
        """
        returns what appears in the display board (the word which is being
        typed by the user)
        :return: what appears in the display board
        """
        return self.CURRRENT_DISPLAY

    def type_in(self, char):
        """
        is given a char to add to the display board and adds it to the existing
        data
        :param char: a char to add
        :return: None
        """
        self.CURRRENT_DISPLAY += char

    def set_disaplay_to_error(self):
        """
        sets the display to a message which indicates the user tried to insert
        an invalid word
        :return: None
        """
        self.CURRRENT_DISPLAY = self.INVALID_WORD

    def set_display_to_word_repetition(self):
        """
        sets the display to a message which indicates the user tried to insert
        a word he already guessed before
        :return: None
        """
        self.CURRRENT_DISPLAY = self.WORD_REP

    def do_clear(self):
        """
        clears the display board
        :return: None
        """
        self.CURRRENT_DISPLAY = ""

    def get_found_words(self):
        """
        returns what appears on the words that were found board
        :return: what appears on the words that were found board
        """
        return self.FOUND_WORDS

    def add_word_to_board(self, word):
        """
        is given a word to add to the board which contains all the words that
        were found
        :param word: a word to add
        :return: None
        """
        self.FOUND_WORDS += [word]

    def set_points(self, points):
        """
        sets the point count of the game
        :param points: points to add to the point count
        :return: None
        """
        self.point_count += points

    def get_points(self):
        """
        returns the current point count of the game
        :return: the current points
        """
        return self.point_count

    def reset_all(self):
        """
        resets all data of the game
        :return: None
        """
        self.point_count = 0
        self.FOUND_WORDS = []
        self.CURRRENT_DISPLAY = ""

