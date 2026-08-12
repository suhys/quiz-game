class QuizGame:
    """ Manages the overall game flows and data """

    # create quizzes list and initial setting
    def __init__(self):
        self.quizzes = []
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
                choice = self.get_int_input("선택: ", self.min_menu,self.max_menu_option)
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