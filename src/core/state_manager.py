class StateManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def change_scene(self, new_scene):
        self.current_scene = new_scene
