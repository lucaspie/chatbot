import json
from difflib import get_close_matches
import unicodedata
from datetime import datetime
import random
import requests
from urllib.parse import quote
from duckduckgo_search import ddg

# ---------------- Normalização ----------------
def normalize(text: str) -> str:
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
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

def data_atual():
    hoje = datetime.now().strftime("%d/%m/%Y")
    print(f"📅 Hoje é {hoje}")

def hora_atual():
    agora = datetime.now().strftime("%H:%M")
    print(f"⏰ Agora são {agora}")

def clima():
    api_key = "SUA_CHAVE_AQUI"
    cidade = input("➡️ Informe a cidade: ").strip()
    if not cidade:
        print("⚠️ Você não digitou a cidade.")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br&units=metric"
    resposta = requests.get(url).json()
    if resposta.get("main"):
        temp = resposta["main"]["temp"]
        condicao = resposta["weather"][0]["description"]
        print(f"🌦️ O clima em {cidade} é {condicao}, com {temp}°C.")
    else:
        print("⚠️ Não consegui obter o clima. Verifique o nome da cidade ou sua API Key.")
        print("Detalhes do erro:", resposta)

def piada():
    piadas = [
        "Por que o livro foi ao médico? Porque ele estava com muitas páginas em branco!",
        "O que o zero disse para o oito? Belo cinto!",
        "Qual o cúmulo do astronauta? Ter um espaço só dele 😅"
    ]
    print("😂 " + random.choice(piadas))

# ---------------- Dicionário de ações ----------------
actions = {
    "cadastrar": cadastrar,
    "liberar_acesso": liberar_acesso,
    "generate_report": generate_report,
    "send_email": send_email,
    "data_atual": data_atual,
    "hora_atual": hora_atual,
    "clima": clima,
    "piada": piada
}

# ---------------- Knowledge base ----------------
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# ---------------- Busca de correspondência ----------------
def find_best_match(user_input: str, knowledge_base: dict) -> dict | None:
    normalized_input = normalize(user_input)
    questions = [q["question"] for q in knowledge_base["questions"]]
    normalized_questions = [normalize(q) for q in questions]
    matches = get_close_matches(normalized_input, normalized_questions, n=1, cutoff=0.5)
    if matches:
        index = normalized_questions.index(matches[0])
        return knowledge_base["questions"][index]
    return None

# ---------------- Busca online Wikipedia ----------------
def buscar_na_wikipedia(termo: str) -> str:
    termo_formatado = quote(termo)
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_formatado}"
    try:
        resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if resposta.status_code == 200:
            data = resposta.json()
            return data.get("extract", "")
        return ""
    except:
        return ""

# ---------------- Busca online DuckDuckGo ----------------
def buscar_online(termo: str) -> str:
    try:
        resultados = ddg(termo, related=True)
        if resultados:
            return resultados[0]['text']
        return "Não encontrei informações confiáveis online."
    except Exception as e:
        return f"Erro ao buscar online: {e}"

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
    print("🤖 Bot avançado iniciado! Digite 'quit' para sair.")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() == "quit":
            print("Bot: Até logo! 👋")
            break

        entry = find_best_match(user_input, knowledge_base)

        if entry:
            print(f"Bot: {entry['answer']}")
            if "action" in entry and entry["action"]:
                executar_acao(entry["action"])
                if not perguntar_mais():
                    break

            # Aprendizado automático de variações
            normalized_input = normalize(user_input)
            normalized_entry_question = normalize(entry["question"])
            if normalized_input != normalized_entry_question:
                knowledge_base["questions"].append({
                    "question": user_input,
                    "answer": entry["answer"],
                    "action": entry.get("action")
                })
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Aprendi uma nova forma de perguntar! ✅")

        else:
            # Busca online múltiplas fontes
            print("Bot: Não sei a resposta, vou pesquisar online...")
            resposta = buscar_online(user_input)
            print(f"Bot: {resposta}")

            # Salva para aprendizado futuro
            knowledge_base["questions"].append({
                "question": user_input,
                "answer": resposta,
                "action": None
            })
            save_knowledge_base('knowledge_base.json', knowledge_base)
            print("Bot: Aprendi uma nova resposta com base na pesquisa! ✅")

if __name__ == "__main__":
    chat_bot()
