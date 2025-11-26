import json
import pandas as pd
import random
from genre_explanations import GENRE_EXPLANATIONS

class ChatbotResponse:
    def __init__(self, template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            self.template_respon = json.load(f)

    def _ambil_template_respon(self, key):
        pilihan = self.template_respon[key]
        return random.choice(pilihan) if isinstance(pilihan, list) else pilihan

    def ambil_penjelasan_genre(self, nama_genre):
        penjelasan = GENRE_EXPLANATIONS.get(nama_genre.lower())
        if penjelasan:
            return f"<b>{nama_genre.title()}</b> {penjelasan}"
        return None

    def format_respon_rekomendasi(self, df_hasil, genre_dicari=None):
        if df_hasil.empty:
            return self._ambil_template_respon("gak_ada_hasil")

        if genre_dicari:
            template = self._ambil_template_respon("header_kasih_rekomendasi")
            kriteria = ", ".join(genre_dicari)
            respon = template.format(criteria=kriteria)
        else:
            respon = self._ambil_template_respon("header_kasih_rekomendasi")

        for no, (_, anime) in enumerate(df_hasil.iterrows(), 1):
    
            genres_raw = anime.get("genres", "")
            themes_raw = anime.get("themes", "")
            
            genre_list = [g.strip() for g in str(genres_raw).split(",")] if pd.notna(genres_raw) and genres_raw else []
            tema_list = [t.strip() for t in str(themes_raw).split(",")] if pd.notna(themes_raw) and themes_raw else []
            
            teks_genre = ", ".join(genre_list) if genre_list else ""
            teks_tema = ", ".join(tema_list) if tema_list else ""
            
            info_parts = []
            if teks_genre:
                info_parts.append(f'<span class="info-label">Genre:</span> <span class="info-value">{teks_genre}</span>')
            if teks_tema:
                info_parts.append(f'<span class="info-label">Tema:</span> <span class="info-value">{teks_tema}</span>')
            html_info = ' <span class="info-separator">•</span> '.join(info_parts)
            
            episode_display = "Tidak tersedia"
            if pd.notna(anime.get("episodes")) and anime["episodes"] != "":
                try:
                    ep = float(anime["episodes"])
                    episode_display = str(int(ep if ep < 100 else round(ep / 100)))
                except:
                    pass
            
            data_anime = {
                "name": str(anime.get("name", "Tidak tersedia")),
                "english_name": str(anime["english_name"]) if pd.notna(anime.get("english_name")) and anime.get("english_name") else "Tidak tersedia",
                "score": float(anime["score"]) if pd.notna(anime.get("score")) else "Tidak tersedia",
                "premiered": str(anime["premiered"]) if pd.notna(anime.get("premiered")) and anime.get("premiered") else "Tidak tersedia",
                "episodes": episode_display,
                "duration": str(anime["duration"]) if pd.notna(anime.get("duration")) and anime.get("duration") else "Tidak tersedia",
                "genres": teks_genre if teks_genre else "Tidak ada",
                "themes": teks_tema if teks_tema else "Tidak ada",
                "synopsis": str(anime["synopsis"]) if pd.notna(anime.get("synopsis")) and anime.get("synopsis") else "Sinopsis tidak tersedia",
                "image_url": str(anime["image_url"]) if pd.notna(anime.get("image_url")) and anime.get("image_url") else "",
                "anime_url": str(anime["anime_url"]) if pd.notna(anime.get("anime_url")) and anime.get("anime_url") else "",
            }
            
            json_encoded = json.dumps(data_anime).replace('"', "&quot;")
            
            respon += f"""<div class="anime-card">
            <div class="anime-title">{no}. {anime['name']}</div>
            <div class="anime-info-row">{html_info}</div>
            <button class="detail-btn" data-anime="{json_encoded}">Lihat Detail</button>
            </div>"""
        
        footer = self._ambil_template_respon("soft_footer")
        respon += footer
        
        return respon.strip()