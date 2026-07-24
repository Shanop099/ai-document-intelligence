from groq import Groq
from config import Config


class GroqClient:

    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def generate(self, prompt: str, temperature: float = 0):

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()


groq_client = GroqClient()