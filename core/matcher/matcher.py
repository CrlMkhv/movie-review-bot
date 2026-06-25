import os
import pandas as pd
from thefuzz import process

class MovieMatcher:
    def __init__(self, dataset_path: str):
        df = pd.read_csv(dataset_path)
        self.df = df
        self.movies = df["name_rus"].dropna().tolist()

    def find(self, query: str, threshold: int = 92):
        result, score = process.extractOne(query, self.movies)
        if score < threshold:
            return None
        row = self.df[self.df["name_rus"] == result].iloc[0]
        return {
            "title": row["name_rus"],
            "kinopoisk_id": int(row["movie_id"])
        }