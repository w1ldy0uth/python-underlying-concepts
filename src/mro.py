from pprint import pprint


class MRO:
  """
  A class that simulates the C3 linearization algorithm (MRO) in Python.

  C3 superclass linearization is an algorithm used primarily to obtain the order
  in which methods should be inherited in the presence of multiple inheritance.

  """

  def __init__(self) -> None:
    self.classes: dict[str, list[str]] = {}

  def add(self, class_name: str, parents: list[str] | None = None) -> None:
    """Registers a class with its direct parents."""
    if parents is None:
      parents = []
    for parent in parents:
      if parent not in self.classes:
        raise ValueError(
            f"Parent class '{parent}' must be defined before '{class_name}'")
    self.classes[class_name] = list(parents)

  def linearize(self, class_name: str) -> list[str]:
    """
    Computes the C3 linearization (MRO) for the given class.

    L[C] = C + merge(L[B1], L[B2], ..., [B1, B2, ...])

    The merge operation selects the first head of any list that does not
    appear in the tail of any other list, removes it from all lists,
    and repeats until all lists are empty.

    Raises TypeError if a consistent MRO is impossible.
    """
    if not self.classes[class_name]:
      return [class_name, "object"]  # implicit root

    if class_name not in self.classes:
      raise KeyError(f"Class '{class_name}' is not defined")

    if not self.classes[class_name]:
      return [class_name]

    parent_linearizations = [self.linearize(
        p) for p in self.classes[class_name]]
    parent_list = list(self.classes[class_name])
    return [class_name] + self._merge(parent_linearizations + [parent_list])

  @staticmethod
  def _merge(lists: list[list[str]]) -> list[str]:
    """Performs the C3 merge operation on a list of linearizations."""
    result = []
    while True:
      lists = [lst for lst in lists if lst]
      if not lists:
        return result

      for lst in lists:
        head = lst[0]
        if all(head not in other[1:] for other in lists):
          result.append(head)
          for lst2 in lists:
            if lst2[0] == head:
              lst2.pop(0)
          break
      else:
        remaining = [str(lst) for lst in lists]
        raise TypeError(
            f"Cannot create a consistent MRO: {', '.join(remaining)}"
        )

  def verify(self, class_name: str) -> bool:
    """Compares computed MRO against Python's own __mro__."""
    computed = self.linearize(class_name)
    ns = {}
    for cls, parents in self.classes.items():
      ns[cls] = type(cls, tuple(ns[p] for p in parents) or (object,), {})
    real = [c.__name__ for c in ns[class_name].__mro__]
    match = computed == real
    print(f"  Computed: {computed}")
    print(f"  Python:   {real}")
    print(f"  Match: {match}")
    return match

  def run(self, verbose: bool = False) -> None:
    """Runs the interactive data entry procedure."""
    print("Enter number of classes to define: ", end="")
    count = int(input())
    print("Enter each class as: ClassName [: Parent1 Parent2 ...]")
    for _ in range(count):
      parts = input().split()
      class_name = parts[0]
      parents = parts[2:] if len(parts) > 1 and parts[1] == ":" else []
      self.add(class_name, parents)
    if verbose:
      pprint(self.classes)

    print("\nC3 Linearization (MRO) for all classes:")
    for cls in self.classes:
      try:
        mro = self.linearize(cls)
        print(f"  {cls}: {' -> '.join(mro)}")
      except TypeError as e:
        print(f"  {cls}: {e}")

    print("\nVerification against Python's __mro__:")
    for cls in self.classes:
      try:
        print(f"  {cls}:")
        self.verify(cls)
      except TypeError:
        print("    (skipped — inconsistent MRO)")


if __name__ == '__main__':
  mro = MRO()
  mro.run(verbose=True)
