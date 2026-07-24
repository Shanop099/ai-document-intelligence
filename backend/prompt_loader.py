from pathlib import Path


class PromptLoader:

    PROMPTS_DIR = Path("prompts")

    @staticmethod
    def load(prompt_name: str) -> str:
        prompt_path = PromptLoader.PROMPTS_DIR / prompt_name

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        return prompt_path.read_text(encoding="utf-8")