import json
from difflib import get_close_matches
import unicodedata
from datetime import datetime
import random
import requests
from duckduckgo_search import DDGS

ddgs = DDGS()

# ---------------------- BUSCA PALAVRAS CHAVES ----------
def buscar_palavras_chave_varios(termo: str) -> list[str]:
    try:
        resultados = ddgs.text(termo, max_results=5)
        palavras_totais = []
        stopwords = {'de', 'a', 'o', 'e', 'do', 'da', 'em', 'um', 'uma', 'com', 'para', 'é'}
        for r in resultados:
            titulo = r['title']
            palavras = [w for w in titulo.split() if w.lower() not in stopwords]
            palavras_totais.extend(palavras)
        return list(set(palavras_totais))
    except Exception as e:
        print("Erro ao buscar palavras-chave:", e)
        return []

# ---------------- Normalização ----------------
def normalize(text: str) -> str:
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text

# ---------------- Funções de ação ----------------
def cadastrar():
    return "📋 Cadastro realizado (exemplo)."

def liberar_acesso():
    return "✅ Acesso liberado com sucesso!"

def generate_report():
    return "🔎 Relatório gerado com sucesso!"

def send_email():
    return "📧 Email enviado!"

def data_atual():
    return f"📅 Hoje é {datetime.now().strftime('%d/%m/%Y')}"

def hora_atual():
    return f"⏰ Agora são {datetime.now().strftime('%H:%M')}"

def clima():
    return "🌦️ Consulta de clima ainda não configurada (precisa de API key)."

def piada():
    piadas = [
        "Por que o livro foi ao médico? Porque ele estava com muitas páginas em branco!",
        "O que o zero disse para o oito? Belo cinto!",
        "Qual o cúmulo do astronauta? Ter um espaço só dele 😅"
    ]
    return "😂 " + random.choice(piadas)

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

# ---------------- Busca online DuckDuckGo ----------------
def buscar_online(termo: str) -> str:
    try:
        resultados = ddgs.text(termo, max_results=5)
        if resultados:
            stopwords = {'de', 'a', 'o', 'e', 'do', 'da', 'em', 'um', 'uma', 'com', 'para', 'é'}
            titulo = resultados[0]['title']
            palavras_chave = [w for w in titulo.split() if w.lower() not in stopwords]
            return ", ".join(palavras_chave)
        return "Não encontrei informações confiáveis online."
    except Exception as e:
        return f"Erro ao buscar online: {e}"

# ---------------- Executa ação ----------------
def executar_acao(action_name: str):
    if action_name in actions:
        return actions[action_name]()
    else:
        return f"⚠️ Ação '{action_name}' não está definida."
