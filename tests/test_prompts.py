import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.services.classifier import ClassificationService


def test_prompt_classification_accuracy(prompt_name, prompt_text):
    test_emails = []

    with open("test_data/productive_emails.json", "r") as f:
        emails = json.load(f)
        for email in emails:
            email["expected_classification"] = "Produtivo"
            test_emails.append(email)

    with open("test_data/unproductive_emails.json", "r") as f:
        emails = json.load(f)
        for email in emails:
            email["expected_classification"] = "Improdutivo"
            test_emails.append(email)

    with open("test_data/edge_case_emails.json", "r") as f:
        emails = json.load(f)
        test_emails.extend(emails)

    classifier = ClassificationService(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307",
        prompt_template=prompt_text,
    )

    correct_classifications = 0
    total = len(test_emails)

    print(f"\nTestando {prompt_name}...")

    for email in test_emails:
        try:
            result = classifier.classify(email["content"])
            predicted_classification = result.get("classification", "")
            expected_classification = email["expected_classification"]

            if predicted_classification == expected_classification:
                correct_classifications += 1
                print("✓", end="")
            else:
                print("✗", end="")
        except Exception as e:
            print("E", end="")

    accuracy = (correct_classifications / total) * 100
    print(f" {correct_classifications}/{total} = {accuracy:.1f}%")
    return accuracy


prompts = {}
for prompt_file in Path("../prompts").glob("prompt_v*.txt"):
    with open(prompt_file, "r") as f:
        prompts[prompt_file.stem] = f.read()

print("Teste A/B de Precisão de Classificação")
print("=" * 36)

results = []
for name, text in prompts.items():
    try:
        accuracy = test_prompt_classification_accuracy(name, text)
        results.append((name, accuracy))
    except Exception as e:
        print(f"\nErro testando {name}: {e}")

print("\n" + "=" * 36)
print("RANKING DE PRECISÃO:")
results.sort(key=lambda x: x[1], reverse=True)
for i, (name, eff) in enumerate(results, 1):
    print(f"{i}. {name}: {eff:.1f}%")

if results:
    print(f"\nMelhor prompt: {results[0][0]} ({results[0][1]:.1f}%)")
    print("Use este prompt para máxima precisão de classificação.")
else:
    print("\nNenhum prompt foi testado com sucesso. Verifique a configuração da API.")
