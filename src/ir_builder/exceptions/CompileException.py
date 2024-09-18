class CompileException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'CompileError: {self.message}'
        else:
            return 'Compilation error'
