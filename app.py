from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

with open("faqs.json", "r") as file:
    faqs = json.load(file)

questions = list(faqs.keys())
answers = list(faqs.values())

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)


def chatbot_response(user_input):

    user_vector = vectorizer.transform([user_input])

    similarity = cosine_similarity(
        user_vector,
        question_vectors
    )

    best_match = similarity.argmax()
    score = similarity[0][best_match]

    if score > 0.2:
        return answers[best_match]

    return "Sorry, I couldn't understand your question. Please ask something related to the FAQs."


def save_history(user, bot):

    with open("chat_history.json","r") as file:
        history=json.load(file)

    history.append({
        "user":user,
        "bot":bot,
        "time":str(datetime.now())
    })

    with open("chat_history.json","w") as file:
        json.dump(history,file,indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat",methods=["POST"])
def chat():

    user_message=request.json["message"]

    reply=chatbot_response(user_message)

    save_history(user_message,reply)

    return jsonify({
        "reply":reply
    })


if __name__=="__main__":
    app.run(debug=True)