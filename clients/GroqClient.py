import os
from groq import Groq

class GroqClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API da Groq é obrigatória (GROQ_API_KEY).")
        self.client = Groq(api_key=self.api_key)

    def invoke(self, prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
        """
        Realiza uma inferência (chat completion) utilizando a biblioteca oficial da Groq.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
            )
            
            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"Erro ao conectar com a Groq: {e}")
            raise
