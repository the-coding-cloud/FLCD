class Hashtable:
    def __init__(self, initial_capacity=37):
        self.__capacity = initial_capacity
        self.__size = 0
        self.__data = [["*empty"] for i in range(self.__capacity)]

    def hashCode(self, element):
        # This function generates the hashcode of a string based on the ASCII code of each character from the string
        # The hashcode consists of the sum of the ASCII codes of the characters

        characters = list(element)  # The string is split into characters

        hashcode = 0  # The sum is initialized with 0

        for character in characters:
            hashcode += ord(character)  # ord(character) returns the ASCII code of the character given as parameter

        return hashcode

    def hashFunction(self, element, index):
        # The collision resolution chosen for this hashtable is open addressing with double hashing: h(x,i) = (h'(x) + i*h"(x)) % hashtable_capacity, i = 0, ..., hashtable_capacity-1
        return (element % self.__capacity + index * (1 + element % (self.__capacity - 1))) % self.__capacity

    def add(self, element):
        # For an element x, we will successively examine the positions h(x,0), h(x,1), ..., h(x, hashtable_capacity-1)
        for i in range(self.__capacity):
            position = self.hashFunction(self.hashCode(element), i)
            print(position)
            if self.__data[position][0] == "*empty":
                self.__data[position][0] = element
                self.__size += 1
                return

    def find(self, element):
        # Same strategy used for adding an element will be used here to find the position of an element
        # -1 will be returned for elements that are not part of the symbol table

        for i in range(self.__capacity):
            position = self.hashFunction(self.hashCode(element), i)
            if self.__data[position][0] == element:
                return position
        else:
            return -1

    def getData(self):
        return self.__data


# This function is used solely for testing purposes
def run():
    ht = Hashtable()

    while True:
        try:
            command = input("0. exit\n1. add\n2. find\n3. print\n")
            if command == "0":
                return

            elif command == "1":
                id = input("identifier: ")
                ht.add(id)
                print(str(ht.getData()))

            elif command == "2":
                id = input("identifier: ")
                position = ht.find(id)
                if position == -1:
                    print("The element is not part of the ST\n")
                else:
                    print('{0} is found at position {1} in the ST\n'.format(id, position))
            elif command == "3":
                print(str(ht.getData()))

            else:
                print("Invalid input\n")
        except ValueError as v:
            print(v)


run()
