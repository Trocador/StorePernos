class FakeWidget:
    def __init__(self, *a, **k): pass
    def pack(self, *a, **k): pass
    def grid(self, *a, **k): pass
    def place(self, *a, **k): pass
    def destroy(self): pass

class FakeEntry(FakeWidget):
    def __init__(self, *a, **k):
        self.value = ""

    def insert(self, index, value):
        self.value = value

    def get(self):
        return self.value

    def delete(self, start, end=None):
        self.value = ""

class FakeButton(FakeWidget):
    def __init__(self, *a, command=None, **k):
        self.command = command

    def invoke(self):
        if self.command:
            self.command()

class FakeTk:
    def withdraw(self): pass
    def destroy(self): pass
