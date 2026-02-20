import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

load_dotenv()

# Load the CSV
CSV_PATH = "data/2018.csv"
df = pd.read_csv(CSV_PATH)

# Give the REPL access to the dataframe
repl_tool = PythonAstREPLTool(locals={"df": df})
repl_tool.name = "python_repl"
repl_tool.description = (
    "Use this to run pandas code on the dataframe `df` to answer questions. "
    "Always use print() to show results. The dataframe is already loaded as `df`."
)

# CSV Inspector tool
@tool
def inspect_csv(_: str = "") -> str:
    """Inspect the CSV file — returns column names, shape, dtypes, and a sample of the data."""
    info = f"""
Shape: {df.shape[0]} rows, {df.shape[1]} columns

Columns & dtypes:
{df.dtypes.to_string()}

First 3 rows:
{df.head(3).to_string()}

Missing values:
{df.isnull().sum().to_string()}
"""
    return info

# LLM
llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

# Tools
tools = [inspect_csv, repl_tool]

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful data analysis assistant. You have access to a CSV file 
containing the World Happiness Report 2018 data. 

When a user asks a question:
1. Inspect the CSV only if you haven't already done so in this conversation
2. Write and run pandas code ONCE to get the answer
3. If you get a valid result, stop immediately and respond — do NOT re-run the same code
4. Explain results clearly in plain English

Be concise and decisive. Trust your first valid result."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Memory — simple list to track chat history
chat_history = []

# Agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    max_iterations=5  # stops the agent from looping endlessly
)
# CLI loop
def main():
    print("📊 CSV Analysis Agent — World Happiness Report 2018")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_input:
            continue

        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Manually update chat history
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response["output"]))

        print(f"\nAgent: {response['output']}\n")

if __name__ == "__main__":
    main()