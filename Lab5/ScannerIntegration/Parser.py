from Lab5.ScannerIntegration.Grammar import Grammar
from Lab5.ScannerIntegration.Scanner import Scanner

class ParserRecursiveDescend:
    # input must be reversed for the pop to work
    # such that the expansion of the work stack to be appended to the input list
    def __init__(self, grammarTextLocation):
        self.grammar = Grammar(grammarTextLocation)
        self.work = []
        self.input = []
        self.state = "q"
        self.index = 0
        self.debug = True
        self.tree = []

    def printParserStep(self, step):
        print("~~~~~~~~~~~~")
        print(step)
        print(self.state)
        print(self.index)
        print(self.work)
        print(self.input)

    def expand(self):
        nonTerminal = self.input.pop(0)
        self.work.append((nonTerminal, 0))
        a = self.grammar.getProductions()[nonTerminal][0]
        self.input = a + self.input
        if self.debug:
            self.printParserStep("expand")

    def advance(self):
        self.work.append(self.input.pop(0))
        self.index += 1
        if self.debug:
            self.printParserStep("advance")

    def momentaryInsuccess(self):
        self.state = "b"
        if self.debug:
            self.printParserStep("mom insuccess")

    def back(self):
        self.input = [self.work.pop()] + self.input
        self.index -= 1
        if self.debug:
            self.printParserStep("back")

    def success(self):
        self.state = "f"
        self.index += 1
        if self.debug:
            self.printParserStep("success")

    def anotherTry(self):
        if self.debug:
            self.printParserStep("another try")
        if self.index == 0 and self.work[len(self.work) - 1][0] == self.grammar.getStartSymbol():
            raise Exception("ERROR")

        (currentNonTerm, nonTermIndex) = self.work.pop()
        currentNonTermProductions = self.grammar.getProductions()[currentNonTerm]

        if len(currentNonTermProductions) - 1 > nonTermIndex:
            self.state = "q"
            self.work.append((currentNonTerm, nonTermIndex + 1))

            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            aux = currentNonTermProductions[nonTermIndex + 1]
            self.input = aux + self.input

        else:
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            self.input = [currentNonTerm] + self.input

    def checkWordLength(self, w):
        if len(w) > self.index:
            return self.input[0] == w[self.index]
        return False

    # [-1, 0, 0, 0, 0]
    # [S, a, [S, a, [S, c]], b, S,]

    def parseTree(self, work):
        # the idea is that the parse tree will be computed based on the work stack
        # we start from the root (starting symbol), then set the links between nodes while processing each production in the work stack
        father = -1

        for index in range(0, len(work)):
            if type(work[index]) == tuple:
                self.tree.append(Node(work[index][0]))
                self.tree[index].production = work[index][1]
            else:
                self.tree.append(Node(work[index]))

        for index in range(0, len(work)):
            if type(work[index]) == tuple:
                self.tree[index].father = father
                father = index
                lengthProduction = len(self.grammar.getProductions()[work[index][0]][work[index][1]])

                vectorIndex = []
                # [1, 2, 3, 4] 4  o sa aiba offseturi cand dau de nonTerminale
                # [1, 2, 9, 21]
                for i in range(1, lengthProduction + 1):
                    vectorIndex.append(index + i)
                for i in range(0, lengthProduction):
                    if self.tree[vectorIndex[i]].production != -1:  # if it is a nonTerminal compute offset
                        offset = self.getProductionOffset(vectorIndex[i])
                        for j in range(i + 1, lengthProduction):
                            vectorIndex[j] += offset
                for i in range(0, lengthProduction - 1):
                    self.tree[vectorIndex[i]].sibling = vectorIndex[i + 1]

            else:
                self.tree[index].father = father
                father = -1

        for index in range(0, len(work)):
            print(index, " ", str(self.tree[index]))

    def getProductionOffset(self, index):
        production = self.grammar.getProductions()[self.work[index][0]][self.work[index][1]]
        lengthOfProduction = len(production)
        offset = lengthOfProduction
        for i in range(1, lengthOfProduction + 1):
            if type(self.work[index + i]) == tuple:
                offset += self.getProductionOffset(index + i)
        return offset

    def run(self, w):
        self.state = "q"
        self.index = 0
        self.work = []
        self.input = [self.grammar.getStartSymbol()]
        while self.state != "t" and self.state != "e":
            if self.state == "q":
                # Done condition
                if len(self.input) == 0 and self.index == len(w):
                    self.state = "t"
                else:
                    # expand condition, top of beta is non terminal
                    if self.input[0] in self.grammar.getNonTerminals():
                        self.expand()
                    # advance condition, top of beta is terminal and it matches the index of the w
                    elif self.input[0] in self.grammar.getTerminals() and self.checkWordLength(w):
                        self.advance()
                    # Woopsie -> we have a momentary insuccess
                    else:
                        self.momentaryInsuccess()
            else:
                if self.state == "b":
                    # back
                    if self.work[len(self.work) - 1] in self.grammar.getTerminals():
                        self.back()
                    # anotherTry
                    else:
                        self.anotherTry()
        if self.state == "e":
            print("ERROR")
        else:
            print("Sequence accepted")
            print(self.work, self.input, self.index)


class Node:
    # this is a node in the parse tree, an arbitrary tree using the father sibling representation
    # all nodes are connected with only 2 links - the father and the right sibling
    # these nodes will be stored in a python list
    def __init__(self, value):
        self.father = -1
        self.sibling = -1
        self.value = value
        self.production = -1

    def __str__(self):
        return str(self.value) + " " + str(self.father) + " " + str(self.sibling)


p = ParserRecursiveDescend("g2-codes.txt")
s = Scanner()
pif, st = s.scan("p.in")
sequence = []
for e in pif:
    sequence.append(str(e[0]))
print(sequence)
p.run(sequence)
