

class QuestionSystem:
    """Manages questioning process by providing inputs to question_selector, selecting questions,
    processing answers and updating game state."""

    def __init__(self, game_state, question_selector):

        self.max_questions = 5
        self.game_state = game_state
        self.question_selector = question_selector


