import pandas as pd
import re
from mapping import GENRE_MAPPING, THEME_MAPPING


class ModulRekomendasi:
    def __init__(self, dataset_path):
        self.df_anime = pd.read_csv(dataset_path, sep=";")
        
        self.df_anime['score'] = self.df_anime['score'].apply(
            lambda x: float(x) / 100 if x > 10 else float(x)
        )

        self.df_anime['genre_tema_gabungan'] = self.df_anime.apply(
            self._gabungkan_genre_tema, axis=1
        )

        self.df_anime = self.df_anime[self.df_anime['genre_tema_gabungan'].notna()].reset_index(drop=True)

        self.df_anime['genre_tema_gabungan'] = (
            self.df_anime['genre_tema_gabungan'].str.lower()
        )
        self.df_anime['genres_normalized'] = self.df_anime['genre_tema_gabungan'].apply(
            lambda x: [
                re.sub(r"\s+", " ", g.strip()
                                    .replace("-", " ")
                                    .replace("(", "")
                                    .replace(")", "")
                    ).strip()
                for g in str(x).split(",")
            ]
        )

        blacklist = {"boys love", "ecchi", "erotica", "girls love", "hentai"}

        def punya_blacklist(genres):
            return any(g in blacklist for g in genres)

        self.df_anime = self.df_anime[~self.df_anime['genres_normalized'].apply(punya_blacklist)]
        self.df_anime = self.df_anime.reset_index(drop=True)

        self.semua_genre_tema = self._kumpulkan_genre()

        self.normalisasi_genre = {**GENRE_MAPPING, **THEME_MAPPING}

        self.genre_panjang = sorted(
            [g for g in self.semua_genre_tema if len(g.split()) > 1],
            key=lambda x: len(x.split()), reverse=True
        )

        self.df_anime = self._filter_unique_franchises()

    def _gabungkan_genre_tema(self, row):
        """
        Gabungin kolom 'genres' dan 'themes' jadi satu string.
        Format: "genre1, genre2, tema1, tema2"
        Skip kalau keduanya kosong.
        """
        genres = str(row['genres']).strip() if pd.notna(row['genres']) else ""
        themes = str(row['themes']).strip() if pd.notna(row['themes']) else ""
        
        hasil = []
        if genres:
            hasil.append(genres)
        if themes:
            hasil.append(themes)
        
        return ", ".join(hasil) if hasil else None
    
    def _extract_franchise(self, title):
        if not isinstance(title, str):
            return ""
        
        t = title.lower().strip()
        
        franchise_keywords = [
            'naruto', 'bleach', 'one piece', 'fairy tail', 'dragon ball',
            'gintama', 'hunter x hunter', 'demon slayer', 'attack on titan',
            'my hero academia', 'sword art online', 'fate', 'jojo',
        ]
        
        for keyword in franchise_keywords:
            if keyword in t:
                return keyword
        t = re.sub(r'\s+(?:\d+(?:st|nd|rd|th))?\s*(?:season|part|cour)', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s+(?:season|part|cour)\s+\d+', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s+s\d+\b', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s+(?:i{1,3}|iv|v|vi{1,3}|ix|x)$', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s*[:\-–—]\s*.+$', '', t)
        t = re.sub(r'\.\s+.+$', '', t)
        t = re.sub(r'\s+film\b', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s+(?:movie|ova|ona|special|recap|gaiden|gekijouban)\s*\d*', '', t, flags=re.IGNORECASE)
        t = re.sub(r'\s+\d+\s*$', '', t)
        t = re.sub(r'[^\w\s]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        
        return t
    
    def _get_content_priority(self, title):
        t = str(title).lower()
        sequel_keywords = [
            r'\b(?:season|part|cour)\s+[2-9]',
            r'\bs[2-9]\b',
            r'\b(?:2nd|3rd|4th|5th|6th|7th|8th|9th|10th)\s+(?:season|part)',
            r'\b(?:ii|iii|iv|v|vi|vii|viii|ix|x)\b'
        ]
        if any(re.search(p, t) for p in sequel_keywords):
            return "sequel"
        if any(k in t for k in ['movie', 'film', 'theater', 'theatre', 'gekijouban', 'gekijoban']):
            return "movie"
        
        return "original"
        
    def _filter_unique_franchises(self):
        self.df_anime['franchise_key'] = self.df_anime['name'].apply(self._extract_franchise)
        self.df_anime['content_priority'] = self.df_anime['name'].apply(self._get_content_priority)
        priority_map = {'original': 0, 'sequel': 1, 'movie': 2}
        self.df_anime['priority_num'] = self.df_anime['content_priority'].map(priority_map)
        df_sorted = self.df_anime.sort_values(
            by=['priority_num', 'anime_id'],
            ascending=[True, True]
        )
        df_unique = df_sorted.drop_duplicates(subset='franchise_key', keep='first')
        df_unique = df_unique.drop(columns=['franchise_key', 'content_priority', 'priority_num']).reset_index(drop=True)
        
        return df_unique
    
    def _kumpulkan_genre(self):
        genre_unik = set()
        for baris in self.df_anime["genre_tema_gabungan"].dropna():
            for genre in baris.split(","):
                genre = genre.strip().replace("-", " ")
                genre = genre.replace("(", "").replace(")", "")
                genre = re.sub(r"\s+", " ", genre).strip()
                if genre:
                    genre_unik.add(genre)
        return genre_unik

    def ekstrak_genre(self, input_bersih):
        genre_ketemu = []
        for genre_multi in self.genre_panjang:
            if genre_multi in input_bersih:
                if genre_multi not in genre_ketemu:
                    genre_ketemu.append(genre_multi)
        kata_kepake = set()
        for genre in genre_ketemu:
            for kata in genre.split():
                kata_kepake.add(kata)
        tokens = input_bersih.split()
        for kata in tokens:
            if kata in kata_kepake:
                continue
            if kata in self.semua_genre_tema:
                if kata not in genre_ketemu:
                    genre_ketemu.append(kata)
            else:
                standar = self.normalisasi_genre.get(kata)
                if standar and standar in self.semua_genre_tema:
                    if standar not in genre_ketemu:
                        genre_ketemu.append(standar)
        
        return genre_ketemu

    def seleksi_anime(self, genre_dicari):
        hasil = []
        
        for _, anime in self.df_anime.iterrows():
            genre_anime = anime["genres_normalized"]
            cocok = sum(1 for g in genre_dicari if g in genre_anime)
            
            if cocok > 0:
                data = anime.to_dict()
                data["jumlah_cocok"] = cocok
                data["total_genre"] = len(genre_anime)
                hasil.append(data)
        
        if not hasil:
            return pd.DataFrame()
        
        df = pd.DataFrame(hasil)
        df = df.sort_values(
            by=["jumlah_cocok", "total_genre", "score"], 
            ascending=[False, True, False]
        )
        
        return df

    def recommender(self, genre_dicari):
        if not genre_dicari:
            return pd.DataFrame()
        return self.seleksi_anime(genre_dicari)