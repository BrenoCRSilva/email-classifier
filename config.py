import os


def load_from_file():
    try:
        with open("prompt.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Prompt padrão aqui..."


class Config:
    SUPPORTED_FILE_TYPES = [".txt", ".docx"]
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL = "claude-3-haiku-20240307"
    PROMPT_TEMPLATE = load_from_file()
