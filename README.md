# Email Classifier

Aplicação Flask para classificação automática de emails utilizando Claude AI da Anthropic.

## Arquitetura

### Estrutura do Projeto
```
email-classifier/
├── app/
│   ├── __init__.py             # Factory pattern para criação da app
│   ├── api/
│   │   └── routes.py           # Endpoints REST
│   ├── services/
│   │   ├── classifier.py       # Serviço de classificação via Claude
│   │   └── file_processor.py   # Processamento de arquivos .txt/.docx
│   └── static/
│       └── routes.py           # Servir arquivos estáticos
├── static/                     # Frontend SPA
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── prompts/                    # Templates de prompt para IA
├── tests/                      # Dados de teste e casos de uso
├── config.py                   # Configurações centralizadas
├── index.py                    # Ponto de entrada WSGI
└── vercel.json                 # Configuração de deploy
```

### Componentes Principais

#### `ClassificationService` (classifier.py)
- Wrapper para API do Claude (Anthropic)
- Modelo: `claude-3-haiku-20240307`
- Temperature: 0.1 para consistência
- Max tokens: 400
- Sanitização de JSON response com regex para escape de newlines

#### `FileProcessingService` (file_processor.py)
- Extração de texto de arquivos .txt e .docx
- Fallback de encoding para .txt (utf-8, latin-1, cp1252)
- Validação de tipos baseada em extensão
- Limite de tamanho configurável (10MB)

#### Blueprint Structure
- `/api/*` - REST endpoints
- `/` - Servir interface estática

## API Endpoints

### POST `/api/classify`
Classifica conteúdo de email e gera resposta sugerida.

**Request:**
```json
{
  "email_content": "string"
}
```

**Response:**
```json
{
  "classification": "Produtivo|Improdutivo",
  "suggested_response": "string"
}
```

### POST `/api/upload`
Processa upload de arquivo e extrai conteúdo.

**Request:** `multipart/form-data` com campo `file`

**Response:**
```json
{
  "email_content": "string",
  "filename": "string"
}
```

## Configuração

### Environment Variables
- `ANTHROPIC_API_KEY`: Chave da API Claude (obrigatória)

### Config Class (config.py)
```python
SUPPORTED_FILE_TYPES = [".txt", ".docx"]
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
ANTHROPIC_MODEL = "claude-3-haiku-20240307"
PROMPT_TEMPLATE = "..."  # Template estruturado em português
```

## Lógica de Classificação

### Critérios Implementados no Prompt
- **Produtivo**: Demandas de trabalho, clientes, reuniões, prazos
- **Improdutivo**: Cortesias, conversas sociais, felicitações
- **Regra de Precedência**: Conteúdo misto → Produtivo

### Geração de Respostas
- Contexto baseado na classificação
- Tom profissional para emails produtivos
- Cortesia para emails improdutivos
- Handling de conteúdo inapropriado

## Stack Tecnológico

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin requests
- **Anthropic SDK**: Integração com Claude AI
- **python-docx**: Processamento de documentos Word
- **lxml**: Parsing XML/HTML

### Frontend
- Vanilla JavaScript (SPA)
- Interface de chat interativa
- Upload de arquivos via drag-and-drop
- Contador de caracteres

### Deploy
- **Vercel**: Serverless deployment
- Python runtime para Flask
- Static file serving para frontend

## Tratamento de Erros

### API Errors
- `KeyError`: Campos obrigatórios ausentes
- `ValueError`: Tipos de arquivo não suportados
- `anthropic.APIError`: Erros da API Claude
- `json.JSONDecodeError`: Response malformado da IA

### File Processing
- Validação de extensão
- Múltiplos encodings para .txt
- Limite de tamanho de arquivo
- Sanitização de conteúdo

## Considerações de Segurança

- Validação rigorosa de input
- Sanitização de JSON response
- Limit de upload configurável
- CORS habilitado para cross-origin
- Não exposição de chaves de API no frontend