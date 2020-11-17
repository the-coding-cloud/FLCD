class Grammar:
    def __init__(self, filename):
        self.__terminals = []
        self.__nonTerminals = []
        self.__productions = {}
        self.__startSymbol = None
        self.__readFile(filename)

    def __readFile(self, filename):
        with open(filename, "r") as file:
            temp = file.readline()
            self.__nonTerminals = temp.strip().split(" ")

            temp = file.readline()
            self.__terminals = temp.strip().split(" ")

            temp = file.readline()
            self.__startSymbol = temp.strip()

            for line in file:
                temp = line.strip().split(" ")
                if (temp[0]) in self.__productions.keys():
                    self.__productions[temp[0]].append(temp[1].split("#"))
                else:
                    self.__productions[temp[0]] = [temp[1].split("#")]

    def printTerminals(self):
        print("Set of terminals: ", self.__terminals)

    def printNonTerminals(self):
        print("Set of non-terminals: ", self.__nonTerminals)

    def printStartSymbol(self):
        print("Start symbol ", self.__startSymbol)

    def printProductions(self):
        print("Set of productions: ", self.__productions)

    def printProductionsForNonTerminal(self, nt):
        if nt in self.__productions.keys():
            print("The productions for {0} are:".format(nt))
            for p in self.__productions[nt]:
                print(nt + "->" + "".join(p))
        else:
            print("There is no such non terminal")


def printMenu():
    print("0. Exit")
    print("1. Print set of terminals")
    print("2. Print set of non-terminals")
    print("3. Print set of productions")
    print("4. Print start symbol")
    print("5. Print set of productions for a nonterminal")


def run():
    g = Grammar("g1.txt")

    while True:
        print("----------------------------------")
        printMenu()
        command = int(input(">> Choose command: "))

        if command == 1:
            g.printTerminals()
        elif command == 2:
            g.printNonTerminals()
        elif command == 3:
            g.printProductions()
        elif command == 4:
            g.printStartSymbol()
        elif command == 5:
            nt = input("Non terminal: ")
            g.printProductionsForNonTerminal(nt)
        elif command == 0:
            return
        else:
            print("Try again")


run()