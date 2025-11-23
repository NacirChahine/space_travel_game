class Scene:
    def __init__(self, game):
        self.game = game

    def process_input(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError
