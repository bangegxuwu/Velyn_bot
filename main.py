from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)

chatbot = Chatbot(
    dataset_path="dataset/top_anime_dataset_v2.csv",
    intent_path="dataset/intent.json",
    template_path="dataset/template_respon.json",
    preprocessor_path="model/preprocessor.pkl",
    model_path="model/model.pkl",
    vectorizer_path="model/vectorizer.pkl",
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        pesan = request.json.get("message", "").strip()
        
        if not pesan:
            return jsonify({"reply": "Maaf, pesanmu kosong."})
        
        balasan = chatbot.chat(pesan)
        return jsonify({"reply": balasan})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Maaf, ada error nih."})


if __name__ == "__main__":
    app.run(debug=False)