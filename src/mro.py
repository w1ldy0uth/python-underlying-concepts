import pprint


class MRO:
    """
    A class that simulate the algorithm of method resolution (MRO C3) in Python.

    C3 superclass linearization is an algorithm used primarily to obtain the order
    in which methods should be inherited in the presence of multiple inheritance."""

    def __init__(self) -> None:
        """
        Constructor

        classes: dict
            contains all relationships between classes
        parents: list
            auxiliary list to recursively collect all parents of the specified class
        """

        self.classes = {}
        self._parents = []

    def add(self, clss) -> None:
        """
        Adds a class into a collection of classes
        Input type <class_name> [: <parent_class_name1> <parent_class_name2> ...]
        """

        if len(clss) == 1:
            self.classes[clss[0]] = list()
        else:
            self.classes[clss[0]] = clss[2:]

    def confirmation(self, parent, child) -> bool:
        """Confirms if the specified relation <parent_class> <child_class> is real in given scheme"""

        if parent == child:  # all classes inherit themselves
            return True
        self._parents += self.classes[child]
        for elt in self.classes[child]:
            self.confirmation(parent, elt)
        if parent in self._parents:
            return True
        return False

    def run(self, verbose=False) -> None:
        """Runs the data entry procedure and shows the result of given requests"""

        print("Enter an amount of requests for adding classes relations: ", end="")
        requests = int(input())
        print("Enter a requested relations in each line (<class> [: <class1>, <class2>, ...]):")
        for i in range(requests):
            rels = input().split(" ")
            self.add(rels)
        if verbose:
            pprint.pprint(self.classes)

        print("Enter an amount of requests for checking classes relations: ", end="")
        requests = int(input())
        print("Enter a requested relations between two classes in each line (<class> <class>):")
        for i in range(requests):
            cls1, cls2 = input().split()
            self._parents.clear()
            if self.confirmation(cls1, cls2):
                print("Relation confirmed")
            else:
                print("No such relation")


if __name__ == '__main__':
    mro = MRO()
    mro.run(verbose=True)
