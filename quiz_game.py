import json
import os

from quiz import Quiz

DATA_FILE = "state.json"

class QuizGame:
    """ Manages the overall game flows and data """

    # create quizzes list and initial setting
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.quizzes = self._default_quizzes()
        self.best_score = 0
        self.load_data()
        self.max_menu_option = 5
        self.min_menu_option = 1

    def load_data(self):
        """Load data from state.json. Fall back to defaults if missing or corrupted."""
        if not os.path.exists(self.data_file):
            print("No saved data found. Starting with default quizzes.")
            self.quizzes = self._default_quizzes()
            self.best_score = 0
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            if not self.quizzes:
                self.quizzes = self._default_quizzes()
            print(
                f"Loaded saved data. "
                f"({len(self.quizzes)} quizzes, best score {self.best_score})"
            )
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("Data file is corrupted. Resetting to default quizzes.")
            self.quizzes = self._default_quizzes()
            self.best_score = 0

    def save_data(self):
        """Save the current quiz list and best score to state.json."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"Error while saving: {e}")        

    @staticmethod
    def _default_quizzes():
        """Default 6 quizzes (Programming / IT trivia) used when no file exists."""
        raw = [
            (
                "Who created Python?",
                ["Guido van Rossum", "Linus Torvalds", "Dennis Ritchie", "James Gosling"],
                1,
                "His nickname was 'BDFL' (Benevolent Dictator For Life).",
            ),
            (
                "What does HTML stand for?",
                [
                    "Hyper Text Markup Language",
                    "High Tech Modern Language",
                    "Home Tool Markup Language",
                    "Hyperlink and Text Markup Language",
                ],
                1,
                "A markup language used to structure web pages.",
            ),
            (
                "Which Git command clones a remote repository locally?",
                ["git pull", "git clone", "git fetch", "git push"],
                2,
                "Used when downloading a repository for the first time.",
            ),
            (
                "Which of these is NOT a built-in Python data type?",
                ["list", "dict", "array", "tuple"],
                3,
                "This one requires importing a standard library module.",
            ),
            (
                "What does HTTP status code 404 mean?",
                ["Server error", "Success", "Not found", "Unauthorized"],
                3,
                "It means the requested resource doesn't exist on the server.",
            ),
            (
                "Which is NOT one of the 4 pillars of OOP?",
                ["Encapsulation", "Inheritance", "Polymorphism", "Compilation"],
                4,
                "This is the process of translating code into machine code.",
            ),
        ]
        return [Quiz(q, c, a, h) for q, c, a, h in raw]

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

    # ---------- Menu ----------

    def print_menu(self):
            print("=" * 40)
            print(".         quiz game         ")
            print("1. Play quiz")
            print("2. Add quiz")
            print("3. List quizzes")
            print("4. Show best score")
            print("5. Exit")
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
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()    
                elif choice == 3:
                    self.list_quizzes()   
                elif choice == 4:
                    self.show_score()  
                elif choice == 5:
                    self.save_data()
                    print("\nExiting the game. Goodbye!") 
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n\nInput interrupted. Saving data before exit.")
            self.save_data()   

    # ---------- Feature 1: play quiz ----------

    def play_quiz(self):
        if not self.quizzes:
            print("\nNo quizzes registered. Please add one first.")
            return

        print(f"\nStarting quiz! ({len(self.quizzes)} questions total)")
        correct_count = 0

        for i, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(index=i)

            user_answer = self.input("Your answer: ", 1, len(quiz.choices))
            while user_answer is None:
                user_answer = self.input("Your answer: ", 1, len(quiz.choices))

            if quiz.check_answer(user_answer):
                print("Correct!")
                correct_count += 1
            else:
                print(f"Wrong. The correct answer was {quiz.answer}.")

        total = len(self.quizzes)
        score = round(correct_count / total * 100)
        print("=" * 40)
        self.save_data()
        print(f"Result: {correct_count}/{total} correct! ({score} points)")

        if score > self.best_score:
            self.best_score = score
            print("New best score!")
        print("=" * 40)

    # ---------- Feature 2: add quiz ----------

    def add_quiz(self):
        print("\nAdding a new quiz.")

        question = input("Enter the question: ").strip()
        if question == "":
            print("Question is empty. Cancelling.")
            return

        choices = []
        for i in range(1, 5):
            c = input(f"Choice {i}: ").strip()
            if c == "":
                print("A choice is empty. Cancelling.")
                return
            choices.append(c)

        answer = self.input("Correct choice number (1-4): ", 1, 4)
        while answer is None:
            answer = self.input("Correct choice number (1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        print("\nQuiz added!")
        self.save_data()

    # ---------- Feature 3: list quizzes ----------

    def list_quizzes(self):
        if not self.quizzes:
            print("\nNo quizzes registered.")
            return

        print(f"\nRegistered quizzes ({len(self.quizzes)} total)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)  

    # ---------- Feature 4: show best score ----------

    def show_score(self):
        if self.best_score == 0:
            print("\nYou haven't played yet. Try a quiz first!")
            return
        print(f"\nBest score: {self.best_score}")          

