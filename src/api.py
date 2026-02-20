"""
FastAPI server exposing the CSV Analysis Agent as a REST API.

Run with:
    uvicorn src.api:app --reload
"""

from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

from .agent import create_agent

# --- App setup ---
app = FastAPI(
    title="CSV Analysis Agent API",
    description="Analyze CSV data using natural language queries powered by LangChain & OpenAI.",
    version="0.1.0",
)

# --- Agent ---
agent_executor = create_agent()

# --- In-memory session store (chat history per session) ---
sessions: dict[str, list] = {}


# --- Schemas ---
class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    session_id: str


# --- Routes ---
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    """
    Send a natural language question to the CSV analysis agent.

    - **question**: Your question about the data (e.g. "Which country is the happiest?")
    - **session_id**: Optional. Pass a session ID to maintain conversation context across requests.
      If omitted, a new session is created.
    """
    # Resolve or create session
    session_id = request.session_id or str(uuid4())
    chat_history = sessions.setdefault(session_id, [])

    # Invoke agent
    response = agent_executor.invoke({
        "input": request.question,
        "chat_history": chat_history,
    })

    # Update chat history
    chat_history.append(HumanMessage(content=request.question))
    chat_history.append(AIMessage(content=response["output"]))

    return QueryResponse(
        answer=response["output"],
        session_id=session_id,
    )
