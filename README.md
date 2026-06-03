````markdown
# 🤖 AI Agent Knowledge & Decision Support System

An enterprise-grade **Retrieval-Augmented Generation (RAG)** system powered by autonomous AI agents. This application enables users to upload documents in multiple formats and ask natural language questions, receiving accurate, context-aware responses grounded in the enterprise knowledge base.

## 📌 Overview

This system demonstrates a **complete Generative AI and Agentic AI workflow** by:

1. **Document Ingestion** - Processing multiple document formats (PDF, TXT, CSV, Excel, DOCX, JSON, YAML)
2. **Semantic Chunking** - Breaking documents into retrievable chunks with overlap
3. **Embeddings & Vector Storage** - Converting text to semantic embeddings for similarity search
4. **Intelligent Retrieval** - Finding the most relevant content using vector similarity
5. **RAG Pipeline** - Combining retrieved context with LLM for grounded responses
6. **Agentic Reasoning** - AI agents that plan, retrieve, reason, and validate outputs
7. **Safety Controls** - Input validation, error handling, and hallucination reduction

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  User Interface (API/UI)                    │
│         (/upload-document, /ask-question, /health)          │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌──────────────┐      ┌──────────────────┐
│   Document   │      │   Query          │
│   Upload     │      │   Processing     │
└──────┬───────┘      └────────┬─────────┘
       │                       │
       ▼                       ▼
┌──────────────────────────────────────────┐
│    Document Processing Engine            │
│  - PDF/TXT/CSV/Excel/DOCX/JSON/YAML      │
│  - Text extraction & normalization       │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│      Semantic Chunking                   │
│  - Split into overlapping chunks         │
│  - Preserve semantic boundaries          │
│  - Size: 1000 tokens, Overlap: 200       │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│    Embedding Generation                  │
│  - sentence-transformers/all-MiniLM      │
│  - 384-dimensional vectors               │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   Vector Database Storage                │
│  - FAISS (local) / Pinecone (cloud)      │
│  - ChromaDB (developer-friendly)         │
│  - Similarity indexing                   │
└──────┬───────────────────────────────────┘
       │
       │ ◄─────────────────────┐
       │                       │
    User Query              Retrieval
       │                       │
       ▼                       ▼
┌──────────────────────────────────────────┐
│     AI Agent Orchestrator                │
│  1. Planner - Plan retrieval strategy    │
│  2. Retriever - Execute search tools     │
│  3. Reasoner - Analyze context           │
│  4. Validator - Verify responses         │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│    RAG Pipeline                          │
│  - Embed user query                      │
│  - Vector similarity search (top-k=5)    │
│  - Build context window                  │
│  - Construct prompt with context         │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│   LLM (GPT-4 / Claude)                   │
│  - Generate grounded response            │
│  - Apply safety guardrails               │
│  - Include source citations              │
└──────┬───────────────────────────────────┘
       │
       ▼
    Response with Sources
