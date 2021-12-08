
class Namespaces:
    """A class that simulates how namespaces work in Python"""

    def __init__(self) -> None:
        """
        Constructor

        namespaces: dict
            stores all namespaces as a two-dimensional dictionary,
            where every namespace has its variables (list) and parent
        """

        self.namespaces = {
            "global": {
                "variables": [],
                "parent": None
            }
        }

    def create(self, namespace, parent) -> None:
        """Creates a new namespace with a specified parent namespace"""

        self.namespaces[namespace] = {
            "variables": [],
            "parent": parent
        }

    def add(self, namespace, variable) -> None:
        """Adds a new variable into a specified namespace"""

        self.namespaces[namespace]["variables"].append(variable)

    def get(self, namespace, variable) -> None or str:
        """Gets a namespace of specified variable"""

        if variable in self.namespaces[namespace]["variables"]:
            return namespace
        elif self.namespaces[namespace]["parent"] is None:
            return None
        else:
            return self.get(self.namespaces[namespace]['parent'], variable)

    def run(self) -> None:
        """Runs an algorithm for specified entry data"""

        print("Enter an amount of requests for adding classes relations: ", end="")
        n = int(input())
        print("Describe a request (<type> <namespace> <namespace/variable>):")
        for i in range(n):
            request, namespace, obj = input().split()
            if request == "create":
                self.create(namespace, obj)
            elif request == "add":
                self.add(namespace, obj)
            elif request == "get":
                print(self.get(namespace, obj))


if __name__ == "__main__":
    ns = Namespaces()
    ns.run()
