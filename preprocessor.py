import re
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

KAMUS_NORMALISASI = {
    "kau": "kamu",
    "lu": "kamu",
    "loe": "kamu",
    "lo":"kamu",
    "kmu":"kamu",
    "anda": "kamu",
    "hi": "hai",
    "hey": "hai",
    "hei": "hai",
    "helo": "hai",
    "hello": "hai",
    "halo": "hai",
    "vel": "velyn",
    "bot": "velyn",
    "aja": "saja",
    "ampe": "sampai",
    "sampe": "sampai",
    "ama": "sama",
    "sm": "sama",
    
    
    "thx": "terima kasih",
    "tengkyu": "terima kasih",
    "thanks": "terima kasih",
    "makasi": "terima kasih",
    "makasih": "terima kasih",
    "trimakasih": "terima kasih",
    "makaciw": "terima kasih",
    "tengkiu": "terima kasih",
    "sankyu": "terima kasih",
    
    
    "gw": "saya",
    "gua": "saya",
    "aku": "saya",
    "ak": "saya",
    "w": "saya",
    "gue":"saya",
    
    
    "gak": "tidak",
    "nggak": "tidak",
    "ga": "tidak",
    "engga": "tidak",
    "g": "tidak",
    "nope": "tidak",
    "kagak": "tidak",
    "kaga": "tidak",
    "enggak": "tidak",
    "gaada": "tidak ada",
    "gada": "tidak ada",
    
    
    "gimana": "bagaimana",
    "gmn": "bagaimana",
    "gmana": "bagaimana",
    "gimanakah": "bagaimana",
    "gimna": "bagaimana",
    "apakah": "apa",
    "apaan": "apa",
    "knp": "kenapa",
    "knapa": "kenapa",
    "napa": "kenapa",
    "dimana": "mana",
    "dmn": "mana",
    "dmana": "mana",
    "kemana": "mana",
    "mudeng": "paham",
    
    
    "udah": "sudah",
    "dah": "sudah",
    "udh": "sudah",
    "pengen": "ingin",
    "pgn": "ingin",
    "mo": "ingin",
    "mau": "ingin",
    "mw": "ingin",
    "pingin": "ingin",
    "pen": "ingin",
    "pgen": "ingin",
    
    
    "gitu": "begitu",
    "gt": "begitu",
    "cuman": "hanya",
    "cuma": "hanya",
    "cm": "hanya",
    "kaya": "seperti",
    "kayak": "seperti",
    "kyak": "seperti",
    "kyk": "seperti",
    "banget": "sangat",
    "bgt": "sangat",
    "bener": "benar",
    "bnr": "benar",
    
    
    "rekomendasiin": "rekomendasi",
    "rekomendasikan": "rekomendasi",
    "cariin": "cari",
    "carikan": "cari",
    "saranin": "saran",
    "sarankan": "saran",
    "kasiin": "kasih",
    "kasihkan": "kasih",
    "bandingin": "banding",
    "bandingkan": "banding",
    "jelasin": "jelas",
    "jelaskan": "jelas",
    "tlg": "tolong",
    
    
    "req": "request",
    "rekomen": "rekomendasi",
    "recom": "rekomendasi",
    "rekomend": "rekomendasi",
    "rekom": "rekomendasi",
    "recommend": "rekomendasi",
    
    
    "nyari": "mencari",
    "nyariin": "mencari",
    
    
    "nanya": "tanya",
    "nanyain": "tanya",
    
    
    "yg": "yang",
    "dgn": "dengan",
    "utk": "untuk",
    "buat": "untuk",
    "krn": "karena",
    "jd": "jadi",
    "tp": "tetapi",
    "tapi": "tetapi",
    "emang": "memang",
    "kalo": "kalau",
    "klo": "kalau",
    "klau": "kalau",
    "ato": "atau",
    "atw": "atau",
    "lbih": "lebih",
    
    
    "okay": "oke",
    "ok": "oke",
    "oks": "oke",
    "okeh": "oke",
    "oce": "oke",
    "y": "iya",
    "ya": "iya",
    "yap": "iya",
    "yaps": "iya",
    "yoi": "iya",
    "yup": "iya",
    "yups": "iya",
    "sip": "iya",
    "siap": "iya",
    "met": "selamat",
    "slamat": "selamat",
    "pengertian":"definisi",
    "arti":"definisi",
    "tutorial":"panduan",
    
    
    "gamau": "tidak ingin",
    "gmau": "tidak ingin",
    "gkmau": "tidak ingin",
    "gakmau": "tidak ingin",
    "males": "malas",
    "mls": "malas",
    "ogah": "tidak",
    "gajadi": "tidak jadi",
    "gajd": "tidak jadi",
    "skip": "lewati",
    
    
    "info": "informasi",
       
    
    "cocok": "sesuai",
    "sesuai": "sesuai",
    "pas": "sesuai",
    "faham": "paham",
    "ngerti": "paham",
    "tau": "tahu",
    
    
    "preferensi": "pilih",
    "pilihan": "pilih",
    "opsi": "pilih",
    "option": "pilih",
    "serah": "terserah",
    "trsrh": "terserah",
    "random": "random",
    
    
    "database": "data",
    "source": "sumber",
    
    
    "bandingkan": "banding",
    "bandingin": "banding",
    "compare": "banding",
    
    
    "usia": "umur",
    
    
    "ganti": "ubah",
    "berbeda": "beda",
    "tutor":"panduan",
    
    "tuh": "itu",
    "ayok": "ayo",
    "yuk": "ayo",
    "ayuk": "ayo",
    "kenalin":"kenal",
    "pakenya":"pakai",
    "kelar":"selesai",
    "ni":"ini",
    "nyeritain":"ceritakan",
    "pakenya":"pakainya",
    "perkenalin":"perkenalkan",
    "samlekom":"assalamualaikum","lanjutin":"lanjutkan","dilanjutin":"dilanjutkan","list":"daftar","disaranin":"disarankan","ngga":"tidak",
}

