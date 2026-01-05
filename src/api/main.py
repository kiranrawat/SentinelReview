from fastapi import FastAPI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

app = FastAPI(title="Sentinel Review API", version="1.0.0")


@app.get("/review-pr", tags=["Review PR"])
async def review_pr(github_url: str):
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "http",  # HTTP-based remote server
                # Ensure you start your math server on port 8080
                "url": "http://localhost:8080/mcp",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_agent("gpt-5", tools)
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": f"Review the PR at {github_url}"}]}
    )

    return {"message": f"Reviewing PR at {github_url}"}


@app.post("/test-mcp", tags=["Test MCP"])
async def test_mcp(prompt: str):
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "http",  # HTTP-based remote server
                # Ensure you start your math server on port 8080
                "url": "http://localhost:8080/mcp",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent("gpt-5", tools)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    user_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )
    res = ''
    for response in [math_response, weather_response, user_response]:
        res += response['messages'][-1].content + "\n"
    return {"message": "All MCP calls completed successfully."}
