from transformers import MarianMTModel, MarianTokenizer


class Translator:
    def __init__(self, source_language, target_language, text):
        super(Translator, self).__init__()
        self.source_language = source_language
        self.target_language = target_language
        self.text = text

    def set_translate(self):
        model_name = f"opus-mt-{self.source_language}-{self.target_language}"
        tokenizer = MarianTokenizer.from_pretrained(f"./language_models/{model_name}")
        pretrained_model = MarianMTModel.from_pretrained(
            f"./language_models/{model_name}"
        )
        translated = pretrained_model.generate(
            **tokenizer(self.text, return_tensors="pt", padding=True)
        )
        translation = [
            tokenizer.decode(t, skip_special_tokens=True) for t in translated
        ]
        return str(translation).strip("['']")
