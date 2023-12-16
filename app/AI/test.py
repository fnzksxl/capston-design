from transformers import pipeline
import requests

from app.AI import config
from app.config import settings

nlg_pipeline = pipeline(
    "text2text-generation", model=config.model_path, tokenizer=config.model_name
)


def generate_text(text, num_return_sequences=1, max_length=60):
    target_style_name = "표준어"
    text = f"{target_style_name} 말투로 변환:{text}"
    out = nlg_pipeline(text, num_return_sequences=num_return_sequences, max_length=max_length)
    return [x["generated_text"] for x in out]


def translate_with_papago(text, source_lang="ko", target_lang="en"):
    url = "https://openapi.naver.com/v1/papago/n2mt"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": settings.CLIENT_ID,
        "X-Naver-Client-Secret": settings.CLIENT_SECRET,
    }

    data = {"source": source_lang, "target": target_lang, "text": text}

    response = requests.post(url, headers=headers, data=data)
    translation_result = response.json()
    translated_text = translation_result["message"]["result"]["translatedText"]

    return translated_text
