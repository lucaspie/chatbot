from flask import Flask, render_template, request, jsonify
from bot import load_knowledge_base, find_best_match, executar_acao, save_knowledge_base, buscar_online, normalize

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def chat_bot():
    data = request.get_json()
    user_input = data.get("pergunta", "").strip()

    if not user_input:
        return jsonify({"resposta": "Bot: Não entendi sua pergunta."})

    knowledge_base = load_knowledge_base('knowledge_base.json')

    entry = find_best_match(user_input, knowledge_base)

    if entry:
        resposta = entry['answer']

        # Se tiver ação associada
        if "action" in entry and entry["action"]:
            executar_acao(entry["action"])

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

    else:
        # Busca online
        resposta = buscar_online(user_input)

        # Salva para aprendizado futuro
        knowledge_base["questions"].append({
            "question": user_input,
            "answer": resposta,
            "action": None
        })
        save_knowledge_base('knowledge_base.json', knowledge_base)

    return jsonify({"resposta": f"Bot: {resposta}"})


if __name__ == "__main__":
    app.run(debug=True)
