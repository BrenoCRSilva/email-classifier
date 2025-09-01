from flask import Blueprint, current_app, request, jsonify

from ..services.classifier import ClassificationService
from ..services.file_processor import FileProcessingService

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/classify", methods=["POST"])
def classify():
    try:
        data = request.get_json()
        classifier = ClassificationService(
            api_key=current_app.config["ANTHROPIC_API_KEY"],
            model=current_app.config["ANTHROPIC_MODEL"],
            prompt_template=current_app.config["PROMPT_TEMPLATE"],
        )
        result = classifier.classify(data["email_content"])
        return jsonify(result), 200
    except KeyError:
        return (
            jsonify({"error": "Campo 'email_content' ausente no corpo da requisição"}),
            400,
        )


@api_bp.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        file_processor = FileProcessingService()

        if not file or file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        extracted_text = file_processor.extract_text(file, file.filename)

        return jsonify({"email_content": extracted_text, "filename": file.filename})

    except KeyError:
        return jsonify({"error": "No file provided"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "File processing failed"}), 500
