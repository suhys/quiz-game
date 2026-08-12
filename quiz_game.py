import json
import os
import random

from datetime import datetime
from quiz import Quiz

DATA_FILE = "state.json"

class QuizGame:
    """ Manages the overall game flows and data """

    # create quizzes list and initial setting
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.quizzes = self._default_quizzes()
        self.best_score = 0
        self.score_history = []  
        self.load_data()
        self.max_menu_option = 7
        self.min_menu_option = 1

    def load_data(self):
        """Load data from state.json. Fall back to defaults if missing or corrupted."""
        if not os.path.exists(self.data_file):
            print("No saved data found. Starting with default quizzes.")
            self.quizzes = self._default_quizzes()
            self.best_score = 0
            self.score_history = []
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            self.score_history = data.get("score_history", [])
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
            self.score_history = []

    def save_data(self):
        """Save the current quiz list and best score to state.json."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history, 
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
    def input(prompt, min_value, max_value):
        raw = input(prompt).strip()

        if raw == "":
            print(f"Input is empty. Enter a number between {min_value}-{max_value}.")
            return None

        try:
            value = int(raw)
        except ValueError:
            print(f"Invalid input. Enter a number between {min_value}-{max_value}.")
            return None

        if not (min_value <= value <= max_value):
            print(f"Invalid input. Enter a number between {min_value}-{max_value}.")
            return None

        return value

    # ---------- Menu ----------

    def print_menu(self):
            print("=" * 40)
            print("        Quiz Game        ")
            print("=" * 40)
            print("1. Play quiz")
            print("2. Add quiz")
            print("3. List quizzes")
            print("4. Delete quiz")
            print("5. Show best score")
            print("6. Show score history")
            print("7. Exit")
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
                    self.delete_quiz()  
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    self.show_score_history()        
                elif choice == 7:
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

        max_count = len(self.quizzes)
        count = self.input(f"How many questions? (1-{max_count}): ", 1, max_count)
        while count is None:
            count = self.input(f"How many questions? (1-{max_count}): ", 1, max_count)

        quiz_order = self.quizzes.copy()
        random.shuffle(quiz_order)
        selected = quiz_order[:count]

        print(f"\nStarting quiz! ({count} questions)")
        correct_count = 0

        for i, quiz in enumerate(selected, start=1):
            print("-" * 40)
            quiz.display(index=i)

            user_answer = self._get_answer_with_hint(quiz)

            if quiz.check_answer(user_answer):
                print("Correct!")
                correct_count += 1
            else:
                print(f"Wrong. The correct answer was {quiz.answer}.")

        score = round(correct_count / count * 100)
        print("=" * 40)
        print(f"Result: {correct_count}/{count} correct! ({score} points)")

        if score > self.best_score:
            self.best_score = score
            print("New best score!")

        self.score_history.append({
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        self.save_data()
        print("=" * 40)

    def _get_answer_with_hint(self, quiz):
        """
        Get the user's answer for a quiz. Typing 'h' shows a hint
        (bonus feature) instead of counting as an answer attempt.
        """
        while True:
            raw = input("Your answer (or 'h' for a hint): ").strip()

            if raw.lower() == "h":
                if quiz.hint:
                    print(f"Hint: {quiz.hint}")
                else:
                    print("No hint available for this question.")
                continue

            if raw == "":
                print(f"Input is empty. Enter a number between 1-{len(quiz.choices)}.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print(f"Invalid input. Enter a number between 1-{len(quiz.choices)}.")
                continue

            if not (1 <= value <= len(quiz.choices)):
                print(f"Invalid input. Enter a number between 1-{len(quiz.choices)}.")
                continue

            return value

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

        answer = self.input(f"Correct choice number (1-4): ", 1, 4)
        while answer is None:
            answer = self.input(f"Correct choice number (1-4): ", 1, 4)

        hint = input("Hint (optional, press Enter to skip): ").strip()

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_data()
        print("\nQuiz added!")

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

    # ---------- Feature 4 (bonus): delete quiz ----------

    def delete_quiz(self):
        if not self.quizzes:
            print("\nNo quizzes registered.")
            return

        self.list_quizzes()
        index = self.input(
            f"Number to delete (1-{len(self.quizzes)}): ", 1, len(self.quizzes)
        )
        while index is None:
            index = self.input(
                f"Number to delete (1-{len(self.quizzes)}): ", 1, len(self.quizzes)
            )

        removed = self.quizzes.pop(index - 1)
        self.save_data()
        print(f"\nDeleted: {removed.question}")

    # ---------- Feature 5: show best score ----------

    def show_score(self):
        if self.best_score == 0:
            print("\nYou haven't played yet. Try a quiz first!")
            return
        print(f"\nBest score: {self.best_score}")          

    # ---------- Feature 6 (bonus): score history ----------

    def show_score_history(self):
        if not self.score_history:
            print("\nNo score history yet.")
            return

        print(f"\nScore history ({len(self.score_history)} entries)")
        print("-" * 40)
        for i, entry in enumerate(self.score_history, start=1):
            print(f"[{i}] {entry['date']} - {entry['score']} points")
        print("-" * 40)

