###########################
# FILE: boggle.py
# WRITER: michal ivianski , michaliv , 207182452
#         maya kedem, maya_kedem, 209544121
# EXERCISE: intro2cs1 ex12 2021
# DESCRIPTION: A program that runs Boggle game using GUI.
# WEB PAGES I USED: https://katzr.net/9da5f0
#                   https://katzr.net/d47847
##########################
BOARD_LEN = 4

def load_words_dict(file_path):
    """
    is given a file path and returns a dict of all words in the file as keys,
    and True as their value
    :param file_path: a file which includes words
    :return: a dict of all words in the file as keys and True as value
    """
    words_dict = {}
    words = open(file_path)
    for word in words:
        the_word = word.strip()
        words_dict[the_word] = True
    words.close()
    return words_dict


def is_valid_path(board, path, words):
    """
    is given a path and checks if the word in this path on the board is a
    valid word from the words list
    :param board: a board item (a list of lists)
    :param path: a list of tuples which represents an optional path (_buttons)
    :param words: a dict of all optional words
    :return: the word if the path matches one, else- None
    """
    if check_path_validity(path): # if the indexes are next to each other
        check_word = create_word_from_path(path, board)
        if check_word in words:
            return check_word
        else:
            return None

def create_word_from_path(path, board):
    """
    is given a board and a path on the board (a list of indexes) and returns
    the word that is built from the letter in those indexes on the board
    :param path: a list of tuples representing a path on the board- following
    indexes
    :return: The word in those indexes on the board
    """
    check_word = ""
    for tup in path:
        row = tup[0]
        col = tup[1]
        if 0 <= row <= 3 and 0 <= col <= 3:
            letter = board[row][col]
            check_word += letter
    return check_word

def check_path_validity(path):
    """
    checks if the difference between the x coord and y coord of two following
    indexes is larger then one (in absolute rate). If it is, it's not a valid,
    so it returns None. Else- returns True.
    :param path: a list of tuples representing a path on the board- following
    indexes
    :return: True if valid, None otherwise
    """
    for i in range(len(path) - 1):
        if abs(path[i][0] - path[i + 1][0]) <= 1 and \
                abs(path[i][1] - path[i + 1][1]) <= 1:
            continue
        else:
            return None
    return True

def all_words_in_length(n, words):
    """
    is given an int (n) and a dict of words, and returns a list of all words in
    length of n from the dict
    :param n: an int representing the wanted length
    :param words: a dict of words
    :return: a list of all words in length of n from the dict
    """
    words_in_len = []
    for key in words.keys():
        if len(key) == n:
            words_in_len.append(key)
    return words_in_len

def all_coords(board):
    """
    is given a board item and returns a dict of all _buttons of board as keys and
    the letter in this coord as value
    :param board: a board item (list of lists)
    :return: a dict of all _buttons of the board as keys and the letters in this
    _buttons as values
    """
    all_coords_dict = {}
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            all_coords_dict[(i,j)] = board[i][j]
    return all_coords_dict

def find_length_n_words(n, board, words):
    """
    finds all words from words list which are in the length of n in the board
    :param n: an int representing needed length
    :param board: a board item
    :param words: a dict of words
    :return: a list of tuples- each tuples contains a word and a list of tuples
    which are the _buttons of this word in the board
    """
    # filter the words to only a list of words which are in the length of n:
    # if n >= 3 and n <= 16:
    words_in_correct_len = all_words_in_length(n, words)
    all_coordis = all_coords(board) # all _buttons of the board
    all_words = find_in_the_borad(words_in_correct_len, all_coordis)
    if all_words:
        return all_words
    else:
        return []


def check_the_word_created(one_list, word, all_coords_dict):
    """
    is given a list of tuples which represents a path, turns it to a word and
    checks if this word matches the given word.
    :param one_list:  a list of tuples which represents a path on the board
    :param word: the given word
    :param all_coords_dict: a dict of all _buttons of board as keys and their
    chars as value
    :return: True if matches, False otherwise
    """
    word_check = ""
    for coord in one_list:
        for key, value in all_coords_dict.items():
            if coord==key:
                word_check += value
    if word_check == word:
        return True
    else:
        return False

