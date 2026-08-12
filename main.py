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

class QuizGame:
    """ Manages the overall game flows and data """

    # create quizzes list and initial setting
    def __init__(self):
        self.quizzes = self._default_quizzes()
        self.best_scsore = 0
        self.max_menu_option = 5
        self.min_menu_option = 1

    @staticmethod
    # user input
    def input(user_menu_input, min_value, max_value):
        """
        Get an integer input within min and max value
        - Strips whitespace, catches conversion failures, out-of-range, and empty input.
        - Returns None on any problem so the user can re-prompt
        """
        user_input = input(user_menu_input).strip()

        if user_input =="":
            print(f"⚠️ 입력이 비어있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            return None

        try:
            value = int(user_input)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            return None

        if not (min_value <= value <= max_value):
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            return None

        return value

    def print_menu(self):
         print("=" * 40)
         print("quiz game")
         print("1. 퀴즈풀기")
         print("2. 퀴즈추가")
         print("3. 퀴즈목록")
         print("4. 점수확인")
         print("5. 종료")
         print("=" * 40)

    def run(self):
        """ Main menu loop. Handles exit safely"""
        try:
            while True:
                self.print_menu()
                choice = self.input("선택: ", self.min_menu_option,self.max_menu_option)
                if choice is None:
                    continue

                if choice == 1:
                    print("")
                elif choice == 2:
                    print("")     
                elif choice == 3:
                    print("")   
                elif choice == 4:
                    print("")   
                elif choice == 5:
                    print("")   
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")


def main():
        game = QuizGame()
        game.run()

if __name__ == "__main__":
    main()