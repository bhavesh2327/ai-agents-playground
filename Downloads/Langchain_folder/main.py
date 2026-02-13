from dotenv import load_dotenv
import os
from typing_extensions import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in your .env")

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Initialize Gemini LLM
chat_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY
)

# Define Graph State
class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

def llm_call(state: GraphState) -> dict:
    """Call the LLM using conversation messages and append AI response."""
    response = chat_llm.invoke(state["messages"])  # AIMessage
    return {
        "messages": [response]
    }

def token_counter(state: GraphState) -> dict:
    """Count tokens (simple word count) in the last AI message."""
    last_msg = state["messages"][-1]
    text = last_msg.content
    token_number = len(text.split())
    summary = f"Total token number in the generated answer (word count) is {token_number}"
    return {
        "messages": [AIMessage(content=summary)]
    }

# Build the graph
builder = StateGraph(GraphState)
builder.add_node("llm_call", llm_call)
builder.add_node("token_counter", token_counter)
builder.set_entry_point("llm_call")
builder.add_edge("llm_call", "token_counter")
builder.set_finish_point("token_counter")

# Compile the app
app = builder.compile()

def main():
    """Execute the LangGraph workflow with Gemini"""
    print("=" * 60)
    print("LangGraph with Gemini - LLM Call + Token Counter")
    print("=" * 60)
    
    # Invoke the graph
    result = app.invoke({
        "messages": [HumanMessage(content="Hi, this is Sunny. Say hello in detail.")]
    })
    
    print("\n📋 Results:")
    print("-" * 60)
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        print(f"\n[{i}] {msg_type}:")
        print(f"    {msg.content}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
