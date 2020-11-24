from Lab5.Grammar import Grammar


class ParserRecursiveDescend:
    #input must be reversed for the pop to work
    # such that the expansion of the work stack to be ___appended___ in the input list
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

    def anotherTry(self):
        if self.index == 1 and self.work[len(self.work)-1][0] == self.grammar.getStartSymbol():
            raise Exception("ERROR")
        currentNonTerm,nonTermIndex = self.work.pop()
        currentNonTermProductions = self.grammar.printProductionsForNonTerminal(currentNonTerm)
        if len(currentNonTermProductions)-1 > nonTermIndex:
            self.state = "q"
            self.work.append((currentNonTerm,nonTermIndex+1))
            #self.input.pop()  #handle this better, just one terminal will pop, not the whole non terminal expansion
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop()
            self.input.append(currentNonTermProductions[nonTermIndex])
        else:
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop()
            self.input.append(currentNonTerm)

