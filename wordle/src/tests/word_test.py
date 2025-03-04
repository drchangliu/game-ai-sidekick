from classes.Word import Word


def test_word_complete():
    # tests word_complete function
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")
    word_obj.add_letter("p")
    word_obj.add_letter("y")

    assert word_obj.word_complete() == True


def test_word_empty():
    # tests word_complete function
    word_obj = Word("happy", [], 0)

    assert word_obj.word_complete() == False


def test_word_incomplete():
    # tests word_complete function
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("b")
    word_obj.add_letter("p")
    word_obj.add_letter("p")
    word_obj.add_letter("y")

    assert word_obj.word_complete() == False


def test_word_add_letter_overflow():
    # Tests add letter function
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")
    word_obj.add_letter("p")
    word_obj.add_letter("y")
    word_obj.add_letter("y")

    # will not let more than 5 letters into a word
    assert word_obj.guessed_word == "HAPPY"


def test_word_add_letter_incomplete():
    # Tests the add letter function
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")

    assert word_obj.guessed_word == "HAP"  # sees that add letter only added 3 char


def test_word_delete_letter():
    # Tests the delete letter function
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")
    word_obj.add_letter("p")
    word_obj.add_letter("y")
    word_obj.delete_letter()

    # Sees that the char was deleted off the string.
    assert word_obj.guessed_word == "HAPP"
