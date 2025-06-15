from fastapi import APIRouter
from pydantic import BaseModel
from googletrans import Translator

router = APIRouter()
translator = Translator()

class TranslationInput(BaseModel):
    text: str
    dest_lang: str

@router.post("/translate")
def translate_text(data: TranslationInput):
    translated = translator.translate(data.text, dest=data.dest_lang)
    return {
        "original": data.text,
        "translated": translated.text,
        "source_lang": translated.src
    }