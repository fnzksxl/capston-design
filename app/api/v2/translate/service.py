from app.AI import test
from ..user import utils


async def itemTranslate(data, cred):
    if await utils.verify_user(cred):
        translated_text = test.generate_text(data.dialect)[0]  # Translation
        english_text = test.translate_with_papago(translated_text)
        chinese_text = test.translate_with_papago(translated_text, target_lang="zh-CN")
        japanese_text = test.translate_with_papago(translated_text, target_lang="ja")

        return {
            "dialect": data.dialect,
            "standard": translated_text,
            "english": english_text,
            "chinese": chinese_text,
            "japanese": japanese_text,
        }
