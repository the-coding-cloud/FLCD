class FA:
    def __init__(self, filename):
        self.__states = []
        self.__alphabet = []
        self.__transitions = {}
        self.__initialState = None
        self.__finalStates = []

        self.__readFA(filename)

    def __readFA(self, filename):
        with open(filename, "r") as file:
            # Read the first line, containing all the possible states for the FA, separated by space
            temp = file.readline()
            self.__states = temp.strip().split(" ")

            # Read the second line, containing all the accepted characters for the FA
            temp = file.readline()
            self.__alphabet = temp.strip().split(" ")

            # Read the third line, containing all the transitions accepted in the FA
            # For easiness in processing, the following rules in representation were applied
            # 1. Transitions are separated by ;
            # 2. The elements in the transition function are separated by ,
            temp = file.readline()
            transitions = temp.strip().split(";")
            for transition in transitions:
                t = transition.split(",")
                # Since we have a DFA, it is easier to store the transition functions in a dictionary,
                # where the key is a tuple of the form (q, a), q - current state, a - element from the alphabet
                # and the value is the next state
                self.__transitions[(t[0], t[1])] = t[2]

            # Read the fourth line, containing the initial state
            temp = file.readline()
            self.__initialState = temp.strip()

            # Read the fifth line, containing the final states, separated by space
            temp = file.readline()
            self.__finalStates = temp.strip().split(" ")

    def printStates(self):
        print("Set of states: ", self.__states)

    def printAlphabet(self):
        print("FA alphabet: ", self.__alphabet)

    def printInitialState(self):
        print("Initial state: ", self.__initialState)

    def printFinalStates(self):
        print("Final states: ", self.__finalStates)

    def printTransitions(self):
        print("Transitions: ")
        for t in self.__transitions.keys():
            print("delta({0}, {1}) = {2}".format(t[0], t[1], self.__transitions[t]))

    def checkSequenceAcceptance(self, sequence):
        currentState = self.__initialState

        while sequence != "":
            transitionKey = (currentState, sequence[0])

            if transitionKey in self.__transitions.keys():
                currentState = self.__transitions[transitionKey]
                sequence = sequence[1:]

            else:
                return False

        if currentState not in self.__finalStates:
            return False

        else:
            return True
