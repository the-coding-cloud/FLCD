from Lab5.Grammar import Grammar


class ParserRecursiveDescend:
    #input must be reversed for the pop to work
    # such that the expansion of the work stack to be ___appended___ in the input list
    def __init__(self, grammarTextLocation):
        self.grammar = Grammar(grammarTextLocation)
        self.work = []
        self.input = []
        self.state = "q"
        self.index = 0
        self.debug = True

    def printParserStep(self):
        print("~~~~~~~~~~~~")
        print(self.state)
        print(self.index)
        print(self.work)
        print(self.input)

    def expand(self):
        nonterminal = self.input.pop(0)
        self.work.append((nonterminal, 0))
        a = self.grammar.getProductions()[nonterminal][0]
        self.input = a +  self.input
        if self.debug:
            self.printParserStep()

    def advance(self):
        self.work.append(self.input.pop(0))
        self.index += 1
        if self.debug:
            self.printParserStep()
    def momentaryInsuccess(self):
        self.state = "b"
        if self.debug:
            self.printParserStep()
    def back(self):
        self.input.append(self.work.pop())
        self.index -= 1
        if self.debug:
            self.printParserStep()
    def success(self):
        self.state = "f"
        self.index += 1
        if self.debug:
            self.printParserStep()
    def anotherTry(self):
        if self.debug:
            self.printParserStep()
        if self.index == 0 and self.work[len(self.work)-1][0] == self.grammar.getStartSymbol():
            raise Exception("ERROR")
        (currentNonTerm,nonTermIndex) = self.work.pop()
        currentNonTermProductions = self.grammar.getProductions()[currentNonTerm]
        if len(currentNonTermProductions)-1 > nonTermIndex:
            self.state = "q"
            self.work.append((currentNonTerm,nonTermIndex+1))
            #self.input.pop()  #handle this better, just one terminal will pop, not the whole non terminal expansion
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            aux = currentNonTermProductions[nonTermIndex + 1]
            self.input = aux + self.input
        else:
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            self.input = [currentNonTerm] + self.input


    def run(self, w):
        self.state = "q"
        self.index = 0
        self.work = []
        self.input= [self.grammar.getStartSymbol()]
        while self.state != "t" and self.state != "e":
            if self.state == "q":
                #Done condition
                if len(self.input) == 0 and self.index == len(w):
                    self.state = "t"
                else:
                    #expand condition, top of beta is non terminal
                    if self.input[0] in self.grammar.getNonTerminals():
                        self.expand()
                    #advance condition, top of beta is terminal and it matches the index of the w
                    elif self.input[0] in self.grammar.getTerminals() and self.input[0] == w[self.index]:
                        self.advance()
                    #Woopsie -> we have a momentary insuccess
                    else :
                        self.momentaryInsuccess()
            else:
                if self.state == "b":
                    #back
                    if self.work[len(self.work)-1] in self.grammar.getTerminals():
                        self.back()
                    #anotherTry
                    else:
                        self.anotherTry()
        if self.state == "e":
            print("ERROR")
        else:
            print("Sequence accepted")
            print(self.work, self.input, self.index)






p = ParserRecursiveDescend("g1.text")
p.run(['a','a','c','b','c'])
