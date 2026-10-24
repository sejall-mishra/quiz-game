import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")


class Question:
    def __init__(self, text, options, answer):
        self.text = text
        self.options = options
        self.answer = answer  # 1 to 4

    def show(self, number):
        print(f"\nQ{number}. {self.text}")
        for i, option in enumerate(self.options, start=1):
            print(f"   {i}. {option}")

    def is_correct(self, choice):
        return choice == self.answer

    def correct_text(self):
        return self.options[self.answer - 1]


class Leaderboard:
    def __init__(self, filename):
        self.filename = filename
        self.entries = self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)

    def add(self, name, score, total):
        self.entries.append({"name": name, "score": score, "total": total})
        self.entries.sort(key=lambda e: e["score"] / e["total"], reverse=True)
        self.entries = self.entries[:10]
        self.save()

    def show(self):
        print("\n=== LEADERBOARD (Top 5) ===")
        if not self.entries:
            print("No scores yet. Be the first!")
            return
        for rank, entry in enumerate(self.entries[:5], start=1):
            print(f"{rank}. {entry['name']} - {entry['score']}/{entry['total']}")


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def ask(self, question, number):
        question.show(number)
        while True:
            choice = input("Your answer (1-4): ").strip()
            if choice in ("1", "2", "3", "4"):
                break
            print("Please type 1, 2, 3 or 4.")

        if question.is_correct(int(choice)):
            print("Correct!")
            self.score += 1
        else:
            print(f"Wrong! The correct answer is: {question.correct_text()}")

    def run(self):
        self.score = 0
        for number, question in enumerate(self.questions, start=1):
            self.ask(question, number)
        return self.score


def load_questions(filename):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    return [Question(q["question"], q["options"], q["answer"]) for q in data]


def get_number(prompt, low, high):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and low <= int(value) <= high:
            return int(value)
        print(f"Please type a number from {low} to {high}.")


def play(all_questions, leaderboard):
    name = input("Enter your name: ").strip() or "Player"
    count = get_number(
        f"How many questions? (1-{len(all_questions)}): ", 1, len(all_questions)
    )
    selected = random.sample(all_questions, count)

    quiz = Quiz(selected)
    score = quiz.run()
    percentage = score / count * 100

    print(f"\n{name}, your score: {score}/{count} ({percentage:.0f}%)")
    if percentage == 100:
        print("Perfect score!")
    elif percentage >= 60:
        print("Good job!")
    else:
        print("Keep practising!")

    leaderboard.add(name, score, count)


def main():
    try:
        questions = load_questions(QUESTIONS_FILE)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("Could not load questions.json. Check that the file exists and is correct.")
        return

    leaderboard = Leaderboard(LEADERBOARD_FILE)
    print("Welcome to the Python Quiz Game!")

    while True:
        print("\n1. Play quiz")
        print("2. View leaderboard")
        print("3. Quit")
        choice = get_number("Choose an option: ", 1, 3)

        if choice == 1:
            play(questions, leaderboard)
        elif choice == 2:
            leaderboard.show()
        else:
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()