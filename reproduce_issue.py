
import copy

class BaseContext:
    def __init__(self):
        self.dicts = [1, 2, 3]

    def __copy__(self):
        # This is the line causing issues in Django
        duplicate = copy.copy(super())
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
    print(d.dicts)
    print(d.other)
except Exception as e:
    print(f"Copy failed: {e}")
