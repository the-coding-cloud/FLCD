from Lab3.Hashtable import Hashtable


class Scanner:
    def __init__(self):
        self.__st = Hashtable()
        self.__operators = []
        self.__separators = []
        self.__keywords = []
        self.__tokenCodes = {}
        self.__pif = []
        self.__processTokens("tokens.in")

    def scan(self, fileName):
        self.__st = Hashtable()  # Start from scratch the scanning
        self.__pif = []

        lineNumber = 1  # Keep track of the line number
        message = None  # In this variable we will store any potential lexical error messages
        with open(fileName, "r") as file:  # We read the program from the file line by line
            for line in file:
                if line != "\n":  # If the line is not empty, we start processing it
                    tokens = self.__tokenize(line.strip())  # We __tokenize the line
                    if not self.__isSeparator(tokens[
                                                  -1]):  # We check if it ends with a separator (because all statements in my mini language end with a separator)
                        self.__writeScanningOutput(fileName, "Missing separator on line {0}".format(
                            lineNumber))  # If it doesn't end in a separator, we stop here and write to the file an error message
                        return
                    # print(tokens)
                    for token in tokens:
                        tokenType = self.__classify(
                            token)  # We process now each token - firstly, we __classify it (check if it's a constant, identifier or a token from the language)
                        if tokenType is None:  # If it can't be classified, we return an error message stating which is the problematic token and on what line
                            print("Invalid token on line {0} -> {1}".format(lineNumber, token))
                            message = "Invalid token on line {0} -> {1}".format(lineNumber, token)
                            self.__writeScanningOutput(fileName, message)
                            return
                        else:
                            self.__codify(token,
                                          tokenType)  # If we reach this point, everything is ok and we just add the token to the PIF
                lineNumber += 1

        self.__writeScanningOutput(fileName,
                                   message)  # After scanning the entire program, we can write the output to a file
        # return self.pif, self.st

    def __writeScanningOutput(self, fileName, message=None):
        if message is None:  # If there is no error message, we can write the ST and PIF to the corresponding file with the extension .out
            filename = fileName.split(".")[0] + ".out"
            file = open(filename, "w")
            st = self.__st.getData()
            file.write("--- Symbol Table ---\n")
            file.write("Pos. | Value\n")
            for i in range(len(st)):
                if st[i][0] != "*empty":
                    file.write("{0} ---- {1}\n".format(i, st[i][0]))

            file.write("\n--- PIF ---\n")
            file.write("Code | ST Position\n")
            for line in self.__pif:
                file.write("{0} ---- {1}\n".format(line[0], line[1]))

        else:
            filename = fileName.split(".")[0] + ".out"
            file = open(filename, "w")
            file.write(message)

    def __tokenize(self, string):
        tokens = []
        token = ""

        isString = False

        for char in string:
            # The tokenizing is done character by character, verifying certain cases at each step
            if not self.__isOperator(char) and not self.__isSeparator(
                    char):  # The splitting is done by separators and operators
                if (
                        char == "\"" or char == "\'") and isString is False:  # If this is the beginning of a string/char constant, we add the character to the token and continue processing
                    token += char
                    isString = True

                elif (
                        char == "\"" or char == "\'") and isString is True:  # If this is the end of a string/char constant, we add the token to the list and reinitialize the variable with the empty string
                    token += char
                    isString = False
                    tokens.append(token)
                    token = ""

                elif isString is True:  # If this is inside a string/char constant, we add the character to the token and continue processing
                    token += char

                elif char == " ":  # If we are not processing a string/char constant and we encounter a " ", we can safely assume it's the end of a token and add it to the list
                    if token != "":
                        tokens.append(token)
                        token = ""

                else:
                    token += char

            else:  # If we reach a separator/operator, we add the token previously processed to the list, then we add the operator/separator to the list of tokens too
                if token != "":
                    tokens.append(token)
                tokens.append(char)
                token = ""

        return tokens

    def __classify(self, token):
        if self.__isSeparator(token) or self.__isOperator(token) or self.__isKeyword(token):
            return -1
        elif self.__isIdentifier(token):
            return 0
        elif self.__isConstant(token):
            return 1
        else:
            return None

    def __codify(self, token, tokenType):
        if tokenType == -1:  # If the token is an operator/separator/keyword, we add it to the PIF with its corresponding code and position -1 (since it's not in the ST)
            code = self.__tokenCodes[token]
            self.__pif.append([code, -1])

        elif tokenType == 0:  # If the token is an identifier, we check if it already exists in the ST and retrieve its position; otherwise we add it to the ST
            STposition = self.__st.find(token)
            if STposition == -1:
                self.__st.add(token)
                STposition = self.__st.find(token)

            self.__pif.append(
                [0, STposition])  # We add the token with code 0 and the ST position previously retrieved to the PIF

        elif tokenType == 1:  # If the token is a constant, we check if it already exists in the ST and retrieve its position; otherwise we add it to the ST
            STposition = self.__st.find(token)
            if STposition == -1:
                self.__st.add(token)
                STposition = self.__st.find(token)

            self.__pif.append(
                [1, STposition])  # We add the token with code 1 and the ST position previously retrieved to the PIF

    def __isOperator(self, token):
        if token in self.__operators:
            return True

        return False

    def __isSeparator(self, token):
        if token in self.__separators:
            return True

        return False

    def __isKeyword(self, token):
        if token in self.__keywords:
            return True

        return False

    @staticmethod
    def __isInt(n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    def __isConstant(self, token):
        if not self.__isInt(token):
            if (token[0] not in ["\'", "\""]) or (token[len(token) - 1] not in ["\'", "\""]):
                return False
            for char in token:
                if (not char.isalnum()) and (
                        char not in [" ", "!", "?", "(", ")", "-", ".", ",", ";", ":", "\'", "\""]):
                    return False
            return True
        return True

    @staticmethod
    def __isIdentifier(token):
        if token[0].isnumeric():
            return False
        elif not token.isalnum():
            return False

        return True

    def __processTokens(self, fileName):
        # This is the functions where we load the tokens of the language from a file to the memory
        with open(fileName, "r") as file:
            for line in file:
                tokens = line.strip().split(" ")
                self.__tokenCodes[tokens[0]] = int(tokens[2])

                code = int(tokens[2])
                if 2 <= code <= 9:
                    self.__operators.append(tokens[0])
                elif 10 <= code <= 14:
                    self.__separators.append(tokens[0])
                else:
                    self.__keywords.append(tokens[0])


scanner = Scanner()
scanner.scan("p1.in")
scanner.scan("p1-err.in")
scanner.scan("p2.in")
scanner.scan("p3.in")
