class BaseAgent:
    def __init__(self, **params):
        self.params = params

    def run(self, state):
        raise NotImplementedError
