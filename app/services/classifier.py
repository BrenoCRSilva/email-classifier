import anthropic
import json


class ClassificationService:
    def __init__(self, api_key, model, prompt_template):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.prompt_template = prompt_template

    def classify(self, email_content):
        try:
            prompt = self._build_prompt(email_content)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = response.content[0].text.strip()  # type: ignore

            # Passo necessário para garantir integridade do JSON na resposta
            import re

            def escape_newlines(match):
                content = match.group(1)
                return '"' + content.replace("\n", "\\n").replace("\r", "\\r") + '"'

            response_text = re.sub(
                r'"([^"]*?)"', escape_newlines, response_text, flags=re.DOTALL
            )

            return json.loads(response_text)

        except json.JSONDecodeError:
            return {"error": "Resposta inválida da IA"}

        except anthropic.APIError as e:
            raise ValueError(f"Erro da API Claude: {str(e)}")

        except Exception as e:
            raise ValueError(f"Classificação falhou: {str(e)}")

    def _build_prompt(self, email_content):
        return self.prompt_template.format(email_content=email_content)
