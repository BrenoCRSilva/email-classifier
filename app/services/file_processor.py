from flask import current_app
from docx import Document
import io


class FileProcessingService:
    def extract_text(self, file, filename):
        supported_types = current_app.config.get("SUPPORTED_FILE_TYPES")

        if not any(filename.lower().endswith(ext) for ext in supported_types):
            raise ValueError(
                f"Unsupported file type. Supported: {', '.join(supported_types)}"
            )

        filename_lower = filename.lower()
        if filename_lower.endswith(".docx"):
            return self._extract_from_docx(file)
        elif filename_lower.endswith(".txt"):
            return self._extract_from_txt(file)

    def _extract_from_docx(self, file):
        doc = Document(io.BytesIO(file.read()))
        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(text_parts)

    def _extract_from_txt(self, file):
        content = file.read()
        encodings = ["utf-8", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue

        raise ValueError("Could not decode text file")
