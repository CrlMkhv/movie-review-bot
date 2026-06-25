import os
from core.llm.gigachat_client import LLMClient
from core.matcher.matcher import MovieMatcher
from core.scraper.review_loader import ReviewLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ServiceManager:
    def __init__(self):
        self.llm = LLMClient()
        self.matcher = MovieMatcher(os.path.join(BASE_DIR, "data", "kp_final.csv"))
        self.loader = ReviewLoader(os.path.join(BASE_DIR, "data", "dataset"))

    def handle_query(self, query: str):
        extracted = self.llm.extract_movie_title(query)
        print(f"Извлечено: {extracted}")

        matched = self.matcher.find(extracted)
        if not matched:
            return "Фильм не найден в базе"

        print(f"Найдено: {matched['title']} (ID: {matched['kinopoisk_id']})")

        reviews = self.loader.get_reviews(matched["kinopoisk_id"])
        total = sum(len(v) for v in reviews.values())
        if total == 0:
            return f"Упс, у нас пока нет отзывов на фильм «{matched['title']}»"

        print(f"Отзывов найдено: pos={len(reviews['pos'])}, neu={len(reviews['neu'])}, neg={len(reviews['neg'])}")

        summary = self.llm.summarize_reviews(matched["title"], reviews)
        return summary