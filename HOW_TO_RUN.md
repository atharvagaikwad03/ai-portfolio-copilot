# How to Run AI Portfolio Copilot

## One-time setup

1. **Install dependencies**
   ```bash
   cd /Users/atharvagaikwad/ai-portfolio-copilot

   # Python (use existing venv at project root)
   source venv/bin/activate
   pip install -r requirements.txt

   # Node.js (from project root)
   npm install
   ```

2. **Configure environment**
   - Ensure `.env` exists in the project root (copy from `.env.example` if needed).
   - Set at least:
     - `OPENAI_API_KEY` – your OpenAI API key
     - `PINECONE_API_KEY` – your Pinecone API key (optional for RAG; leave unset to run without RAG)
     - `PINECONE_ENVIRONMENT` – e.g. `us-east-1`

3. **Optional: seed the knowledge base** (only if using Pinecone)
   ```bash
   source venv/bin/activate
   cd backend/python
   PYTHONPATH=/Users/atharvagaikwad/ai-portfolio-copilot/backend/python python -m scripts.initialize_knowledge_base
   ```

---

## Running the project

You need **two terminals**: one for the Python backend, one for the Node.js gateway.

### Terminal 1 – Python backend (port 8000)

```bash
cd /Users/atharvagaikwad/ai-portfolio-copilot
source venv/bin/activate
cd backend/python
PYTHONPATH=/Users/atharvagaikwad/ai-portfolio-copilot/backend/python python -m api.server
```

Wait until you see: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 – Node.js gateway (port 3000)

```bash
cd /Users/atharvagaikwad/ai-portfolio-copilot
npm start
```

You should see: `Node.js server running on port 3000`

---

## Using the app

- **Chat API:** `POST http://localhost:3000/api/chat` with JSON body: `{"message": "Your question"}`
- **Health check:** open http://localhost:3000/health
- **Frontend:** open `frontend/example.html` in your browser (file:// or via a simple HTTP server)

---

## Quick test

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your projects"}'
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Address already in use` (port 8000 or 3000) | Stop the other process: `kill $(lsof -ti:8000)` or `kill $(lsof -ti:3000)` |
| `ModuleNotFoundError` (Python) | Activate venv and run from project root with `PYTHONPATH` as above |
| `Pinecone not configured` | Set `PINECONE_API_KEY` in `.env` and restart the Python server |
| Node `Cannot find module 'cors'` | Run `npm install` from project root |
