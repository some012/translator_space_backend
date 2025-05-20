from typing import Annotated

import torch
from fastapi import Depends
from transformers import MarianMTModel, MarianTokenizer

from app.enums.language import LanguageEnums


class TranslationService:

    def _resolve_translation_language_in_file(self, language: str) -> LanguageEnums:
        handle_language = {
            "en": LanguageEnums.EN.value,
            "fr": LanguageEnums.FR.value,
            "uk": LanguageEnums.UK.value,
            "es": LanguageEnums.ES.value,
        }

        if language not in handle_language:
            raise ValueError(f"Unsupported language code: {language}")

        return handle_language[language]

    async def translate(
        self,
        texts: str | list[str],
        language: str,
        max_length=512,
        num_beams=5,
    ):
        try:
            # Определение устройства (GPU или CPU)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            model_name = self._resolve_translation_language_in_file(language)

            # Загрузка токенизатора и модели
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name).to(device)

            # Токенизация входных текстов с учётом максимальной длины
            inputs = tokenizer(
                texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length,
            ).to(device)

            # Генерация перевода с использованием beam search
            translated_tokens = model.generate(
                **inputs,
                num_beams=num_beams,
                early_stopping=True,
                max_length=max_length,
            )

            # Декодирование переведённых токенов в текст
            translated_texts = tokenizer.batch_decode(
                translated_tokens, skip_special_tokens=True
            )

            return translated_texts

        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            return []

    @staticmethod
    def register():
        return TranslationService()

    @staticmethod
    def register_deps():
        return Annotated[TranslationService, Depends(get_translation_service)]


async def get_translation_service():
    return TranslationService()
