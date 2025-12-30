
import copy

class BaseContext:
    def __init__(self):
        self.dicts = [1, 2, 3]

    def __copy__(self):
        # FIX: Do not use copy(super())
        # duplicate = copy(super())
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

class Context(BaseContext):
    def __init__(self):
        super().__init__()
        self.other = "value"
    
    def __copy__(self):
        duplicate = super().__copy__()
        duplicate.other = self.other
        return duplicate

try:
    c = Context()
    d = copy.copy(c)
    print("Copy successful")
    print(f"Original dicts: {c.dicts}")
    print(f"Copied dicts: {d.dicts}")
    print(f"Original other: {c.other}")
    print(f"Copied other: {d.other}")
    
    # Verify it is a deep copy of the list (shallow copy of content) as intended by slice [:]
    c.dicts.append(4)
    print(f"Modified original dicts: {c.dicts}")
    print(f"Copied dicts after mod: {d.dicts}")
    
except Exception as e:
    print(f"Copy failed: {e}")
