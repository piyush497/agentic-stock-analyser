# How to Run in Production

## Install dependencies
```bash
pip install -r requirements.txt
```

## Ensure Java API is running
- The Java API should be available at: http://localhost:8080

## Configure OpenAI API key
- Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY = "your-api-key"
```
- macOS/Linux (bash/zsh):
```bash
export OPENAI_API_KEY="your-api-key"
```

## Run the server
```bash
uvicorn main_server:app --reload
```

## Access the app
- Open your browser to: http://127.0.0.1:8000/

## Notes
> The LangChain Agent logic is isolated, making it easy to test or swap out the agent without touching the web server. The web server clearly handles just the request/response cycle.

## Dependencies

| Package | Purpose in this app | Role |
| --- | --- | --- |
| fastapi | The modern web framework that defines the `/chat` endpoint and serves the HTML. | Backend Server |
| uvicorn[standard] | The high-performance ASGI server used to run the FastAPI application. | Server Runner |
| langchain-core | Provides the base classes and infrastructure for LangChain, such as tool and prompt templates. | Agent Foundation |
| langchain-openai | The specific integration package to connect to and use the GPT model. | LLM Connection |
| requests | Used within the `call_java_api_tool` function to make HTTP calls to your external Java API. | Tool Execution |
| pydantic | Used by both FastAPI (for request validation) and LangChain (for defining the `args_schema` of your tool). | Data Validation |