def find_in_the_borad(words, all_coords_dict):
    """
    is given all the words which are in the same length and returns only the
    words which appear on the board. an helper function to find_length_n_words
    :param words: a list of words in a certain length
    :param all_coords_dict:  a dict of all _buttons of board as keys and their
    chars as value
    :return: a list of tuples- each tuples contains a word and a list of tuples
    which are the _buttons of this word in the board
    """
    one_list = []
    final_list = []
    all_paths = []
    for word in words:
        for coord, letter in all_coords_dict.items():
            if word[0] in letter:
                # start searching from the first appearance of the first letter
                # in the word on the board:
                append_to_final_list(coord, word, all_coords_dict,
                                     one_list, all_paths, final_list)
            one_list = []
    return final_list

def append_to_final_list(coord, word, all_coords_dict, one_list, all_paths,
                         final_list):
    """
    uses an helper function to check if a word appears on the board, and if it
    does- adds the path of its' _buttons to the final list of paths
    :param coord: a coord on the board
    :param word: the given word to check if appears on the board
    :param all_coords_dict: a dict of all _buttons of board as keys and their
    chars as value
    :param one_list: a path to try
    :param all_paths: all paths of a given word in the board
    :param final_list: the list of all words that apper on the board and their
    path (_buttons)
    :return: None
    """
    _helper(coord[0], coord[1], word, 0, all_coords_dict,
            one_list + [(coord[0], coord[1])], all_paths)
    for a_list in all_paths:
        if check_the_word_created(a_list, word, all_coords_dict):
            path = (word, a_list)
            if path not in final_list:
                final_list.append(path)

def check_repetition(list):
    """
    checks if a given tuple appears more then once in a given path.
    :param list: a list of tuples
    :return: True if doesn't, False if does appear more than once
    """
    for tup in list:
        if list.count(tup) > 1:
            return False
    else:
        return True


def _helper(x, y, word, i, all_coords_dict, one_list, all_paths):
    """
    an helper function to find_in_the_board which uses recursion to find all
    paths of appearances of a given word in the board
    :param x: x coord
    :param y: y coord
    :param word: a word to search in the board
    :param i: a running index (used to run on the letters of the given word)
    :param all_coords_dict: a dict of all _buttons of board as keys and their
    chars as value
    :param one_list: the current path checked
    :param all_paths: a list of all paths of a given word
    :return: None
    """
    if (x,y) not in all_coords_dict.keys() or i > len(word): # invalid coord
        return

    # if the word created from the path is valid, append it to all_paths:
    if i == len(word) or \
            check_the_word_created(one_list, word, all_coords_dict)\
            and check_repetition(one_list):
        all_paths.append(one_list)
        return

    cur_coord = all_coords_dict[(x, y)]
    if word[i] in cur_coord:
        _helper(x + 1, y, word, i + len(cur_coord), all_coords_dict, one_list +
                [(x + 1, y)], all_paths)
        _helper(x, y + 1, word, i + len(cur_coord), all_coords_dict, one_list +
                [(x, y + 1)], all_paths)
        _helper(x - 1, y, word, i + len(cur_coord), all_coords_dict, one_list +
                [(x - 1, y)], all_paths)
        _helper(x, y - 1, word, i + len(cur_coord), all_coords_dict, one_list +
                [(x, y - 1)], all_paths)
        _helper(x + 1, y - 1, word, i + len(cur_coord),
                all_coords_dict, one_list + [(x + 1, y - 1)], all_paths)
        _helper(x - 1, y + 1, word, i + len(cur_coord),
                all_coords_dict, one_list + [(x - 1, y + 1)], all_paths)
        _helper(x - 1, y - 1, word, i + len(cur_coord),
                all_coords_dict, one_list + [(x - 1, y - 1)], all_paths)
        _helper(x + 1, y + 1, word, i + len(cur_coord),
                all_coords_dict, one_list + [(x + 1, y + 1)], all_paths)