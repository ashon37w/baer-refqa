"""Text model adapter for C1 (Text-Oracle) and C2 (Text-ASR) conditions."""
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch


class TextQAAdapter:
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self._device)

    def answer(self, question: str, context: str) -> float:
        """Returns confidence score for the answer."""
        inputs = self.tokenizer(question, context, return_tensors="pt")
        inputs = {k: v.to(self._device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        probs = torch.softmax(start_logits + end_logits, dim=-1)
        confidence = probs.max().item()
        return confidence
