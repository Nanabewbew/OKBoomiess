from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize LangChain models
boomer_chain = ConversationChain(
    llm=ChatOpenAI(temperature=0.7, openai_api_key="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"),
    memory=ConversationBufferMemory()
)

baby_chain = ConversationChain(
    llm=ChatOpenAI(temperature=0.9, openai_api_key="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"),
    memory=ConversationBufferMemory()
)

@app.route('/start', methods=['POST'])
def start_conversation():
    data = request.json
    if not data or 'age_group' not in data:
        return jsonify({"error": "Invalid request"}), 400
    age_group = data['age_group']
    if age_group == "Boomers":
        return jsonify({"message": "Welcome, Boomer! How can I assist you today?"})
    elif age_group == "Babies":
        return jsonify({"message": "Hey there, kiddo! Wassup?"})
    else:
        return jsonify({"error": "Invalid age group"}), 400

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'age_group' not in data or 'user_input' not in data:
        return jsonify({"error": "Invalid request"}), 400

    age_group = data['age_group']
    user_input = data['user_input'].strip().lower()  # Normalize user input for easier matching

    # Predefined responses for each age group (keys are now lowercase)
    responses = {
        "Boomers": {
            "hello": "Hello! How can I assist you today?",
            "how are you": "I'm doing great! Thanks for asking. What about you?",
            "hey what's the news": "The news today is quite interesting. Have you read anything?",
            "default": "That's intriguing. Tell me more!"
        },
        "Babies": {
            "hello": "Hi there, kiddo! What’s up?",
            "play": "Let’s play! What’s your favorite game?",
            "wats yo favorite color": "Mah favorite color is blue mann. It's rizzy. What’s yours?",
            "default": "I’m not sure I got that, but it sounds fun!"
        }
    }

    # Select the appropriate responses for the age group
    age_responses = responses.get(age_group, {})
    response = age_responses.get(user_input, age_responses.get("default", "I don't understand that."))

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
