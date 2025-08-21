import json
from difflib import get_close_matches
import unicodedata

def normalize(text: str) -> str:
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def generate_report():
    print("🔎 Relatório gerado com sucesso!")

def send_email():
    print("📧 Email enviado para o destinatário!")

actions = {
    "generate_report": generate_report,
    "send_email": send_email
}

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    normalized_question = normalize(user_question)
    normalized_questions = [normalize(q) for q in questions]

    matches: list = get_close_matches(normalized_question, normalized_questions, n=1, cutoff=0.4)
    if matches:
        # pega a pergunta original correspondente
        index = normalized_questions.index(matches[0])
        return questions[index]
    return None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            entry = next(q for q in knowledge_base["questions"] if q["question"] == best_match)
            print(f'Bot: {entry["answer"]}')

            if "action" in entry:
                action_name = entry["action"]
                if action_name in actions:
                    actions[action_name]()   # executa a função associada

        else:
            print('Bot: I don’t know the answer, can you teach me?')
            new_answer: str = input('Type here (or "skip" to ignore): ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thanks, I learned something new!")

if __name__ == '__main__':
    chat_bot()