STOPWORDS = {
    "yang","dan","atau","pada","yuk","dengan","karena","sehingga",
    "bahwa","yaitu","yakni","adalah","ialah","merupakan","akan","sedang","telah",
    "velyn","pun","kah","tuh","nih","sih","dong","deh","dah","yah","oh","eh","nah","kok",
    "kan","juga","loh","lah","lho","weh","wih","wah","buset","haha","hahaha","hehe",
    "hehehe","wkwk","wkwkwk","nya","uh","uhh","uhhh","ehh","emm","emmm","mm","hmm",
    "mhmmm","btw","please","pls","plis","jir","anjir","bjir", "ini","ayo","saja","di","ke","nya","saat",
}


class TextPreprocessor:
    def __init__(self):
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        self.kamus = KAMUS_NORMALISASI  
        self.stopwords = STOPWORDS 

    def case_folding(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s-]", " ", text)
        text = text.replace("-", " ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenization(self, text):
        tokens = word_tokenize(text)
        return [t for t in tokens if t.isalpha()]

    def normalization(self, tokens):
        hasil = []
        for token in tokens:
            normal = self.kamus.get(token, token)
            if normal:
                hasil.append(normal)
        return hasil

    def stopwords_removal(self, tokens):
        return [t for t in tokens if t not in self.stopwords] 

    def stemming(self, text):
        return self.stemmer.stem(text)

    def text_preprocessing(self, text):
        if not isinstance(text, str):
            return ""

        
        text = self.case_folding(text)

        
        tokens = self.tokenization(text)

        
        tokens = self.normalization(tokens)

        
        tokens = self.stopwords_removal(tokens)

        
        text = " ".join(tokens)

        
        text = self.stemming(text)

        return text
