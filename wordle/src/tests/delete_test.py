from classes.Word import Word


def test_delete_letter_empty_word():
    # Test deleting a letter from an empty guessed word
    game = Word("", [], 0)
    game.add_letter(" ")
    game.locked = False
    game.delete_letter()
    assert game.guessed_word == ""


def test_delete_letter_locked_game():
    # Test to delete a letter when the game is locked should not work
    game = Word("tests", [], 0)
    game.add_letter("t")
    game.add_letter("e")
    game.add_letter("s")
    game.add_letter("t")
    game.add_letter("s")
    game.locked = True
    game.delete_letter()
    assert game.guessed_word == "TESTS"


def test_delete_letter_non_empty_word():
    # Test deleting all letters from a guessed word when the game is not locked
    game = Word("tests", [], 0)
    game.add_letter("t")
    game.add_letter("e")
    game.add_letter("s")
    game.add_letter("t")
    game.add_letter("s")
    game.locked = False
    game.delete_letter()
    game.delete_letter()
    game.delete_letter()
    game.delete_letter()
    game.delete_letter()
    assert game.guessed_word == ""
