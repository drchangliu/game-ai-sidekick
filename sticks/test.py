import unittest
from sticks import Sticks_Game

class Test_Sticks_Game(unittest.TestCase):
    def test_new_game(self):
        game = Sticks_Game()
        self.assertEqual(game.turn, 0)
        self.assertEqual(game.p1, [1, 1])
        self.assertEqual(game.p2, [1, 1])

    def test_state(self):
        game = Sticks_Game("1234")
        state = game.state()
        self.assertEqual(state, "1234")
        game.turn += 1
        state = game.state()
        self.assertEqual(state, "3412")

    def test_attack(self):
        game = Sticks_Game()
        game.move("A:A C") # p1 attack p2
        self.assertEqual(game.p2, [2, 1])
        game.move("A:A C") # p2 attack p1
        self.assertEqual(game.p1, [3, 1])
        game.move("A:A C") # p1 attack p2
        self.assertEqual(game.p2, [0, 1])

    def test_split(self):
        game = Sticks_Game("0404")
        game.move("S:B") # p1
        self.assertEqual(game.p1, [2, 2])
        game.move("S:B") # p2
        self.assertEqual(game.p2, [2, 2])

    def test_is_over(self):
        game = Sticks_Game("4444")
        self.assertFalse(game.is_over())
        game.move("A:A D")
        self.assertFalse(game.is_over())
        game.move("A:A D")
        self.assertFalse(game.is_over())
        game.move("A:A C")
        self.assertTrue(game.is_over())

    def test_attack_is_legal(self):
        # Cant attack nothing
        game = Sticks_Game("3130")
        self.assertFalse(game.is_legal("A:A D"))
        self.assertFalse(game.is_legal("A:B D"))

        # Normal attack rules
        self.assertTrue(game.is_legal("A:A C"))
        self.assertTrue(game.is_legal("A:B C"))

        # Cant attack with nothing
        game = Sticks_Game("0133")
        self.assertFalse(game.is_legal("A:A C"))
        self.assertFalse(game.is_legal("A:A D"))

        # Cant attack when game is over
        game = Sticks_Game("0011")
        self.assertFalse(game.is_legal("A:A D"))
        self.assertFalse(game.is_legal("A:B D"))
        self.assertFalse(game.is_legal("A:A C"))
        self.assertFalse(game.is_legal("A:B C"))

    def test_split_is_legal(self):
        # Normal usage
        game = Sticks_Game("4020")
        self.assertTrue(game.is_legal("S:A"))
        game.turn += 1
        self.assertTrue(game.is_legal("S:A"))

        # Cant split with non-zero other hand
        game = Sticks_Game("1412")
        self.assertFalse(game.is_legal("S:B"))
        game.turn += 1
        self.assertFalse(game.is_legal("S:B"))
        
        # Cant split odd numbers
        game = Sticks_Game("3101")
        self.assertFalse(game.is_legal("S:A"))
        self.assertFalse(game.is_legal("S:B"))
        
        # Cant split nothing
        game = Sticks_Game("1010")
        self.assertFalse(game.is_legal("S:B"))
        
        # Cant split when game is over
        game = Sticks_Game("4000")
        self.assertFalse(game.is_legal("S:A"))

    def test_sanity(self):
        self.assertTrue(True)
        self.assertFalse(False)

if __name__ == "__main__":
    unittest.main()
