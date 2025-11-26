import json
import pickle
from recommender import ModulRekomendasi
from chatbot_respons import ChatbotResponse
from intent_handler import PengenalanIntent


class Chatbot:
    def __init__(self, dataset_path, intent_path, template_path, 
                 preprocessor_path, model_path, vectorizer_path):
        
        self.genre_terlarang = {"hentai", "ecchi", "erotica", "boys love", 
                               "girls love", "yuri", "yaoi", "bokep", "porno","hentong","vanila","ntr"}
        
        with open(preprocessor_path, "rb") as f:
            self.preprocessor = pickle.load(f)
        
        with open(intent_path, "r", encoding="utf-8") as f:
            data_intent = json.load(f)
        
        self.intent_handler = PengenalanIntent(
            data_intent=data_intent,
            model_path=model_path,
            vectorizer_path=vectorizer_path,
            template_path=template_path,
        )
        
        self.core = ModulRekomendasi(dataset_path)
        
        self.generator = ChatbotResponse(template_path)
        self.max_hasil = 5

    def chat(self, pesan_user):
        print("Input:", pesan_user)
        
        input_bersih = self.preprocessor.text_preprocessing(pesan_user)
        print("Input bersih:", input_bersih)
        
        if any(bad in input_bersih for bad in self.genre_terlarang):
            return self.generator._ambil_template_respon("genre_terlarang")
        
        intent = self.intent_handler.pilih_tag(input_bersih)
        
        if intent in {"salam", "perkenalan", "mau", 
                    "gak_mau", "terimakasih", "selamat_tinggal", 
                    "tanya_cara_pakai", "tanya_fitur",
                    "tanya_lagi_ngapain", "tanya_tempat_nonton", "tanya_genre_tema",
                    "tanya_jumlah_rekomendasi", "udah_pernah_nonton",
                    "komplain_hasil", "pertanyaan_dasar_anime",
                    "anime_pemula", "gak_ada_preferensi",
                    "minta_pilihin", "minta_satu_terbaik_setelah_rekomendasi"}:
            return self.intent_handler.ambil_respon(intent)
        
        if intent == "nanyain_genre":
            genre = self.core.ekstrak_genre(input_bersih)
            if genre:
                return self.generator.ambil_penjelasan_genre(genre[0])
            return self.intent_handler.ambil_respon("nanyain_genre")
        
        genre = self.core.ekstrak_genre(input_bersih)
        
        if genre:
            return self._proses_rekomendasi(input_bersih)
        
        if intent == "minta_rekomendasi":
            return self.intent_handler.ambil_respon(intent)
        return self.generator._ambil_template_respon("fallback")

    def _proses_rekomendasi(self, input_bersih):
        genre = self.core.ekstrak_genre(input_bersih)
                
        df_hasil = self.core.recommender(genre)
        
        if df_hasil.empty:
            return self.generator._ambil_template_respon("gak_ada_hasil")
        
        df_top = df_hasil.head(self.max_hasil)
        return self.generator.format_respon_rekomendasi(df_top, genre)