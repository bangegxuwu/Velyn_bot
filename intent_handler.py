import numpy as np
import pickle
import json
import random


class PengenalanIntent:
    def __init__(self, data_intent, model_path, vectorizer_path, template_path):
        self.data_intent = data_intent
        self.threshold = 0.30

        with open(model_path, "rb") as f:
            self.model_naive_bayes = pickle.load(f)
        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(template_path, "r", encoding="utf-8") as f:
            self.template_respon = json.load(f)

        self.list_intent = self.model_naive_bayes.classes_

    def pilih_tag(self, input_bersih):
        vektor = self.vectorizer.transform([input_bersih])
        proba = self.model_naive_bayes.predict_proba(vektor)[0]

        urutan = np.argsort(proba)[::-1]
        intent_top = self.list_intent[urutan]
        proba_top = proba[urutan]

        if proba_top[0] < self.threshold:
            return "unknown"

        return intent_top[0]


    def ambil_respon(self, intent):
        if intent == "unknown":
            return None

        for item in self.data_intent:
            if item["tag"] == intent:
                if item["responses"]:
                    return random.choice(item["responses"])

        return None
