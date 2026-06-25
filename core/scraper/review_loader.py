import os
import random

class ReviewLoader:
    def __init__(self, reviews_folder: str):
        self.folder = reviews_folder

    def get_reviews(self, kinopoisk_id: int, per_sentiment: int = 5) -> dict:
        result = {"pos": [], "neu": [], "neg": []}
        for sentiment in ["pos", "neu", "neg"]:
            path = os.path.join(self.folder, sentiment)
            if not os.path.exists(path):
                continue
            files = [f for f in os.listdir(path) if f.startswith(f"{kinopoisk_id}-")]
            random.shuffle(files)
            for filename in files[:per_sentiment]:
                filepath = os.path.join(path, filename)
                with open(filepath, encoding="utf-8") as f:
                    result[sentiment].append(f.read().strip())
        return result