```

---

## 📋 Development Roadmap (10 Tasks)

| Task | Status | Description |
|------|--------|-------------|
| 1 | ✅ Done | **Set up project foundation** - Repository, environment, structure |
| 2 | ⏳ Next | **Design user interaction layer** - FastAPI endpoints |
| 3 | ⏳ Todo | **Implement document ingestion** - Multi-format support |
| 4 | ⏳ Todo | **Prepare data for semantic search** - Chunking strategy |
| 5 | ⏳ Todo | **Build vector-based knowledge store** - Embeddings & indexing |
| 6 | ⏳ Todo | **Implement intelligent retrieval** - Similarity search |
| 7 | ⏳ Todo | **Develop RAG pipeline** - LLM integration |
| 8 | ⏳ Todo | **Implement agent-based reasoning** - Multi-step workflow |
| 9 | ⏳ Todo | **Add reliability & safety controls** - Error handling & validation |
| 10 | ⏳ Todo | **Deploy & document** - Production-ready deployment |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | High-performance REST API |
| **ASGI Server** | Uvicorn | Application server |
| **LLM** | OpenAI (GPT-4) | Advanced reasoning & generation |
| **Agentic Framework** | LangChain + LlamaIndex | Agent orchestration & tools |
| **Embeddings** | Sentence Transformers | Text vectorization (384-dim) |
| **Vector DB** | FAISS / Pinecone / ChromaDB | Semantic search & storage |
| **Document Processing** | PyPDF, python-docx, pandas, PyYAML | Multi-format support |
| **Data Validation** | Pydantic | Type safety & validation |
| **Logging** | Loguru | Advanced logging & monitoring |
| **Testing** | Pytest | Unit & integration tests |
| **Code Quality** | Black, Flake8, isort | Code formatting & linting |

---

## 📂 Project Structure

```
ai-agent-knowledge-system/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entry point ✅
│   ├── config.py                   # Configuration management ✅
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/                 # API endpoints (Task 2)
│   │   │   ├── documents.py        # /upload-document, /list, /delete
│   │   │   ├── queries.py          # /ask-question, /history
│   │   │   └── health.py           # /health, /status
│   │   └── schemas.py              # Pydantic models ✅ (26 schemas)
│   ├── services/
│   │   ├── document_service.py     # Document processing (Task 3)
│   │   ├── chunking_service.py     # Semantic chunking (Task 4)
│   │   ├── embedding_service.py    # Embeddings generation (Task 5)
│   │   ├── retriever_service.py    # Document retrieval (Task 6)
│   │   └── rag_service.py          # RAG pipeline (Task 7)
│   ├── agents/
│   │   ├── base_agent.py           # Base agent class
│   │   ├── rag_agent.py            # RAG-specific agent (Task 8)
│   │   ├── tools.py                # Agent tools
│   │   └── prompts.py              # System prompts
│   ├── core/
│   │   ├── document_processor.py    # Document parsing
│   │   ├── vector_store.py         # Vector DB interface
│   │   └── llm_service.py          # LLM interactions
│   ├── utils/
│   │   ├── logger.py               # Loguru logging ✅
│   │   ├── errors.py               # Custom exceptions ✅ (8 types)
│   │   └── validators.py           # Input validation ✅
│   └── models/
│       └── schemas.py              # Database models
├── data/                           # Data directory
├── uploaded_documents/             # Document uploads
├── processed_data/                 # Processed documents
├── vector_store/                   # Vector DB storage
├── logs/                          # Application logs
├── tests/
│   ├── test_documents.py
│   ├── test_queries.py
│   ├── test_agent.py
│   └── conftest.py
├── notebooks/
│   ├── exploration.ipynb
│   └── development.ipynb
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example                   # Environment template ✅
├── .gitignore                     # Git config ✅
├── requirements.txt               # Dependencies ✅
├── setup.py                       # Package setup ✅
└── README.md                      # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- pip or conda
- OpenAI API key
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/samdas1982/ai-agent-knowledge-system.git
cd ai-agent-knowledge-system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 5: Run Application
```bash
# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation: http://localhost:8000/docs
# OpenAPI Schema: http://localhost:8000/openapi.json
# Health Check: http://localhost:8000/health
```

---

## 📡 API Endpoints (Task 2 - Coming Soon)

### Document Management
```
POST   /api/documents/upload          # Upload document
GET    /api/documents                 # List all documents
GET    /api/documents/{doc_id}        # Get document info
DELETE /api/documents/{doc_id}        # Delete document
```

### Query & Chat
```
POST   /api/queries/ask               # Ask question with RAG
GET    /api/queries/history           # Get query history
POST   /api/queries/chat              # Multi-turn conversation
```

### System
```
GET    /health                        # Health check (Status 200)
GET    /api/status                    # System status
GET    /                              # API information
```

---

## ⚙️ Configuration

### Environment Variables (.env)

**LLM Configuration**
```env
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

**Embedding Model**
```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

**Vector Database**
```env
VECTOR_DB_TYPE=faiss              # Options: faiss, pinecone, chromadb
VECTOR_DB_PATH=./vector_store
```

**Document Processing**
```env
MAX_UPLOAD_SIZE_MB=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
SUPPORTED_FORMATS=pdf,txt,csv,xlsx,docx,json,yaml
```

**Retrieval Configuration**
```env
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.5
```

**Agent Configuration**
```env
AGENT_TYPE=react
AGENT_TIMEOUT=300
MAX_ITERATIONS=10
```

---

## 🤖 Agent Workflow (Task 8)

### Agent Roles & Responsibilities

1. **Planner** 
   - Analyzes user query
   - Determines retrieval strategy
   - Plans multi-step reasoning

2. **Retriever**
   - Converts query to embedding
   - Searches vector database
   - Fetches top-k relevant chunks

3. **Reasoner**
   - Analyzes retrieved context
   - Identifies relevant information
   - Plans response structure

4. **Response Generator**
   - Constructs prompt with context
   - Calls LLM
   - Includes source citations

5. **Validator**
   - Checks factual accuracy
   - Reduces hallucinations
   - Applies safety guardrails

