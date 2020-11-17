from Lab5.Grammar import Grammar


class ParserRecursiveDescend:
    def __init__(self):
        self.grammar = Grammar("g1.txt")
        self.work = []
        self.input = []
        self.state = "q"
        self.index = 1

    def expand(self):
        nonterminal = self.input.pop()
        self.work.append((nonterminal, 0))
        self.input.append(self.grammar.getProductions()[nonterminal][0])

    def advance(self):
        self.work.append(self.input.pop())
        self.index += 1

    def momentaryInsuccess(self):
        self.state = "b"

    def back(self):
        self.input.append(self.work.pop())
        self.index -= 1

    def success(self):
        self.state = "f"
        self.index += 1
    