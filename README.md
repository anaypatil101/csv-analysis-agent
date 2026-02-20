# 📊 CSV Analysis Agent

An interactive agent that lets you analyze CSV files using natural language. Powered by **OpenAI** and **LangChain**, it reads your data into a pandas DataFrame and answers questions conversationally — no code required from the user.

> Currently ships with the **World Happiness Report 2018** dataset as a demo, but can be adapted to any CSV.

---

## ✨ Features

- **Natural Language Queries** — Ask questions about your data in plain English and get clear, concise answers.
- **Pandas Code Execution** — The agent writes and executes pandas code under the hood via a sandboxed Python REPL.
- **CSV Auto-Inspection** — A built-in tool lets the agent inspect column names and types, data shape, sample rows, and missing values — all on demand.
- **Conversational Memory** — Chat history is maintained across turns, so you can ask follow-up questions naturally.
- **Guardrails** — Max iteration limits prevent the agent from looping endlessly, and results are trusted on the first valid execution.

---

## 🛠️ Tech Stack

| Component         | Technology                          |
| ----------------- | ----------------------------------- |
| LLM               | OpenAI GPT-5-mini (via `langchain-openai`) |
| Agent Framework   | LangChain (`AgentExecutor`, tool-calling agent) |
| Code Execution    | `langchain-experimental` Python AST REPL |
| Data Handling      | pandas                              |
| Environment Mgmt  | python-dotenv                       |
| Package Manager   | uv                                  |
| Python Version    | 3.12+                               |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- [**uv**](https://docs.astral.sh/uv/) package manager
- An **OpenAI API key**

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/csv-analysis-agent.git
   cd csv-analysis-agent
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

4. **Run the agent**

   ```bash
   uv run python src/agent.py
   ```

---

## 💬 Usage

Once running, you'll see an interactive prompt:

```
📊 CSV Analysis Agent — World Happiness Report 2018
Type 'exit' to quit

You: 
```

Just type your question and press Enter. The agent will inspect the data, write the necessary pandas code, execute it, and return a human-readable answer.

### Example Queries

```
You: Which country has the highest happiness score?
You: What's the average GDP per capita across all countries?
You: Show me the top 5 countries by social support
You: Is there a correlation between freedom and happiness score?
You: How many countries have a generosity score above 0.3?
```

Type `exit` or `quit` to end the session.

---

### REST API

Start the FastAPI server:

```bash
uv run uvicorn src.api:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs are auto-generated at [`/docs`](http://127.0.0.1:8000/docs).

#### `POST /query`

Send a natural language question:

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Which country is the happiest?"}'
```

Response:

```json
{
  "answer": "Finland has the highest happiness score of 7.632.",
  "session_id": "a1b2c3d4-..."
}
```

Pass the returned `session_id` in subsequent requests to maintain conversation context.

#### `GET /health`

Returns `{"status": "ok"}` — useful for uptime monitoring.

---

## 📁 Project Structure

```
csv-analysis-agent/
├── main.py              # Default entry point (placeholder)
├── src/
│   ├── agent.py         # Core agent logic — LLM, tools & prompt
│   └── api.py           # FastAPI server — REST endpoint for the agent
├── data/
│   └── 2018.csv         # World Happiness Report 2018 dataset
├── pyproject.toml       # Project metadata & dependencies
├── .env                 # API keys (not committed)
├── .gitignore
├── .python-version      # Pinned Python version (3.12)
└── README.md
```

---

## ⚙️ How It Works

1. **Data Loading** — The CSV file is loaded into a pandas DataFrame on startup.
2. **Tool Registration** — Two tools are registered with the agent:
   - `inspect_csv` — Returns schema info, sample rows, and missing value counts.
   - `python_repl` — A sandboxed Python REPL with the DataFrame pre-loaded as `df`.
3. **Prompt Engineering** — A system prompt instructs the agent to inspect the data first, write pandas code once, trust its result, and explain findings clearly.
4. **Conversation Loop** — User inputs are sent to the `AgentExecutor`, which orchestrates LLM reasoning and tool calls. Chat history is persisted for multi-turn context.

---

## 📊 Dataset

This project uses the [World Happiness Report](https://www.kaggle.com/datasets/unsdsn/world-happiness) dataset, published on Kaggle by the **United Nations Sustainable Development Solutions Network (UNSDSN)**.

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute.
