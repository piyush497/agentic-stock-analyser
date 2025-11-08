import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from agent_logic import initialize_agent  # Import logic from the separate file

# Initialize FastAPI app
app = FastAPI(title="Agentic Stock Chatbot Server")

# Initialize the agent once at startup
AGENT_EXECUTOR = initialize_agent()

# Pydantic model for the incoming chat request
class ChatRequest(BaseModel):
    prompt: str = Field(description="The user's input query.")

@app.get("/", response_class=HTMLResponse)
async def serve_chatbot_ui():
    """
    Serves the main HTML chatbot interface.
    
    NOTE: In a production setup, you would typically use FastAPI's StaticFiles 
    or a template engine (like Jinja2) to serve 'chatbot_frontend.html'. 
    For simplicity in this environment, we will simulate loading the file contents.
    """
    try:
        # Load the HTML content from the file to serve the UI
        with open("chatbot_frontend.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend file not found! Ensure 'chatbot_frontend.html' is in the same directory.</h1>", status_code=500)

@app.post("/chat", response_class=JSONResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives the user's prompt, executes the LangChain Agent, and returns the response.
    """
    if AGENT_EXECUTOR is None:
        return JSONResponse(
            status_code=503,
            content={"response": "The Agent is not configured. Please ensure OPENAI_API_KEY is set correctly."}
        )

    try:
        # Invoke the pre-initialized agent executor with the user's prompt
        result = AGENT_EXECUTOR.invoke({"input": request.prompt})
        
        # Return only the final output string from the agent
        return JSONResponse(content={"response": result.get('output', 'Agent failed to produce a coherent output.')})

    except Exception as e:
        print(f"Agent Execution Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"response": f"An unexpected error occurred during agent execution: {type(e).__name__}. See server logs."}
        )