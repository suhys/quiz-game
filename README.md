```markdown
# 나만의 퀴즈 게임

## 프로젝트 개요
터미널에서 실행하는 4지선다형 퀴즈 게임입니다. 퀴즈를 풀고, 새 문제를 추가하고,
목록을 확인하고, 최고 점수를 기록합니다. 프로그램을 종료해도 `state.json`에
데이터가 저장되어 다음 실행 때 이어집니다.

## 퀴즈 주제 선정 이유
주제는 **프로그래밍 / IT 상식**입니다. Python/Git 등 이 과제에서 직접 배운
개념을 퀴즈로 다시 정리해보면 복습 효과가 있을 것 같아 선택했습니다.

## 실행 방법
```bash
python main.py
```
(Windows에서 `python`이 안 되면 `py main.py`, Mac/Linux는 `python3 main.py`)

## 기능 목록
- 퀴즈 풀기: 등록된 문제를 순서대로 출제하고 정답 여부를 알려주며, 다 풀면 점수를 계산합니다.
- 퀴즈 추가: 문제/선택지 4개/정답 번호를 입력받아 새 퀴즈를 등록합니다.
- 퀴즈 목록: 등록된 퀴즈 문제 목록을 확인합니다.
- 점수 확인: 지금까지의 최고 점수를 확인합니다.
- 잘못된 입력(공백/문자/범위 밖/빈 입력)과 Ctrl+C 등에도 안전하게 동작합니다.

## 파일 구조
```
quiz-game/
├── main.py # 진입점 (QuizGame을 만들어서 시작)
├── quiz.py # Quiz 클래스 (문제 하나)
├── quiz_game.py # QuizGame 클래스 (게임 전체 흐름 + 데이터)
├── state.json # 퀴즈 데이터 + 최고 점수 (자동 생성됨)
├── .gitignore
└── README.md
```

## 데이터 파일 설명 (`state.json`)
프로젝트 루트에 UTF-8로 저장되며, 다음 구조를 가집니다.

```json
{
  "quizzes": [
    {
      "question": "Python을 만든 사람은?",
      "choices": ["Guido van Rossum", "Linus Torvalds", "Dennis Ritchie", "James Gosling"],
      "answer": 1,
      "hint": "이 사람의 별명은 'BDFL'이었습니다."
    }
  ],
  "best_score": 83
}
```

- `quizzes`: 등록된 퀴즈 목록. 각 항목은 문제(`question`), 선택지 4개(`choices`),
  정답 번호(`answer`, 1~4), 힌트(`hint`, 선택)로 구성됩니다.
- `best_score`: 지금까지 기록한 최고 점수 (0~100점).
- 파일이 없거나 손상된 경우, 프로그램은 기본 퀴즈 데이터로 자동 복구합니다.
```


## Note
This line was added for the clone/pull exercise.

## Note #오후
