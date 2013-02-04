class State:
    """
    This is an abstract class for a game state.
    The "tick" method is called to update the state,
    and the "render" method to draw the current frame on the screen.
    """
    def render(me, game):
        raise NotImplementedError, "Abstract method 'render' not implemented."

    def tick(me, game):
        raise NotImplementedError, "Abstract method 'tick 'not implemented."

    def changeState(me, game, state):
        game.pushState(state)