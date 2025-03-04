import random

class Sticks_Game:
    def __init__(self, pos="1111"):
        self.turn = 0
        # Ex. "3124" -> p1 = [3, 1], p2 = [2, 4]
        self.p1 = [int(c) for c in pos[:2]]
        self.p2 = [int(c) for c in pos[2:]]
        self.history = ["Game start"]

    def state(self):
        # State is represented as a 4 digit number
        # Ex. 3124, This can be notated as ABCD
        # AB is the left (A), and right (B) hands of-
        # the player that is next to move
        # Ex. [3, 1], [2, 4] -> "31", "24"
        p1 = ''.join([str(s) for s in self.p1])
        p2 = ''.join([str(s) for s in self.p2])
        return p1 + p2 if self.is_p1() else p2 + p1

    def to_index(self, char):
        match char:
            case 'A': return 0
            case 'B': return 1
            case 'C': return 0
            case 'D': return 1
            case _: return 99

    def is_p1(self):
        return self.turn % 2 == 0

    def is_over(self):
        return all(x == 0 for x in self.p1) or all(x == 0 for x in self.p2)

    def is_legal(self, move):
        if self.is_over(): return False
        if not move or not isinstance(move, str): return False
        (type, tail) = move.split(":", maxsplit=1)
        if not type or not tail: return False
        match type:
            case 'A':
                splits = tail.split(maxsplit=1)
                if len(splits) < 2: return False
                (source, target) = splits
                source_i = self.to_index(source)
                target_i = self.to_index(target)
                if source_i < 0 or source_i > 1: return False
                if target_i < 0 or target_i > 1: return False
                if self.is_p1():
                    if self.p1[source_i] <= 0: return False
                    if self.p2[target_i] <= 0: return False
                else:
                    if self.p2[source_i] <= 0: return False
                    if self.p1[target_i] <= 0: return False
            case 'S':
                source_i = self.to_index(tail)
                if source_i < 0 or source_i > 1: return False
                target_i = 1 if source_i == 0 else 0
                if self.is_p1():
                    if self.p1[source_i] % 2 != 0: return False
                    if self.p1[target_i] != 0: return False
                else:
                    if self.p2[source_i] % 2 != 0: return False
                    if self.p2[target_i] != 0: return False
            case _:
                return False

        return True
    
    def move(self, move):
        prev = self.state()
        (type, tail) = move.split(":", maxsplit=1)
        match type:
            case 'A': # Attack
                (source, target) = tail.split(maxsplit=1)
                source_i = self.to_index(source)
                target_i = self.to_index(target)
                if self.is_p1():
                    sum = self.p2[target_i] + self.p1[source_i]
                    self.p2[target_i] = sum if sum < 5 else 0
                else:
                    sum = self.p1[target_i] + self.p2[source_i]
                    self.p1[target_i] = sum if sum < 5 else 0

            case 'S': # Split
                source_i = self.to_index(tail)
                target_i = 1 if source_i == 0 else 0
                if self.is_p1():
                    self.p1[source_i] //= 2
                    self.p1[target_i] += self.p1[source_i]
                else:
                    self.p2[source_i] //= 2
                    self.p2[target_i] += self.p2[source_i]

        # Update history
        self.turn += 1
        post = self.state()
        self.history.append(f'{self.turn}) [{prev}] {move} -> [{post}]')
        if self.is_over(): self.history.append(f"Game over, Player {"2" if self.is_p1() else "1"} Wins") # Game ends on losers turn, flip P1 and P2

def main():
    print(" ==== Sticks/Chopsticks Game ==== ")
    tutorial = input("Would you like a tutorial (y/n): ")
    if tutorial.lower() == "y":
        print(" === Description === ")
        print("Chopsticks is a turn-based game where players use finger counts to \nto eliminate both opponents' hands by making them exceed five fingers.\n")
        print(" === Moves === ")
        print(" == Attack (A) == \nUse: Attack an enemy hand, adding your hand count to theirs\nFormat: 'A:<Your Hand> <Enemy Hand>'\nExample: 'A:A C'")
        print(" == Split (S) == \nUse: Split even number of fingers between both hands\nFormat: 'S:<Your Hand>'\nExample: 'S:A'\n")
        input()
    game = Sticks_Game()
    # "A:A C" - Attack A to C -> C=C+A
    # "S:A"   - Split A       -> A=A/2 B=A/2
    while not game.is_over():
        # Player 1
        print("State: " + game.state())
        move = input("Player 1 Move: ")
        while not game.is_legal(move):
            print("Invalid move. Try again.")
            move = input("Player 1 Move: ")
        game.move(move)

        if game.is_over():
            break

        # Player 2
        print("State: " + game.state())
        move = input("Player 2 Move: ")
        while not game.is_legal(move):
            print("Invalid move. Try again.")
            move = input("Player 2 Move: ")
        game.move(move)


if __name__ == "__main__":
    main()
