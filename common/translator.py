from transformers import MarianMTModel, MarianTokenizer


class Translator:
    def __init__(self, src_lang: str, trg_lang: str, text: str):
        super(Translator, self).__init__()
        self.src_lang = src_lang
        self.trg_lang = trg_lang
        self.text = text

    def set_translate(self) -> str:
        model = f"opus-mt-{self.src_lang}-{self.trg_lang}"
        token = MarianTokenizer.from_pretrained(f"./language_models/{model}")
        trained = MarianMTModel.from_pretrained(f"./language_models/{model}")
        generate = trained.generate(
            **token(self.text, return_tensors="pt", padding=True)
        )
        result = [token.decode(t, skip_special_tokens=True) for t in generate]
        return str(result).strip("['']")
