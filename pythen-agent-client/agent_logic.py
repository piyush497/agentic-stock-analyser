import requests
import os
from pydantic import BaseModel, Field
from typing import Optional

from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

JAVA_API_BASE_URL = os.getenv("JAVA_API_BASE_URL", "http://localhost:8080/api/v1/stock") 

class StockDataInput(BaseModel):
    """Input for the stock price retrieval tool."""
    symbol: str = Field(description="The stock ticker symbol (e.g., GOOG, MSFT). Must be capitalized.")

@tool("get_current_stock_price", args_schema=StockDataInput)
def call_java_api_tool(symbol: str) -> str:
    """
    Calls the external Java API service to retrieve the current market price for a stock.
    Returns the price or an error message as a string.
    """
    endpoint = f"{JAVA_API_BASE_URL}/{symbol.upper()}"
    
    try:
        response = requests.get(endpoint, timeout=3)
        response.raise_for_status() 
        data = response.json()
        
        if data.get("status") == "SUCCESS":
            price = data.get("current_price")
            return f"The current price for {symbol} is ${price:.2f}"
        else:
            return f"Error: Java API returned status {data.get('status')} - {data.get('message')}"
            
    except requests.exceptions.RequestException as e:
        return f"CRITICAL ERROR: Could not connect to the Java API at {JAVA_API_BASE_URL}. Check if the service is running. Error: {e}"


def initialize_agent() -> Optional[AgentExecutor]:
    """Sets up and returns the LangChain AgentExecutor."""
    if not os.getenv("OPENAI_API_KEY"):
        print("CRITICAL: OPENAI_API_KEY environment variable not set. Agent will not function.")
        return None

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    tools = [call_java_api_tool]

    system_prompt = (
        "You are a sophisticated Financial Analyst Agent. Your role is to analyze stock prices "
        "using your available tool and provide clear advice (BUY, HOLD, or SELL). "
        "If the price is significantly below the user's target, recommend BUY. "
        "If it's near or above the target, recommend HOLD. Be concise and professional."
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    print("--- LangChain Agent Initialized Successfully ---")
    return agent_executor