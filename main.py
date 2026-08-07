class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_scsore = 0

    def menu(self):
         print("=" * 40)
         print("quiz game")
         print("1. 퀴즈풀기")
         print("2. 퀴즈추가")
         print("3. 퀴즈목록")
         print("4. 점수확인")
         print("5. 종료")
         print("=" * 40)

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.get_int_input("선택: ")
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