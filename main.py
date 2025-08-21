import json
from difflib import get_close_matches
import unicodedata

# ---------------- Normalização ----------------
def normalize(text: str) -> str:
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

# ---------------- Funções de ação ----------------
def cadastrar():
    print("Bot: Vamos criar um cadastro de teste.")
    nome = input("➡️ Informe seu nome: ")
    email = input("➡️ Informe seu email: ")
    idade = input("➡️ Informe sua idade: ")
    cadastro = {"nome": nome, "email": email, "idade": idade}
    print("Bot: Cadastro realizado com sucesso!")
    print(f"📋 Dados cadastrados: {cadastro}")

def liberar_acesso():
    print("Bot: Vamos liberar o acesso.")
    email = input("➡️ Informe o email do usuário: ")
    print("Bot: ✅ Acesso liberado com sucesso!")
    print(f"📧 Email: {email} | Status: ACESSO LIBERADO")

def generate_report():
    print("🔎 Relatório gerado com sucesso!")

def send_email():
    print("📧 Email enviado para o destinatário!")

# ---------------- Dicionário de ações ----------------
actions = {
    "cadastrar": cadastrar,
    "liberar_acesso": liberar_acesso,
    "generate_report": generate_report,
    "send_email": send_email
}

# ---------------- Knowledge base ----------------
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# ---------------- Busca de correspondência ----------------
def find_best_match(user_input: str, questions: list[str]) -> str | None:
    normalized_input = normalize(user_input)
    normalized_questions = [normalize(q) for q in questions]
    matches = get_close_matches(normalized_input, normalized_questions, n=1, cutoff=0.4)
    if matches:
        return questions[normalized_questions.index(matches[0])]
    return None

# ---------------- Executa ação ----------------
def executar_acao(action_name: str):
    if action_name in actions:
        actions[action_name]()
    else:
        print(f"Bot: ⚠️ Ação '{action_name}' não está definida.")

# ---------------- Fluxo de encerramento ----------------
def perguntar_mais() -> bool:
    resposta = input("Bot: Gostaria de fazer mais alguma coisa? (sim/não): ").lower()
    if resposta in ["não", "nao"]:
        print("Bot: Ok! Até mais 👋")
        return False
    else:
        print("Bot: Ok, me diga o que deseja fazer.")
        return True

# ---------------- Loop principal ----------------
def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    comandos = [q["question"] for q in knowledge_base["questions"]]

    print("🤖 Bot iniciado! Digite 'quit' para sair.")

    while True:
        user_input = input("Você: ").strip()

        if user_input.lower() == "quit":
            print("Bot: Até logo! 👋")
            break

        # Procura melhor correspondência
        best_match = find_best_match(user_input, comandos)

        if best_match:
            entry = next(q for q in knowledge_base["questions"] if q["question"] == best_match)
            print(f"Bot: {entry['answer']}")

            # Executa ação se houver
            if "action" in entry:
                executar_acao(entry["action"])
                if not perguntar_mais():
                    break
        else:
            # Bot não sabe a resposta → aprendizado
            print("Bot: I don’t know the answer, can you teach me?")
            new_answer = input("Type here (or 'skip' to ignore): ")
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thanks, I learned something new!")

if __name__ == "__main__":
    chat_bot()
