from classes.Word import Word


def test_empty_word():
    word_obj = Word("", [], 0)

    assert word_obj.length() == 0


def test_half_word():
    word_obj = Word("hap", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")

    assert word_obj.length() == 3


def test_full_word():
    word_obj = Word("happy", [], 0)

    word_obj.add_letter("h")
    word_obj.add_letter("a")
    word_obj.add_letter("p")
    word_obj.add_letter("p")
    word_obj.add_letter("y")

    assert word_obj.length() == 5
