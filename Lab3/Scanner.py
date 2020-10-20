from Lab3.Hashtable import Hashtable


class Scanner:
    def __init__(self):
        self.st = Hashtable()
        self.operators = []
        self.separators = []
        self.keywords = []
        self.tokenCodes = {}
        self.pif = []
        self.processTokens("tokens.in")

    def scan(self, fileName):
        lineNumber = 1
        with open(fileName, "r") as file:
            for line in file:
                if line != "\n":
                    tokens = self.tokenize(line)
                    for token in tokens:
                        tokenType = self.classify(token)
                        if tokenType is None:
                            print("Invalid token on line {0} -> {1}".format(lineNumber, token))
                            # TODO: write to file
                            return
                        else:
                            self.codify(token, tokenType)

        self.writePIF()
        return self.pif, self.st

    def writePIF(self):
        # TODO: write output to file
        return

    def tokenize(self, string):
        tokens = []
        token = ""

        isString = False

        for char in string:
            if not self.isOperator(char) and not self.isSeparator(char):
                if (char == "\"" or char == "\'") and isString is False:
                    token += char
                    isString = True

                elif (char == "\"" or char == "\'") and isString is True:
                    token += char
                    isString = False
                    tokens.append(token)
                    token = ""

                elif isString is True:
                    token += char

                elif char == " ":
                    tokens.append(token)
                    token = ""

                else:
                    token += char

            else:
                if token != "":
                    tokens.append(token)
                tokens.append(char)
                token = ""
            # TODO: check for separator at end of line
        return tokens

    def classify(self, token):
        if self.isSeparator(token) or self.isOperator(token) or self.isKeyword(token):
            return -1
        elif self.isConstant(token):
            return 0
        elif self.isIdentifier(token):
            return 1
        else:
            return None

    def codify(self, token, tokenType):
        if tokenType == -1:
            code = self.tokenCodes[token]
            self.pif.append([code, -1])
        elif tokenType == 0:
            STposition = self.st.find(token)
            if STposition == -1:
                self.st.add(token)
                STposition = self.st.find(token)

            self.pif.append([0, STposition])

        elif tokenType == 1:
            STposition = self.st.find(token)
            if STposition == -1:
                self.st.add(token)
                STposition = self.st.find(token)

            self.pif.append([1, STposition])

    def isOperator(self, token):
        if token in self.operators:
            return True

        return False

    def isSeparator(self, token):
        if token in self.separators:
            return True

        return False

    def isKeyword(self, token):
        if token in self.keywords:
            return True

        return False

    @staticmethod
    def isInt(n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    def isConstant(self, token):
        if not self.isInt(token):
            for char in token:
                if (not char.isalnum()) or (char not in [" ", "!", "?", "(", ")", "-", ".", ",", ";", ":"]):
                    return False
            return True
        return True

    @staticmethod
    def isIdentifier(token):
        if token[0].isnumeric():
            return False
        elif not token.isalnum():
            return False

        return True

    def processTokens(self, fileName):
        with open(fileName, "r") as file:
            for line in file:
                tokens = line.split(" ")
                self.tokenCodes[tokens[0]] = tokens[2]

                code = int(tokens[2])
                if 2 <= code <= 7 or code == 10 or code == 11:
                    self.operators.append(tokens[0])
                elif 8 <= code <= 14:
                    self.separators.append(tokens[0])
                else:
                    self.keywords.append(tokens[0])
