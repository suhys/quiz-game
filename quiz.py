class Quiz:
    """ Show single question"""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, index=None):
        """Print the question and its choices."""
        if index is not None:
            print(f"[Question {index}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def check_answer(self, user_answer):
        """Return True if the given answer number is correct."""
        return user_answer == self.answer

    def to_dict(self):
        """Convert to a dict so it can be saved as JSON."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Quiz object from a dict loaded from JSON."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", ""),
        )    