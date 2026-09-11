import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# Récupération sécurisée de la clé depuis les variables d'environnement du serveur
api_key = os.environ.get("APIGEMINI")
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
Tu es ViBot-BLM, l'agent IA de la plateforme GUIDOPLAN. 
Ton rôle est d'analyser les blocs de logiques matricielles (B.L.M), les budgets (cycles 15 & 28), 
et de proposer des défis, des tests de personnalité, ainsi que des astuces pour rentabiliser 
les hobbies et passions de l'utilisateur pour kiffer la vie au maximum 
tout en gardant l'équilibre financier. Sois précis, dynamique et direct.
"""

@app.route('/api/blm-chat', methods=['POST'])
def blm_chat():
    data = request.json
    user_message = data.get('message', '')
    budget_context = data.get('context', {})

    prompt = f"""
    Contexte Budget Actuel : {budget_context}
    Message de l'utilisateur : {user_message}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