### Agent Reasoning Loop
```
User Query
    ↓
Query Embedding & Vector Search
    ↓
Retrieve Top-K Chunks (Top-5)
    ↓
Build Context Window
    ↓
LLM Processing with Context
    ↓
Generate Grounded Response
    ↓
Validate Output
    ↓
Return Response with Sources
```

---

## 📊 Supported Document Formats

| Format | Library | Status |
|--------|---------|--------|
| **PDF** | PyPDF | ✅ Supported |
| **TXT** | os/pathlib | ✅ Supported |
| **CSV** | pandas | ✅ Supported |
| **Excel** | openpyxl/pandas | ✅ Supported |
| **DOCX** | python-docx | ✅ Supported |
| **JSON** | json | ✅ Supported |
| **YAML** | PyYAML | ✅ Supported |

---

## 🔐 Security & Safety Controls (Task 9)

### Input Validation
- File format validation (whitelist)
- File size limits (50MB default)
- Query length validation (3-5000 chars)
- Chunk parameter validation

### Error Handling
- 8 custom exception classes
- Comprehensive logging
- Graceful error responses
- Error tracking & monitoring

### Safety Guardrails
- Hallucination detection
- Factual accuracy checks
- Rate limiting (planned)
- Output verification agent

### Logging & Monitoring
- Loguru with console + file output
- Request/response logging
- Error tracking with stack traces
- Performance metrics

---

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_documents.py -v
```

---

## 📦 Installation Options

### Option 1: Development Mode
```bash
pip install -e .
```

### Option 2: With Optional Dependencies
```bash
# For Pinecone support
pip install -e ".[pinecone]"

# For development
pip install -e ".[dev]"
```

### Option 3: From Requirements (Recommended)
```bash
pip install -r requirements.txt
```

---

## 🐳 Docker Deployment (Task 10)

### Build Docker Image
```bash
docker build -f docker/Dockerfile -t ai-knowledge-system .
```

### Run Container
```bash
docker run -p 8000:8000 \
  --env-file .env \
  --name ai-knowledge \
  ai-knowledge-system
```

### Using Docker Compose
```bash
docker-compose -f docker/docker-compose.yml up
```

---

## 📚 Documentation Structure

- **README.md** - Project overview & quick start (this file)
- **docs/ARCHITECTURE.md** - Detailed system architecture
- **docs/API.md** - Complete API reference
- **docs/AGENTS.md** - Agent design & workflow
- **docs/DEPLOYMENT.md** - Production deployment guide
- **docs/TROUBLESHOOTING.md** - Common issues & solutions

---

## 🔧 Development Workflow

### Branch Naming Convention
```
feature/task-name
bugfix/issue-description
docs/documentation-update
```

### Code Quality
```bash
# Format code
black app/

# Check linting
flake8 app/

# Sort imports
isort app/
```

### Before Committing
```bash
# Run tests
pytest

# Check coverage
pytest --cov=app

# Format code
black app/ && isort app/
```

---

## 📋 Task Completion Status

### ✅ Task 1: Project Foundation (COMPLETED)
- [x] Repository setup
- [x] Virtual environment configuration
- [x] Folder structure created
- [x] Configuration management (config.py)
- [x] API schemas (26 Pydantic models)
- [x] Logging setup (loguru)
- [x] Error handling (8 custom exceptions)
- [x] Input validators
- [x] Requirements.txt with all dependencies
- [x] .gitignore & .env.example
- [x] FastAPI entry point (main.py)

### 📝 Task 2: User Interaction Layer (IN PROGRESS)
- [ ] Document upload endpoint
- [ ] Query endpoint
- [ ] Health check endpoint
- [ ] Request/response handlers
- [ ] Error middleware

### ⏳ Tasks 3-10: To Be Implemented
- Document ingestion
- Semantic chunking
- Vector embeddings
- Document retrieval
- RAG pipeline
- Agent reasoning
- Safety controls
- Deployment & docs

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes with tests
4. Run quality checks: `black . && flake8 app && isort app`
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [FAISS Documentation](https://faiss.ai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/samdas1982/ai-agent-knowledge-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/samdas1982/ai-agent-knowledge-system/discussions)
- **Email**: d.sharmistha@gmail.com

---

## 🎯 Project Status

- **Version**: 1.0.0 (Alpha)
- **Phase**: Foundation Complete ✅
- **Last Updated**: 2026-06-03
- **Development Status**: Active Development 🚀

---

**Built with ❤️ for Enterprise AI Applications**
````
