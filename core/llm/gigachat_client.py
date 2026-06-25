import base64
import os
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.credentials = self._get_credentials()
        self.client = GigaChat(
            credentials=self.credentials,
            scope=os.getenv("GIGACHAT_SCOPE"),
            verify_ssl_certs=False
        )

    def extract_movie_title(self, user_query: str) -> str:
        messages = [
            SystemMessage(content=(
                "Ты помощник, который извлекает название фильма из запроса пользователя. "
                "Верни название фильма ровно так, как оно написано в запросе, без исправлений и изменений. "
                "Верни только само название, без лишних слов."
                "Обязательно верни название на русском языке."
                "Примеры: Что люди думают про джона уика // джона уика"
                "Примеры: Хочу посмотреть интерстелар // интерстелар"
                "Примеры: Планирую посмотреть Аватара // Аватара"
            )),
            HumanMessage(content=user_query)
        ]
        response = self.client.invoke(messages)
        return response.content.strip()

    @staticmethod
    def _get_credentials() -> str:
        client_id = os.getenv("GIGACHAT_CLIENT_ID")
        client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")
        raw = f"{client_id}:{client_secret}"
        encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
        return encoded

    def summarize_reviews(self, title: str, reviews: dict) -> str:
        all_reviews = (
                reviews.get("pos", []) +
                reviews.get("neu", []) +
                reviews.get("neg", [])
        )
        combined = "\n\n".join(all_reviews)

        prompt = prompt = f"""Ты помощник, который анализирует зрительские отзывы на фильмы.
    Тебе дали несколько отзывов на фильм «{title}». 
    Напиши краткий анализ общественного мнения — 3-4 предложения связным текстом.

    Правила:
    - Не пересказывай сюжет и не раскрывай спойлеры
    - Говори о том, что зрители выделяют: атмосфера, актёрская игра, режиссура, эмоции, темп
    - Отражай разные точки зрения если они есть
    - Пиши нейтрально, без своей оценки
    - Не используй заголовки и списки
    - Положительные и отрицательные мнения должны быть разделены
    
    Примеры хорошего ответа:
    "Зрители в целом высоко оценивают актёрскую игру и атмосферу фильма, особо отмечая убедительность главного героя. Многие говорят о сильном эмоциональном воздействии и долгом послевкусии после просмотра. Часть аудитории указывает на медленный темп повествования, однако большинство считает это осознанным авторским решением."
    "Комментаторы разделились во мнениях: одни называют фильм шедевром с выдающейся операторской работой, другие считают сюжет излишне запутанным. Практически все сходятся в том, что картина требует внимательного просмотра и не отпускает до финальных титров."

    Отзывы:
    {combined}
    """

        messages = [HumanMessage(content=prompt)]
        response = self.client.invoke(messages)
        return response.content.strip()

if __name__ == "__main__":
    gigachat_client = LLMClient()
    data = gigachat_client.extract_movie_title("")
    print(data)