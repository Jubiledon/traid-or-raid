# agents/llm_client.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()


class GemmaClient:

    def __init__(
        self,
        model_path: str = "./google/gemma-3-1b-it-local",
        temperature: float = 0.7,
    ):
        self.temperature = temperature
        self.device = self._detect_device()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
        ).to(self.device)

    def generate(self, prompt: str) -> str:
        inputs = self._encode(prompt)
        output = self._generate(inputs)

        return self._decode(output, inputs)

    def _detect_device(self) -> str:
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _encode(self, prompt: str):
        return self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
        ).to(self.device)

    def _generate(self, inputs):
        with torch.no_grad():
            return self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=100,
                temperature=self.temperature,
                do_sample=True,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id,
            )

    def _decode(self, output, inputs) -> str:
        new_tokens = output[0][inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(
            new_tokens,
            skip_special_tokens=True,
        )

class AnthropicClient: 
    def __init__(
        self,
        model_path: str = None,       # ignored
        temperature: float = 0.7,
    ):
        self.temperature = temperature
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text